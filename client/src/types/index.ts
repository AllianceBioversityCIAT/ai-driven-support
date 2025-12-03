/**
 * TypeScript type definitions for the API
 */

export interface Ticket {
  id: number;
  subject: string;
  type: string;
  status: string;
  priority: string;
  created_at: string;
  updated_at: string;
  requester_id: number;
  description?: string;
  conversations?: Conversation[];
  custom_fields?: Record<string, any>;
}

export interface Conversation {
  id: number;
  body: string;
  user_id?: number;
  created_at: string;
}

export interface TicketSummary {
  ticket_id: number;
  subject: string;
  summary: string;
  classification: string;
  automation_opportunities: string[];
}

export interface APIResponse<T> {
  status: string;
  data: T;
  message?: string;
}

export interface PaginatedResponse<T> {
  page: number;
  per_page: number;
  total_count: number;
  data: T[];
}
