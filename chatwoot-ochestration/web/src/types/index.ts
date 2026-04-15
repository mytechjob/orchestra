export interface User {
  id: number;
  username: string;
  email: string;
  role: 'admin' | 'user';
  created_at: string;
}

export interface Customer {
  id: number;
  chatwoot_contact_id: string;
  name: string | null;
  email: string | null;
  phone: string | null;
  extracted_data: any;
  created_at: string;
}

export interface Message {
  sender: 'user' | 'agent';
  content: string;
  time: string;
}

export interface Conversation {
  conversation_id: string;
  status: string;
  created_at: string;
  messages: Message[];
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface ChatResponse {
  user_id: number;
  response: string;
  customer_provided: boolean;
}
