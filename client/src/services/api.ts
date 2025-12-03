import type { AxiosInstance, AxiosError } from 'axios';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface PaginationData {
  page: number;
  per_page: number;
  total: number;
  has_more: boolean;
}

interface ListTicketsResponse {
  tickets: any[];
  pagination: PaginationData;
}

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor for auth token (if needed)
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('auth_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Add error interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Tickets
  async listTickets(
    page: number = 1,
    per_page: number = 30,
    groupId?: number | null
  ): Promise<ListTicketsResponse> {
    const response = await this.client.get('/tickets', {
      params: { page, per_page, ...(groupId && { group_id: groupId }) },
    });
    // Extract nested pagination data from response.data.data structure
    const { data } = response.data;
    return {
      tickets: data?.tickets || [],
      pagination: data?.pagination || {
        page,
        per_page,
        total: 0,
        has_more: false,
      },
    };
  }

  async getTicket(id: number, include_conversations: boolean = false) {
    const response = await this.client.get(`/tickets/${id}`, {
      params: { include_conversations },
    });
    return response.data;
  }

  async getTicketSummary(id: number) {
    const response = await this.client.get(`/tickets/${id}/summary`);
    return response.data;
  }

  async searchTickets(query: string) {
    const response = await this.client.get('/tickets/search', {
      params: { query },
    });
    return response.data;
  }

  async getTicketConversations(ticket_id: number) {
    const response = await this.client.get(`/tickets/${ticket_id}`, {
      params: { include_conversations: true },
    });
    return response.data?.ticket?.conversations || [];
  }

  // Health
  async getHealth() {
    const response = await this.client.get('/health');
    return response.data;
  }
}

export const apiClient = new APIClient();

// Export as ticketAPI for backward compatibility
export const ticketAPI = apiClient;
