"""API routes for LLM monitoring and management."""

from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.core.llm import get_local_llm
from src.core.logger import logger

router = APIRouter()


class ModelInfo(BaseModel):
    """Model information."""
    name: str
    status: str


class LLMStats(BaseModel):
    """LLM usage statistics."""
    total_requests: int
    total_tokens: int
    avg_response_time: str
    error_rate: str
    cost_saved: str
    cache_stats: Dict[str, Any]


class TestPrompt(BaseModel):
    """Test prompt request."""
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 100


@router.get("/status")
async def get_llm_status() -> Dict[str, Any]:
    """Get LLM service status."""
    llm = get_local_llm()

    is_available = await llm.is_available()

    return {
        "status": "healthy" if is_available else "unhealthy",
        "model": llm.model,
        "base_url": llm.base_url,
        "available": is_available,
    }


@router.get("/models", response_model=List[ModelInfo])
async def list_models() -> List[ModelInfo]:
    """List all installed models."""
    llm = get_local_llm()

    try:
        models = await llm.list_models()
        return [ModelInfo(name=model, status="installed") for model in models]
    except Exception as e:
        logger.error(f"Failed to list models: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/models/{model_name}/pull")
async def pull_model(model_name: str) -> Dict[str, Any]:
    """Pull a model from Ollama library."""
    llm = get_local_llm()

    logger.info(f"Pulling model via API: {model_name}")

    try:
        success = await llm.pull_model(model_name)

        if success:
            return {"status": "success", "model": model_name, "message": "Model pulled successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to pull model")

    except Exception as e:
        logger.error(f"Model pull failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/models/{model_name}")
async def delete_model(model_name: str) -> Dict[str, Any]:
    """Delete a local model."""
    llm = get_local_llm()

    try:
        success = await llm.delete_model(model_name)

        if success:
            return {"status": "success", "model": model_name, "message": "Model deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete model")

    except Exception as e:
        logger.error(f"Model deletion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=LLMStats)
async def get_stats() -> LLMStats:
    """Get LLM usage statistics."""
    llm = get_local_llm()

    metrics = llm.get_metrics()
    cache_stats = llm.get_cache_stats()

    return LLMStats(
        total_requests=metrics["total_requests"],
        total_tokens=metrics["total_tokens"],
        avg_response_time=metrics["avg_response_time"],
        error_rate=metrics["error_rate"],
        cost_saved=metrics["cost_saved"],
        cache_stats=cache_stats,
    )


@router.post("/cache/clear")
async def clear_cache() -> Dict[str, Any]:
    """Clear LLM response cache."""
    llm = get_local_llm()

    llm.clear_cache()

    return {"status": "success", "message": "Cache cleared"}


@router.post("/test")
async def test_llm(request: TestPrompt) -> Dict[str, Any]:
    """Test LLM with a prompt."""
    llm = get_local_llm()

    try:
        response = await llm.chat_completion(
            messages=[{"role": "user", "content": request.prompt}],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        return {
            "status": "success",
            "prompt": request.prompt,
            "response": response,
            "model": llm.model,
        }

    except Exception as e:
        logger.error(f"LLM test failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check() -> dict:
    """Health check for LLM monitoring."""
    return {"status": "healthy", "module": "llm_monitoring"}
