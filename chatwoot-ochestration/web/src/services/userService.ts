import api from '../api/axios';
import type { User } from '../types';

export const userService = {
  getUsers: async (): Promise<User[]> => {
    const response = await api.get('/api/users');
    return response.data;
  },

  createUser: async (userData: any): Promise<User> => {
    const response = await api.post('/api/users', userData);
    return response.data;
  }
};
