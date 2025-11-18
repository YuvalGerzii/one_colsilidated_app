#!/bin/bash
# Setup script for local LLMs (100% FREE - No API keys needed!)

set -e

echo "=========================================="
echo "  Enterprise AI - Local LLM Setup"
echo "  100% FREE - No API Keys Required!"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Ollama is running
echo -e "${BLUE}Checking Ollama service...${NC}"
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${YELLOW}Ollama service not accessible at localhost:11434${NC}"
    echo "Please ensure Ollama is running:"
    echo "  docker-compose up -d ollama"
    echo ""
    echo "Or if running docker-compose for all services:"
    echo "  docker-compose up -d"
    exit 1
fi

echo -e "${GREEN}✓ Ollama service is running${NC}"
echo ""

# Function to pull a model
pull_model() {
    local model_name=$1
    local description=$2

    echo -e "${BLUE}Pulling ${description}...${NC}"
    echo "Model: ${model_name}"

    if curl -s -X POST http://localhost:11434/api/pull \
        -d "{\"name\": \"${model_name}\"}" \
        -H "Content-Type: application/json" | grep -q "success"; then
        echo -e "${GREEN}✓ ${description} downloaded successfully${NC}"
    else
        # Try alternative method
        docker exec enterprise-ai-ollama ollama pull ${model_name}
        echo -e "${GREEN}✓ ${description} downloaded${NC}"
    fi
    echo ""
}

# Pull recommended models
echo "=========================================="
echo "  Downloading Recommended Models"
echo "=========================================="
echo ""

# 1. Small, fast model for general tasks (recommended)
pull_model "llama3.2:3b" "Llama 3.2 3B (Small, Fast)"

# 2. Embedding model for semantic search
pull_model "nomic-embed-text" "Nomic Embed Text (Embeddings)"

echo ""
echo "=========================================="
echo "  Optional Models (Comment out if not needed)"
echo "=========================================="
echo ""

# Uncomment these if you want more powerful models
# pull_model "llama3.1:8b" "Llama 3.1 8B (Balanced)"
# pull_model "llama3.1:70b" "Llama 3.1 70B (Most Capable - requires GPU)"
# pull_model "codellama:13b" "Code Llama 13B (Code Generation)"
# pull_model "mistral:7b" "Mistral 7B (Fast & Capable)"

echo ""
echo "=========================================="
echo "  Testing Models"
echo "=========================================="
echo ""

# Test the main model
echo -e "${BLUE}Testing llama3.2:3b...${NC}"
response=$(curl -s -X POST http://localhost:11434/api/generate \
    -d '{"model": "llama3.2:3b", "prompt": "Say hello in one sentence.", "stream": false}' \
    -H "Content-Type: application/json" | grep -o '"response":"[^"]*"' | cut -d'"' -f4)

if [ -n "$response" ]; then
    echo -e "${GREEN}✓ Model test successful!${NC}"
    echo "Response: $response"
else
    echo -e "${YELLOW}⚠ Model test returned empty response${NC}"
fi

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo -e "${GREEN}✓ Local LLMs are ready to use!${NC}"
echo ""
echo "Available models:"
docker exec enterprise-ai-ollama ollama list
echo ""
echo "No API keys needed - everything runs locally!"
echo ""
echo "Next steps:"
echo "  1. Copy .env.example to .env:"
echo "     cp .env.example .env"
echo ""
echo "  2. Start the application:"
echo "     docker-compose up -d"
echo ""
echo "  3. Access the API at:"
echo "     http://localhost:8000/docs"
echo ""
echo "  4. Try translating legacy code:"
echo "     python examples/legacy_migration_example.py"
echo ""
