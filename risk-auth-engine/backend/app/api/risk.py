"""Risk assessment API endpoints."""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.db.database import get_db
from app.db.redis_client import set_json
from app.db.models import RiskAssessment, AuthEvent
from app.core.risk_engine import RiskEngine

router = APIRouter(prefix="/risk", tags=["Risk Assessment"])
risk_engine = RiskEngine()


class RiskAssessmentRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=255, description="Unique user identifier")
    ip_address: str = Field(..., description="Client IP address")
    device_fingerprint: Optional[str] = Field(None, max_length=255, description="Device fingerprint hash")
    location: Optional[dict] = Field(None, description="GPS coordinates {lat, lon, city, country}")
    timestamp: Optional[datetime] = Field(None, description="Event timestamp (defaults to now)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "ip_address": "203.0.113.45",
                "device_fingerprint": "abc123...",
                "location": {"lat": 40.7128, "lon": -74.0060, "city": "New York", "country": "US"},
            }
        }


class RiskAssessmentResponse(BaseModel):
    risk_score: float = Field(..., ge=0.0, le=1.0)
    risk_level: str = Field(..., pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    recommended_action: str = Field(..., pattern="^(ALLOW|MFA|BLOCK|REVIEW)$")
    factors: list = Field(default_factory=list)
    raw_scores: dict = Field(default_factory=dict)
    assessment_id: Optional[int] = None


@router.post("/assess", response_model=RiskAssessmentResponse)
async def assess_risk(
    request: RiskAssessmentRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Perform real-time risk assessment for an authentication attempt.
    
    Returns risk score (0.0-1.0), risk level, recommended action,
    and detailed factor breakdown.
    """
    try:
        result = await risk_engine.assess_risk(
            user_id=request.user_id,
            ip_address=request.ip_address,
            device_fingerprint=request.device_fingerprint,
            location=request.location,
            timestamp=request.timestamp or datetime.utcnow(),
        )
        
        # Persist assessment to database
        assessment = RiskAssessment(
            user_id=request.user_id,
            ip_address=request.ip_address,
            device_fingerprint=request.device_fingerprint,
            location=request.location,
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            recommended_action=result["recommended_action"],
            factors=result["factors"],
        )
        db.add(assessment)
        await db.commit()
        await db.refresh(assessment)
        
        result["assessment_id"] = assessment.id
        
        # Store event for velocity tracking
        event_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "ip_address": request.ip_address,
            "device_fingerprint": request.device_fingerprint,
        }
        await set_json(f"events:{request.user_id}:recent", event_data, ttl=3600)
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Risk assessment failed: {str(e)}"
        )


@router.post("/evaluate-and-update")
async def evaluate_and_update_baseline(
    request: RiskAssessmentRequest,
    action_taken: str = "ALLOW",
    success: bool = True,
    db: AsyncSession = Depends(get_db),
):
    """
    Evaluate risk and update user baseline after authentication.
    Call this after the user completes login (success or failure).
    """
    # First assess risk
    result = await assess_risk(request, db)
    
    # Update baseline (only on success)
    if success:
        await risk_engine.update_baseline(
            user_id=request.user_id,
            device_fingerprint=request.device_fingerprint,
            ip_address=request.ip_address,
            location=request.location,
            success=True,
        )
    
    # Log auth event
    auth_event = AuthEvent(
        user_id=request.user_id,
        event_type="LOGIN_SUCCESS" if success else "LOGIN_FAILURE",
        ip_address=request.ip_address,
        device_fingerprint=request.device_fingerprint,
        location=request.location,
        success=success,
        failure_reason=None if success else f"Risk level: {result['risk_level']}",
    )
    db.add(auth_event)
    await db.commit()
    
    return {
        **result,
        "baseline_updated": success,
        "action_taken": action_taken,
    }


@router.get("/user/{user_id}/history")
async def get_user_risk_history(
    user_id: str,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """Get recent risk assessments for a user."""
    from sqlalchemy import select, desc
    
    query = (
        select(RiskAssessment)
        .where(RiskAssessment.user_id == user_id)
        .order_by(desc(RiskAssessment.created_at))
        .limit(limit)
    )
    result = await db.execute(query)
    assessments = result.scalars().all()
    
    return {
        "user_id": user_id,
        "count": len(assessments),
        "assessments": [
            {
                "id": a.id,
                "risk_score": a.risk_score,
                "risk_level": a.risk_level,
                "recommended_action": a.recommended_action,
                "factors": a.factors,
                "ip_address": a.ip_address,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            }
            for a in assessments
        ],
    }


@router.get("/user/{user_id}/baseline")
async def get_user_baseline(user_id: str):
    """Get current user baseline (for debugging/monitoring)."""
    from app.db.redis_client import get_json
    
    baseline = await get_json(f"baseline:{user_id}")
    if not baseline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No baseline found for user {user_id}"
        )
    
    return {"user_id": user_id, "baseline": baseline}
