import { create } from 'zustand';

export interface Ticket {
  group_id: number;
  id: number;
  subject: string;
  type: string;
  status: string;
  priority: string;
  created_at: string;
  updated_at: string;
  requester_id: number;
  description?: string;
  conversations?: any[];
}

export interface PaginationState {
  page: number;
  per_page: number;
  total: number;
  has_more: boolean;
}

interface TicketStore {
  tickets: Ticket[];
  selectedTicket: Ticket | null;
  isLoading: boolean;
  error: string | null;
  pagination: PaginationState;
  setTickets: (tickets: Ticket[]) => void;
  appendTickets: (tickets: Ticket[]) => void;
  setSelectedTicket: (ticket: Ticket | null) => void;
  setIsLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setPagination: (pagination: PaginationState) => void;
  setCurrentPage: (page: number) => void;
}

export const useTicketStore = create<TicketStore>((set) => ({
  tickets: [],
  selectedTicket: null,
  isLoading: false,
  error: null,
  pagination: {
    page: 1,
    per_page: 30,
    total: 0,
    has_more: false,
  },
  setTickets: (tickets) => set({ tickets }),
  appendTickets: (newTickets) =>
    set((state) => ({
      tickets: [...state.tickets, ...newTickets],
    })),
  setSelectedTicket: (ticket) => set({ selectedTicket: ticket }),
  setIsLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),
  setPagination: (pagination) => set({ pagination }),
  setCurrentPage: (page) =>
    set((state) => ({
      pagination: { ...state.pagination, page },
    })),
}));

interface AuthStore {
  isAuthenticated: boolean;
  user: any | null;
  setAuthenticated: (value: boolean) => void;
  setUser: (user: any) => void;
}

export const useAuthStore = create<AuthStore>((set) => ({
  isAuthenticated: false,
  user: null,
  setAuthenticated: (value) => set({ isAuthenticated: value }),
  setUser: (user) => set({ user }),
}));
