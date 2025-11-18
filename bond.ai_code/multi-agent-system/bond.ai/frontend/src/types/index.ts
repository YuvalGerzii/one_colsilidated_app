export interface User {
  id: string;
  email: string;
  name: string;
  createdAt: string;
  onboardingCompleted: boolean;
}

export interface UserProfile {
  id: string;
  userId: string;
  needs: UserNeed[];
  offerings: UserOffering[];
  bio?: string;
  industry?: string;
  location?: string;
  linkedinUrl?: string;
  websiteUrl?: string;
}

export interface UserNeed {
  id: string;
  category: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  tags: string[];
}

export interface UserOffering {
  id: string;
  category: string;
  description: string;
  capacity: 'limited' | 'moderate' | 'high';
  tags: string[];
}

export interface Match {
  id: string;
  userId: string;
  matchedUserId: string;
  matchedUser: User;
  score: number;
  mutualBenefit: number;
  status: 'pending' | 'accepted' | 'rejected' | 'negotiating';
  createdAt: string;
  matchReasons: string[];
}

export interface Negotiation {
  id: string;
  matchId: string;
  status: 'active' | 'completed' | 'failed';
  currentRound: number;
  proposals: Proposal[];
  agreement?: Agreement;
  createdAt: string;
  updatedAt: string;
}

export interface Proposal {
  id: string;
  negotiationId: string;
  proposedBy: string;
  whatTheyGet: string[];
  whatTheyGive: string[];
  rationale: string;
  response?: 'accepted' | 'countered' | 'rejected';
  createdAt: string;
}

export interface Agreement {
  id: string;
  negotiationId: string;
  terms: {
    party1Gets: string[];
    party1Gives: string[];
    party2Gets: string[];
    party2Gives: string[];
  };
  mutualBenefit: number;
  signedAt: string;
}

export interface Connection {
  id: string;
  userId: string;
  connectedUserId: string;
  connectedUser: User;
  relationship: string;
  status: 'active' | 'paused' | 'ended';
  agreedTerms: Agreement;
  createdAt: string;
}

export interface Notification {
  id: string;
  userId: string;
  type: 'new_match' | 'negotiation_update' | 'proposal_received' | 'agreement_reached' | 'connection_update';
  title: string;
  message: string;
  data?: any;
  read: boolean;
  priority: 'low' | 'medium' | 'high';
  createdAt: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface OnboardingData {
  name: string;
  bio: string;
  industry: string;
  location: string;
  needs: Omit<UserNeed, 'id'>[];
  offerings: Omit<UserOffering, 'id'>[];
  linkedinUrl?: string;
  websiteUrl?: string;
}
