# Free LLM Integration Research & Recommendations

**Date:** 2025-11-13
**Purpose:** Evaluate free, self-hosted LLM solutions for real estate dashboard integration

---

## Executive Summary

After researching multiple options, I recommend **Ollama with LiteLLM** for implementing local LLM integration with the following benefits:
- OpenAI-compatible API interface
- No GPU required for lightweight models
- Built-in fallback and retry mechanisms
- Docker-based deployment for isolation
- Cost-effective (no API fees)
- Privacy-focused (data stays local)

---

## Evaluated Options

### 1. **Ollama** ⭐ RECOMMENDED
**Docker Hub:** `ollama/ollama`

**Pros:**
- Easiest to set up and use
- Excellent model management
- Active community and regular updates
- OpenAI-compatible REST API
- Supports GGUF quantized models
- No GPU required for small models
- Production-ready in 2025

**Cons:**
- Limited to inference only (no training)
- Requires 4-8GB RAM minimum

**Best Lightweight Models for Production:**
| Model | Size | RAM Required | Use Case |
|-------|------|--------------|----------|
| **Llama 3.2 1B Instruct** (q4_k_m) | ~700MB | 2GB | Text generation, summaries |
| **Phi-3 Mini** (3.8B) | ~2.3GB | 4GB | General purpose, coding |
| **Gemma 2B** | ~1.5GB | 3GB | Lightweight chat, Q&A |
| **TinyLlama 1.1B** | ~600MB | 2GB | Ultra-lightweight tasks |

**Docker Compose Example:**
```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped
    environment:
      - OLLAMA_HOST=0.0.0.0:11434
      - OLLAMA_ORIGINS=*
    deploy:
      resources:
        limits:
          memory: 6G
          cpus: '3.0'
        reservations:
          memory: 4G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

volumes:
  ollama_data:
    driver: local
```

---

### 2. **LocalAI**
**Docker Hub:** `localai/localai`

**Pros:**
- True drop-in replacement for OpenAI API
- Supports multiple model formats (GGUF, HuggingFace, etc.)
- Multi-modal capabilities (text, image, audio)
- All-in-one Docker images available
- No GPU required

**Cons:**
- More complex configuration
- Larger Docker images
- Less user-friendly than Ollama

**Docker Setup:**
```bash
# CPU-only with pre-configured models
docker run -d \
  --name localai \
  -p 8080:8080 \
  -v localai_data:/build/models \
  localai/localai:latest-aio-cpu
```

---

### 3. **LiteLLM Proxy** ⭐ RECOMMENDED AS FALLBACK LAYER
**GitHub:** `BerriAI/litellm`

**Pros:**
- Unified interface for 80+ LLM providers (1,800+ models)
- Built-in fallback, retry, and load balancing
- Cost tracking and logging
- Can proxy to Ollama + cloud APIs
- OpenAI-compatible endpoints
- Excellent for hybrid deployments

**Cons:**
- Not a model server itself (requires Ollama/LocalAI)
- Adds extra layer of complexity

**Use Case:** Use LiteLLM as a proxy in front of Ollama to add:
- Automatic fallback to cloud APIs (OpenAI, Anthropic) if local fails
- Retry logic with exponential backoff
- Request logging and monitoring
- Load balancing across multiple Ollama instances

---

## Recommended Architecture

### **Option A: Simple Setup (Recommended for MVP)**
```
Frontend → Backend API → Ollama (Local LLM)
                       ↓ (on error)
                    Fallback to OpenAI API
```

**Implementation:**
- Run Ollama in Docker with Gemma 2B or Phi-3 Mini
- Python client with try/except fallback logic
- Use `litellm` Python library for unified interface

### **Option B: Production Setup with LiteLLM Proxy**
```
Frontend → Backend API → LiteLLM Proxy → Ollama (Primary)
                                       → OpenAI (Fallback)
                                       → Anthropic (Fallback 2)
```

**Implementation:**
- LiteLLM Proxy handles routing and fallbacks
- Backend only calls LiteLLM proxy
- Automatic retry and failover

---

## Best Practices for Implementation

### 1. **Resource Management**
```yaml
# Recommended Docker resource limits
deploy:
  resources:
    limits:
      memory: 6G      # Max memory
      cpus: '3.0'     # Max CPU cores
    reservations:
      memory: 4G      # Guaranteed memory
```

### 2. **Health Checks**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:11434/api/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s
```

### 3. **Python Client with Fallback**
```python
from litellm import completion
import os

def generate_text(prompt: str, temperature: float = 0.7):
    """Generate text with automatic fallback"""
    try:
        # Try local Ollama first
        response = completion(
            model="ollama/gemma:2b",
            messages=[{"role": "user", "content": prompt}],
            api_base="http://localhost:11434",
            temperature=temperature,
            max_retries=2,
            timeout=30
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Local LLM failed: {e}, falling back to OpenAI")
        # Fallback to OpenAI
        response = completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=temperature
        )
        return response.choices[0].message.content
```

### 4. **Environment Variables**
```bash
# .env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma:2b
OPENAI_API_KEY=sk-xxx  # Fallback only
LLM_TIMEOUT=30
LLM_MAX_RETRIES=2
```

### 5. **Security Considerations**
- Run containers as non-root users
- Use reverse proxy (nginx) for external access
- Implement rate limiting
- Validate and sanitize all prompts
- Set resource limits to prevent DoS

---

## Lightweight Model Comparison

| Model | Parameters | Quantized Size | RAM | Speed | Quality | Best For |
|-------|-----------|----------------|-----|-------|---------|----------|
| TinyLlama 1.1B | 1.1B | ~600MB | 2GB | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | Simple tasks, ultra-fast |
| Gemma 2B | 2B | ~1.5GB | 3GB | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | General purpose, Q&A |
| Llama 3.2 1B | 1B | ~700MB | 2GB | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Text generation |
| Phi-3 Mini | 3.8B | ~2.3GB | 4GB | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Coding, reasoning |

**Recommendation:** Start with **Gemma 2B** or **Llama 3.2 1B** for best balance of performance and quality.

---

## Implementation Steps

### Step 1: Setup Ollama with Docker
```bash
# Create docker-compose.yml
docker-compose up -d ollama

# Pull model
docker exec ollama ollama pull gemma:2b
```

### Step 2: Test Ollama API
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gemma:2b",
  "prompt": "What is a real estate cap rate?",
  "stream": false
}'
```

### Step 3: Install Python Client
```bash
pip install litellm
```

### Step 4: Create LLM Service Module
```python
# backend/services/llm_service.py
from litellm import completion
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(
        self,
        primary_model: str = "ollama/gemma:2b",
        fallback_model: str = "gpt-3.5-turbo",
        ollama_base: str = "http://localhost:11434"
    ):
        self.primary_model = primary_model
        self.fallback_model = fallback_model
        self.ollama_base = ollama_base

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> dict:
        """Generate text with automatic fallback"""
        try:
            response = completion(
                model=self.primary_model,
                messages=[{"role": "user", "content": prompt}],
                api_base=self.ollama_base,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=30
            )
            return {
                "text": response.choices[0].message.content,
                "model": self.primary_model,
                "source": "local"
            }
        except Exception as e:
            logger.warning(f"Local LLM failed: {e}, using fallback")
            response = completion(
                model=self.fallback_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return {
                "text": response.choices[0].message.content,
                "model": self.fallback_model,
                "source": "cloud"
            }
```

### Step 5: Add API Endpoint
```python
# backend/api/endpoints/llm.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()

class GenerateRequest(BaseModel):
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 500

@router.post("/generate")
async def generate_text(request: GenerateRequest):
    """Generate text using LLM with automatic fallback"""
    try:
        result = await llm_service.generate(
            prompt=request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Cost Analysis

### Local LLM (Ollama)
- **Setup Cost:** $0
- **Ongoing Cost:** Electricity (~$5-10/month for 24/7)
- **Per Request:** $0
- **Monthly at 10k requests:** ~$5-10

### Cloud API (OpenAI GPT-3.5)
- **Setup Cost:** $0
- **Per 1k tokens:** ~$0.001
- **Monthly at 10k requests (avg 500 tokens each):** ~$5-10

### Hybrid Approach (Recommended)
- **Primary:** Local Ollama (80% of requests)
- **Fallback:** OpenAI (20% of requests)
- **Monthly Cost:** ~$6-12

**ROI:** Local LLM pays for itself within 1 month compared to 100% cloud usage.

---

## Monitoring & Observability

### Key Metrics to Track
1. **Request latency** (local vs fallback)
2. **Fallback rate** (should be <10%)
3. **Model memory usage**
4. **Token usage and costs**
5. **Error rates**

### Recommended Tools
- **Prometheus + Grafana** for metrics
- **LiteLLM** built-in logging
- **Docker stats** for resource monitoring

---

## Potential Use Cases for Real Estate Dashboard

1. **Property Description Generation**
   - Generate listing descriptions from property features
   - Model: Gemma 2B or Phi-3 Mini

2. **Market Analysis Summaries**
   - Summarize market trends and data
   - Model: Llama 3.2 1B

3. **Customer Query Responses**
   - Answer common real estate questions
   - Model: Gemma 2B

4. **Data Extraction & Classification**
   - Extract entities from property documents
   - Model: Phi-3 Mini

5. **Investment Analysis Reports**
   - Generate insights from financial data
   - Model: Phi-3 Mini or Gemma 2B

---

## Next Steps

1. ✅ Research completed
2. ⬜ Add Ollama service to docker-compose.yml
3. ⬜ Install litellm Python package
4. ⬜ Create LLM service module with fallback logic
5. ⬜ Add API endpoints for text generation
6. ⬜ Implement frontend integration
7. ⬜ Add monitoring and logging
8. ⬜ Performance testing and optimization
9. ⬜ Documentation for team

---

## References

- [Ollama Official Docs](https://ollama.ai/docs)
- [LocalAI GitHub](https://github.com/mudler/LocalAI)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Docker Model Runner](https://www.docker.com/blog/run-llms-locally/)
- [Best Practices 2025](https://markaicode.com/ollama-production-deployment-enterprise-guide/)

---

## Security & Compliance Notes

- All data stays on-premises (GDPR compliant)
- No data sent to third parties (unless fallback triggered)
- Implement request logging for audit trails
- Consider adding content filtering for user inputs
- Set rate limits to prevent abuse

---

**Document Version:** 1.0
**Last Updated:** 2025-11-13
**Author:** Claude Code AI Assistant
