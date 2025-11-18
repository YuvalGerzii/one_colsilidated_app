# LLM Deployment Guide

**Status:** ✅ Implementation Complete - Ready to Deploy
**Date:** 2025-11-13

---

## ✅ What's Been Implemented

### 1. Infrastructure Configuration
- ✅ Docker Compose updated with Ollama service
- ✅ Environment variables configured
- ✅ Resource limits set (4GB RAM, 2 CPU)
- ✅ Health checks configured

### 2. Backend Services
- ✅ `llm_service.py` - Complete LLM service with graceful degradation
- ✅ `enhanced_clause_analysis.py` - LLM-enhanced clause analysis
- ✅ API endpoints at `/api/v1/llm/*`
- ✅ Settings configuration with all LLM parameters

### 3. API Endpoints Created
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/llm/health` | GET | Check LLM service status |
| `/api/v1/llm/metrics` | GET | Get performance metrics |
| `/api/v1/llm/generate` | POST | General text generation |
| `/api/v1/llm/summarize` | POST | Text summarization |
| `/api/v1/llm/generate-property-description` | POST | Property descriptions |

---

## 🚀 Deployment Steps

### Step 1: Start Ollama Container

```bash
cd /home/user/real_estate_dashboard

# Start only the Ollama service
docker compose up -d ollama

# Check if it's running
docker ps | grep ollama
```

**Expected output:**
```
CONTAINER ID   IMAGE                   STATUS        PORTS
xxxxx          ollama/ollama:latest    Up 10 secs    0.0.0.0:11434->11434/tcp
```

### Step 2: Wait for Ollama to Be Healthy

```bash
# Wait for health check to pass (up to 60 seconds)
docker compose ps ollama
```

**Wait until STATUS shows:**
```
NAME                 STATUS
real_estate_ollama   Up 30 seconds (healthy)
```

### Step 3: Pull Gemma 2B Model

```bash
# Pull the lightweight Gemma 2B model (~1.5GB download)
docker exec real_estate_ollama ollama pull gemma:2b
```

**Expected output:**
```
pulling manifest
pulling 8ccb4...: 100% ▕████████████████▏ 1.6 GB
pulling manifest
success
```

**⏱️ Time:** First pull takes 2-5 minutes depending on internet speed.

### Step 4: Verify Model Installation

```bash
# List installed models
docker exec real_estate_ollama ollama list
```

**Expected output:**
```
NAME       ID           SIZE     MODIFIED
gemma:2b   8ccb...      1.6 GB   3 seconds ago
```

### Step 5: Test Ollama API

```bash
# Test the Ollama health endpoint
curl http://localhost:11434/api/health

# Test generation (optional)
curl http://localhost:11434/api/generate -d '{
  "model": "gemma:2b",
  "prompt": "Hello, how are you?",
  "stream": false
}'
```

**Expected output from health:**
```json
{}
```
*(Empty JSON means healthy)*

### Step 6: Restart Backend to Load LLM Service

```bash
# Restart backend to initialize LLM service
docker compose restart backend

# Watch backend logs
docker compose logs -f backend
```

**Look for:**
```
INFO - LLM Service initialized - Enabled: True, Model: gemma:2b, Base URL: http://ollama:11434
INFO - 🚀 Real Estate Dashboard started successfully!
```

### Step 7: Test LLM Integration

```bash
# Test LLM health check
curl http://localhost:8000/api/v1/llm/health

# Test text generation
curl -X POST http://localhost:8000/api/v1/llm/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Describe a 3 bedroom house",
    "max_tokens": 100
  }'
```

**Expected health check response:**
```json
{
  "status": "healthy",
  "available": true,
  "model": "gemma:2b",
  "metrics": {
    "total_requests": 0,
    "successful_requests": 0,
    "cache_hit_rate": 0
  }
}
```

**Expected generation response:**
```json
{
  "text": "A charming 3-bedroom home offers comfortable living space...",
  "available": true,
  "model": "gemma:2b",
  "metadata": {
    "prompt_tokens": 6,
    "completion_tokens": 95,
    "total_tokens": 101
  }
}
```

---

## 📊 Verification Checklist

- [ ] Ollama container is running
- [ ] Ollama health check returns `{}`
- [ ] Gemma 2B model is downloaded (1.6 GB)
- [ ] Backend logs show "LLM Service initialized"
- [ ] `/api/v1/llm/health` returns `available: true`
- [ ] `/api/v1/llm/generate` returns generated text
- [ ] Check API docs at http://localhost:8000/docs (search for "llm")

---

## 🔧 Troubleshooting

### Issue: Ollama health check fails

**Solution:**
```bash
# Check Ollama logs
docker compose logs ollama

# Restart Ollama
docker compose restart ollama

# Wait 60 seconds for startup
sleep 60

# Try health check again
curl http://localhost:11434/api/health
```

### Issue: Model not found error

**Solution:**
```bash
# List models
docker exec real_estate_ollama ollama list

# If empty, pull the model again
docker exec real_estate_ollama ollama pull gemma:2b
```

### Issue: Backend can't connect to Ollama

**Check:**
1. Both containers are on the same network
2. Backend env var `OLLAMA_BASE_URL=http://ollama:11434` (use service name, not localhost)

```bash
# Check network
docker compose ps

# Restart backend
docker compose restart backend
```

### Issue: LLM requests timing out

**Check resource limits:**
```bash
# Check Ollama memory usage
docker stats real_estate_ollama

# If memory is maxed out, increase limit in docker-compose.yml:
# limits:
#   memory: 6G  # Increase from 4G
```

### Issue: "LLM service unavailable" in API response

**This is expected behavior!** The service uses graceful degradation:
- Check `/api/v1/llm/health` to see status
- If unavailable, app continues working without LLM
- Fix Ollama and features will automatically use LLM again

---

## 📈 Monitoring

### View Real-Time Metrics

```bash
# LLM service metrics
curl http://localhost:8000/api/v1/llm/metrics
```

**Response:**
```json
{
  "total_requests": 47,
  "successful_requests": 45,
  "failed_requests": 2,
  "cache_hits": 12,
  "total_tokens_generated": 3420,
  "avg_response_time": 1.34,
  "cache_hit_rate": 0.255,
  "success_rate": 0.957
}
```

### Monitor Container Resources

```bash
# Watch resource usage
docker stats real_estate_ollama

# View logs
docker compose logs -f ollama
```

### Check Backend Logs

```bash
# Filter for LLM-related logs
docker compose logs backend | grep LLM
```

---

## 🎯 Testing Endpoints

### 1. Health Check

```bash
curl http://localhost:8000/api/v1/llm/health | jq
```

### 2. Generate Property Description

```bash
curl -X POST http://localhost:8000/api/v1/llm/generate-property-description \
  -H "Content-Type: application/json" \
  -d '{
    "bedrooms": 3,
    "bathrooms": 2.5,
    "sqft": 1800,
    "property_type": "Single Family Home",
    "amenities": "Pool, Updated kitchen, Hardwood floors",
    "location": "Miami, FL"
  }' | jq
```

### 3. Summarize Text

```bash
curl -X POST http://localhost:8000/api/v1/llm/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This luxury waterfront property features 4 spacious bedrooms, 3.5 bathrooms, and stunning ocean views. The gourmet kitchen includes top-of-the-line appliances, granite countertops, and a large island perfect for entertaining. The master suite offers a private balcony, walk-in closet, and spa-like bathroom. Additional features include a heated pool, 3-car garage, and smart home technology throughout.",
    "max_summary_length": 100
  }' | jq
```

### 4. General Text Generation

```bash
curl -X POST http://localhost:8000/api/v1/llm/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What are the key considerations when investing in multifamily real estate?",
    "system_prompt": "You are a real estate investment expert",
    "temperature": 0.7,
    "max_tokens": 300
  }' | jq
```

---

## 🌐 Access API Documentation

Once backend is running:
```
http://localhost:8000/docs
```

Search for **"llm"** to see all LLM endpoints with interactive testing.

---

## 🔄 Graceful Degradation Demo

### Test 1: With Ollama Running

```bash
curl -X POST http://localhost:8000/api/v1/llm/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello"}' | jq '.available'
```
**Result:** `true`

### Test 2: Stop Ollama

```bash
docker compose stop ollama

curl -X POST http://localhost:8000/api/v1/llm/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello"}' | jq '.available'
```
**Result:** `false` (app still works, just returns `available: false`)

### Test 3: Restart Ollama

```bash
docker compose start ollama
sleep 30  # Wait for health check

curl -X POST http://localhost:8000/api/v1/llm/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello"}' | jq '.available'
```
**Result:** `true` (automatically working again!)

---

## 📝 Environment Variables

All configured in `docker-compose.yml`:

```yaml
# Backend environment variables
ENABLE_LLM: "True"                    # Enable/disable LLM features
OLLAMA_BASE_URL: http://ollama:11434  # Ollama service URL
OLLAMA_MODEL: gemma:2b                # Model to use
LLM_TIMEOUT: 30                       # Request timeout (seconds)
LLM_MAX_RETRIES: 2                    # Retry attempts
```

To disable LLM:
```yaml
ENABLE_LLM: "False"
```

---

## 🎓 Next Steps

### 1. Frontend Integration (Future)
- Add LLM-powered features to UI
- Show "AI Generated" badges
- Handle unavailable state gracefully

### 2. Add More Use Cases
- Market analysis summaries
- Investment recommendations
- Risk assessment narratives
- Contract analysis

### 3. Optimize Performance
- Tune cache TTLs based on usage
- Adjust resource limits
- Monitor token usage

### 4. Production Deployment
- Set `ENABLE_LLM: "True"` in production
- Monitor logs and metrics
- Set up alerts for failures

---

## 💾 Resource Usage

**Expected Usage:**
- **Disk:** 1.6 GB (model storage)
- **RAM:** 2-4 GB (during inference)
- **CPU:** 1-2 cores (during inference)
- **Network:** None (100% local)

**Cost:** $0/month (100% free)

---

## ✅ Success Criteria

You've successfully deployed the LLM service when:

1. ✅ Ollama container is healthy
2. ✅ Gemma 2B model is loaded
3. ✅ `/api/v1/llm/health` returns `available: true`
4. ✅ Text generation works
5. ✅ Backend logs show no LLM errors
6. ✅ API docs show LLM endpoints

---

## 🆘 Getting Help

**Common Issues:**
- Ollama not starting → Check Docker resources (need 4GB free RAM)
- Model download fails → Check internet connection, retry
- Backend can't connect → Check docker network, use service name not localhost
- Slow responses → Normal for first request (model loading), subsequent requests faster

**Logs to Check:**
```bash
docker compose logs ollama       # Ollama container logs
docker compose logs backend      # Backend API logs
docker compose ps                # Service status
```

---

**Status:** ✅ Ready to deploy!
**Last Updated:** 2025-11-13
