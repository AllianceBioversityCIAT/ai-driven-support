import React, { useState } from 'react';
import styles from './AIAnalysisPanel.module.css';
import { Button } from './Button';

interface AnalysisResult {
  summary?: string;
  classification?: string;
  opportunities?: string[];
  sentiment?: string;
}

interface AIAnalysisPanelProps {
  ticketId?: string;
  ticketData?: any;
  onClose?: () => void;
}

const AIAnalysisPanel: React.FC<AIAnalysisPanelProps> = ({ ticketId, onClose }) => {
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [analysisType, setAnalysisType] = useState<'request' | 'thread' | null>(null);

  const handleAnalyze = async (type: 'request' | 'thread') => {
    try {
      if (!ticketId) {
        setError('No ticket ID provided');
        return;
      }

      setLoading(true);
      setError(null);
      setAnalysis(null);
      setAnalysisType(type);

      const API_URL = 'http://localhost:8000';
      const url = `${API_URL}/api/tickets/${ticketId}/analyze`;

      console.log(`🤖 Analyzing ticket ${ticketId} (${type}) at ${url}`);

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      console.log(`📡 Response status: ${response.status}`);

      if (!response.ok) {
        const errorText = await response.text();
        console.error(`❌ API Error: ${response.status} - ${errorText}`);
        throw new Error(`HTTP Error: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Analysis response:', data);

      if (data.analysis) {
        setAnalysis(data.analysis);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      console.error('❌ Error analyzing ticket:', message);
      setError(`Failed to analyze: ${message}`);
    } finally {
      setLoading(false);
    }
  };

  const closeModal = () => {
    setAnalysisType(null);
    setAnalysis(null);
    setError(null);
    if (onClose) onClose();
  };

  return (
    <div className={styles.modal}>
      <div className={styles.modalContent}>
        <button className={styles.closeButton} onClick={closeModal}>
          ×
        </button>

        {!analysisType ? (
          // Selection screen
          <div>
            <h2>🤖 AI Analysis</h2>
            <p style={{ marginBottom: '20px', color: '#666' }}>What would you like to analyze?</p>

            <div style={{ display: 'flex', gap: '10px', flexDirection: 'column' }}>
              <Button onClick={() => handleAnalyze('request')}>📝 Analyze Request Only</Button>
              <Button onClick={() => handleAnalyze('thread')}>💬 Analyze with Thread</Button>
            </div>
          </div>
        ) : (
          // Results screen
          <div>
            <h2>🤖 AI Analysis Results</h2>
            <p style={{ fontSize: '0.9rem', color: '#666', marginBottom: '15px' }}>
              Analysis type:{' '}
              <strong>{analysisType === 'request' ? 'Request Only' : 'Request + Thread'}</strong>
            </p>

            {error && <div className={styles.error}>❌ {error}</div>}

            {loading && <div className={styles.loading}>🔄 Analyzing ticket...</div>}

            {analysis && (
              <div className={styles.results}>
                {analysis.summary && (
                  <div className={styles.section}>
                    <h4>📋 Summary</h4>
                    <p style={{ whiteSpace: 'pre-wrap' }}>{analysis.summary}</p>
                  </div>
                )}

                {analysis.classification && (
                  <div className={styles.section}>
                    <h4>🏷️ Classification</h4>
                    <p>
                      <strong>{analysis.classification}</strong>
                    </p>
                  </div>
                )}

                {analysis.sentiment && (
                  <div className={styles.section}>
                    <h4>😊 Sentiment & Emotions</h4>
                    <p>{analysis.sentiment}</p>
                  </div>
                )}

                {analysis.opportunities && analysis.opportunities.length > 0 && (
                  <div className={styles.section}>
                    <h4>⚡ Automation Opportunities</h4>
                    <ul>
                      {analysis.opportunities.map((opp: string, idx: number) => (
                        <li key={idx}>{opp}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
              <Button onClick={() => setAnalysisType(null)}>⬅️ Back</Button>
              <Button onClick={closeModal}>✖️ Close</Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AIAnalysisPanel;
