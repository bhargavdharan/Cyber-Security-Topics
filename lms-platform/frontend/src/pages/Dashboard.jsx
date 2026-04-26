import React, { useState, useEffect } from 'react';
import api from '../services/api';
import TopicCard from '../components/TopicCard';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const navigate = useNavigate();
  const [topics, setTopics] = useState([]);
  const [progress, setProgress] = useState([]);
  const [stats, setStats] = useState({});
  const [quizResults, setQuizResults] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [topicsRes, progressRes, statsRes, quizRes] = await Promise.all([
        api.get('/topics/'),
        api.get('/topics/progress'),
        api.get('/stats'),
        api.get('/topics/quiz-results')
      ]);
      setTopics(topicsRes.data);
      setProgress(progressRes.data);
      setStats(statsRes.data);
      setQuizResults(quizRes.data);
    } catch (err) {
      console.error('Failed to fetch data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getProgressForTopic = (topicId) => {
    return progress.find(p => p.topic_id === topicId);
  };

  const completedCount = progress.filter(p => p.completed).length;
  const avgProgress = progress.length > 0 
    ? Math.round(progress.reduce((sum, p) => sum + p.completion_percentage, 0) / progress.length)
    : 0;

  // Find next recommended topic (first incomplete)
  const nextTopic = topics.find(t => {
    const p = getProgressForTopic(t.id);
    return !p || !p.completed;
  });

  // Calculate quiz stats
  const avgQuizScore = quizResults.length > 0
    ? Math.round(quizResults.reduce((sum, q) => sum + (q.score / q.total_questions * 100), 0) / quizResults.length)
    : 0;

  const totalQuizzes = quizResults.length;

  // Get category breakdown
  const categoryBreakdown = topics.reduce((acc, topic) => {
    const p = getProgressForTopic(topic.id);
    const cat = topic.category;
    if (!acc[cat]) acc[cat] = { total: 0, completed: 0 };
    acc[cat].total += 1;
    if (p?.completed) acc[cat].completed += 1;
    return acc;
  }, {});

  if (loading) {
    return (
      <div className="d-flex justify-content-center mt-5">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container py-4">
      {/* Welcome Header */}
      <div className="row mb-4">
        <div className="col-12">
          <h2 className="mb-1">Cybersecurity Learning Platform</h2>
          <p className="text-muted">Master cybersecurity through interactive lessons, simulations, and quizzes</p>
        </div>
      </div>

      {/* Stats Row */}
      <div className="row g-3 mb-4">
        <div className="col-md-3">
          <div className="card stats-card p-3">
            <div className="d-flex align-items-center">
              <i className="bi bi-book fs-2 me-3"></i>
              <div>
                <h6 className="mb-0">Total Topics</h6>
                <h3 className="mb-0">{topics.length}</h3>
              </div>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card stats-card p-3">
            <div className="d-flex align-items-center">
              <i className="bi bi-check-circle fs-2 me-3"></i>
              <div>
                <h6 className="mb-0">Completed</h6>
                <h3 className="mb-0">{completedCount}</h3>
              </div>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card stats-card p-3">
            <div className="d-flex align-items-center">
              <i className="bi bi-graph-up fs-2 me-3"></i>
              <div>
                <h6 className="mb-0">Avg Progress</h6>
                <h3 className="mb-0">{avgProgress}%</h3>
              </div>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card stats-card p-3">
            <div className="d-flex align-items-center">
              <i className="bi bi-trophy fs-2 me-3"></i>
              <div>
                <h6 className="mb-0">Avg Quiz Score</h6>
                <h3 className="mb-0">{avgQuizScore}%</h3>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Row */}
      <div className="row g-4 mb-4">
        {/* Overall Progress + Next Topic */}
        <div className="col-lg-8">
          <div className="card mb-4">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center mb-3">
                <h5 className="card-title mb-0">Overall Progress</h5>
                <span className="badge bg-primary">{completedCount}/{topics.length} Topics</span>
              </div>
              <div className="progress" style={{ height: '12px' }}>
                <div 
                  className="progress-bar bg-success progress-bar-striped progress-bar-animated" 
                  role="progressbar" 
                  style={{ width: `${avgProgress}%` }}
                >
                  {avgProgress > 10 && `${avgProgress}%`}
                </div>
              </div>
              <p className="text-muted mt-2 mb-0">
                You've completed <strong>{completedCount}</strong> out of <strong>{topics.length}</strong> topics. 
                {avgProgress < 100 && ' Keep going!'}
                {avgProgress === 100 && ' Amazing work! 🎉'}
              </p>
            </div>
          </div>

          {/* Category Breakdown */}
          <div className="card">
            <div className="card-header bg-white">
              <h6 className="mb-0"><i className="bi bi-pie-chart me-2"></i>Progress by Category</h6>
            </div>
            <div className="card-body">
              <div className="row g-3">
                {Object.entries(categoryBreakdown).map(([cat, data]) => {
                  const pct = Math.round((data.completed / data.total) * 100);
                  return (
                    <div className="col-md-6" key={cat}>
                      <div className="d-flex justify-content-between small mb-1">
                        <span>{cat}</span>
                        <span className="text-muted">{data.completed}/{data.total}</span>
                      </div>
                      <div className="progress" style={{ height: '8px' }}>
                        <div 
                          className={`progress-bar ${pct === 100 ? 'bg-success' : 'bg-primary'}`}
                          role="progressbar" 
                          style={{ width: `${pct}%` }}
                        ></div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>

        {/* Right Sidebar */}
        <div className="col-lg-4">
          {/* Next Recommended Topic */}
          {nextTopic && (
            <div className="card mb-4 border-primary">
              <div className="card-header bg-primary text-white">
                <h6 className="mb-0"><i className="bi bi-lightning-charge me-2"></i>Continue Learning</h6>
              </div>
              <div className="card-body">
                <h5>{nextTopic.title}</h5>
                <p className="text-muted small">{nextTopic.description}</p>
                <div className="d-flex justify-content-between align-items-center">
                  <span className="badge bg-secondary">{nextTopic.category}</span>
                  <button 
                    className="btn btn-sm btn-primary"
                    onClick={() => navigate(`/topic/${nextTopic.slug}`)}
                  >
                    Start Learning <i className="bi bi-arrow-right ms-1"></i>
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Quiz Scores Summary */}
          <div className="card mb-4">
            <div className="card-header bg-white">
              <h6 className="mb-0"><i className="bi bi-clipboard-check me-2"></i>Quiz Performance</h6>
            </div>
            <div className="card-body">
              {totalQuizzes > 0 ? (
                <>
                  <div className="text-center mb-3">
                    <div className="display-4 fw-bold text-primary">{avgQuizScore}%</div>
                    <div className="text-muted small">Average Score</div>
                  </div>
                  <div className="list-group list-group-flush">
                    {quizResults.slice(0, 5).map((quiz, i) => {
                      const scorePct = Math.round((quiz.score / quiz.total_questions) * 100);
                      return (
                        <div key={i} className="list-group-item d-flex justify-content-between align-items-center px-0">
                          <div className="small text-truncate" style={{maxWidth: '70%'}}>{quiz.quiz_name}</div>
                          <span className={`badge ${scorePct >= 80 ? 'bg-success' : scorePct >= 60 ? 'bg-warning text-dark' : 'bg-danger'}`}>
                            {quiz.score}/{quiz.total_questions}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </>
              ) : (
                <div className="text-center py-3">
                  <i className="bi bi-clipboard-data fs-1 text-muted"></i>
                  <p className="text-muted mt-2 mb-0">No quizzes taken yet.<br/>Take your first quiz to see results here!</p>
                </div>
              )}
            </div>
          </div>

          {/* Quick Stats */}
          <div className="card">
            <div className="card-header bg-white">
              <h6 className="mb-0"><i className="bi bi-activity me-2"></i>Activity Summary</h6>
            </div>
            <div className="card-body">
              <div className="d-flex justify-content-between mb-2">
                <span className="text-muted">Quizzes Taken</span>
                <span className="fw-bold">{totalQuizzes}</span>
              </div>
              <div className="d-flex justify-content-between mb-2">
                <span className="text-muted">Simulations Run</span>
                <span className="fw-bold">{stats.total_simulations || 0}</span>
              </div>
              <div className="d-flex justify-content-between mb-2">
                <span className="text-muted">Completion Rate</span>
                <span className="fw-bold">{Math.round((completedCount / topics.length) * 100)}%</span>
              </div>
              <div className="d-flex justify-content-between">
                <span className="text-muted">Topics Remaining</span>
                <span className="fw-bold">{topics.length - completedCount}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Topics Grid */}
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h4 className="mb-0">Learning Modules</h4>
        <span className="text-muted small">{completedCount} of {topics.length} completed</span>
      </div>
      <div className="row g-4">
        {topics.map(topic => (
          <div className="col-md-6 col-lg-4" key={topic.id}>
            <TopicCard 
              topic={topic} 
              progress={getProgressForTopic(topic.id)} 
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
