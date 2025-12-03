import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '../services/api';
import { useTicketStore } from '../store';

export const useTickets = () => {
  const { setTickets, appendTickets, setIsLoading, setError, setPagination } = useTicketStore();
  const [loading, setLoading] = useState(true);

  const fetchTickets = useCallback(
    async (page: number = 1, per_page: number = 30, groupId?: number | null) => {
      setIsLoading(true);
      if (page === 1) setLoading(true); // Only show loading for first page
      setError(null);

      try {
        console.log('📋 Fetching tickets...', { page, per_page, groupId });
        const response = await apiClient.listTickets(page, per_page, groupId);
        console.log('✅ Response:', response);

        if (response?.tickets) {
          // If it's the first page, replace tickets; otherwise append
          if (page === 1) {
            setTickets(response.tickets);
          } else {
            appendTickets(response.tickets);
          }
          setPagination(response.pagination);
        } else {
          if (page === 1) {
            setTickets([]);
          }
        }
      } catch (error: any) {
        console.error('❌ Error:', error);
        setError('Failed to fetch tickets');
        if (page === 1) {
          setTickets([]);
        }
      } finally {
        setIsLoading(false);
        if (page === 1) setLoading(false);
      }
    },
    [setTickets, appendTickets, setIsLoading, setError, setPagination]
  );

  const searchTickets = useCallback(
    async (query: string) => {
      setIsLoading(true);
      try {
        console.log('🔍 Searching tickets for:', query);
        const response = await apiClient.searchTickets(query);
        if (response?.status === 'success') {
          setTickets(response.results || []);
        }
      } catch (error: any) {
        console.error('❌ Search error:', error);
        setError('Failed to search tickets');
      } finally {
        setIsLoading(false);
      }
    },
    [setTickets, setIsLoading, setError]
  );

  useEffect(() => {
    fetchTickets();
  }, [fetchTickets]);

  return {
    loading,
    fetchTickets,
    searchTickets,
  };
};

export const useTicketDetail = () => {
  const { setSelectedTicket, setIsLoading, setError } = useTicketStore();
  const fetchTicketDetail = useCallback(
    async (ticketId: number) => {
      setIsLoading(true);
      try {
        console.log('🎫 Fetching ticket detail:', ticketId);
        const response = await apiClient.getTicket(ticketId, true);

        if (response?.status === 'success' && response?.ticket) {
          setSelectedTicket(response.ticket);
          return response.ticket;
        }
      } catch (error: any) {
        console.error('❌ Error fetching ticket detail:', error);
        setError('Failed to fetch ticket details');
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    [setSelectedTicket, setIsLoading, setError]
  );

  return {
    fetchTicketDetail,
  };
};
