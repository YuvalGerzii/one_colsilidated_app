import React, { useState, useCallback } from 'react';
import api from '../../services/api';
import './IntentBasedSearch.css';

interface SearchResult {
  userId: string;
  name: string;
  jobTitle: string;
  company: string;
  matchScore: number;
  reasoning: string[];
  profileImage?: string;
}

interface Intent {
  primaryIntent: string;
  confidence: number;
  entities: {
    people: string[];
    skills: string[];
    industries: string[];
    locations: string[];
  };
  suggestedActions: Array<{
    action: string;
    priority: string;
  }>;
}

export const IntentBasedSearch: React.FC = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [intent, setIntent] = useState<Intent | null>(null);
  const [results, setResults] = useState<SearchResult[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = useCallback(async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await api.intentBasedSearch(query);

      setIntent(response.intent);
      setResults(response.results || []);
    } catch (err: any) {
      setError(err.message || 'Search failed');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  }, [query]);

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSearch();
    }
  };

  const getIntentBadgeColor = (intent: string): string => {
    const colors: Record<string, string> = {
      seeking_connection: 'blue',
      offering_help: 'green',
      requesting_introduction: 'purple',
      seeking_collaboration: 'orange',
      sharing_opportunity: 'teal',
    };
    return colors[intent] || 'gray';
  };

  return (
    <div className="intent-search">
      <div className="search-header">
        <h2>🔍 Intent-Based Search</h2>
        <p className="search-subtitle">
          Describe what you're looking for in natural language
        </p>
      </div>

      <div className="search-input-container">
        <textarea
          className="search-input"
          placeholder="Example: Looking for someone who can help with fundraising in Europe..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          rows={3}
        />
        <button
          className="search-button"
          onClick={handleSearch}
          disabled={loading || !query.trim()}
        >
          {loading ? '🔄 Analyzing...' : '🚀 Search'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          ⚠️ {error}
        </div>
      )}

      {intent && (
        <div className="intent-detected">
          <div className="intent-header">
            <h3>🎯 Detected Intent</h3>
            <span className={`intent-badge ${getIntentBadgeColor(intent.primaryIntent)}`}>
              {intent.primaryIntent.replace(/_/g, ' ')}
            </span>
            <span className="confidence-score">
              {Math.round(intent.confidence * 100)}% confidence
            </span>
          </div>

          {intent.entities && (
            <div className="entities-detected">
              {intent.entities.skills.length > 0 && (
                <div className="entity-group">
                  <strong>Skills:</strong>{' '}
                  {intent.entities.skills.map((skill, i) => (
                    <span key={i} className="entity-tag skill">{skill}</span>
                  ))}
                </div>
              )}

              {intent.entities.industries.length > 0 && (
                <div className="entity-group">
                  <strong>Industries:</strong>{' '}
                  {intent.entities.industries.map((industry, i) => (
                    <span key={i} className="entity-tag industry">{industry}</span>
                  ))}
                </div>
              )}

              {intent.entities.locations.length > 0 && (
                <div className="entity-group">
                  <strong>Locations:</strong>{' '}
                  {intent.entities.locations.map((location, i) => (
                    <span key={i} className="entity-tag location">{location}</span>
                  ))}
                </div>
              )}
            </div>
          )}

          {intent.suggestedActions && intent.suggestedActions.length > 0 && (
            <div className="suggested-actions">
              <h4>💡 Suggested Actions</h4>
              <ul>
                {intent.suggestedActions.map((action, i) => (
                  <li key={i} className={`action-${action.priority}`}>
                    <span className="action-priority">[{action.priority}]</span>
                    {action.action}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {results.length > 0 && (
        <div className="search-results">
          <h3>📋 Found {results.length} Matches</h3>

          <div className="results-grid">
            {results.map((result) => (
              <div key={result.userId} className="result-card">
                <div className="result-header">
                  <div className="result-avatar">
                    {result.profileImage ? (
                      <img src={result.profileImage} alt={result.name} />
                    ) : (
                      <div className="avatar-placeholder">
                        {result.name.split(' ').map(n => n[0]).join('')}
                      </div>
                    )}
                  </div>
                  <div className="result-info">
                    <h4>{result.name}</h4>
                    <p className="job-title">{result.jobTitle}</p>
                    <p className="company">{result.company}</p>
                  </div>
                  <div className="match-score">
                    <div className="score-circle">
                      {result.matchScore}
                    </div>
                    <span className="score-label">Match</span>
                  </div>
                </div>

                {result.reasoning && result.reasoning.length > 0 && (
                  <div className="reasoning">
                    <strong>Why this match:</strong>
                    <ul>
                      {result.reasoning.map((reason, i) => (
                        <li key={i}>{reason}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <div className="result-actions">
                  <button className="btn-primary">Connect</button>
                  <button className="btn-secondary">View Profile</button>
                  <button className="btn-tertiary">Request Intro</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {!loading && results.length === 0 && intent && (
        <div className="no-results">
          <p>No matches found for your query.</p>
          <p>Try adjusting your search or exploring recommended connections.</p>
        </div>
      )}
    </div>
  );
};

export default IntentBasedSearch;
