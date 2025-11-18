/**
 * LLM Service
 * Integration with local LLM (Ollama) for agent conversations
 * Provides natural language generation for negotiations
 */

import axios, { AxiosInstance } from 'axios';

export interface LLMConfig {
  baseURL: string;
  model: string;
  temperature?: number;
  maxTokens?: number;
}

export interface ChatMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface GenerateOptions {
  temperature?: number;
  maxTokens?: number;
  stopSequences?: string[];
}

/**
 * Ollama LLM Service
 * Uses local Ollama instance for free LLM inference
 */
export class OllamaLLMService {
  private client: AxiosInstance;
  private model: string;
  private defaultTemperature: number;
  private defaultMaxTokens: number;

  constructor(config?: Partial<LLMConfig>) {
    const baseURL = config?.baseURL || process.env.OLLAMA_URL || 'http://localhost:11434';
    this.model = config?.model || process.env.OLLAMA_MODEL || 'llama2';
    this.defaultTemperature = config?.temperature || 0.7;
    this.defaultMaxTokens = config?.maxTokens || 2000;

    this.client = axios.create({
      baseURL,
      timeout: 60000, // 60 second timeout
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  /**
   * Chat completion
   */
  async chat(
    messages: ChatMessage[],
    options?: GenerateOptions
  ): Promise<string> {
    try {
      // Convert messages to Ollama format
      const prompt = this.formatMessagesForOllama(messages);

      const response = await this.client.post('/api/generate', {
        model: this.model,
        prompt,
        temperature: options?.temperature || this.defaultTemperature,
        stream: false,
        options: {
          num_predict: options?.maxTokens || this.defaultMaxTokens,
          stop: options?.stopSequences,
        },
      });

      return response.data.response;
    } catch (error) {
      console.error('Ollama API error:', error);
      throw new Error('Failed to generate response from LLM');
    }
  }

  /**
   * Format chat messages for Ollama
   */
  private formatMessagesForOllama(messages: ChatMessage[]): string {
    let prompt = '';

    for (const msg of messages) {
      if (msg.role === 'system') {
        prompt += `### System:\n${msg.content}\n\n`;
      } else if (msg.role === 'user') {
        prompt += `### User:\n${msg.content}\n\n`;
      } else if (msg.role === 'assistant') {
        prompt += `### Assistant:\n${msg.content}\n\n`;
      }
    }

    prompt += '### Assistant:\n';
    return prompt;
  }

  /**
   * Generate negotiation proposal
   */
  async generateProposal(context: {
    userName: string;
    userNeeds: string[];
    userOfferings: string[];
    otherName: string;
    otherNeeds: string[];
    otherOfferings: string[];
  }): Promise<{
    whatUserGets: string[];
    whatUserGives: string[];
    rationale: string;
  }> {
    const messages: ChatMessage[] = [
      {
        role: 'system',
        content: `You are a skilled business negotiator. Your task is to create fair, mutually beneficial proposals.
You must analyze both parties' needs and offerings and propose a balanced exchange.
Output format:
GETS:
- Item 1
- Item 2
GIVES:
- Item 1
- Item 2
RATIONALE:
Explanation of why this is fair and beneficial.`,
      },
      {
        role: 'user',
        content: `Create a negotiation proposal for ${context.userName}.

${context.userName}'s Needs:
${context.userNeeds.map((n) => `- ${n}`).join('\n')}

${context.userName}'s Offerings:
${context.userOfferings.map((o) => `- ${o}`).join('\n')}

${context.otherName}'s Needs:
${context.otherNeeds.map((n) => `- ${n}`).join('\n')}

${context.otherName}'s Offerings:
${context.otherOfferings.map((o) => `- ${o}`).join('\n')}

Create a fair proposal that maximizes mutual benefit.`,
      },
    ];

    const response = await this.chat(messages, {
      temperature: 0.7,
      maxTokens: 1000,
    });

    return this.parseProposal(response, context.userName);
  }

  /**
   * Parse LLM-generated proposal
   */
  private parseProposal(
    response: string,
    userName: string
  ): {
    whatUserGets: string[];
    whatUserGives: string[];
    rationale: string;
  } {
    const gets: string[] = [];
    const gives: string[] = [];
    let rationale = '';

    const getsMatch = response.match(/GETS:?\s*([\s\S]*?)(?=GIVES|$)/i);
    if (getsMatch) {
      const getsText = getsMatch[1];
      const lines = getsText.split('\n').filter((l) => l.trim().startsWith('-'));
      gets.push(...lines.map((l) => l.replace(/^-\s*/, '').trim()));
    }

    const givesMatch = response.match(/GIVES:?\s*([\s\S]*?)(?=RATIONALE|$)/i);
    if (givesMatch) {
      const givesText = givesMatch[1];
      const lines = givesText.split('\n').filter((l) => l.trim().startsWith('-'));
      gives.push(...lines.map((l) => l.replace(/^-\s*/, '').trim()));
    }

    const rationaleMatch = response.match(/RATIONALE:?\s*([\s\S]*?)$/i);
    if (rationaleMatch) {
      rationale = rationaleMatch[1].trim();
    }

    return {
      whatUserGets: gets,
      whatUserGives: gives,
      rationale: rationale || 'Fair exchange of value',
    };
  }

  /**
   * Generate introduction message
   */
  async generateIntroduction(context: {
    userName: string;
    userTitle: string;
    userCompany?: string;
    otherName: string;
    needs: string[];
    offerings: string[];
  }): Promise<string> {
    const messages: ChatMessage[] = [
      {
        role: 'system',
        content: `You are writing a professional introduction message for business networking.
Be friendly, concise, and highlight mutual value. Keep it under 200 words.`,
      },
      {
        role: 'user',
        content: `Write an introduction message from ${context.userName} (${context.userTitle}${context.userCompany ? ` at ${context.userCompany}` : ''}) to ${context.otherName}.

What ${context.userName} is looking for:
${context.needs.map((n) => `- ${n}`).join('\n')}

What ${context.userName} can offer:
${context.offerings.map((o) => `- ${o}`).join('\n')}

Write a warm, professional introduction.`,
      },
    ];

    return await this.chat(messages, {
      temperature: 0.8,
      maxTokens: 300,
    });
  }

  /**
   * Analyze proposal and generate response
   */
  async analyzeProposalAndRespond(context: {
    userName: string;
    proposedTerms: {
      gets: string[];
      gives: string[];
    };
    userNeeds: string[];
    userOfferings: string[];
    concerns?: string[];
  }): Promise<{
    shouldAccept: boolean;
    response: string;
    concerns: string[];
  }> {
    const messages: ChatMessage[] = [
      {
        role: 'system',
        content: `You are analyzing a business proposal. Evaluate if it meets the user's needs fairly.
Output format:
DECISION: ACCEPT or COUNTER or REJECT
RESPONSE: Your response message
CONCERNS:
- Concern 1 (if any)
- Concern 2`,
      },
      {
        role: 'user',
        content: `Analyze this proposal for ${context.userName}.

Proposed Terms:
Gets:
${context.proposedTerms.gets.map((g) => `- ${g}`).join('\n')}

Gives:
${context.proposedTerms.gives.map((g) => `- ${g}`).join('\n')}

${context.userName}'s Needs:
${context.userNeeds.map((n) => `- ${n}`).join('\n')}

${context.userName}'s Offerings:
${context.userOfferings.map((o) => `- ${o}`).join('\n')}

${context.concerns ? `\nKnown Concerns:\n${context.concerns.map((c) => `- ${c}`).join('\n')}` : ''}

Should this proposal be accepted, countered, or rejected? Explain why.`,
      },
    ];

    const response = await this.chat(messages, {
      temperature: 0.7,
      maxTokens: 500,
    });

    return this.parseAnalysis(response);
  }

  /**
   * Parse LLM analysis response
   */
  private parseAnalysis(response: string): {
    shouldAccept: boolean;
    response: string;
    concerns: string[];
  } {
    const decisionMatch = response.match(/DECISION:?\s*(ACCEPT|COUNTER|REJECT)/i);
    const decision = decisionMatch ? decisionMatch[1].toUpperCase() : 'COUNTER';

    const responseMatch = response.match(/RESPONSE:?\s*([\s\S]*?)(?=CONCERNS|$)/i);
    const responseText = responseMatch ? responseMatch[1].trim() : response;

    const concerns: string[] = [];
    const concernsMatch = response.match(/CONCERNS:?\s*([\s\S]*?)$/i);
    if (concernsMatch) {
      const concernsText = concernsMatch[1];
      const lines = concernsText.split('\n').filter((l) => l.trim().startsWith('-'));
      concerns.push(...lines.map((l) => l.replace(/^-\s*/, '').trim()));
    }

    return {
      shouldAccept: decision === 'ACCEPT',
      response: responseText,
      concerns,
    };
  }

  /**
   * Check if Ollama is available
   */
  async checkHealth(): Promise<boolean> {
    try {
      await this.client.get('/api/tags');
      return true;
    } catch (error) {
      return false;
    }
  }

  /**
   * List available models
   */
  async listModels(): Promise<string[]> {
    try {
      const response = await this.client.get('/api/tags');
      return response.data.models?.map((m: any) => m.name) || [];
    } catch (error) {
      console.error('Failed to list models:', error);
      return [];
    }
  }
}

// Singleton instance
let llmServiceInstance: OllamaLLMService | null = null;

/**
 * Get LLM service instance
 */
export function getLLMService(): OllamaLLMService {
  if (!llmServiceInstance) {
    llmServiceInstance = new OllamaLLMService();
  }
  return llmServiceInstance;
}

/**
 * Initialize LLM service and check health
 */
export async function initLLMService(): Promise<{
  available: boolean;
  models: string[];
}> {
  const llm = getLLMService();

  const available = await llm.checkHealth();
  const models = available ? await llm.listModels() : [];

  if (available) {
    console.log('✓ Ollama LLM service available');
    console.log(`  Models: ${models.join(', ')}`);
  } else {
    console.warn('⚠ Ollama LLM service not available');
    console.warn('  Install Ollama from https://ollama.ai');
    console.warn('  Run: ollama pull llama2');
  }

  return { available, models };
}
