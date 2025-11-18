/**
 * API Service Layer
 * Centralized API calls for Bond.AI frontend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3005/api';

interface ApiOptions extends RequestInit {
  token?: string;
}

class ApiService {
  private token: string | null = null;

  setToken(token: string) {
    this.token = token;
    localStorage.setItem('bondai_token', token);
  }

  getToken(): string | null {
    if (!this.token) {
      this.token = localStorage.getItem('bondai_token');
    }
    return this.token;
  }

  clearToken() {
    this.token = null;
    localStorage.removeItem('bondai_token');
  }

  private async request<T>(
    endpoint: string,
    options: ApiOptions = {}
  ): Promise<T> {
    const token = options.token || this.getToken();

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Request failed' }));
      throw new Error(error.error || error.message || 'Request failed');
    }

    return response.json();
  }

  // Auth
  async login(email: string, password: string) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async register(data: { email: string; password: string; name: string }) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Recommendations
  async getRecommendations(params?: {
    limit?: number;
    minScore?: number;
    includeIntroductions?: boolean;
    includeGapFill?: boolean;
    includeDiversity?: boolean;
  }) {
    const query = new URLSearchParams(params as any).toString();
    return this.request(`/recommendations?${query}`);
  }

  async getNetworkGaps() {
    return this.request('/recommendations/network-gaps');
  }

  async getWeeklyDigest() {
    return this.request('/recommendations/weekly-digest');
  }

  // Match Quality
  async analyzeMatch(targetId: string) {
    return this.request(`/match-quality/${targetId}`);
  }

  async compareMatch(targetId: string) {
    return this.request('/match-quality/compare', {
      method: 'POST',
      body: JSON.stringify({ targetId }),
    });
  }

  async findBestMatches(params?: {
    limit?: number;
    minScore?: number;
    excludeExisting?: boolean;
    diversityWeight?: number;
  }) {
    const query = new URLSearchParams(params as any).toString();
    return this.request(`/match-quality/best-matches?${query}`);
  }

  // Collaboration
  async predictCollaboration(targetId: string) {
    return this.request('/collaboration/predict', {
      method: 'POST',
      body: JSON.stringify({ targetId }),
    });
  }

  async getCollaborationOpportunities(params?: {
    type?: string;
    minProbability?: number;
    limit?: number;
  }) {
    const query = new URLSearchParams(params as any).toString();
    return this.request(`/collaboration/opportunities?${query}`);
  }

  // Network Analysis
  async getCommunities(minSize?: number) {
    const query = minSize ? `?minCommunitySize=${minSize}` : '';
    return this.request(`/network-analysis/communities${query}`);
  }

  async getUserCommunities(userId: string) {
    return this.request(`/network-analysis/communities/user/${userId}`);
  }

  async getCommunityRecommendations() {
    return this.request('/network-analysis/communities/recommendations');
  }

  async getNetworkSnapshot() {
    return this.request('/network-analysis/temporal/snapshot');
  }

  async getNetworkTrends(timeframe: 'week' | 'month' | 'quarter' | 'year' = 'month') {
    return this.request(`/network-analysis/temporal/trends?timeframe=${timeframe}`);
  }

  async getUserTrajectory() {
    return this.request('/network-analysis/temporal/trajectory');
  }

  async getNetworkHealth() {
    return this.request('/network-analysis/temporal/health');
  }

  // Relationships
  async analyzeRelationshipHealth(targetId?: string) {
    const endpoint = targetId
      ? `/relationships/health/${targetId}`
      : '/relationships/health';
    return this.request(endpoint);
  }

  async getRelationshipHealthSummary() {
    return this.request('/relationships/health/summary');
  }

  // Search
  async searchUsers(query: string, filters?: any) {
    return this.request('/search', {
      method: 'POST',
      body: JSON.stringify({ query, filters }),
    });
  }

  async intentBasedSearch(message: string) {
    return this.request('/search/intent', {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  }

  // Opportunities
  async getOpportunities(type?: string) {
    const query = type ? `?type=${type}` : '';
    return this.request(`/opportunities${query}`);
  }

  async dismissOpportunity(opportunityId: string) {
    return this.request(`/opportunities/${opportunityId}/dismiss`, {
      method: 'POST',
    });
  }

  async pursueOpportunity(opportunityId: string) {
    return this.request(`/opportunities/${opportunityId}/pursue`, {
      method: 'POST',
    });
  }

  // Conversations
  async getConversations() {
    return this.request('/conversations');
  }

  async getConversation(conversationId: string) {
    return this.request(`/conversations/${conversationId}`);
  }

  async analyzeConversation(conversationId: string) {
    return this.request(`/conversations/${conversationId}/analyze`);
  }

  async sendMessage(recipientId: string, subject: string, body: string) {
    return this.request('/conversations/send', {
      method: 'POST',
      body: JSON.stringify({ recipientId, subject, body }),
    });
  }

  // Introductions
  async generateIntroduction(person1Id: string, person2Id: string, context?: string) {
    return this.request('/introductions/generate', {
      method: 'POST',
      body: JSON.stringify({ person1Id, person2Id, context }),
    });
  }

  async sendIntroduction(person1Id: string, person2Id: string, message: string) {
    return this.request('/introductions/send', {
      method: 'POST',
      body: JSON.stringify({ person1Id, person2Id, message }),
    });
  }
}

export const api = new ApiService();
export default api;
