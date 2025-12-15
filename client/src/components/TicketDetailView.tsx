import React, { useState } from 'react';
import { GlassCard } from './GlassCard';
import { Button } from './Button';
import { TicketReplyPanel } from './TicketReplyPanel';
import { TicketConversations } from './TicketConversations';
import AIAnalysisPanel from './AIAnalysisPanel';
import styles from './TicketDetailView.module.css';

interface Ticket {
  id: number;
  subject: string;
  description: string;
  description_text?: string;
  status: number;
  priority: number;
  group_id?: number;
  category?: string;
  sub_category?: string;
  requester_id: number;
  created_at: string;
  updated_at: string;
  type?: string;
  custom_fields?: Record<string, any>;
  attachments?: Array<{
    id: number;
    name: string;
    size: number;
    attachment_url: string;
  }>;
  reply_cc_emails?: string[];
  cc_emails?: string[];
  conversations?: Array<{
    id: number;
    body: string;
    created_at: string;
    updated_at: string;
    private: boolean;
    author: {
      id: number;
      name: string;
      email: string;
    };
  }>;
}

interface TicketDetailViewProps {
  ticket: Ticket | null;
  isLoading: boolean;
  error: string | null;
  onBack: () => void;
}

const priorityLevels: Record<number, string> = {
  1: 'Low',
  2: 'Medium',
  3: 'High',
  4: 'Urgent',
};

const statusLevels: Record<number, string> = {
  2: 'Open',
  3: 'Pending',
  4: 'Resolved',
  5: 'Closed',
};

const priorityColors: Record<string, string> = {
  Low: '#10b981',
  Medium: '#f59e0b',
  High: '#ef4444',
  Urgent: '#dc2626',
};

const groupMap: Record<number, string> = {
  26000250424: 'IT Innovation and Business Development',
  26000171555: 'IT Network Infrastructure and Security',
  26000171552: 'IT Operations and Service Desk',
};

const TicketDetailView: React.FC<TicketDetailViewProps> = ({
  ticket,
  isLoading,
  error,
  onBack,
}) => {
  const [showAIAnalysis, setShowAIAnalysis] = useState(false);

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <div className={styles.spinner}></div>
          <p>Loading ticket details...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.container}>
        <Button onClick={onBack}>← Back</Button>
        <GlassCard>
          <div className={styles.error}>
            <p style={{ color: '#ef4444' }}>Error: {error}</p>
          </div>
        </GlassCard>
      </div>
    );
  }

  if (!ticket) {
    return (
      <div className={styles.container}>
        <Button onClick={onBack}>← Back</Button>
        <GlassCard>
          <div className={styles.empty}>
            <p>No ticket found</p>
          </div>
        </GlassCard>
      </div>
    );
  }

  const priority = priorityLevels[ticket.priority] || 'Unknown';
  const status = statusLevels[ticket.status] || 'Unknown';

  return (
    <div className={styles.container}>
      {/* Back Button */}
      <div className={styles.backButton}>
        <Button onClick={onBack}>← Back to Tickets</Button>
        <Button onClick={() => setShowAIAnalysis(true)}>AI Analysis</Button>
      </div>

      {/* AI Analysis Modal - Only show when requested */}
      {showAIAnalysis && (
        <AIAnalysisPanel
          ticketId={ticket.id.toString()}
          onClose={() => setShowAIAnalysis(false)}
        />
      )}

      {/* Header */}
      <GlassCard className={styles.headerCard}>
        <div className={styles.header}>
          <div className={styles.titleSection}>
            <h1 className={styles.title}>{ticket.subject}</h1>
            <p className={styles.ticketId}>Ticket #{ticket.id}</p>
          </div>
          <div className={styles.badges}>
            <span className={styles.priority} style={{ borderColor: priorityColors[priority] }}>
              {priority}
            </span>
            <span className={styles.status}>{status}</span>
          </div>
        </div>
      </GlassCard>

      {/* Main Content Grid */}
      <div className={styles.contentGrid}>
        {/* Description & Conversations */}
        <div className={styles.mainColumn}>
          {/* Description */}
          <GlassCard className={styles.descriptionCard}>
            <div className={styles.section}>
              <h2 className={styles.sectionTitle}>Description</h2>
              <div className={styles.description}>
                {ticket.description_text || ticket.description}
              </div>
            </div>
          </GlassCard>

          {/* Conversations Thread */}
          {ticket.conversations && ticket.conversations.length > 0 && (
            <TicketConversations conversations={ticket.conversations} />
          )}

          {/* Reply Panel */}
          <TicketReplyPanel
            ticketId={ticket.id}
            onReplySuccess={() => {
              console.log('Reply sent, you can refresh ticket data here');
            }}
          />
        </div>

        {/* Details Sidebar */}
        <div className={styles.sidebar}>
          {/* Metadata */}
          <GlassCard>
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>Details</h3>
              <div className={styles.details}>
                <div className={styles.detailRow}>
                  <span className={styles.label}>Type:</span>
                  <span className={styles.value}>{ticket.type || 'N/A'}</span>
                </div>
                <div className={styles.detailRow}>
                  <span className={styles.label}>Category:</span>
                  <span className={styles.value}>{ticket.category || 'N/A'}</span>
                </div>
                <div className={styles.detailRow}>
                  <span className={styles.label}>Sub Category:</span>
                  <span className={styles.value}>{ticket.sub_category || 'N/A'}</span>
                </div>
                <div className={styles.detailRow}>
                  <span className={styles.label}>Group:</span>
                  <span className={styles.value}>
                    {ticket.group_id
                      ? groupMap[ticket.group_id] || `Group ${ticket.group_id}`
                      : 'N/A'}
                  </span>
                </div>
                <div className={styles.detailRow}>
                  <span className={styles.label}>Status:</span>
                  <span className={styles.value}>{status}</span>
                </div>
                <div className={styles.detailRow}>
                  <span className={styles.label}>Priority:</span>
                  <span className={styles.value}>{priority}</span>
                </div>
              </div>
            </div>
          </GlassCard>

          {/* Dates */}
          <GlassCard>
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>Timeline</h3>
              <div className={styles.details}>
                <div className={styles.detailRow}>
                  <span className={styles.label}>Created:</span>
                  <span className={styles.value}>
                    {new Date(ticket.created_at).toLocaleString()}
                  </span>
                </div>
                <div className={styles.detailRow}>
                  <span className={styles.label}>Updated:</span>
                  <span className={styles.value}>
                    {new Date(ticket.updated_at).toLocaleString()}
                  </span>
                </div>
              </div>
            </div>
          </GlassCard>

          {/* CC Emails */}
          {ticket.cc_emails && ticket.cc_emails.length > 0 && (
            <GlassCard>
              <div className={styles.section}>
                <h3 className={styles.sectionTitle}>CC Emails</h3>
                <div className={styles.emailList}>
                  {ticket.cc_emails.map((email, idx) => (
                    <div key={idx} className={styles.email}>
                      {email}
                    </div>
                  ))}
                </div>
              </div>
            </GlassCard>
          )}

          {/* Attachments */}
          {ticket.attachments && ticket.attachments.length > 0 && (
            <GlassCard>
              <div className={styles.section}>
                <h3 className={styles.sectionTitle}>Attachments</h3>
                <div className={styles.attachmentList}>
                  {ticket.attachments.map((attachment) => (
                    <a
                      key={attachment.id}
                      href={attachment.attachment_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className={styles.attachmentItem}
                    >
                      <span>📎 {attachment.name}</span>
                      <span className={styles.size}>{(attachment.size / 1024).toFixed(2)} KB</span>
                    </a>
                  ))}
                </div>
              </div>
            </GlassCard>
          )}
        </div>
      </div>
    </div>
  );
};

export default TicketDetailView;
