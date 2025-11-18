# Free LLM Implementation Plan - Real Estate Dashboard

**Date:** 2025-11-13
**Target:** 100% Free, Production-Ready LLM Integration
**Principle:** Graceful Degradation - App works with or without LLM

---

## 🎯 Executive Summary

This plan implements a **completely free** local LLM using Ollama with **graceful degradation** as the fallback strategy. If the LLM service is unavailable, features continue working with existing logic (pattern matching, rule-based systems, or simply return "LLM unavailable" status).

**Key Principles:**
- ✅ 100% Free (Ollama + Gemma 2B)
- ✅ Non-breaking (app works without LLM)
- ✅ Best practices (service pattern, error handling, monitoring)
- ✅ Lightweight (2GB RAM, ~1.5GB model)
- ✅ Production-ready (Docker, health checks, logging)

---

## 📊 Current App Analysis

### Existing Infrastructure
- **Backend:** FastAPI with service pattern
- **Database:** PostgreSQL
- **Cache:** Redis
- **Deployment:** Docker Compose
- **ML Stack:** Already has transformers, sentence-transformers, torch

### Existing Features That Can Benefit from LLM
1. **Clause Analysis Service** (`clause_analysis_service.py`)
   - Current: Pattern matching with regex
   - Enhancement: LLM-powered clause interpretation and risk assessment

2. **Natural Language Query** (`natural_language_query.py`)
   - Current: sentence-transformers + pattern matching
   - Enhancement: Direct LLM query interpretation

3. **Report Generation** (reports endpoints)
   - Current: Template-based
   - Enhancement: LLM-generated summaries and insights

4. **Market Intelligence** (market_intelligence endpoints)
   - Current: Data aggregation
   - Enhancement: LLM-generated market insights

5. **PDF Extraction** (`pdf_extraction_service.py`)
   - Current: Rule-based extraction
   - Enhancement: LLM-powered document understanding

6. **Legal Services** (enhanced_legal endpoints)
   - Current: Template-based
   - Enhancement: LLM contract analysis and generation

---

## 🏗️ Architecture Design

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         Business Logic Services                      │   │
│  │  (clause_analysis, reports, market_intelligence)     │   │
│  └───────────────────┬─────────────────────────────────┘   │
│                      │                                       │
│                      ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           LLM Service (NEW)                          │   │
│  │  • Request validation                                │   │
│  │  • Graceful degradation                              │   │
│  │  • Error handling                                    │   │
│  │  • Caching                                           │   │
│  │  • Monitoring                                        │   │
│  └───────────────────┬─────────────────────────────────┘   │
│                      │                                       │
│                      ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         Ollama Client                                │   │
│  │  • HTTP requests to Ollama                           │   │
│  │  • Retry logic                                       │   │
│  │  • Timeout handling                                  │   │
│  └───────────────────┬─────────────────────────────────┘   │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
           ┌─────────────────────────┐
           │   Ollama Container       │
           │   Model: gemma:2b        │
           │   Port: 11434            │
           │   Resource: 4GB RAM      │
           └─────────────────────────┘
```

### Graceful Degradation Flow

```
User Request
    │
    ▼
Business Service (e.g., clause_analysis)
    │
    ├─── Try: LLM Service
    │     │
    │     ├── Success → Return LLM Result
    │     │
    │     └── Failure → Log & Continue
    │              │
    │              ▼
    └─── Fallback: Existing Logic
         │
         └── Return Result (with metadata: llm_used=False)
```

---

## 🔧 Implementation Details

### 1. Docker Compose Configuration

**File:** `docker-compose.yml`

```yaml
services:
  # ... existing services (db, backend, frontend)

  # Ollama LLM Service
  ollama:
    image: ollama/ollama:latest
    container_name: real_estate_ollama
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0:11434
      - OLLAMA_ORIGINS=*
      - OLLAMA_NUM_PARALLEL=1          # Limit concurrent requests
      - OLLAMA_MAX_LOADED_MODELS=1     # Only load one model at a time
    deploy:
      resources:
        limits:
          memory: 4G                    # Max 4GB RAM
          cpus: '2.0'                   # Max 2 CPU cores
        reservations:
          memory: 2G                    # Reserve 2GB
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    networks:
      - real_estate_network

volumes:
  ollama_data:
    driver: local
  # ... existing volumes

networks:
  real_estate_network:
    driver: bridge
```

### 2. Settings Configuration

**File:** `backend/app/settings.py` (additions)

```python
# ================================
# LLM CONFIGURATION
# ================================
ENABLE_LLM: bool = Field(
    default=True,
    description="Enable local LLM features (Ollama)"
)
OLLAMA_BASE_URL: str = Field(
    default="http://ollama:11434",
    description="Ollama API base URL"
)
OLLAMA_MODEL: str = Field(
    default="gemma:2b",
    description="Ollama model to use"
)
LLM_TIMEOUT: int = Field(
    default=30,
    description="LLM request timeout in seconds"
)
LLM_MAX_RETRIES: int = Field(
    default=2,
    description="Maximum retries for LLM requests"
)
LLM_CACHE_TTL: int = Field(
    default=3600,
    description="LLM response cache TTL (seconds)"
)
LLM_TEMPERATURE: float = Field(
    default=0.7,
    description="LLM generation temperature (0-1)"
)
LLM_MAX_TOKENS: int = Field(
    default=500,
    description="Maximum tokens to generate"
)
```

### 3. LLM Service Implementation

**File:** `backend/app/services/llm_service.py`

```python
"""
LLM Service - Local Language Model Integration with Ollama

Provides LLM capabilities with graceful degradation.
If Ollama is unavailable, returns None without breaking the app.
"""

import logging
import hashlib
import json
from typing import Optional, Dict, Any, List
from datetime import datetime
import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from app.settings import settings
from app.services.cache_service import cache_service

logger = logging.getLogger(__name__)


class LLMServiceError(Exception):
    """Base exception for LLM service errors"""
    pass


class LLMUnavailableError(LLMServiceError):
    """Raised when LLM service is unavailable"""
    pass


class LLMService:
    """
    Service for interacting with local Ollama LLM.

    Features:
    - Graceful degradation (returns None on failure)
    - Response caching
    - Retry logic with exponential backoff
    - Request/response logging
    - Health monitoring
    """

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.timeout = settings.LLM_TIMEOUT
        self.max_retries = settings.LLM_MAX_RETRIES
        self.cache_ttl = settings.LLM_CACHE_TTL
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS
        self.enabled = settings.ENABLE_LLM

        # Metrics tracking
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "cache_hits": 0,
            "total_tokens_generated": 0,
            "avg_response_time": 0.0
        }

        logger.info(
            f"LLM Service initialized - "
            f"Enabled: {self.enabled}, "
            f"Model: {self.model}, "
            f"Base URL: {self.base_url}"
        )

    async def health_check(self) -> Dict[str, Any]:
        """
        Check if Ollama service is healthy.

        Returns:
            Dictionary with health status
        """
        if not self.enabled:
            return {
                "status": "disabled",
                "available": False,
                "message": "LLM service is disabled in settings"
            }

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/health")

                if response.status_code == 200:
                    return {
                        "status": "healthy",
                        "available": True,
                        "model": self.model,
                        "metrics": self.metrics
                    }
                else:
                    return {
                        "status": "unhealthy",
                        "available": False,
                        "message": f"Unexpected status code: {response.status_code}"
                    }
        except Exception as e:
            logger.warning(f"LLM health check failed: {e}")
            return {
                "status": "unavailable",
                "available": False,
                "message": str(e)
            }

    def _generate_cache_key(self, prompt: str, **kwargs) -> str:
        """Generate cache key from prompt and parameters"""
        cache_data = {
            "prompt": prompt,
            "model": self.model,
            **kwargs
        }
        cache_str = json.dumps(cache_data, sort_keys=True)
        return f"llm_cache:{hashlib.md5(cache_str.encode()).hexdigest()}"

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(httpx.RequestError),
        reraise=True
    )
    async def _make_ollama_request(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Make request to Ollama API with retry logic.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Generation temperature (overrides default)
            max_tokens: Max tokens to generate (overrides default)

        Returns:
            Response dictionary from Ollama

        Raises:
            httpx.RequestError: On network/connection errors
            httpx.HTTPStatusError: On HTTP errors
        """
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature or self.temperature,
                "num_predict": max_tokens or self.max_tokens
            }
        }

        start_time = datetime.now()

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json=payload
            )
            response.raise_for_status()

        elapsed = (datetime.now() - start_time).total_seconds()

        result = response.json()

        # Update metrics
        self.metrics["avg_response_time"] = (
            (self.metrics["avg_response_time"] * self.metrics["successful_requests"] + elapsed)
            / (self.metrics["successful_requests"] + 1)
        )

        logger.info(f"LLM request completed in {elapsed:.2f}s")

        return result

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        use_cache: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Generate text using LLM with graceful degradation.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt for context
            temperature: Generation temperature (0-1, lower = more focused)
            max_tokens: Maximum tokens to generate
            use_cache: Whether to use cached responses

        Returns:
            Dictionary with generated text and metadata, or None if LLM unavailable

        Example:
            >>> result = await llm_service.generate(
            ...     "Summarize this contract clause",
            ...     system_prompt="You are a legal expert"
            ... )
            >>> if result:
            ...     print(result["text"])
            ... else:
            ...     print("LLM unavailable, using fallback")
        """
        self.metrics["total_requests"] += 1

        if not self.enabled:
            logger.debug("LLM service is disabled")
            self.metrics["failed_requests"] += 1
            return None

        # Check cache
        if use_cache:
            cache_key = self._generate_cache_key(
                prompt,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )

            cached = await cache_service.get(cache_key)
            if cached:
                logger.info("LLM cache hit")
                self.metrics["cache_hits"] += 1
                return json.loads(cached)

        try:
            # Make request to Ollama
            response = await self._make_ollama_request(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )

            # Extract response
            text = response.get("message", {}).get("content", "")

            result = {
                "text": text,
                "model": self.model,
                "source": "local_llm",
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": {
                    "prompt_tokens": response.get("prompt_eval_count", 0),
                    "completion_tokens": response.get("eval_count", 0),
                    "total_tokens": (
                        response.get("prompt_eval_count", 0) +
                        response.get("eval_count", 0)
                    )
                }
            }

            # Update metrics
            self.metrics["successful_requests"] += 1
            self.metrics["total_tokens_generated"] += result["metadata"]["total_tokens"]

            # Cache result
            if use_cache:
                await cache_service.set(
                    cache_key,
                    json.dumps(result),
                    ttl=self.cache_ttl
                )

            return result

        except httpx.TimeoutException:
            logger.warning(f"LLM request timeout after {self.timeout}s")
            self.metrics["failed_requests"] += 1
            return None

        except httpx.HTTPStatusError as e:
            logger.error(f"LLM HTTP error: {e.response.status_code} - {e.response.text}")
            self.metrics["failed_requests"] += 1
            return None

        except httpx.RequestError as e:
            logger.error(f"LLM request error: {e}")
            self.metrics["failed_requests"] += 1
            return None

        except Exception as e:
            logger.error(f"Unexpected LLM error: {e}", exc_info=True)
            self.metrics["failed_requests"] += 1
            return None

    async def generate_structured(
        self,
        prompt: str,
        output_format: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Generate structured output (JSON) from LLM.

        Args:
            prompt: User prompt
            output_format: Description of expected JSON structure
            system_prompt: Optional system prompt
            **kwargs: Additional arguments for generate()

        Returns:
            Dictionary with parsed JSON or None
        """
        full_system_prompt = (
            f"{system_prompt}\n\n" if system_prompt else ""
        ) + f"You must respond with valid JSON in this format: {output_format}"

        result = await self.generate(
            prompt=prompt,
            system_prompt=full_system_prompt,
            **kwargs
        )

        if not result:
            return None

        # Try to parse JSON from response
        try:
            text = result["text"].strip()
            # Extract JSON if wrapped in markdown code blocks
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]

            parsed = json.loads(text)
            result["parsed"] = parsed
            return result

        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse LLM JSON response: {e}")
            return result  # Return unparsed result

    def get_metrics(self) -> Dict[str, Any]:
        """Get service metrics"""
        return {
            **self.metrics,
            "cache_hit_rate": (
                self.metrics["cache_hits"] / self.metrics["total_requests"]
                if self.metrics["total_requests"] > 0 else 0
            ),
            "success_rate": (
                self.metrics["successful_requests"] / self.metrics["total_requests"]
                if self.metrics["total_requests"] > 0 else 0
            )
        }


# Global instance
llm_service = LLMService()
```

### 4. Enhanced Clause Analysis Service

**File:** `backend/app/services/enhanced_clause_analysis.py`

```python
"""
Enhanced Clause Analysis with LLM Support

Combines existing pattern matching with optional LLM analysis.
Falls back gracefully to pattern matching if LLM unavailable.
"""

from typing import Dict, List, Optional
import logging

from app.services.clause_analysis_service import (
    ClauseAnalysisService,
    ClauseType,
    RiskLevel,
    ExtractedClause
)
from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)


class EnhancedClauseAnalysisService(ClauseAnalysisService):
    """
    Enhanced clause analysis with LLM support.

    If LLM is available:
        - Uses LLM for deeper clause interpretation
        - Provides more nuanced risk assessment
        - Generates detailed recommendations

    If LLM is unavailable:
        - Falls back to pattern matching (existing logic)
        - Still provides functional analysis
    """

    async def analyze_clause_with_llm(
        self,
        clause: ExtractedClause
    ) -> Dict[str, any]:
        """
        Enhance clause analysis with LLM insights.

        Args:
            clause: Extracted clause from pattern matching

        Returns:
            Enhanced analysis with LLM insights
        """
        system_prompt = """You are a legal expert specializing in contract analysis.
Analyze the provided contract clause and provide:
1. A clear interpretation in plain English
2. Potential risks or concerns
3. Recommendations for improvement

Be concise and practical."""

        prompt = f"""Analyze this {clause.clause_type.value} clause:

"{clause.text}"

Current risk assessment: {clause.risk_level.value}
Identified risk factors: {', '.join(clause.risk_factors) if clause.risk_factors else 'None'}

Provide your analysis."""

        result = await llm_service.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3,  # Lower temp for more focused analysis
            max_tokens=300
        )

        if result:
            return {
                "clause": clause,
                "llm_analysis": result["text"],
                "llm_used": True,
                "enhanced": True
            }
        else:
            # Fallback to existing analysis
            return {
                "clause": clause,
                "llm_analysis": None,
                "llm_used": False,
                "enhanced": False,
                "message": "LLM unavailable - using pattern-based analysis only"
            }

    async def analyze_document(
        self,
        document_text: str,
        use_llm: bool = True
    ) -> Dict[str, any]:
        """
        Analyze full document with optional LLM enhancement.

        Args:
            document_text: Full contract text
            use_llm: Whether to use LLM for enhancement

        Returns:
            Complete analysis with all clauses
        """
        # Use existing pattern matching to extract clauses
        extracted_clauses = self.extract_all_clauses(document_text)

        # Enhance with LLM if requested and available
        if use_llm:
            enhanced_clauses = []
            for clause in extracted_clauses:
                enhanced = await self.analyze_clause_with_llm(clause)
                enhanced_clauses.append(enhanced)

            # Generate overall document summary with LLM
            summary = await self._generate_document_summary(
                document_text,
                extracted_clauses
            )

            return {
                "clauses": enhanced_clauses,
                "summary": summary,
                "llm_enhanced": True,
                "total_clauses": len(extracted_clauses)
            }
        else:
            # Return pattern-based analysis only
            return {
                "clauses": extracted_clauses,
                "llm_enhanced": False,
                "total_clauses": len(extracted_clauses)
            }

    async def _generate_document_summary(
        self,
        document_text: str,
        clauses: List[ExtractedClause]
    ) -> Optional[str]:
        """Generate overall document summary using LLM"""

        # Extract key info about clauses
        high_risk_count = sum(
            1 for c in clauses
            if c.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]
        )

        clause_types = list(set(c.clause_type.value for c in clauses))

        prompt = f"""Summarize this contract document:

Total clauses identified: {len(clauses)}
High-risk clauses: {high_risk_count}
Clause types found: {', '.join(clause_types)}

Provide a brief 2-3 sentence summary of the overall document risk level and key considerations."""

        result = await llm_service.generate(
            prompt=prompt,
            system_prompt="You are a legal expert. Provide concise contract summaries.",
            temperature=0.3,
            max_tokens=150
        )

        return result["text"] if result else None


# Global instance
enhanced_clause_service = EnhancedClauseAnalysisService()
```

### 5. API Endpoints

**File:** `backend/app/api/v1/endpoints/llm.py`

```python
"""
LLM API Endpoints

Provides endpoints for LLM-powered features.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.services.llm_service import llm_service
from app.services.enhanced_clause_analysis import enhanced_clause_service

router = APIRouter()


# ================================
# REQUEST/RESPONSE MODELS
# ================================

class GenerateRequest(BaseModel):
    """Request model for text generation"""
    prompt: str = Field(..., min_length=1, max_length=5000)
    system_prompt: Optional[str] = Field(None, max_length=1000)
    temperature: Optional[float] = Field(0.7, ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(500, ge=50, le=2000)
    use_cache: bool = True


class GenerateResponse(BaseModel):
    """Response model for text generation"""
    text: Optional[str]
    available: bool
    model: Optional[str]
    metadata: Optional[dict]


class ClauseAnalysisRequest(BaseModel):
    """Request model for clause analysis"""
    document_text: str = Field(..., min_length=10)
    use_llm: bool = True


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    available: bool
    model: Optional[str] = None
    message: Optional[str] = None
    metrics: Optional[dict] = None


# ================================
# ENDPOINTS
# ================================

@router.get("/health", response_model=HealthResponse)
async def llm_health_check():
    """
    Check LLM service health status.

    Returns service status and metrics.
    """
    health = await llm_service.health_check()
    return health


@router.get("/metrics")
async def llm_metrics():
    """
    Get LLM service metrics.

    Returns request counts, cache hit rate, success rate, etc.
    """
    return llm_service.get_metrics()


@router.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """
    Generate text using LLM.

    If LLM is unavailable, returns available=False with null text.
    Client should handle gracefully.
    """
    result = await llm_service.generate(
        prompt=request.prompt,
        system_prompt=request.system_prompt,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        use_cache=request.use_cache
    )

    if result:
        return GenerateResponse(
            text=result["text"],
            available=True,
            model=result["model"],
            metadata=result.get("metadata")
        )
    else:
        return GenerateResponse(
            text=None,
            available=False,
            model=None,
            metadata=None
        )


@router.post("/analyze-clauses")
async def analyze_contract_clauses(request: ClauseAnalysisRequest):
    """
    Analyze contract clauses with optional LLM enhancement.

    Falls back to pattern matching if LLM unavailable.
    """
    try:
        result = await enhanced_clause_service.analyze_document(
            document_text=request.document_text,
            use_llm=request.use_llm
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )
```

### 6. Router Integration

**File:** `backend/app/api/router.py` (additions)

```python
from app.api.v1.endpoints import (
    # ... existing imports
    llm  # NEW
)

# LLM endpoints
api_router.include_router(
    llm.router,
    prefix="/llm",
    tags=["llm", "ai"]
)
```

---

## 📋 Implementation Steps

### Phase 1: Infrastructure Setup

**Step 1.1: Update Docker Compose**
```bash
# Add Ollama service to docker-compose.yml
# Add volume for model persistence
# Add network configuration
```

**Step 1.2: Update Environment Settings**
```bash
# Add LLM configuration to settings.py
# Create .env entries for LLM settings
```

**Step 1.3: Start Ollama and Pull Model**
```bash
docker-compose up -d ollama
docker exec real_estate_ollama ollama pull gemma:2b
```

**Step 1.4: Verify Ollama Health**
```bash
curl http://localhost:11434/api/health
curl http://localhost:11434/api/tags
```

### Phase 2: Service Implementation

**Step 2.1: Create LLM Service**
```bash
# Implement backend/app/services/llm_service.py
# Add health check, retry logic, caching
```

**Step 2.2: Test LLM Service**
```python
# Write unit tests for llm_service
# Test graceful degradation
# Test caching behavior
```

**Step 2.3: Add API Endpoints**
```bash
# Implement backend/app/api/v1/endpoints/llm.py
# Add health, metrics, generate endpoints
```

### Phase 3: Feature Integration

**Step 3.1: Enhance Clause Analysis**
```bash
# Create enhanced_clause_analysis.py
# Integrate with existing clause_analysis_service
# Add fallback logic
```

**Step 3.2: Enhance Report Generation**
```bash
# Add LLM-powered summaries to report service
# Generate market insights
# Create investment recommendations
```

**Step 3.3: Enhance Market Intelligence**
```bash
# Add LLM analysis to market data
# Generate trend summaries
# Create comparative analysis
```

### Phase 4: Testing & Optimization

**Step 4.1: Integration Testing**
```bash
# Test all LLM-enhanced features
# Test graceful degradation
# Verify app works with Ollama stopped
```

**Step 4.2: Performance Testing**
```bash
# Load test LLM endpoints
# Optimize cache settings
# Tune resource limits
```

**Step 4.3: Monitoring Setup**
```bash
# Add logging for LLM requests
# Track metrics (requests, latency, cache hits)
# Set up alerts for failures
```

### Phase 5: Documentation & Deployment

**Step 5.1: User Documentation**
```bash
# Document LLM features
# Create API documentation
# Write troubleshooting guide
```

**Step 5.2: Deployment**
```bash
# Deploy to staging
# Run smoke tests
# Deploy to production
```

---

## 🎯 Use Cases & Implementation Priority

### Priority 1: High-Value, Low-Risk

1. **Property Description Generation**
   - Endpoint: `POST /api/v1/llm/generate-property-description`
   - Input: Property features (beds, baths, sqft, amenities)
   - Output: Marketing-ready description
   - Fallback: Return empty string or template-based description

2. **Market Analysis Summaries**
   - Endpoint: `POST /api/v1/llm/summarize-market-data`
   - Input: Market data JSON
   - Output: 2-3 paragraph summary
   - Fallback: Return raw data

3. **Document Summarization**
   - Endpoint: `POST /api/v1/llm/summarize-document`
   - Input: Document text
   - Output: Executive summary
   - Fallback: Return first paragraph

### Priority 2: Enhanced Existing Features

4. **Enhanced Clause Analysis**
   - Endpoint: `POST /api/v1/llm/analyze-clauses`
   - Enhancement to existing clause_analysis_service
   - Fallback: Existing pattern matching

5. **Natural Language Query Enhancement**
   - Endpoint: `POST /api/v1/llm/query`
   - Enhancement to existing NL query engine
   - Fallback: Existing sentence-transformers logic

### Priority 3: New Features

6. **Investment Recommendations**
   - Endpoint: `POST /api/v1/llm/recommend-investment`
   - Input: Portfolio data, risk profile
   - Output: AI-generated recommendations
   - Fallback: Rule-based recommendations

7. **Risk Assessment Narrative**
   - Endpoint: `POST /api/v1/llm/assess-risk`
   - Input: Property/deal data
   - Output: Risk narrative
   - Fallback: Risk scores only

---

## 📊 Monitoring & Observability

### Key Metrics

```python
{
    "llm_requests_total": 1543,
    "llm_requests_successful": 1489,
    "llm_requests_failed": 54,
    "llm_cache_hits": 687,
    "llm_avg_latency_ms": 1234,
    "llm_total_tokens": 45678,
    "llm_success_rate": 0.965,
    "llm_cache_hit_rate": 0.445
}
```

### Health Check Response

```json
{
  "status": "healthy",
  "available": true,
  "model": "gemma:2b",
  "metrics": {
    "total_requests": 1543,
    "successful_requests": 1489,
    "cache_hit_rate": 0.445,
    "success_rate": 0.965,
    "avg_response_time": 1.234
  }
}
```

### Logging Strategy

```python
# Success
logger.info("LLM request successful", extra={
    "prompt_length": 150,
    "response_length": 350,
    "latency_ms": 1234,
    "cached": False
})

# Degradation
logger.warning("LLM unavailable, using fallback", extra={
    "feature": "clause_analysis",
    "fallback_method": "pattern_matching"
})

# Error
logger.error("LLM request failed", extra={
    "error_type": "timeout",
    "retry_count": 2,
    "fallback_used": True
})
```

---

## 🔒 Security Considerations

1. **Input Validation**
   - Sanitize all prompts
   - Limit prompt length (max 5000 chars)
   - Rate limit requests per user

2. **Output Validation**
   - Validate LLM responses
   - Filter sensitive information
   - Implement content moderation

3. **Resource Protection**
   - Memory limits on Ollama container
   - CPU limits to prevent starvation
   - Request timeouts

4. **Data Privacy**
   - No data leaves local infrastructure
   - Log sanitization (no PII in logs)
   - Secure Redis cache

---

## 💰 Cost Analysis

### Resources Required

| Component | Specification | Cost |
|-----------|--------------|------|
| Ollama Container | 4GB RAM, 2 CPU | $0 (included in existing infra) |
| Gemma 2B Model | 1.5GB storage | $0 (free download) |
| Redis Cache | Existing | $0 |
| API Overhead | Minimal | $0 |
| **Total** | | **$0/month** |

### Performance Estimates

- **Request Latency:** 1-3 seconds per request
- **Throughput:** 10-20 requests/minute (conservative)
- **Cache Hit Rate:** 40-60% (after warm-up)
- **Memory Usage:** 2-4GB (with model loaded)

---

## 🧪 Testing Strategy

### Unit Tests

```python
# tests/test_llm_service.py

async def test_llm_generate_success():
    """Test successful LLM generation"""
    result = await llm_service.generate("Test prompt")
    assert result is not None
    assert "text" in result
    assert result["source"] == "local_llm"

async def test_llm_graceful_degradation():
    """Test graceful degradation when LLM unavailable"""
    # Stop Ollama
    result = await llm_service.generate("Test prompt")
    assert result is None  # Should return None, not raise exception

async def test_llm_caching():
    """Test LLM response caching"""
    result1 = await llm_service.generate("Same prompt")
    result2 = await llm_service.generate("Same prompt")
    assert result2 is not None
    # Second request should be cached (faster)
```

### Integration Tests

```python
# tests/test_enhanced_clause_analysis.py

async def test_clause_analysis_with_llm():
    """Test clause analysis with LLM available"""
    document = "This agreement shall be governed by..."
    result = await enhanced_clause_service.analyze_document(document)
    assert result["llm_enhanced"] is True
    assert len(result["clauses"]) > 0

async def test_clause_analysis_without_llm():
    """Test clause analysis fallback without LLM"""
    # Disable LLM
    settings.ENABLE_LLM = False
    document = "This agreement shall be governed by..."
    result = await enhanced_clause_service.analyze_document(document, use_llm=False)
    assert result["llm_enhanced"] is False
    assert len(result["clauses"]) > 0  # Still works with pattern matching
```

### Load Tests

```bash
# Use locust or k6 for load testing
k6 run --vus 10 --duration 30s tests/load/llm_endpoints.js
```

---

## 📚 API Documentation

### Generate Text

```http
POST /api/v1/llm/generate
Content-Type: application/json

{
  "prompt": "Summarize this property: 3 bed, 2 bath, 1500 sqft",
  "system_prompt": "You are a real estate expert",
  "temperature": 0.7,
  "max_tokens": 200
}
```

**Response (Success):**
```json
{
  "text": "This charming 3-bedroom, 2-bathroom home offers...",
  "available": true,
  "model": "gemma:2b",
  "metadata": {
    "prompt_tokens": 15,
    "completion_tokens": 87,
    "total_tokens": 102
  }
}
```

**Response (LLM Unavailable):**
```json
{
  "text": null,
  "available": false,
  "model": null,
  "metadata": null
}
```

### Health Check

```http
GET /api/v1/llm/health
```

**Response:**
```json
{
  "status": "healthy",
  "available": true,
  "model": "gemma:2b",
  "metrics": {
    "total_requests": 1543,
    "successful_requests": 1489,
    "cache_hit_rate": 0.445,
    "success_rate": 0.965
  }
}
```

---

## 🎓 Best Practices Implemented

1. ✅ **Graceful Degradation** - App works without LLM
2. ✅ **Service Pattern** - Clean separation of concerns
3. ✅ **Caching** - Redis-backed response caching
4. ✅ **Retry Logic** - Exponential backoff on failures
5. ✅ **Health Monitoring** - Health checks and metrics
6. ✅ **Error Handling** - Comprehensive error handling
7. ✅ **Logging** - Structured logging for debugging
8. ✅ **Resource Limits** - Docker resource constraints
9. ✅ **Type Safety** - Pydantic models throughout
10. ✅ **Testing** - Unit, integration, and load tests
11. ✅ **Documentation** - Comprehensive API docs
12. ✅ **Security** - Input validation, rate limiting

---

## 🚀 Quick Start

```bash
# 1. Update Docker Compose
vim docker-compose.yml  # Add Ollama service

# 2. Start services
docker-compose up -d

# 3. Pull model
docker exec real_estate_ollama ollama pull gemma:2b

# 4. Verify
curl http://localhost:11434/api/health

# 5. Test LLM endpoint
curl -X POST http://localhost:8000/api/v1/llm/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, test"}'

# 6. Monitor logs
docker-compose logs -f backend ollama
```

---

## 📝 Next Steps After Implementation

1. **Frontend Integration**
   - Add LLM-powered features to UI
   - Show "AI-generated" badges
   - Handle LLM unavailable state gracefully

2. **Feature Expansion**
   - Add more LLM-powered endpoints
   - Integrate with more existing services
   - Explore multi-modal capabilities

3. **Optimization**
   - Fine-tune cache TTLs
   - Optimize resource limits
   - Implement request prioritization

4. **Advanced Features**
   - Multi-model support (fallback to different models)
   - Streaming responses
   - Function calling support

---

**Document Version:** 1.0
**Last Updated:** 2025-11-13
**Status:** Ready for Implementation
