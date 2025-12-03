import React from 'react';
import { useNavigate } from 'react-router-dom';
import { GlassCard } from './GlassCard';
import styles from './TicketCard.module.css';

interface Ticket {
  id: number;
  subject: string;
  status: number | string;
  priority: number | string;
  created_at: string;
  requester_id?: number;
}

interface TicketCardProps {
  ticket: Ticket;
}

// Mapeo de status números a strings
const statusMap: Record<number, string> = {
  2: 'open',
  3: 'pending',
  4: 'resolved',
  5: 'closed',
};

// Mapeo de priority números a strings
const priorityMap: Record<number, string> = {
  1: 'low',
  2: 'medium',
  3: 'high',
  4: 'urgent',
};

const statusColors: Record<string, string> = {
  open: '#10b981',
  in_progress: '#f59e0b',
  pending: '#f59e0b',
  resolved: '#8b5cf6',
  closed: '#6b7280',
};

const priorityColors: Record<string, string> = {
  low: '#10b981',
  medium: '#f59e0b',
  high: '#ef4444',
  urgent: '#dc2626',
};

export const TicketCard: React.FC<TicketCardProps> = ({ ticket }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/ticket/${ticket.id}`);
  };

  // Convertir números a strings si es necesario
  const statusNum =
    typeof ticket.status === 'number' ? ticket.status : parseInt(ticket.status as string);
  const priorityNum =
    typeof ticket.priority === 'number' ? ticket.priority : parseInt(ticket.priority as string);

  const status = statusMap[statusNum] || 'unknown';
  const priority = priorityMap[priorityNum] || 'medium';

  const statusDisplay = status.replace(/_/g, ' ').toUpperCase().charAt(0) + status.slice(1);
  const priorityDisplay = priority.toUpperCase().charAt(0) + priority.slice(1);

  return (
    <GlassCard onClick={handleClick} hover className={styles.ticketCard}>
      <div className={styles.header}>
        <div className={styles.titleSection}>
          <h3 className={styles.subject}>{ticket.subject}</h3>
          <p className={styles.id}>#{ticket.id}</p>
        </div>
      </div>

      <div className={styles.content}>
        <p className={styles.description}>{ticket.subject}</p>
      </div>

      <div className={styles.footer}>
        <div className={styles.badges}>
          <span
            className={styles.status}
            style={{
              borderColor: statusColors[status] || '#6b7280',
              color: statusColors[status] || '#6b7280',
            }}
          >
            {statusDisplay}
          </span>
          <span
            className={styles.priority}
            style={{
              borderColor: priorityColors[priority] || '#6b7280',
              color: priorityColors[priority] || '#6b7280',
            }}
          >
            {priorityDisplay}
          </span>
        </div>
        <time className={styles.timestamp}>{new Date(ticket.created_at).toLocaleDateString()}</time>
      </div>
    </GlassCard>
  );
};
