import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const assessRisk = async (data) => {
  const response = await api.post('/risk/assess', data);
  return response.data;
};

export const getUserHistory = async (userId) => {
  const response = await api.get(`/risk/user/${userId}/history`);
  return response.data;
};

export const getUserBaseline = async (userId) => {
  const response = await api.get(`/risk/user/${userId}/baseline`);
  return response.data;
};

export const getHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
