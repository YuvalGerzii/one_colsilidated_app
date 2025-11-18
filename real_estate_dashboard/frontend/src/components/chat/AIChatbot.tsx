import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Typography,
  TextField,
  IconButton,
  Avatar,
  Chip,
  CircularProgress,
  List,
  ListItem,
  Grid,
  Collapse,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Tooltip,
} from '@mui/material';
import {
  Send,
  SmartToy,
  Person,
  ExpandMore,
  Insights,
  TrendingUp,
  Assessment,
  Architecture,
  Clear,
  Psychology,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { GlassCard, GlassButton, MicroInteraction } from '../ui/GlassComponents';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  data?: any;
  agent?: string;
  agent_name?: string;
  insights?: string[];
  recommendations?: string[];
  confidence?: number;
  timestamp?: string;
}

interface Agent {
  id: string;
  name: string;
  description: string;
  proficiency: number;
  icon: React.ReactNode;
}

const AIChatbot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Hello! I\'m your AI Real Estate Assistant powered by specialized agents. I can help you with:\n\n• **Property Analysis** - Valuation, cash flow, investment metrics\n• **Market Research** - Trends, demographics, competitive analysis\n• **Investment Strategy** - Portfolio optimization, tax planning\n• **Deal Evaluation** - Underwriting, risk assessment, scenario analysis\n\nHow can I assist you today?',
      timestamp: new Date().toISOString(),
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState('');
  const [currentAgent, setCurrentAgent] = useState<string | null>(null);
  const [expandedData, setExpandedData] = useState<{ [key: number]: boolean }>({});

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const conversationId = useRef(`conv_${Date.now()}`);

  // Agent metadata
  const agents: Agent[] = [
    {
      id: 'property_analyst',
      name: 'Property Analyst',
      description: 'Property valuation & investment metrics',
      proficiency: 0.93,
      icon: <Assessment />,
    },
    {
      id: 'market_researcher',
      name: 'Market Researcher',
      description: 'Market trends & demographics',
      proficiency: 0.91,
      icon: <TrendingUp />,
    },
    {
      id: 'investment_strategist',
      name: 'Investment Strategist',
      description: 'Portfolio & tax optimization',
      proficiency: 0.92,
      icon: <Architecture />,
    },
    {
      id: 'deal_evaluator',
      name: 'Deal Evaluator',
      description: 'Underwriting & risk assessment',
      proficiency: 0.94,
      icon: <Insights />,
    },
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingMessage]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setStreamingMessage('');

    try {
      // Use streaming endpoint for real-time response
      const response = await fetch('http://localhost:8001/api/v1/ai-chatbot/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          conversation_id: conversationId.current,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      let accumulatedMessage = '';
      let responseData: any = {};
      let agentName = '';

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const lines = chunk.split('\n\n');

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = JSON.parse(line.slice(6));

              if (data.type === 'agent_selected') {
                setCurrentAgent(data.agent);
                agentName = data.agent_name;
              } else if (data.type === 'message_chunk') {
                accumulatedMessage += data.content;
                setStreamingMessage(accumulatedMessage);
              } else if (data.type === 'complete') {
                responseData = data;
              }
            }
          }
        }
      }

      // Add complete message
      const assistantMessage: Message = {
        role: 'assistant',
        content: accumulatedMessage,
        data: responseData.data,
        agent: responseData.agent,
        agent_name: agentName,
        insights: responseData.insights,
        recommendations: responseData.recommendations,
        confidence: responseData.confidence,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setStreamingMessage('');
      setCurrentAgent(null);
    } catch (error: any) {
      console.error('Chat error:', error);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'I apologize, but I encountered an error. Please try again.',
          timestamp: new Date().toISOString(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        role: 'assistant',
        content: 'Chat cleared. How can I help you?',
        timestamp: new Date().toISOString(),
      },
    ]);
    conversationId.current = `conv_${Date.now()}`;
  };

  const getAgentIcon = (agentId?: string) => {
    const agent = agents.find((a) => a.id === agentId);
    return agent?.icon || <Psychology />;
  };

  const toggleDataExpand = (index: number) => {
    setExpandedData((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  const formatConfidence = (confidence?: number) => {
    if (!confidence) return null;
    const pct = (confidence * 100).toFixed(0);
    return (
      <Chip
        label={`${pct}% Confidence`}
        size="small"
        sx={{
          background: `linear-gradient(135deg, ${
            confidence > 0.85 ? '#10b981' : confidence > 0.70 ? '#f59e0b' : '#ef4444'
          }, ${confidence > 0.85 ? '#059669' : confidence > 0.70 ? '#d97706' : '#dc2626'})`,
          color: '#fff',
          fontWeight: 600,
        }}
      />
    );
  };

  return (
    <Box sx={{ p: 3, height: 'calc(100vh - 100px)', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Avatar
            sx={{
              width: 56,
              height: 56,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            }}
          >
            <SmartToy sx={{ fontSize: 32 }} />
          </Avatar>
          <Box>
            <Typography variant="h4" sx={{ fontWeight: 700 }}>
              AI Real Estate Assistant
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Powered by Multi-Agent Intelligence
            </Typography>
          </Box>
        </Box>
        <Tooltip title="Clear conversation">
          <IconButton onClick={handleClearChat} color="primary">
            <Clear />
          </IconButton>
        </Tooltip>
      </Box>

      {/* Available Agents */}
      <Box sx={{ mb: 3 }}>
        <Grid container spacing={2}>
          {agents.map((agent) => (
            <Grid item xs={12} sm={6} md={3} key={agent.id}>
              <MicroInteraction variant="lift">
                <GlassCard
                  sx={{
                    p: 2,
                    cursor: 'pointer',
                    transition: 'all 0.3s',
                    border: currentAgent === agent.id ? '2px solid #667eea' : undefined,
                    '&:hover': {
                      borderColor: '#667eea',
                    },
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 1 }}>
                    <Avatar
                      sx={{
                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        width: 40,
                        height: 40,
                      }}
                    >
                      {agent.icon}
                    </Avatar>
                    <Box sx={{ flex: 1 }}>
                      <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                        {agent.name}
                      </Typography>
                      <Typography variant="caption" color="text.secondary" display="block">
                        {agent.description}
                      </Typography>
                    </Box>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Box
                      sx={{
                        flex: 1,
                        height: 6,
                        borderRadius: 3,
                        background: 'rgba(255, 255, 255, 0.1)',
                        overflow: 'hidden',
                      }}
                    >
                      <Box
                        sx={{
                          width: `${agent.proficiency * 100}%`,
                          height: '100%',
                          background: 'linear-gradient(90deg, #667eea, #764ba2)',
                          borderRadius: 3,
                        }}
                      />
                    </Box>
                    <Typography variant="caption" sx={{ fontWeight: 600 }}>
                      {(agent.proficiency * 100).toFixed(0)}%
                    </Typography>
                  </Box>
                </GlassCard>
              </MicroInteraction>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Messages Area */}
      <GlassCard sx={{ flex: 1, p: 3, overflowY: 'auto', mb: 2 }}>
        <List>
          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <ListItem
                  sx={{
                    display: 'flex',
                    justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
                    alignItems: 'flex-start',
                    mb: 2,
                  }}
                >
                  <Box
                    sx={{
                      maxWidth: '75%',
                      display: 'flex',
                      gap: 2,
                      flexDirection: message.role === 'user' ? 'row-reverse' : 'row',
                    }}
                  >
                    {/* Avatar */}
                    <Avatar
                      sx={{
                        width: 40,
                        height: 40,
                        background:
                          message.role === 'user'
                            ? 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'
                            : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      }}
                    >
                      {message.role === 'user' ? <Person /> : getAgentIcon(message.agent)}
                    </Avatar>

                    {/* Message Content */}
                    <Box sx={{ flex: 1 }}>
                      <Box
                        sx={{
                          p: 2,
                          borderRadius: 2,
                          background:
                            message.role === 'user'
                              ? 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'
                              : 'rgba(255, 255, 255, 0.05)',
                          backdropFilter: 'blur(10px)',
                          border: '1px solid rgba(255, 255, 255, 0.1)',
                        }}
                      >
                        {message.agent_name && (
                          <Chip
                            label={message.agent_name}
                            size="small"
                            sx={{ mb: 1, fontWeight: 600 }}
                          />
                        )}

                        <Typography
                          component="div"
                          sx={{
                            '& p': { mb: 1 },
                            '& ul, & ol': { pl: 2, mb: 1 },
                            '& li': { mb: 0.5 },
                            '& strong': { fontWeight: 700 },
                            '& code': {
                              background: 'rgba(0, 0, 0, 0.2)',
                              padding: '2px 6px',
                              borderRadius: 1,
                            },
                          }}
                        >
                          <ReactMarkdown>{message.content}</ReactMarkdown>
                        </Typography>

                        {message.confidence && (
                          <Box sx={{ mt: 1 }}>{formatConfidence(message.confidence)}</Box>
                        )}
                      </Box>

                      {/* Insights & Recommendations */}
                      {(message.insights || message.recommendations) && (
                        <Accordion
                          sx={{
                            mt: 1,
                            background: 'rgba(255, 255, 255, 0.03)',
                            backdropFilter: 'blur(10px)',
                          }}
                        >
                          <AccordionSummary expandIcon={<ExpandMore />}>
                            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                              View Detailed Analysis
                            </Typography>
                          </AccordionSummary>
                          <AccordionDetails>
                            {message.insights && message.insights.length > 0 && (
                              <Box sx={{ mb: 2 }}>
                                <Typography variant="subtitle2" sx={{ fontWeight: 700, mb: 1 }}>
                                  🔍 Key Insights
                                </Typography>
                                <Box component="ul" sx={{ pl: 2, m: 0 }}>
                                  {message.insights.map((insight, i) => (
                                    <Typography component="li" key={i} variant="body2" sx={{ mb: 0.5 }}>
                                      {insight}
                                    </Typography>
                                  ))}
                                </Box>
                              </Box>
                            )}

                            {message.recommendations && message.recommendations.length > 0 && (
                              <Box>
                                <Typography variant="subtitle2" sx={{ fontWeight: 700, mb: 1 }}>
                                  💡 Recommendations
                                </Typography>
                                <Box component="ul" sx={{ pl: 2, m: 0 }}>
                                  {message.recommendations.map((rec, i) => (
                                    <Typography component="li" key={i} variant="body2" sx={{ mb: 0.5 }}>
                                      {rec}
                                    </Typography>
                                  ))}
                                </Box>
                              </Box>
                            )}
                          </AccordionDetails>
                        </Accordion>
                      )}
                    </Box>
                  </Box>
                </ListItem>
              </motion.div>
            ))}

            {/* Streaming Message */}
            {streamingMessage && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
              >
                <ListItem sx={{ display: 'flex', justifyContent: 'flex-start', alignItems: 'flex-start' }}>
                  <Box sx={{ maxWidth: '75%', display: 'flex', gap: 2 }}>
                    <Avatar
                      sx={{
                        width: 40,
                        height: 40,
                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      }}
                    >
                      {getAgentIcon(currentAgent || undefined)}
                    </Avatar>

                    <Box
                      sx={{
                        p: 2,
                        borderRadius: 2,
                        background: 'rgba(255, 255, 255, 0.05)',
                        backdropFilter: 'blur(10px)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                      }}
                    >
                      <Typography component="div">
                        <ReactMarkdown>{streamingMessage}</ReactMarkdown>
                      </Typography>
                      <CircularProgress size={16} sx={{ mt: 1 }} />
                    </Box>
                  </Box>
                </ListItem>
              </motion.div>
            )}
          </AnimatePresence>
        </List>
        <div ref={messagesEndRef} />
      </GlassCard>

      {/* Input Area */}
      <GlassCard sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Ask me about property analysis, market research, investment strategy, or deal evaluation..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage();
              }
            }}
            multiline
            maxRows={3}
            disabled={isLoading}
            sx={{
              '& .MuiOutlinedInput-root': {
                background: 'rgba(255, 255, 255, 0.03)',
                '& fieldset': {
                  borderColor: 'rgba(255, 255, 255, 0.1)',
                },
              },
            }}
          />
          <GlassButton
            onClick={handleSendMessage}
            disabled={isLoading || !inputMessage.trim()}
            sx={{ px: 3, py: 1.5 }}
          >
            {isLoading ? <CircularProgress size={24} /> : <Send />}
          </GlassButton>
        </Box>
      </GlassCard>
    </Box>
  );
};

export default AIChatbot;
