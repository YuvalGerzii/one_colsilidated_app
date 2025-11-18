import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import './RelationshipHealthDashboard.css';

interface RelationshipHealth {
  userId: string;
  userName: string;
  overallHealth: number;
  healthCategory: 'thriving' | 'healthy' | 'declining' | 'at_risk' | 'dormant';
  metrics: Record<string, number>;
  trend: {
    direction: 'improving' | 'stable' | 'declining';
    projection30Days: number;
  };
  risks: Array<{ type: string; severity: string; description: string }>;
  recommendations: Array<{ action: string; priority: string; timeframe: string }>;
}

interface NetworkHealthSummary {
  overallNetworkHealth: number;
  totalRelationships: number;
  distribution: Record<string, number>;
  topConcerns: Array<{ userId: string; userName: string; health: number; risk: string }>;
  topOpportunities: Array<{ userId: string; userName: string; opportunity: string }>;
}

export const RelationshipHealthDashboard: React.FC = () => {
  const [summary, setSummary] = useState<NetworkHealthSummary | null>(null);
  const [selectedUser, setSelectedUser] = useState<string | null>(null);
  const [userHealth, setUserHealth] = useState<RelationshipHealth | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSummary();
  }, []);

  const loadSummary = async () => {
    setLoading(true);
    try {
      const data = await api.getRelationshipHealthSummary();
      setSummary(data);
    } catch (error) {
      console.error('Failed to load health summary:', error);
    } finally {
      setLoading(false);
    }
  };

  const getHealthColor = (category: string): string => {
    const colors: Record<string, string> = {
      thriving: '#10b981',
      healthy: '#3b82f6',
      declining: '#f59e0b',
      at_risk: '#ef4444',
      dormant: '#6b7280',
    };
    return colors[category] || '#gray';
  };

  if (loading) return <div className="loading">Loading health data...</div>;
  if (!summary) return <div className="error">Failed to load health data</div>;

  return (
    <div className="health-dashboard">
      <div className="dashboard-header">
        <h2>💚 Relationship Health Dashboard</h2>
      </div>

      <div className="health-summary">
        <div className="summary-card overall-health">
          <h3>Overall Network Health</h3>
          <div className="health-score">
            <div className="score-circle large">
              <span>{summary.overallNetworkHealth}</span>
            </div>
          </div>
          <p>{summary.totalRelationships} total relationships</p>
        </div>

        <div className="summary-card distribution">
          <h3>Health Distribution</h3>
          <div className="distribution-bars">
            {Object.entries(summary.distribution).map(([category, count]) => (
              <div key={category} className="distribution-bar">
                <div className="bar-label">
                  <span>{category}</span>
                  <span>{count}</span>
                </div>
                <div className="bar-track">
                  <div
                    className="bar-fill"
                    style={{
                      width: `${(count / summary.totalRelationships) * 100}%`,
                      backgroundColor: getHealthColor(category)
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="concerns-opportunities">
        <div className="concerns-card">
          <h3>⚠️ Top Concerns ({summary.topConcerns.length})</h3>
          <div className="concern-list">
            {summary.topConcerns.map((concern) => (
              <div key={concern.userId} className="concern-item">
                <div className="concern-info">
                  <strong>{concern.userName}</strong>
                  <p>{concern.risk}</p>
                </div>
                <div className="health-indicator">{concern.health}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="opportunities-card">
          <h3>💡 Top Opportunities ({summary.topOpportunities.length})</h3>
          <div className="opportunity-list">
            {summary.topOpportunities.map((opp) => (
              <div key={opp.userId} className="opportunity-item">
                <div className="opportunity-info">
                  <strong>{opp.userName}</strong>
                  <p>{opp.opportunity}</p>
                </div>
                <button className="btn-action">Take Action</button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default RelationshipHealthDashboard;
