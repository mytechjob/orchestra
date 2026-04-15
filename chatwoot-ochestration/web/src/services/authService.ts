import api from '../api/axios';
import type { AuthResponse, User } from '../types';

export const authService = {
  login: async (credentials: any): Promise<AuthResponse> => {
    const response = await api.post('/api/auth/login', credentials);
    return response.data;
  },

  register: async (userData: any): Promise<User> => {
    const response = await api.post('/api/auth/register', userData);
    return response.data;
  },

  getMe: async (): Promise<User> => {
    const response = await api.get('/api/auth/me');
    return response.data;
  }
};
