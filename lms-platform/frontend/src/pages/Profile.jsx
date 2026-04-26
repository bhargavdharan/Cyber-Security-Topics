import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

const Profile = () => {
  const { user } = useAuth();
  const [progress, setProgress] = useState([]);
  const [quizResults, setQuizResults] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProfileData();
  }, []);

  const fetchProfileData = async () => {
    try {
      const [progressRes, quizRes] = await Promise.all([
        api.get('/topics/progress'),
        api.get('/topics/quiz-results')
      ]);
      setProgress(progressRes.data);
      setQuizResults(quizRes.data);
    } catch (err) {
      console.error('Failed to fetch profile data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center mt-5">
        <div className="spinner-border text-primary" role="status"></div>
      </div>
    );
  }

  const completedTopics = progress.filter(p => p.completed);
  const totalProgress = progress.length > 0
    ? Math.round(progress.reduce((sum, p) => sum + p.completion_percentage, 0) / progress.length)
    : 0;

  return (
    <div className="container py-4">
      <div className="row">
        {/* User Info */}
        <div className="col-md-4">
          <div className="card mb-4">
            <div className="card-body text-center">
              <i className="bi bi-person-circle display-1 text-primary"></i>
              <h4 className="mt-3">{user?.full_name || user?.username}</h4>
              <p className="text-muted">@{user?.username}</p>
              <p className="text-muted">{user?.email}</p>
              <span className="badge bg-primary">{user?.role}</span>
            </div>
          </div>

          <div className="card">
            <div className="card-body">
              <h6>Statistics</h6>
              <div className="d-flex justify-content-between mb-2">
                <span>Topics Completed</span>
                <strong>{completedTopics.length}/{progress.length}</strong>
              </div>
              <div className="d-flex justify-content-between mb-2">
                <span>Overall Progress</span>
                <strong>{totalProgress}%</strong>
              </div>
              <div className="d-flex justify-content-between mb-2">
                <span>Quizzes Taken</span>
                <strong>{quizResults.length}</strong>
              </div>
              <div className="progress" style={{ height: '8px' }}>
                <div className="progress-bar" style={{ width: `${totalProgress}%` }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Progress & Quiz Results */}
        <div className="col-md-8">
          <div className="card mb-4">
            <div className="card-header">
              <h5 className="mb-0">Topic Progress</h5>
            </div>
            <div className="card-body">
              {progress.map(p => (
                <div key={p.topic_id} className="mb-3">
                  <div className="d-flex justify-content-between">
                    <span>{p.title}</span>
                    <span>{p.completion_percentage}%</span>
                  </div>
                  <div className="progress" style={{ height: '6px' }}>
                    <div 
                      className={`progress-bar ${p.completion_percentage === 100 ? 'bg-success' : ''}`}
                      style={{ width: `${p.completion_percentage}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">Recent Quiz Results</h5>
            </div>
            <div className="card-body">
              {quizResults.length === 0 ? (
                <p className="text-muted mb-0">No quizzes taken yet. Start learning!</p>
              ) : (
                <div className="table-responsive">
                  <table className="table table-sm">
                    <thead>
                      <tr>
                        <th>Quiz</th>
                        <th>Score</th>
                        <th>Percentage</th>
                        <th>Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      {quizResults.slice(0, 10).map((result, i) => (
                        <tr key={i}>
                          <td>{result.quiz_name}</td>
                          <td>{result.score}/{result.total_questions}</td>
                          <td>
                            <span className={`badge ${(result.score/result.total_questions) >= 0.7 ? 'bg-success' : 'bg-warning'}`}>
                              {Math.round((result.score/result.total_questions) * 100)}%
                            </span>
                          </td>
                          <td>{new Date(result.taken_at).toLocaleDateString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
