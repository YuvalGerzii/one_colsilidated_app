# LLM Frontend Integration Guide

**For React/TypeScript Frontend**

Complete guide for integrating LLM features into your real estate dashboard frontend.

---

## 🎯 Quick Start

### 1. Create LLM API Service

**File:** `frontend/src/services/llmApi.ts`

```typescript
import axios from 'axios';

const API_BASE = process.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export interface GenerateRequest {
  prompt: string;
  system_prompt?: string;
  temperature?: number;
  max_tokens?: number;
  use_cache?: boolean;
}

export interface GenerateResponse {
  text: string | null;
  available: boolean;
  model?: string;
  metadata?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

export interface LLMHealth {
  status: string;
  available: boolean;
  model?: string;
  metrics?: Record<string, any>;
}

class LLMApiService {
  private baseURL = `${API_BASE}/llm`;

  /**
   * Check LLM service health
   */
  async checkHealth(): Promise<LLMHealth> {
    const response = await axios.get<LLMHealth>(`${this.baseURL}/health`);
    return response.data;
  }

  /**
   * Get LLM metrics
   */
  async getMetrics() {
    const response = await axios.get(`${this.baseURL}/metrics`);
    return response.data;
  }

  /**
   * Generate text
   */
  async generate(request: GenerateRequest): Promise<GenerateResponse> {
    const response = await axios.post<GenerateResponse>(
      `${this.baseURL}/generate`,
      request
    );
    return response.data;
  }

  /**
   * Summarize text
   */
  async summarize(text: string, maxLength: number = 150): Promise<GenerateResponse> {
    const response = await axios.post<GenerateResponse>(
      `${this.baseURL}/summarize`,
      { text, max_summary_length: maxLength }
    );
    return response.data;
  }

  /**
   * Generate property description
   */
  async generatePropertyDescription(data: {
    bedrooms: number;
    bathrooms: number;
    sqft: number;
    property_type: string;
    amenities?: string;
    location?: string;
  }): Promise<GenerateResponse> {
    const response = await axios.post<GenerateResponse>(
      `${this.baseURL}/generate-property-description`,
      data
    );
    return response.data;
  }

  /**
   * Analyze market data
   */
  async analyzeMarket(data: {
    market_data: Record<string, any>;
    location: string;
    analysis_focus?: string;
  }): Promise<GenerateResponse> {
    const response = await axios.post<GenerateResponse>(
      `${this.baseURL}/analyze-market`,
      data
    );
    return response.data;
  }

  /**
   * Get investment recommendation
   */
  async getInvestmentRecommendation(data: {
    property_data: Record<string, any>;
    investor_profile?: Record<string, any>;
  }): Promise<GenerateResponse> {
    const response = await axios.post<GenerateResponse>(
      `${this.baseURL}/investment-recommendation`,
      data
    );
    return response.data;
  }

  /**
   * Assess property risk
   */
  async assessRisk(data: {
    property_info: Record<string, any>;
    risk_factors?: string[];
  }): Promise<GenerateResponse> {
    const response = await axios.post<GenerateResponse>(
      `${this.baseURL}/risk-assessment`,
      data
    );
    return response.data;
  }

  /**
   * Compare properties
   */
  async compareProperties(data: {
    properties: Record<string, any>[];
    comparison_criteria?: string[];
  }): Promise<GenerateResponse> {
    const response = await axios.post<GenerateResponse>(
      `${this.baseURL}/compare-properties`,
      data
    );
    return response.data;
  }

  /**
   * Generate deal memo
   */
  async generateDealMemo(data: {
    deal_data: Record<string, any>;
    memo_sections?: string[];
  }): Promise<GenerateResponse> {
    const response = await axios.post<GenerateResponse>(
      `${this.baseURL}/generate-deal-memo`,
      data
    );
    return response.data;
  }

  /**
   * Analyze lease
   */
  async analyzeLease(data: {
    lease_data: Record<string, any>;
    tenant_info?: Record<string, any>;
  }): Promise<GenerateResponse> {
    const response = await axios.post<GenerateResponse>(
      `${this.baseURL}/analyze-lease`,
      data
    );
    return response.data;
  }

  /**
   * Batch generate
   */
  async batchGenerate(data: {
    items: Record<string, any>[];
    operation: string;
    common_params?: Record<string, any>;
  }) {
    const response = await axios.post(
      `${this.baseURL}/batch-generate`,
      data
    );
    return response.data;
  }
}

export const llmApi = new LLMApiService();
```

---

## 🎨 React Components

### 1. LLM Health Indicator

```typescript
// components/LLMHealthIndicator.tsx
import React, { useEffect, useState } from 'react';
import { llmApi, LLMHealth } from '../services/llmApi';

export const LLMHealthIndicator: React.FC = () => {
  const [health, setHealth] = useState<LLMHealth | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const data = await llmApi.checkHealth();
        setHealth(data);
      } catch (error) {
        console.error('Health check failed:', error);
      } finally {
        setLoading(false);
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 60000); // Check every minute

    return () => clearInterval(interval);
  }, []);

  if (loading) return <div>Checking AI status...</div>;

  return (
    <div className={`llm-health ${health?.available ? 'available' : 'unavailable'}`}>
      <span className="status-dot"></span>
      <span className="status-text">
        AI: {health?.available ? 'Online' : 'Offline'}
      </span>
      {health?.model && <span className="model-name">({health.model})</span>}
    </div>
  );
};
```

### 2. Property Description Generator

```typescript
// components/PropertyDescriptionGenerator.tsx
import React, { useState } from 'react';
import { llmApi } from '../services/llmApi';

interface Props {
  property: {
    bedrooms: number;
    bathrooms: number;
    sqft: number;
    property_type: string;
    amenities?: string;
    location?: string;
  };
  onGenerated?: (description: string) => void;
}

export const PropertyDescriptionGenerator: React.FC<Props> = ({
  property,
  onGenerated
}) => {
  const [loading, setLoading] = useState(false);
  const [description, setDescription] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await llmApi.generatePropertyDescription(property);

      if (result.available && result.text) {
        setDescription(result.text);
        onGenerated?.(result.text);
      } else {
        setError('AI service is currently unavailable. Please try again later.');
      }
    } catch (err) {
      setError('Failed to generate description. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="property-description-generator">
      <button
        onClick={handleGenerate}
        disabled={loading}
        className="btn-primary"
      >
        {loading ? (
          <>
            <span className="spinner"></span>
            Generating...
          </>
        ) : (
          <>
            <span className="icon">✨</span>
            Generate AI Description
          </>
        )}
      </button>

      {error && (
        <div className="alert alert-warning">
          {error}
        </div>
      )}

      {description && (
        <div className="generated-description">
          <div className="description-header">
            <span className="badge badge-ai">AI Generated</span>
            <button onClick={() => navigator.clipboard.writeText(description)}>
              📋 Copy
            </button>
          </div>
          <p className="description-text">{description}</p>
        </div>
      )}
    </div>
  );
};
```

### 3. Market Analysis Component

```typescript
// components/MarketAnalysis.tsx
import React, { useState, useEffect } from 'react';
import { llmApi } from '../services/llmApi';

interface Props {
  marketData: Record<string, any>;
  location: string;
}

export const MarketAnalysis: React.FC<Props> = ({ marketData, location }) => {
  const [analysis, setAnalysis] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [llmAvailable, setLlmAvailable] = useState(false);

  useEffect(() => {
    // Check if LLM is available
    llmApi.checkHealth().then(health => {
      setLlmAvailable(health.available);
    });
  }, []);

  const generateAnalysis = async () => {
    setLoading(true);

    try {
      const result = await llmApi.analyzeMarket({
        market_data: marketData,
        location,
        analysis_focus: "Investment opportunities and trends"
      });

      if (result.available && result.text) {
        setAnalysis(result.text);
      }
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!llmAvailable) {
    return (
      <div className="alert alert-info">
        AI analysis is currently unavailable. Showing data only.
      </div>
    );
  }

  return (
    <div className="market-analysis">
      <div className="analysis-header">
        <h3>Market Analysis</h3>
        <button
          onClick={generateAnalysis}
          disabled={loading}
          className="btn-secondary"
        >
          {loading ? 'Analyzing...' : '🤖 Generate AI Analysis'}
        </button>
      </div>

      {analysis && (
        <div className="analysis-content">
          <div className="badge badge-ai">AI-Powered Insights</div>
          <div className="analysis-text">
            {analysis.split('\n').map((paragraph, i) => (
              <p key={i}>{paragraph}</p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
```

### 4. Investment Recommendation Card

```typescript
// components/InvestmentRecommendation.tsx
import React, { useState } from 'react';
import { llmApi } from '../services/llmApi';

interface Props {
  propertyData: Record<string, any>;
  investorProfile?: Record<string, any>;
}

export const InvestmentRecommendation: React.FC<Props> = ({
  propertyData,
  investorProfile
}) => {
  const [recommendation, setRecommendation] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [expanded, setExpanded] = useState(false);

  const getRecommendation = async () => {
    setLoading(true);

    try {
      const result = await llmApi.getInvestmentRecommendation({
        property_data: propertyData,
        investor_profile: investorProfile
      });

      if (result.available && result.text) {
        setRecommendation(result.text);
        setExpanded(true);
      }
    } catch (error) {
      console.error('Recommendation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="investment-recommendation-card">
      <div className="card-header">
        <h4>AI Investment Analysis</h4>
        {!recommendation && (
          <button onClick={getRecommendation} disabled={loading}>
            {loading ? '⏳ Analyzing...' : '🎯 Get Recommendation'}
          </button>
        )}
      </div>

      {recommendation && (
        <div className={`card-body ${expanded ? 'expanded' : 'collapsed'}`}>
          <div className="recommendation-badge">
            <span className="icon">🤖</span>
            AI-Powered Analysis
          </div>

          <div className="recommendation-text">
            {recommendation.split('\n').map((line, i) => (
              <p key={i}>{line}</p>
            ))}
          </div>

          <button
            onClick={() => setExpanded(!expanded)}
            className="btn-link"
          >
            {expanded ? 'Show Less' : 'Show More'}
          </button>
        </div>
      )}
    </div>
  );
};
```

### 5. Batch Property Processor

```typescript
// components/BatchPropertyProcessor.tsx
import React, { useState } from 'react';
import { llmApi } from '../services/llmApi';

interface Property {
  id: string;
  bedrooms: number;
  bathrooms: number;
  sqft: number;
  property_type: string;
}

interface Props {
  properties: Property[];
  onComplete?: (results: Record<string, string>) => void;
}

export const BatchPropertyProcessor: React.FC<Props> = ({
  properties,
  onComplete
}) => {
  const [processing, setProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState<Record<string, string>>({});

  const processBatch = async () => {
    setProcessing(true);
    setProgress(0);

    try {
      const result = await llmApi.batchGenerate({
        items: properties.map(p => ({
          bedrooms: p.bedrooms,
          bathrooms: p.bathrooms,
          sqft: p.sqft,
          property_type: p.property_type
        })),
        operation: 'describe'
      });

      const descriptions: Record<string, string> = {};

      result.results.forEach((res: any, index: number) => {
        if (res.available && res.text) {
          descriptions[properties[index].id] = res.text;
        }
        setProgress(((index + 1) / properties.length) * 100);
      });

      setResults(descriptions);
      onComplete?.(descriptions);
    } catch (error) {
      console.error('Batch processing failed:', error);
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="batch-processor">
      <div className="processor-header">
        <h4>Batch AI Processing</h4>
        <span className="property-count">{properties.length} properties</span>
      </div>

      <button
        onClick={processBatch}
        disabled={processing}
        className="btn-primary btn-block"
      >
        {processing ? (
          <>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${progress}%` }}
              />
            </div>
            Processing {Math.round(progress)}%
          </>
        ) : (
          '🚀 Generate All Descriptions'
        )}
      </button>

      {Object.keys(results).length > 0 && (
        <div className="results-summary">
          ✅ Generated {Object.keys(results).length} descriptions
        </div>
      )}
    </div>
  );
};
```

---

## 🎣 Custom React Hooks

### 1. useLLMHealth Hook

```typescript
// hooks/useLLMHealth.ts
import { useState, useEffect } from 'react';
import { llmApi, LLMHealth } from '../services/llmApi';

export const useLLMHealth = (pollInterval: number = 60000) => {
  const [health, setHealth] = useState<LLMHealth | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const data = await llmApi.checkHealth();
        setHealth(data);
        setError(null);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, pollInterval);

    return () => clearInterval(interval);
  }, [pollInterval]);

  return {
    health,
    loading,
    error,
    isAvailable: health?.available || false
  };
};

// Usage:
// const { isAvailable, health } = useLLMHealth();
```

### 2. usePropertyDescription Hook

```typescript
// hooks/usePropertyDescription.ts
import { useState, useCallback } from 'react';
import { llmApi } from '../services/llmApi';

export const usePropertyDescription = () => {
  const [description, setDescription] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generate = useCallback(async (property: {
    bedrooms: number;
    bathrooms: number;
    sqft: number;
    property_type: string;
    amenities?: string;
    location?: string;
  }) => {
    setLoading(true);
    setError(null);

    try {
      const result = await llmApi.generatePropertyDescription(property);

      if (result.available && result.text) {
        setDescription(result.text);
        return result.text;
      } else {
        setError('AI service unavailable');
        return null;
      }
    } catch (err) {
      setError('Failed to generate description');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const clear = useCallback(() => {
    setDescription(null);
    setError(null);
  }, []);

  return { description, loading, error, generate, clear };
};

// Usage:
// const { description, loading, generate } = usePropertyDescription();
// await generate(propertyData);
```

### 3. useMarketAnalysis Hook

```typescript
// hooks/useMarketAnalysis.ts
import { useState, useCallback } from 'react';
import { llmApi } from '../services/llmApi';

export const useMarketAnalysis = () => {
  const [analysis, setAnalysis] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyze = useCallback(async (
    marketData: Record<string, any>,
    location: string,
    focus?: string
  ) => {
    setLoading(true);
    setError(null);

    try {
      const result = await llmApi.analyzeMarket({
        market_data: marketData,
        location,
        analysis_focus: focus
      });

      if (result.available && result.text) {
        setAnalysis(result.text);
        return result.text;
      } else {
        setError('AI analysis unavailable');
        return null;
      }
    } catch (err) {
      setError('Analysis failed');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  return { analysis, loading, error, analyze };
};
```

---

## 🎨 CSS Styling

```css
/* styles/llm-components.css */

/* LLM Health Indicator */
.llm-health {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.875rem;
}

.llm-health.available {
  background: #d4edda;
  color: #155724;
}

.llm-health.unavailable {
  background: #f8d7da;
  color: #721c24;
}

.llm-health .status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse 2s infinite;
}

/* AI Badge */
.badge-ai {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.badge-ai::before {
  content: '🤖';
}

/* Generated Description */
.generated-description {
  background: #f8f9fa;
  border: 2px dashed #dee2e6;
  border-radius: 8px;
  padding: 16px;
  margin-top: 16px;
}

.description-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.description-text {
  line-height: 1.6;
  color: #495057;
}

/* Loading Spinner */
.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 8px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Progress Bar */
.progress-bar {
  width: 100%;
  height: 4px;
  background: #e9ecef;
  border-radius: 2px;
  overflow: hidden;
  margin-top: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: width 0.3s ease;
}
```

---

## ✅ Best Practices

### 1. Always Check Availability

```typescript
const result = await llmApi.generate({ prompt: "..." });

if (result.available && result.text) {
  // Use the result
} else {
  // Show fallback content or message
}
```

### 2. Show Loading States

```typescript
{loading && <LoadingSpinner />}
{!loading && result && <ResultDisplay result={result} />}
```

### 3. Handle Errors Gracefully

```typescript
try {
  const result = await llmApi.generate({ prompt });
} catch (error) {
  showNotification('AI service temporarily unavailable', 'warning');
  // Use fallback
}
```

### 4. Cache Results

```typescript
// Use React Query for caching
import { useQuery } from '@tanstack/react-query';

const { data, isLoading } = useQuery(
  ['property-description', propertyId],
  () => llmApi.generatePropertyDescription(property),
  { staleTime: 5 * 60 * 1000 } // Cache for 5 minutes
);
```

### 5. Show AI Badges

Always indicate when content is AI-generated:

```tsx
{aiGenerated && (
  <span className="badge badge-ai">AI Generated</span>
)}
```

---

## 🚀 Complete Example

```typescript
// pages/PropertyDetails.tsx
import React from 'react';
import { useLLMHealth, usePropertyDescription } from '../hooks';
import { PropertyDescriptionGenerator } from '../components';

const PropertyDetails = ({ property }) => {
  const { isAvailable } = useLLMHealth();
  const { description, loading, generate } = usePropertyDescription();

  return (
    <div className="property-details">
      <h1>{property.address}</h1>

      {/* Show AI features only if available */}
      {isAvailable && (
        <PropertyDescriptionGenerator
          property={property}
          onGenerated={(desc) => {
            // Save to database or state
            updateProperty({ description: desc });
          }}
        />
      )}

      {/* Standard property info always shown */}
      <PropertyInfo property={property} />
    </div>
  );
};
```

---

**Status:** ✅ Ready to integrate!
**Last Updated:** 2025-11-13
