import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Button,
  Card,
  CardContent,
  TextField,
  Alert,
  List,
  ListItem,
  ListItemText,
  Chip,
  Divider,
  LinearProgress
} from '@mui/material';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import SearchIcon from '@mui/icons-material/Search';
import SchoolIcon from '@mui/icons-material/School';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

function AgentAssistant() {
  const [workerId] = useState(1);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [chatMessage, setChatMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const runComprehensiveAnalysis = async () => {
    try {
      setLoading(true);
      const response = await axios.post(
        `${API_BASE_URL}/agents/comprehensive-analysis/${workerId}`
      );
      setAnalysisResults(response.data);
    } catch (error) {
      console.error('Error running analysis:', error);
    } finally {
      setLoading(false);
    }
  };

  const sendChatMessage = async () => {
    if (!chatMessage.trim()) return;

    try {
      const response = await axios.post(`${API_BASE_URL}/agents/chat`, null, {
        params: {
          message: chatMessage,
          worker_id: workerId
        }
      });

      setChatHistory([
        ...chatHistory,
        { type: 'user', message: chatMessage },
        { type: 'agent', ...response.data }
      ]);
      setChatMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        AI Agent Assistant
      </Typography>

      <Typography variant="body1" color="text.secondary" paragraph>
        Multi-agent AI system that understands gaps, discovers opportunities, and creates your success strategy
      </Typography>

      {/* Quick Actions */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <SmartToyIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
              <Typography variant="h6">Gap Analyzer Agent</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Identifies all your skill and knowledge gaps
              </Typography>
              <Button variant="contained" fullWidth onClick={runComprehensiveAnalysis}>
                Analyze My Gaps
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <SearchIcon sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
              <Typography variant="h6">Opportunity Scout</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Discovers hidden jobs and opportunities
              </Typography>
              <Button variant="contained" color="success" fullWidth onClick={runComprehensiveAnalysis}>
                Find Opportunities
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <SchoolIcon sx={{ fontSize: 40, color: 'warning.main', mb: 1 }} />
              <Typography variant="h6">Learning Strategist</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Creates optimal learning paths
              </Typography>
              <Button variant="contained" color="warning" fullWidth onClick={runComprehensiveAnalysis}>
                Get Learning Plan
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Loading */}
      {loading && <LinearProgress sx={{ mb: 3 }} />}

      {/* Comprehensive Analysis Results */}
      {analysisResults && (
        <Box>
          {/* Gap Analysis Section */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h5" gutterBottom>
              Gap Analysis Results
            </Typography>

            <Alert
              severity={
                analysisResults.gap_analysis.overall_readiness > 70 ? 'success' :
                analysisResults.gap_analysis.overall_readiness > 50 ? 'warning' : 'error'
              }
              sx={{ mb: 2 }}
            >
              <Typography variant="h6">
                Overall Readiness: {analysisResults.gap_analysis.overall_readiness}%
              </Typography>
            </Alert>

            <Typography variant="h6" gutterBottom>
              Prioritized Gaps
            </Typography>
            <List>
              {analysisResults.gap_analysis.prioritized_gaps.map((gap, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={gap.gap}
                    secondary={
                      <>
                        <Chip
                          size="small"
                          label={gap.severity}
                          color={
                            gap.severity === 'critical' ? 'error' :
                            gap.severity === 'high' ? 'warning' : 'default'
                          }
                          sx={{ mr: 1 }}
                        />
                        <Typography variant="body2" component="span">
                          Time to close: {gap.weeks_to_close} weeks
                        </Typography>
                        {gap.mitigation && (
                          <>
                            <br />
                            <Typography variant="caption">
                              {gap.mitigation}
                            </Typography>
                          </>
                        )}
                      </>
                    }
                  />
                </ListItem>
              ))}
            </List>

            <Divider sx={{ my: 2 }} />

            <Typography variant="h6" gutterBottom>
              Recommendations
            </Typography>
            <List>
              {analysisResults.gap_analysis.recommendations.map((rec, index) => (
                <ListItem key={index}>
                  <ListItemText primary={`${index + 1}. ${rec}`} />
                </ListItem>
              ))}
            </List>
          </Paper>

          {/* Opportunities Section */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h5" gutterBottom>
              Opportunities Discovered
            </Typography>

            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Found {analysisResults.opportunities.total_found} opportunities across multiple channels
            </Typography>

            <Grid container spacing={2}>
              {analysisResults.opportunities.top_opportunities.map((opp, index) => (
                <Grid item xs={12} md={6} key={index}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6">
                        {opp.title}
                      </Typography>
                      <Chip label={opp.category} size="small" sx={{ mb: 1 }} />
                      {opp.match_score && (
                        <Typography variant="body2" color="text.secondary">
                          Match Score: {opp.match_score}%
                        </Typography>
                      )}
                      {opp.description && (
                        <Typography variant="body2" sx={{ mt: 1 }}>
                          {opp.description}
                        </Typography>
                      )}
                      {opp.access_method && (
                        <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                          <strong>How to access:</strong> {opp.access_method}
                        </Typography>
                      )}
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>

            <Divider sx={{ my: 2 }} />

            <Typography variant="h6" gutterBottom>
              Action Items
            </Typography>
            <List>
              {analysisResults.opportunities.action_items.map((action, index) => (
                <ListItem key={index}>
                  <ListItemText primary={`${index + 1}. ${action}`} />
                </ListItem>
              ))}
            </List>
          </Paper>

          {/* Integrated Action Plan */}
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Integrated Action Plan
            </Typography>

            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Typography variant="h6" color="error">
                  Phase 1: Immediate
                </Typography>
                <List dense>
                  {analysisResults.integrated_action_plan.phase_1_immediate.map((item, index) => (
                    <ListItem key={index}>
                      <ListItemText primary={item} />
                    </ListItem>
                  ))}
                </List>
              </Grid>

              <Grid item xs={12} md={4}>
                <Typography variant="h6" color="warning.main">
                  Phase 2: Short-term
                </Typography>
                <List dense>
                  {analysisResults.integrated_action_plan.phase_2_short_term.map((item, index) => (
                    <ListItem key={index}>
                      <ListItemText primary={item} />
                    </ListItem>
                  ))}
                </List>
              </Grid>

              <Grid item xs={12} md={4}>
                <Typography variant="h6" color="success.main">
                  Phase 3: Ongoing
                </Typography>
                <List dense>
                  {analysisResults.integrated_action_plan.phase_3_ongoing.map((item, index) => (
                    <ListItem key={index}>
                      <ListItemText primary={item} />
                    </ListItem>
                  ))}
                </List>
              </Grid>
            </Grid>

            <Alert severity="info" sx={{ mt: 3 }}>
              <Typography variant="subtitle2">Success Metrics</Typography>
              {Object.entries(analysisResults.integrated_action_plan.success_metrics).map(([week, metric]) => (
                <Typography variant="body2" key={week}>
                  {week}: {metric}
                </Typography>
              ))}
            </Alert>
          </Paper>
        </Box>
      )}

      {/* Conversational Interface */}
      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Chat with AI Agents
        </Typography>

        <Box sx={{ height: 300, overflowY: 'auto', mb: 2, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
          {chatHistory.length === 0 ? (
            <Typography variant="body2" color="text.secondary">
              Ask me anything about your career transition, gaps, or opportunities!
            </Typography>
          ) : (
            chatHistory.map((msg, index) => (
              <Box key={index} sx={{ mb: 2 }}>
                {msg.type === 'user' ? (
                  <Box sx={{ textAlign: 'right' }}>
                    <Chip label={msg.message} color="primary" />
                  </Box>
                ) : (
                  <Box>
                    <Chip label={msg.agent} size="small" sx={{ mb: 0.5 }} />
                    <Typography variant="body2">{msg.response}</Typography>
                  </Box>
                )}
              </Box>
            ))
          )}
        </Box>

        <Grid container spacing={2}>
          <Grid item xs={10}>
            <TextField
              fullWidth
              placeholder="Ask me anything..."
              value={chatMessage}
              onChange={(e) => setChatMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendChatMessage()}
            />
          </Grid>
          <Grid item xs={2}>
            <Button
              fullWidth
              variant="contained"
              onClick={sendChatMessage}
              sx={{ height: '56px' }}
            >
              Send
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
}

export default AgentAssistant;
