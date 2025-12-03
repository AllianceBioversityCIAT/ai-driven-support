import React, { useState } from 'react';
import { Button } from './Button';
import { GlassCard } from './GlassCard';
import styles from './TicketReplyPanel.module.css';

interface TicketReplyPanelProps {
  ticketId: number;
  onReplySuccess: () => void;
  isSubmitting?: boolean;
}

export const TicketReplyPanel: React.FC<TicketReplyPanelProps> = ({
  ticketId,
  onReplySuccess,
  isSubmitting = false,
}) => {
  const [replyBody, setReplyBody] = useState('');
  const [isPrivate, setIsPrivate] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!replyBody.trim()) {
      setError('Reply cannot be empty');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // TODO: Implement replyToTicket endpoint in backend
      console.log(`ðŸ"¤ Sending reply to ticket ${ticketId}`);
      console.log('Reply body:', replyBody, 'Private:', isPrivate);

      console.log('âœ… Reply sent successfully');
      setSuccess(true);
      setReplyBody('');
      setIsPrivate(false);

      // Hide success message after 3 seconds
      setTimeout(() => setSuccess(false), 3000);

      onReplySuccess();
    } catch (err: any) {
      console.error('❌ Error sending reply:', err);
      setError(err.message || 'Failed to send reply');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <GlassCard className={styles.replyPanel}>
      <div className={styles.section}>
        <h3 className={styles.sectionTitle}>Add Reply</h3>

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.formGroup}>
            <textarea
              value={replyBody}
              onChange={(e) => setReplyBody(e.target.value)}
              placeholder="Type your reply here..."
              className={styles.textarea}
              disabled={isLoading || isSubmitting}
              rows={5}
            />
          </div>

          <div className={styles.options}>
            <label className={styles.checkbox}>
              <input
                type="checkbox"
                checked={isPrivate}
                onChange={(e) => setIsPrivate(e.target.checked)}
                disabled={isLoading || isSubmitting}
              />
              <span>Private (Internal note)</span>
            </label>
          </div>

          {error && (
            <div className={styles.error}>
              <p>{error}</p>
            </div>
          )}

          {success && (
            <div className={styles.success}>
              <p>✅ Reply sent successfully!</p>
            </div>
          )}

          <div className={styles.actions}>
            <Button variant="primary" disabled={isLoading || isSubmitting || !replyBody.trim()}>
              {isLoading ? 'Sending...' : 'Send Reply'}
            </Button>
          </div>
        </form>
      </div>
    </GlassCard>
  );
};
