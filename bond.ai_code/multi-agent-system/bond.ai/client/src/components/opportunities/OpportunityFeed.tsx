import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import './OpportunityFeed.css';

interface Opportunity {
  id: string;
  type: 'collaboration' | 'introduction' | 'hiring' | 'investment' | 'knowledge_exchange' | 'event';
  title: string;
  description: string;
  participantNames: string[];
  score: number;
  confidence: number;
  reasoning: string[];
  potentialValue: number;
  timeframe: string;
  effort: string;
  nextSteps: string[];
  risks: string[];
}

export const OpportunityFeed: React.FC = () => {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>('all');

  useEffect(() => {
    loadOpportunities();
  }, [filter]);

  const loadOpportunities = async () => {
    setLoading(true);
    try {
      const data = await api.getOpportunities(filter === 'all' ? undefined : filter);
      setOpportunities(data.opportunities || []);
    } catch (error) {
      console.error('Failed to load opportunities:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDismiss = async (id: string) => {
    try {
      await api.dismissOpportunity(id);
      setOpportunities(opps => opps.filter(o => o.id !== id));
    } catch (error) {
      console.error('Failed to dismiss opportunity:', error);
    }
  };

  const handlePursue = async (id: string) => {
    try {
      await api.pursueOpportunity(id);
      // Optionally update UI or navigate
    } catch (error) {
      console.error('Failed to pursue opportunity:', error);
    }
  };

  const getTypeIcon = (type: string): string => {
    const icons: Record<string, string> = {
      collaboration: '🤝',
      introduction: '👋',
      hiring: '💼',
      investment: '💰',
      knowledge_exchange: '📚',
      event: '🎯',
    };
    return icons[type] || '✨';
  };

  const getTypeColor = (type: string): string => {
    const colors: Record<string, string> = {
      collaboration: 'blue',
      introduction: 'purple',
      hiring: 'green',
      investment: 'orange',
      knowledge_exchange: 'teal',
      event: 'pink',
    };
    return colors[type] || 'gray';
  };

  if (loading) return <div className="loading">Loading opportunities...</div>;

  return (
    <div className="opportunity-feed">
      <div className="feed-header">
        <h2>💡 Opportunity Feed</h2>
        <div className="filter-tabs">
          {['all', 'collaboration', 'introduction', 'hiring', 'investment'].map(tab => (
            <button
              key={tab}
              className={`filter-tab ${filter === tab ? 'active' : ''}`}
              onClick={() => setFilter(tab)}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>
      </div>

      <div className="opportunities-list">
        {opportunities.length === 0 ? (
          <div className="no-opportunities">
            <p>No opportunities found</p>
            <p className="hint">Check back soon or adjust your filters</p>
          </div>
        ) : (
          opportunities.map((opp) => (
            <div key={opp.id} className="opportunity-card">
              <div className="opp-header">
                <div className="opp-type">
                  <span className="type-icon">{getTypeIcon(opp.type)}</span>
                  <span className={`type-badge ${getTypeColor(opp.type)}`}>
                    {opp.type.replace('_', ' ')}
                  </span>
                </div>
                <div className="opp-score">
                  <div className="score-value">{opp.score}</div>
                  <div className="score-label">Score</div>
                </div>
              </div>

              <h3 className="opp-title">{opp.title}</h3>
              <p className="opp-description">{opp.description}</p>

              {opp.participantNames.length > 0 && (
                <div className="participants">
                  <strong>With:</strong> {opp.participantNames.join(', ')}
                </div>
              )}

              {opp.reasoning.length > 0 && (
                <div className="reasoning">
                  <strong>Why this is a good opportunity:</strong>
                  <ul>
                    {opp.reasoning.map((reason, i) => (
                      <li key={i}>{reason}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="opp-metadata">
                <span className="metadata-item">
                  ⏱️ {opp.timeframe}
                </span>
                <span className="metadata-item">
                  💪 {opp.effort} effort
                </span>
                <span className="metadata-item">
                  🎯 {Math.round(opp.potentialValue * 100)}% value
                </span>
                <span className="metadata-item">
                  ✅ {Math.round(opp.confidence * 100)}% confidence
                </span>
              </div>

              {opp.nextSteps.length > 0 && (
                <div className="next-steps">
                  <strong>Next Steps:</strong>
                  <ol>
                    {opp.nextSteps.map((step, i) => (
                      <li key={i}>{step}</li>
                    ))}
                  </ol>
                </div>
              )}

              <div className="opp-actions">
                <button
                  className="btn-primary"
                  onClick={() => handlePursue(opp.id)}
                >
                  Pursue Opportunity
                </button>
                <button className="btn-secondary">
                  Learn More
                </button>
                <button
                  className="btn-tertiary"
                  onClick={() => handleDismiss(opp.id)}
                >
                  Dismiss
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default OpportunityFeed;
