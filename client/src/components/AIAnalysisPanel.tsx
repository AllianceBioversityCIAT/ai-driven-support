import React, { useState, useEffect } from 'react';
import { apiClient } from '../services/api';
import { GlassCard } from './GlassCard';
import { Button } from './Button';
import styles from './AIAnalysisPanel.module.css';

interface AnalysisData {
  summary: string;
  possible_categories: Array<{
    category: string;
    confidence: 'high' | 'medium' | 'low';
    reason: string;
  }>;
  possible_automations: Array<{
    automation: string;
    description: string;
    feasibility: 'high' | 'medium' | 'low';
  }>;
  user_sentiment: {
    overall_feeling: 'positive' | 'neutral' | 'negative' | 'frustrated' | 'urgent';
    indicators: string[];
    urgency_level: 'low' | 'medium' | 'high' | 'critical';
  };
}

interface AIAnalysisPanelProps {
  ticketId: string;
  ticketData?: any;
  onClose: () => void;
}

const sentimentColors: Record<string, string> = {
  positive: '#10b981',
  neutral: '#6b7280',
  negative: '#ef4444',
  frustrated: '#f59e0b',
  urgent: '#dc2626',
};

const confidenceColors: Record<string, string> = {
  high: '#10b981',
  medium: '#f59e0b',
  low: '#ef4444',
};

const AIAnalysisPanel: React.FC<AIAnalysisPanelProps> = ({ ticketId, ticketData, onClose }) => {
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await apiClient.analyzeTicket(Number(ticketId));

        if (response.status === 'success' && response.analysis.status === 'success') {
          setAnalysis(response.analysis.analysis);
        } else {
          setError(response.analysis.message || 'Failed to analyze ticket');
        }
      } catch (err: any) {
        console.error('Error analyzing ticket:', err);
        setError(err.message || 'Failed to analyze ticket');
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, [ticketId]);

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className={styles.header}>
          <h2>🤖 AI Analysis</h2>
          <button className={styles.closeButton} onClick={onClose}>
            ✕
          </button>
        </div>

        {/* Content */}
        <div className={styles.content}>
          {loading ? (
            <div className={styles.loading}>
              <div className={styles.spinner}></div>
              <p>Analyzing ticket...</p>
            </div>
          ) : error ? (
            <GlassCard>
              <div className={styles.error}>
                <p style={{ color: '#ef4444' }}>⚠️ {error}</p>
              </div>
            </GlassCard>
          ) : analysis ? (
            <>
              {/* Summary */}
              <GlassCard>
                <div className={styles.section}>
                  <h3 className={styles.sectionTitle}>📝 Summary</h3>
                  <p className={styles.summary}>{analysis.summary}</p>
                </div>
              </GlassCard>

              {/* Categories */}
              {analysis.possible_categories && analysis.possible_categories.length > 0 && (
                <GlassCard>
                  <div className={styles.section}>
                    <h3 className={styles.sectionTitle}>🏷️ Possible Categories</h3>
                    <div className={styles.categoriesList}>
                      {analysis.possible_categories.map((cat, idx) => (
                        <div key={idx} className={styles.categoryItem}>
                          <div className={styles.categoryHeader}>
                            <span className={styles.categoryName}>{cat.category}</span>
                            <span
                              className={styles.confidence}
                              style={{ borderColor: confidenceColors[cat.confidence] }}
                            >
                              {cat.confidence}
                            </span>
                          </div>
                          <p className={styles.categoryReason}>{cat.reason}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </GlassCard>
              )}

              {/* Automations */}
              {analysis.possible_automations && analysis.possible_automations.length > 0 && (
                <GlassCard>
                  <div className={styles.section}>
                    <h3 className={styles.sectionTitle}>⚙️ Possible Automations</h3>
                    <div className={styles.automationsList}>
                      {analysis.possible_automations.map((auto, idx) => (
                        <div key={idx} className={styles.automationItem}>
                          <div className={styles.automationHeader}>
                            <span className={styles.automationName}>{auto.automation}</span>
                            <span
                              className={styles.feasibility}
                              style={{ borderColor: confidenceColors[auto.feasibility] }}
                            >
                              {auto.feasibility}
                            </span>
                          </div>
                          <p className={styles.automationDesc}>{auto.description}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </GlassCard>
              )}

              {/* User Sentiment */}
              {analysis.user_sentiment && (
                <GlassCard>
                  <div className={styles.section}>
                    <h3 className={styles.sectionTitle}>💭 User Sentiment</h3>
                    <div className={styles.sentimentBox}>
                      <div className={styles.sentimentRow}>
                        <span className={styles.label}>Overall Feeling:</span>
                        <span
                          className={styles.sentiment}
                          style={{
                            color: sentimentColors[analysis.user_sentiment.overall_feeling],
                          }}
                        >
                          {analysis.user_sentiment.overall_feeling.toUpperCase()}
                        </span>
                      </div>
                      <div className={styles.sentimentRow}>
                        <span className={styles.label}>Urgency Level:</span>
                        <span
                          className={styles.urgency}
                          style={{
                            color:
                              confidenceColors[
                                analysis.user_sentiment.urgency_level === 'critical'
                                  ? 'low'
                                  : analysis.user_sentiment.urgency_level
                              ],
                          }}
                        >
                          {analysis.user_sentiment.urgency_level.toUpperCase()}
                        </span>
                      </div>
                      {analysis.user_sentiment.indicators &&
                        analysis.user_sentiment.indicators.length > 0 && (
                          <div className={styles.indicatorsList}>
                            <span className={styles.label}>Indicators:</span>
                            <div className={styles.indicators}>
                              {analysis.user_sentiment.indicators.map((indicator, idx) => (
                                <span key={idx} className={styles.indicator}>
                                  "{indicator}"
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                    </div>
                  </div>
                </GlassCard>
              )}
            </>
          ) : (
            <div className={styles.empty}>No analysis available</div>
          )}
        </div>

        {/* Footer */}
        <div className={styles.footer}>
          <Button variant="secondary" onClick={onClose}>
            Close
          </Button>
        </div>
      </div>
    </div>
  );
};

export default AIAnalysisPanel;
