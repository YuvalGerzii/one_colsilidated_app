import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Workers
export const createWorker = (workerData) => api.post('/workers/', workerData);
export const getWorker = (workerId) => api.get(`/workers/${workerId}`);
export const getWorkerRiskAssessment = (workerId) => api.get(`/workers/${workerId}/risk-assessment`);
export const getWorkerProfile = (workerId) => api.get(`/workers/${workerId}/profile`);

// Jobs
export const listJobs = (params) => api.get('/jobs/', { params });
export const getJob = (jobId) => api.get(`/jobs/${jobId}`);
export const matchJobsForWorker = (workerId, topN = 10) =>
  api.post('/jobs/match', { worker_id: workerId, top_n: topN });
export const matchSpecificJob = (jobId, workerId) =>
  api.get(`/jobs/${jobId}/match/${workerId}`);

// Skills
export const listSkills = (params) => api.get('/skills/', { params });
export const getSkill = (skillId) => api.get(`/skills/${skillId}`);
export const getInDemandSkills = (limit = 20) => api.get(`/skills/in-demand?limit=${limit}`);
export const getAutomationRiskSkills = (threshold = 60) =>
  api.get(`/skills/automation-risk?threshold=${threshold}`);

// Analytics
export const analyzeSkillGap = (workerId, targetJobId) =>
  api.post('/analytics/skill-gap', { worker_id: workerId, target_job_id: targetJobId });
export const recommendLearningPath = (workerId, targetJobId, preferences = {}) =>
  api.post('/analytics/learning-path', {
    worker_id: workerId,
    target_job_id: targetJobId,
    ...preferences
  });
export const getMarketTrends = () => api.get('/analytics/market-trends');
export const getWorkerStatistics = () => api.get('/analytics/worker-statistics');

// Enterprise
export const createEnterprise = (enterpriseData) => api.post('/enterprise/', enterpriseData);
export const getEnterprise = (enterpriseId) => api.get(`/enterprise/${enterpriseId}`);
export const getWorkforceDashboard = (enterpriseId) =>
  api.get(`/enterprise/${enterpriseId}/dashboard`);
export const getWorkforcePlanning = (enterpriseId) =>
  api.get(`/enterprise/${enterpriseId}/workforce-planning`);

// ==================== Digital Twin ====================
export const digitalTwinAPI = {
  getMacroRiskIndex: () => api.get('/digital-twin/macro-risk-index'),
  predictDisplacement: (data) => api.post('/digital-twin/displacement-prediction', data),
  getRegionHeatmap: (region) => api.get(`/digital-twin/region-heatmap/${region}`),
  runScenario: (scenario) => api.post('/digital-twin/scenario-modeling', scenario),
};

// ==================== AI Agents ====================
export const agentsAPI = {
  comprehensiveAnalysis: (workerId) => api.post(`/agents/comprehensive-analysis/${workerId}`),
  chat: (message, workerId) => api.post(`/agents/chat?message=${encodeURIComponent(message)}&worker_id=${workerId}`),
  fullAnalysis: (workerId) => api.post(`/agents/full-agent-analysis/${workerId}`),
};

// ==================== Study Buddy ====================
export const studyBuddyAPI = {
  getContributor: (contributorId) => api.get(`/study-buddy/contributors/${contributorId}`),
  getContributorAnalytics: (contributorId, period = 'last_30_days') =>
    api.get(`/study-buddy/contributors/${contributorId}/analytics?period=${period}`),
  searchResources: (params) => api.get('/study-buddy/resources/search', { params }),
  getPath: (pathId) => api.get(`/study-buddy/paths/${pathId}`),
  enrollInPath: (pathId, userId) => api.post(`/study-buddy/paths/${pathId}/enroll?user_id=${userId}`),
  getLearningDashboard: (userId) => api.get(`/study-buddy/learning-curves/${userId}/dashboard`),
  getContentRecommendations: (userId, params) =>
    api.post(`/study-buddy/recommendations/content?user_id=${userId}`, null, { params }),
  getFeed: (userId, limit = 20) => api.get(`/study-buddy/feed/${userId}?limit=${limit}`),
  getCreditBalance: (userId) => api.get(`/study-buddy/credits/balance/${userId}`),
  getLeaderboard: (type = 'reputation', period = 'monthly') =>
    api.get(`/study-buddy/analytics/leaderboard?leaderboard_type=${type}&period=${period}`),
};

// ==================== Economic Copilot ====================
export const economicCopilotAPI = {
  analyzeJobOffer: (data) => api.post('/economic-copilot/analyze-job-offer', data),
  analyzeRetirement: (data) => api.post('/economic-copilot/retirement-impact', data),
  comprehensiveDecision: (data) => api.post('/economic-copilot/comprehensive-decision', data),
};

// ==================== Gig Economy ====================
export const gigAPI = {
  matchSkills: (data) => api.post('/gig/match-skills-to-gigs', data),
  optimizePortfolio: (data) => api.post('/gig/portfolio-optimization', data),
  getDashboard: (workerId) => api.get(`/gig/dashboard/${workerId}`),
};

// ==================== Corporate ====================
export const corporateAPI = {
  getTransformationDashboard: (companyId) => api.get(`/corporate/transformation-dashboard/${companyId}`),
  calculateFairnessScore: (data) => api.post('/corporate/fairness-score', data),
};

// ==================== Progress ====================
export const progressAPI = {
  getDashboard: (workerId) => api.get(`/progress/dashboard/${workerId}`),
  getAchievements: (workerId) => api.get(`/progress/achievements/${workerId}`),
};

// ==================== Multi-Agent System ====================
export const masAPI = {
  // Workflows
  startCareerTransition: (data) => api.post('/mas/workflows/career-transition', data),
  startLearningConsensus: (data) => api.post('/mas/workflows/learning-consensus', data),
  startMarketAnalysis: (data) => api.post('/mas/workflows/market-analysis', data),
  startResourceCuration: (data) => api.post('/mas/workflows/resource-curation', data),
  getWorkflowProgress: (workflowId) => api.get(`/mas/workflows/${workflowId}/progress`),

  // Agent coordination
  requestCollaboration: (data) => api.post('/mas/collaboration/request', data),
  distributeTask: (data) => api.post('/mas/tasks/distribute', data),
  getTaskStatus: (taskId) => api.get(`/mas/tasks/${taskId}/status`),

  // Shared environment
  readSharedKnowledge: (key) => api.get(`/mas/shared-environment/knowledge/${key}`),
  getRecentEvents: (params) => api.get('/mas/shared-environment/events', { params }),
  getEnvironmentMetrics: () => api.get('/mas/shared-environment/metrics'),

  // System status
  getSystemStatus: () => api.get('/mas/status'),
  listAgents: () => api.get('/mas/agents'),
  getAgentDetails: (agentId) => api.get(`/mas/agents/${agentId}`),
  activateAgent: (agentId) => api.post(`/mas/agents/${agentId}/activate`),
  deactivateAgent: (agentId) => api.post(`/mas/agents/${agentId}/deactivate`),

  // Network & analytics
  getAgentNetwork: () => api.get('/mas/network/visualization'),
  getConversation: (conversationId) => api.get(`/mas/conversations/${conversationId}`),
  getPerformanceAnalytics: () => api.get('/mas/analytics/performance'),
  getCollaborationPatterns: () => api.get('/mas/analytics/collaboration-patterns'),

  // Message processing
  processMessages: (maxMessages) => api.post(`/mas/messages/process?max_messages=${maxMessages}`),
};

export default api;
