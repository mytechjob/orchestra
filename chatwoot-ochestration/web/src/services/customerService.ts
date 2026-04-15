import api from '../api/axios';
import type { Customer, Conversation, ChatResponse } from '../types';

export const customerService = {
  getCustomerInfo: async (contactId: string): Promise<Customer> => {
    const response = await api.get(`/api/customers/${contactId}`);
    return response.data;
  },

  getCustomerConversations: async (contactId: string): Promise<{ conversations: Conversation[] }> => {
    const response = await api.get(`/api/customers/${contactId}/conversations`);
    return response.data;
  },

  chatWithAgent: async (message: string): Promise<ChatResponse> => {
    const response = await api.post('/api/user/chat', { message });
    return response.data;
  }
};
