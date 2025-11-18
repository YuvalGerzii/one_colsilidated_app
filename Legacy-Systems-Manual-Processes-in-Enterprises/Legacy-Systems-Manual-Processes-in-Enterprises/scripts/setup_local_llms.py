#!/usr/bin/env python3
"""
Setup script for local LLMs - Python version
100% FREE - No API keys needed!
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.llm import LocalLLMClient
from loguru import logger


async def main():
    """Setup local LLMs."""
    print("=" * 50)
    print("  Enterprise AI - Local LLM Setup")
    print("  100% FREE - No API Keys Required!")
    print("=" * 50)
    print()

    # Initialize client
    client = LocalLLMClient()

    # Check if Ollama is available
    print("Checking Ollama service...")
    is_available = await client.is_available()

    if not is_available:
        print("❌ Ollama service not accessible!")
        print()
        print("Please start Ollama:")
        print("  docker-compose up -d ollama")
        print()
        return 1

    print("✓ Ollama service is running")
    print()

    # Pull recommended models
    models_to_pull = [
        ("llama3.2:3b", "Llama 3.2 3B - Small, fast model for general tasks"),
        ("nomic-embed-text", "Nomic Embed Text - Embeddings for semantic search"),
    ]

    print("=" * 50)
    print("  Downloading Recommended Models")
    print("=" * 50)
    print()

    for model_name, description in models_to_pull:
        print(f"📥 {description}")
        print(f"   Model: {model_name}")

        success = await client.pull_model(model_name)

        if success:
            print(f"✓ Downloaded successfully")
        else:
            print(f"⚠ Failed to download {model_name}")

        print()

    # List available models
    print("=" * 50)
    print("  Available Models")
    print("=" * 50)
    print()

    models = await client.list_models()
    if models:
        for model in models:
            print(f"  • {model}")
    else:
        print("  No models found")

    print()

    # Test the model
    print("=" * 50)
    print("  Testing Model")
    print("=" * 50)
    print()

    print("Testing llama3.2:3b...")
    try:
        response = await client.chat_completion(
            messages=[{"role": "user", "content": "Say hello in one sentence."}],
            temperature=0.7,
            max_tokens=50,
        )
        print(f"✓ Model test successful!")
        print(f"Response: {response}")
    except Exception as e:
        print(f"⚠ Model test failed: {e}")

    print()
    print("=" * 50)
    print("  Setup Complete!")
    print("=" * 50)
    print()
    print("✓ Local LLMs are ready to use!")
    print()
    print("No API keys needed - everything runs locally!")
    print()
    print("Next steps:")
    print("  1. Copy .env.example to .env:")
    print("     cp .env.example .env")
    print()
    print("  2. Start the application:")
    print("     docker-compose up -d")
    print()
    print("  3. Access the API at:")
    print("     http://localhost:8000/docs")
    print()
    print("  4. Try translating legacy code:")
    print("     python examples/legacy_migration_example.py")
    print()

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
