import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Navigation } from '../components/Navigation';
import TicketDetailView from '../components/TicketDetailView';
import { useTicketDetail } from '../hooks/useTickets';
import styles from './TicketPage.module.css';

export const TicketPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { fetchTicketDetail } = useTicketDetail();
  const [ticket, setTicket] = React.useState<any>(null);
  const [isLoading, setIsLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  useEffect(() => {
    if (!id) {
      setError('Ticket ID not provided');
      setIsLoading(false);
      return;
    }

    const loadTicket = async () => {
      try {
        setIsLoading(true);
        const ticketId = parseInt(id, 10);
        console.log(`🔄 Loading ticket ${ticketId}...`);
        const response = await fetchTicketDetail(ticketId);

        console.log('✅ Raw response:', response);

        // Extract ticket data from nested structure
        const ticketData = response.ticket || response;
        const conversations = response.conversations || [];

        setTicket(response);

        console.log('✅ Ticket loaded:', ticketData);
        console.log('📎 Attachments:', ticketData?.attachments);
        console.log('📧 CC Emails:', ticketData?.cc_emails);
        console.log('📝 Description:', ticketData?.description_text);
        console.log('🔄 Conversations:', conversations.length);
        console.log('💬 Conversations data:', conversations);

        setError(null);
      } catch (err: any) {
        console.error('❌ Error loading ticket:', err);
        setError(err.message || 'Failed to load ticket');
      } finally {
        setIsLoading(false);
      }
    };

    loadTicket();
  }, [id, fetchTicketDetail]);

  const handleBack = () => {
    navigate('/');
  };

  // Extract ticket data from nested structure AND include conversations
  const ticketData = ticket?.ticket || ticket;
  const conversations = ticket?.conversations || [];

  console.log('🎫 Final ticketData:', ticketData);
  console.log('💬 Final conversations:', conversations);

  return (
    <div className={styles.page}>
      <Navigation title="FreshAI Service" />
      <main className={styles.container}>
        <TicketDetailView
          ticket={ticketData ? { ...ticketData, conversations } : null}
          isLoading={isLoading}
          error={error}
          onBack={handleBack}
        />
      </main>
    </div>
  );
};
