import React from 'react';
import { useNavigate } from 'react-router-dom';

const iconMap = {
  'shield': 'bi-shield-check',
  'network': 'bi-diagram-3',
  'desktop': 'bi-pc-display',
  'lock': 'bi-lock',
  'globe': 'bi-globe',
  'firewall': 'bi-fire',
  'search': 'bi-search',
  'ambulance': 'bi-life-preserver',
  'cloud': 'bi-cloud',
  'mobile': 'bi-phone',
  'brain': 'bi-lightbulb',
  'industry': 'bi-building',
  'user-secret': 'bi-incognito',
  'code': 'bi-code-slash',
  'rocket': 'bi-rocket',
};

const TopicCard = ({ topic, progress }) => {
  const navigate = useNavigate();
  const iconClass = iconMap[topic.icon] || 'bi-book';
  const completion = progress?.completion_percentage || 0;
  const isCompleted = progress?.completed;

  return (
    <div className="card topic-card" onClick={() => navigate(`/topic/${topic.slug}`)}>
      <div className="card-body p-4">
        <div className="d-flex justify-content-between align-items-start">
          <div>
            <i className={`bi ${iconClass} topic-icon`}></i>
            <h5 className="card-title mb-2">{topic.title}</h5>
            <span className="badge bg-secondary mb-2">{topic.category}</span>
          </div>
          {isCompleted && (
            <span className="badge bg-success">
              <i className="bi bi-check-circle me-1"></i>Done
            </span>
          )}
        </div>
        
        <p className="card-text text-muted small">{topic.description}</p>
        
        <div className="mt-3">
          <div className="d-flex justify-content-between small mb-1">
            <span>Progress</span>
            <span>{completion}%</span>
          </div>
          <div className="progress" style={{ height: '6px' }}>
            <div 
              className={`progress-bar ${completion === 100 ? 'bg-success' : ''}`}
              role="progressbar" 
              style={{ width: `${completion}%` }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TopicCard;
