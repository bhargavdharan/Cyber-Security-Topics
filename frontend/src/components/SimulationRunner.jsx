import React, { useState } from 'react';
import api from '../services/api';

const SimulationRunner = ({ simulationName, topicId, title }) => {
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const runSimulation = async () => {
    setLoading(true);
    setError('');
    setOutput('');
    
    try {
      const response = await api.post(`/simulations/run/${simulationName}`, {
        topic_id: topicId
      });
      setOutput(response.data.output);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to run simulation');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card mb-4">
      <div className="card-header d-flex justify-content-between align-items-center">
        <h6 className="mb-0">
          <i className="bi bi-terminal me-2"></i>
          {title || simulationName}
        </h6>
        <button 
          className="btn btn-sm btn-primary"
          onClick={runSimulation}
          disabled={loading}
        >
          {loading ? (
            <><span className="spinner-border spinner-border-sm me-2"></span>Running...</>
          ) : (
            <><i className="bi bi-play-fill me-1"></i>Run</>
          )}
        </button>
      </div>
      <div className="card-body">
        {error && (
          <div className="alert alert-danger">{error}</div>
        )}
        {output && (
          <pre className="simulation-output bg-dark text-light p-3 rounded" style={{maxHeight: '400px', overflow: 'auto', fontSize: '0.85rem'}}>
            <code>{output}</code>
          </pre>
        )}
        {!output && !error && !loading && (
          <p className="text-muted text-center mb-0">Click "Run" to execute the simulation</p>
        )}
      </div>
    </div>
  );
};

export default SimulationRunner;
