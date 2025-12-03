import React from 'react';
import { GlassCard } from './GlassCard';
import styles from './TicketConversations.module.css';

interface Conversation {
  id: number;
  body: string;
  body_text?: string;
  private: boolean;
  user_id?: number;
  created_at: string;
  updated_at?: string;
  source?: number;
  from_email?: string;
  to_emails?: string[];
  cc_emails?: string[];
  incoming?: boolean;
  attachments?: Array<{
    id: number;
    name: string;
    size: number;
    attachment_url: string;
  }>;
}

interface TicketConversationsProps {
  conversations: Conversation[];
  isLoading?: boolean;
}

const sourceMap: Record<number, string> = {
  0: '📧 Email',
  1: '💬 Portal',
  2: '📞 Phone',
  3: '🔧 API',
  4: '⚙️ System',
  1002: '📧 Email Forward',
};

export const TicketConversations: React.FC<TicketConversationsProps> = ({
  conversations,
  isLoading = false,
}) => {
  console.log('🔄 TicketConversations rendered with:', conversations);

  if (isLoading) {
    return (
      <GlassCard>
        <div className={styles.loading}>
          <div className={styles.spinner}></div>
          <p>Loading conversations...</p>
        </div>
      </GlassCard>
    );
  }

  if (!conversations || conversations.length === 0) {
    return (
      <GlassCard>
        <div className={styles.emptyState}>
          <p>No conversations yet</p>
        </div>
      </GlassCard>
    );
  }

  return (
    <div className={styles.conversationsContainer}>
      <h2 className={styles.title}>Conversation Thread ({conversations.length})</h2>

      <div className={styles.timeline}>
        {conversations.map((conversation) => {
          return (
            <div key={conversation.id} className={styles.conversationItem}>
              {/* Timeline dot */}
              <div className={styles.timelineDot} />

              {/* Conversation card */}
              <GlassCard
                className={`${styles.conversationCard} ${
                  conversation.private ? styles.private : ''
                }`}
              >
                {/* Header with source and timestamp */}
                <div className={styles.conversationHeader}>
                  <div className={styles.headerInfo}>
                    <div className={styles.source}>
                      {sourceMap[conversation.source || 0] || '📧 Email'}
                    </div>
                    {conversation.private && (
                      <span className={styles.privateLabel}>🔒 Private Note</span>
                    )}
                    {conversation.from_email && (
                      <span className={styles.sender}>{conversation.from_email}</span>
                    )}
                  </div>
                  <time className={styles.timestamp}>
                    {new Date(conversation.created_at).toLocaleString()}
                  </time>
                </div>

                {/* Email Recipients Section */}
                {(conversation.to_emails?.length ||
                  0 > 0 ||
                  conversation.cc_emails?.length ||
                  0 > 0) && (
                  <div className={styles.emailRecipients}>
                    {conversation.to_emails && conversation.to_emails.length > 0 && (
                      <div className={styles.emailGroup}>
                        <span className={styles.emailLabel}>To:</span>
                        <span className={styles.emailValues}>
                          {conversation.to_emails.join(', ')}
                        </span>
                      </div>
                    )}

                    {conversation.cc_emails && conversation.cc_emails.length > 0 && (
                      <div className={styles.emailGroup}>
                        <span className={styles.emailLabel}>CC:</span>
                        <span className={styles.emailValues}>
                          {conversation.cc_emails.join(', ')}
                        </span>
                      </div>
                    )}
                  </div>
                )}

                {/* Divider */}
                {(conversation.to_emails?.length ||
                  0 > 0 ||
                  conversation.cc_emails?.length ||
                  0 > 0) && <div className={styles.divider} />}

                {/* Body */}
                <div className={styles.conversationBody}>
                  {conversation.body_text || conversation.body}
                </div>

                {/* Attachments */}
                {conversation.attachments && conversation.attachments.length > 0 && (
                  <div className={styles.attachments}>
                    <h4 className={styles.attachmentsTitle}>Attachments</h4>
                    <div className={styles.attachmentList}>
                      {conversation.attachments.map((attachment) => (
                        <a
                          key={attachment.id}
                          href={attachment.attachment_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className={styles.attachmentItem}
                        >
                          <span>📎 {attachment.name}</span>
                          <span className={styles.size}>
                            {(attachment.size / 1024).toFixed(2)} KB
                          </span>
                        </a>
                      ))}
                    </div>
                  </div>
                )}
              </GlassCard>
            </div>
          );
        })}
      </div>
    </div>
  );
};
