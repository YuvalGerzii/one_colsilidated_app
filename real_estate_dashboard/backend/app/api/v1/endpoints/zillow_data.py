"""
Zillow Property Data API Endpoints

Provides endpoints for property data scraping and analysis using HomeHarvest.
Uses background tasks to avoid timeout issues with long-running scrapes.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio
import uuid
import json
from enum import Enum

router = APIRouter()

# In-memory task storage (use Redis in production)
scrape_tasks: Dict[str, Dict[str, Any]] = {}


class ListingType(str, Enum):
    FOR_SALE = "for_sale"
    FOR_RENT = "for_rent"
    SOLD = "sold"
    PENDING = "pending"


class ScrapeRequest(BaseModel):
    location: str = Field(..., description="ZIP code, city, or address to search")
    listing_type: ListingType = Field(default=ListingType.FOR_SALE)
    past_days: int = Field(default=30, ge=1, le=365, description="Days of data to retrieve")
    delay_seconds: float = Field(default=3.0, ge=1.0, le=10.0, description="Delay between requests")


class MultiLocationScrapeRequest(BaseModel):
    locations: List[str] = Field(..., max_length=10, description="List of locations (max 10)")
    listing_type: ListingType = Field(default=ListingType.FOR_SALE)
    delay_seconds: float = Field(default=5.0, ge=3.0, le=15.0, description="Delay between requests")


class CompSearchRequest(BaseModel):
    address: str = Field(..., description="Subject property address")
    min_beds: Optional[int] = Field(default=None, ge=0, le=10)
    max_beds: Optional[int] = Field(default=None, ge=0, le=10)
    past_days: int = Field(default=180, ge=30, le=365)
    radius_miles: float = Field(default=1.0, ge=0.1, le=5.0)


class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str
    created_at: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    progress: Optional[int] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None


def run_scrape_task(task_id: str, location: str, listing_type: str, past_days: int, delay_seconds: float):
    """Background task to run property scraping"""
    try:
        scrape_tasks[task_id]["status"] = "running"
        scrape_tasks[task_id]["progress"] = 10

        # Import homeharvest
        try:
            from homeharvest import scrape_property
        except ImportError:
            scrape_tasks[task_id]["status"] = "failed"
            scrape_tasks[task_id]["error"] = "homeharvest package not installed. Run: pip install homeharvest"
            return

        scrape_tasks[task_id]["progress"] = 30

        # Perform scrape
        import time
        time.sleep(delay_seconds)  # Respect rate limits

        properties = scrape_property(
            location=location,
            listing_type=listing_type,
            past_days=past_days
        )

        scrape_tasks[task_id]["progress"] = 80

        # Convert to dict and store results
        if properties is not None and len(properties) > 0:
            result_data = properties.to_dict(orient='records')

            # Calculate summary stats
            prices = [p.get('list_price') or p.get('sold_price') for p in result_data if p.get('list_price') or p.get('sold_price')]

            scrape_tasks[task_id]["result"] = {
                "count": len(result_data),
                "location": location,
                "listing_type": listing_type,
                "properties": result_data[:100],  # Limit to 100 for response size
                "summary": {
                    "total_count": len(result_data),
                    "avg_price": sum(prices) / len(prices) if prices else 0,
                    "min_price": min(prices) if prices else 0,
                    "max_price": max(prices) if prices else 0,
                }
            }
            scrape_tasks[task_id]["status"] = "completed"
        else:
            scrape_tasks[task_id]["result"] = {
                "count": 0,
                "location": location,
                "listing_type": listing_type,
                "properties": [],
                "summary": {"total_count": 0}
            }
            scrape_tasks[task_id]["status"] = "completed"

        scrape_tasks[task_id]["progress"] = 100
        scrape_tasks[task_id]["completed_at"] = datetime.utcnow().isoformat()

    except Exception as e:
        scrape_tasks[task_id]["status"] = "failed"
        scrape_tasks[task_id]["error"] = str(e)
        scrape_tasks[task_id]["completed_at"] = datetime.utcnow().isoformat()


@router.post("/scrape", response_model=TaskResponse)
async def start_property_scrape(
    request: ScrapeRequest,
    background_tasks: BackgroundTasks
):
    """
    Start a background property scraping task.

    Returns a task_id that can be used to check status and retrieve results.
    This prevents timeout issues with long-running scrapes.
    """
    task_id = str(uuid.uuid4())

    scrape_tasks[task_id] = {
        "status": "pending",
        "progress": 0,
        "result": None,
        "error": None,
        "created_at": datetime.utcnow().isoformat(),
        "completed_at": None,
        "request": request.dict()
    }

    # Add to background tasks
    background_tasks.add_task(
        run_scrape_task,
        task_id,
        request.location,
        request.listing_type.value,
        request.past_days,
        request.delay_seconds
    )

    return TaskResponse(
        task_id=task_id,
        status="pending",
        message=f"Scrape task started for {request.location}. Use GET /task/{task_id} to check status.",
        created_at=scrape_tasks[task_id]["created_at"]
    )


@router.get("/task/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """
    Get the status and results of a scraping task.
    """
    if task_id not in scrape_tasks:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    task = scrape_tasks[task_id]

    return TaskStatusResponse(
        task_id=task_id,
        status=task["status"],
        progress=task.get("progress"),
        result=task.get("result"),
        error=task.get("error"),
        created_at=task["created_at"],
        completed_at=task.get("completed_at")
    )


@router.get("/tasks")
async def list_tasks(
    status: Optional[str] = Query(default=None, description="Filter by status"),
    limit: int = Query(default=20, ge=1, le=100)
):
    """
    List all scraping tasks with optional status filter.
    """
    tasks = []
    for task_id, task in scrape_tasks.items():
        if status and task["status"] != status:
            continue
        tasks.append({
            "task_id": task_id,
            "status": task["status"],
            "created_at": task["created_at"],
            "completed_at": task.get("completed_at"),
            "location": task.get("request", {}).get("location")
        })

    # Sort by created_at descending
    tasks.sort(key=lambda x: x["created_at"], reverse=True)

    return {"tasks": tasks[:limit], "total": len(tasks)}


@router.delete("/task/{task_id}")
async def delete_task(task_id: str):
    """
    Delete a completed or failed task.
    """
    if task_id not in scrape_tasks:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    task = scrape_tasks[task_id]
    if task["status"] == "running":
        raise HTTPException(status_code=400, detail="Cannot delete a running task")

    del scrape_tasks[task_id]
    return {"message": f"Task {task_id} deleted"}


@router.post("/quick-search")
async def quick_property_search(
    location: str = Query(..., description="ZIP code or city to search"),
    listing_type: ListingType = Query(default=ListingType.FOR_SALE),
    limit: int = Query(default=10, ge=1, le=50)
):
    """
    Quick synchronous property search with timeout protection.

    Limited to small result sets to avoid timeouts.
    For larger searches, use the /scrape endpoint.
    """
    try:
        from homeharvest import scrape_property
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="homeharvest package not installed. Run: pip install homeharvest"
        )

    try:
        # Use asyncio with timeout for protection
        loop = asyncio.get_event_loop()

        def do_scrape():
            return scrape_property(
                location=location,
                listing_type=listing_type.value,
                past_days=7  # Short window for quick search
            )

        # Run with 30 second timeout
        properties = await asyncio.wait_for(
            loop.run_in_executor(None, do_scrape),
            timeout=30.0
        )

        if properties is not None and len(properties) > 0:
            result_data = properties.head(limit).to_dict(orient='records')
            return {
                "count": len(result_data),
                "location": location,
                "listing_type": listing_type.value,
                "properties": result_data
            }
        else:
            return {
                "count": 0,
                "location": location,
                "listing_type": listing_type.value,
                "properties": []
            }

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Search timed out. Use /scrape endpoint for background processing."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/market-stats/{location}")
async def get_market_stats(
    location: str,
    past_days: int = Query(default=90, ge=30, le=365)
):
    """
    Get market statistics for a location.

    Returns average prices, trends, and inventory stats.
    """
    try:
        from homeharvest import scrape_property
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="homeharvest package not installed"
        )

    try:
        loop = asyncio.get_event_loop()

        def do_scrape():
            # Get both active and sold for comparison
            active = scrape_property(
                location=location,
                listing_type="for_sale",
                past_days=7
            )
            sold = scrape_property(
                location=location,
                listing_type="sold",
                past_days=past_days
            )
            return active, sold

        active, sold = await asyncio.wait_for(
            loop.run_in_executor(None, do_scrape),
            timeout=45.0
        )

        stats = {
            "location": location,
            "active_listings": {},
            "sold_properties": {},
            "market_indicators": {}
        }

        # Active listings stats
        if active is not None and len(active) > 0:
            active_prices = [p for p in active['list_price'].dropna().tolist()]
            stats["active_listings"] = {
                "count": len(active),
                "avg_price": sum(active_prices) / len(active_prices) if active_prices else 0,
                "median_price": sorted(active_prices)[len(active_prices)//2] if active_prices else 0,
                "min_price": min(active_prices) if active_prices else 0,
                "max_price": max(active_prices) if active_prices else 0
            }

        # Sold properties stats
        if sold is not None and len(sold) > 0:
            sold_prices = [p for p in sold['sold_price'].dropna().tolist()]
            stats["sold_properties"] = {
                "count": len(sold),
                "avg_price": sum(sold_prices) / len(sold_prices) if sold_prices else 0,
                "median_price": sorted(sold_prices)[len(sold_prices)//2] if sold_prices else 0,
                "min_price": min(sold_prices) if sold_prices else 0,
                "max_price": max(sold_prices) if sold_prices else 0,
                "period_days": past_days
            }

            # Market indicators
            if stats["active_listings"].get("count", 0) > 0 and stats["sold_properties"].get("count", 0) > 0:
                monthly_sales = stats["sold_properties"]["count"] / (past_days / 30)
                months_inventory = stats["active_listings"]["count"] / monthly_sales if monthly_sales > 0 else 0

                stats["market_indicators"] = {
                    "months_of_inventory": round(months_inventory, 1),
                    "market_type": "Seller's Market" if months_inventory < 4 else ("Balanced" if months_inventory < 6 else "Buyer's Market"),
                    "list_to_sold_ratio": round(stats["active_listings"]["avg_price"] / stats["sold_properties"]["avg_price"], 2) if stats["sold_properties"]["avg_price"] > 0 else 1.0
                }

        return stats

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Market stats calculation timed out"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def zillow_health_check():
    """
    Check if Zillow data service is available.
    """
    try:
        from homeharvest import scrape_property
        return {
            "status": "healthy",
            "homeharvest": "installed",
            "message": "Zillow data service is available"
        }
    except ImportError:
        return {
            "status": "degraded",
            "homeharvest": "not installed",
            "message": "Install homeharvest: pip install homeharvest"
        }
