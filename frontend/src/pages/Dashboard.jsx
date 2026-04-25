import React, { useState, useEffect } from 'react';
import api from '../services/api';
import TopicCard from '../components/TopicCard';

const Dashboard = () => {
  const [topics, setTopics] = useState([]);
  const [progress, setProgress] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [topicsRes, progressRes, statsRes] = await Promise.all([
        api.get('/topics/'),
        api.get('/topics/progress'),
        api.get('/stats')
      ]);
      setTopics(topicsRes.data);
      setProgress(progressRes.data);
      setStats(statsRes.data);
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
              <i className="bi bi-people fs-2 me-3"></i>
              <div>
                <h6 className="mb-0">Learners</h6>
                <h3 className="mb-0">{stats.total_users || 0}</h3>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Overall Progress */}
      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">Overall Progress</h5>
          <div className="progress" style={{ height: '10px' }}>
            <div 
              className="progress-bar bg-success" 
              role="progressbar" 
              style={{ width: `${avgProgress}%` }}
            ></div>
          </div>
          <p className="text-muted mt-2 mb-0">
            You've completed {completedCount} out of {topics.length} topics
          </p>
        </div>
      </div>

      {/* Topics Grid */}
      <h4 className="mb-3">Learning Modules</h4>
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
