import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import './ConversationIntelligencePanel.css';

interface Conversation {
  id: string;
  recipientId: string;
  recipientName: string;
  lastMessage: string;
  lastMessageAt: Date;
  unreadCount: number;
  sentiment?: 'positive' | 'neutral' | 'negative';
  intent?: string;
}

interface ConversationAnalysis {
  overallSentiment: string;
  keyTopics: string[];
  suggestedResponses: string[];
  intents: Array<{
    primaryIntent: string;
    confidence: number;
  }>;
  actionItems?: string[];
  nextBestAction?: string;
}

export const ConversationIntelligencePanel: React.FC = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<ConversationAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [composing, setComposing] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    setLoading(true);
    try {
      const data = await api.getConversations();
      setConversations(data.conversations || []);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadConversationAnalysis = async (conversationId: string) => {
    try {
      const data = await api.analyzeConversation(conversationId);
      setAnalysis(data);
    } catch (error) {
      console.error('Failed to analyze conversation:', error);
    }
  };

  const handleSelectConversation = (conversationId: string) => {
    setSelectedConversation(conversationId);
    loadConversationAnalysis(conversationId);
  };

  const handleSendMessage = async () => {
    if (!message.trim() || !selectedConversation) return;

    const conversation = conversations.find(c => c.id === selectedConversation);
    if (!conversation) return;

    try {
      await api.sendMessage(conversation.recipientId, '', message);
      setMessage('');
      setComposing(false);
      loadConversations();
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  const useSuggestedResponse = (response: string) => {
    setMessage(response);
    setComposing(true);
  };

  const getSentimentColor = (sentiment?: string): string => {
    const colors: Record<string, string> = {
      positive: '#10b981',
      neutral: '#6b7280',
      negative: '#ef4444',
    };
    return colors[sentiment || 'neutral'] || '#6b7280';
  };

  const getSentimentEmoji = (sentiment?: string): string => {
    const emojis: Record<string, string> = {
      positive: '😊',
      neutral: '😐',
      negative: '😟',
    };
    return emojis[sentiment || 'neutral'] || '😐';
  };

  if (loading) return <div className="loading">Loading conversations...</div>;

  return (
    <div className="conversation-intelligence">
      <div className="intelligence-header">
        <h2>💬 Conversation Intelligence</h2>
      </div>

      <div className="conversation-layout">
        <div className="conversation-list">
          <h3>Recent Conversations</h3>
          {conversations.length === 0 ? (
            <div className="no-conversations">
              <p>No active conversations</p>
            </div>
          ) : (
            conversations.map((conv) => (
              <div
                key={conv.id}
                className={`conversation-item ${selectedConversation === conv.id ? 'active' : ''}`}
                onClick={() => handleSelectConversation(conv.id)}
              >
                <div className="conv-avatar">
                  {conv.recipientName.split(' ').map(n => n[0]).join('')}
                </div>
                <div className="conv-info">
                  <div className="conv-header">
                    <strong>{conv.recipientName}</strong>
                    {conv.unreadCount > 0 && (
                      <span className="unread-badge">{conv.unreadCount}</span>
                    )}
                  </div>
                  <p className="conv-preview">{conv.lastMessage}</p>
                  <div className="conv-meta">
                    <span className="conv-time">
                      {new Date(conv.lastMessageAt).toLocaleDateString()}
                    </span>
                    {conv.sentiment && (
                      <span
                        className="conv-sentiment"
                        style={{ color: getSentimentColor(conv.sentiment) }}
                      >
                        {getSentimentEmoji(conv.sentiment)}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        <div className="conversation-analysis">
          {!selectedConversation ? (
            <div className="no-selection">
              <p>Select a conversation to see intelligent insights</p>
            </div>
          ) : analysis ? (
            <>
              <div className="analysis-section">
                <h4>📊 Conversation Analysis</h4>

                <div className="sentiment-overview">
                  <div className="sentiment-indicator">
                    <span className="sentiment-emoji">
                      {getSentimentEmoji(analysis.overallSentiment)}
                    </span>
                    <span className="sentiment-label">
                      {analysis.overallSentiment} conversation
                    </span>
                  </div>
                </div>

                {analysis.keyTopics.length > 0 && (
                  <div className="key-topics">
                    <strong>Key Topics:</strong>
                    <div className="topic-tags">
                      {analysis.keyTopics.map((topic, i) => (
                        <span key={i} className="topic-tag">{topic}</span>
                      ))}
                    </div>
                  </div>
                )}

                {analysis.intents.length > 0 && (
                  <div className="detected-intents">
                    <strong>Detected Intents:</strong>
                    {analysis.intents.map((intent, i) => (
                      <div key={i} className="intent-item">
                        <span>{intent.primaryIntent.replace(/_/g, ' ')}</span>
                        <span className="confidence">
                          {Math.round(intent.confidence * 100)}%
                        </span>
                      </div>
                    ))}
                  </div>
                )}

                {analysis.actionItems && analysis.actionItems.length > 0 && (
                  <div className="action-items">
                    <strong>⚡ Action Items:</strong>
                    <ul>
                      {analysis.actionItems.map((item, i) => (
                        <li key={i}>{item}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {analysis.nextBestAction && (
                <div className="next-action">
                  <h4>🎯 Next Best Action</h4>
                  <p>{analysis.nextBestAction}</p>
                </div>
              )}

              {analysis.suggestedResponses.length > 0 && (
                <div className="suggested-responses">
                  <h4>💡 Suggested Responses</h4>
                  {analysis.suggestedResponses.map((response, i) => (
                    <div key={i} className="suggested-response">
                      <p>{response}</p>
                      <button
                        className="btn-use-response"
                        onClick={() => useSuggestedResponse(response)}
                      >
                        Use This
                      </button>
                    </div>
                  ))}
                </div>
              )}

              <div className="compose-section">
                {!composing ? (
                  <button
                    className="btn-compose"
                    onClick={() => setComposing(true)}
                  >
                    ✏️ Compose Reply
                  </button>
                ) : (
                  <div className="compose-form">
                    <textarea
                      className="compose-textarea"
                      placeholder="Write your message..."
                      value={message}
                      onChange={(e) => setMessage(e.target.value)}
                      rows={4}
                    />
                    <div className="compose-actions">
                      <button
                        className="btn-send"
                        onClick={handleSendMessage}
                        disabled={!message.trim()}
                      >
                        Send
                      </button>
                      <button
                        className="btn-cancel"
                        onClick={() => {
                          setComposing(false);
                          setMessage('');
                        }}
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </>
          ) : (
            <div className="loading">Analyzing conversation...</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ConversationIntelligencePanel;
