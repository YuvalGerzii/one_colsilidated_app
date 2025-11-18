"""
LLM API Endpoints

Provides endpoints for LLM-powered features with graceful degradation.
"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException, status, Body, Query
from pydantic import BaseModel, Field

from app.services.llm_service import llm_service

router = APIRouter()


# ================================
# REQUEST/RESPONSE MODELS
# ================================

class GenerateRequest(BaseModel):
    """Request model for text generation"""
    prompt: str = Field(..., min_length=1, max_length=5000, description="Input prompt for text generation")
    system_prompt: Optional[str] = Field(None, max_length=1000, description="Optional system prompt for context")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=1.0, description="Generation temperature (0-1)")
    max_tokens: Optional[int] = Field(500, ge=50, le=2000, description="Maximum tokens to generate")
    use_cache: bool = Field(True, description="Whether to use cached responses")


class GenerateResponse(BaseModel):
    """Response model for text generation"""
    text: Optional[str] = Field(None, description="Generated text (null if LLM unavailable)")
    available: bool = Field(..., description="Whether LLM service is available")
    model: Optional[str] = Field(None, description="Model name used")
    metadata: Optional[dict] = Field(None, description="Generation metadata (tokens, timing)")


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="Service status (healthy/unhealthy/unavailable/disabled)")
    available: bool = Field(..., description="Whether LLM is available for use")
    model: Optional[str] = Field(None, description="Model name")
    message: Optional[str] = Field(None, description="Additional status message")
    metrics: Optional[dict] = Field(None, description="Service metrics")


class MetricsResponse(BaseModel):
    """Response model for metrics"""
    total_requests: int
    successful_requests: int
    failed_requests: int
    cache_hits: int
    total_tokens_generated: int
    avg_response_time: float
    cache_hit_rate: float
    success_rate: float


class SummarizeRequest(BaseModel):
    """Request model for text summarization"""
    text: str = Field(..., min_length=10, max_length=10000, description="Text to summarize")
    max_summary_length: int = Field(150, ge=50, le=500, description="Maximum summary length in tokens")


class PropertyDescriptionRequest(BaseModel):
    """Request model for property description generation"""
    bedrooms: int = Field(..., ge=0, le=20)
    bathrooms: float = Field(..., ge=0, le=20)
    sqft: int = Field(..., ge=100, le=100000)
    property_type: str = Field(..., max_length=100)
    amenities: Optional[str] = Field(None, max_length=1000)
    location: Optional[str] = Field(None, max_length=200)


class MarketAnalysisRequest(BaseModel):
    """Request model for market analysis"""
    market_data: dict = Field(..., description="Market data to analyze")
    location: str = Field(..., max_length=200, description="Market location")
    analysis_focus: Optional[str] = Field(None, max_length=500, description="Specific aspects to focus on")


class InvestmentRecommendationRequest(BaseModel):
    """Request model for investment recommendation"""
    property_data: dict = Field(..., description="Property financial data")
    investor_profile: Optional[dict] = Field(None, description="Investor preferences and constraints")


class RiskAssessmentRequest(BaseModel):
    """Request model for risk assessment"""
    property_info: dict = Field(..., description="Property and deal information")
    risk_factors: Optional[List[str]] = Field(None, description="Specific risk factors to evaluate")


class ComparePropertiesRequest(BaseModel):
    """Request model for property comparison"""
    properties: List[dict] = Field(..., min_length=2, max_length=5, description="Properties to compare")
    comparison_criteria: Optional[List[str]] = Field(None, description="Specific criteria to compare")


class DealMemoRequest(BaseModel):
    """Request model for deal memo generation"""
    deal_data: dict = Field(..., description="Complete deal information")
    memo_sections: Optional[List[str]] = Field(None, description="Specific sections to include")


class LeaseAnalysisRequest(BaseModel):
    """Request model for lease analysis"""
    lease_data: dict = Field(..., description="Lease terms and conditions")
    tenant_info: Optional[dict] = Field(None, description="Tenant information")


# ================================
# ENDPOINTS
# ================================

@router.get("/health", response_model=HealthResponse, tags=["llm"])
async def llm_health_check():
    """
    Check LLM service health status.

    Returns service status, availability, and metrics.

    **Possible Statuses:**
    - `healthy`: LLM service is running and responding
    - `unhealthy`: LLM service is running but not responding correctly
    - `unavailable`: Cannot connect to LLM service
    - `disabled`: LLM service is disabled in settings
    """
    health = await llm_service.health_check()
    return health


@router.get("/metrics", response_model=MetricsResponse, tags=["llm"])
async def llm_metrics():
    """
    Get LLM service metrics.

    Returns:
    - Request counts (total, successful, failed)
    - Cache statistics (hits, hit rate)
    - Performance metrics (avg response time, tokens generated)
    - Success rate
    """
    return llm_service.get_metrics()


@router.post("/generate", response_model=GenerateResponse, tags=["llm"])
async def generate_text(request: GenerateRequest):
    """
    Generate text using local LLM.

    **Graceful Degradation:**
    If LLM is unavailable, returns `available=False` with `text=null`.
    Client should handle gracefully by using fallback logic.

    **Example Request:**
    ```json
    {
      "prompt": "Summarize this property: 3 bed, 2 bath, 1500 sqft",
      "system_prompt": "You are a real estate expert",
      "temperature": 0.7,
      "max_tokens": 200
    }
    ```

    **Example Response (Success):**
    ```json
    {
      "text": "This charming 3-bedroom, 2-bathroom home...",
      "available": true,
      "model": "gemma:2b",
      "metadata": {
        "prompt_tokens": 15,
        "completion_tokens": 87,
        "total_tokens": 102
      }
    }
    ```

    **Example Response (LLM Unavailable):**
    ```json
    {
      "text": null,
      "available": false,
      "model": null,
      "metadata": null
    }
    ```
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


@router.post("/summarize", response_model=GenerateResponse, tags=["llm"])
async def summarize_text(request: SummarizeRequest):
    """
    Summarize long text into a concise summary.

    **Use Cases:**
    - Property descriptions
    - Market reports
    - Document summaries
    - Contract overviews

    **Example:**
    ```json
    {
      "text": "Long property description or market analysis...",
      "max_summary_length": 150
    }
    ```
    """
    system_prompt = "You are an expert at creating concise, informative summaries. Provide a clear summary in 2-3 sentences."

    prompt = f"Summarize the following text:\n\n{request.text}"

    result = await llm_service.generate(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=0.3,  # Lower temperature for more focused summaries
        max_tokens=request.max_summary_length,
        use_cache=True
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


@router.post("/generate-property-description", response_model=GenerateResponse, tags=["llm"])
async def generate_property_description(request: PropertyDescriptionRequest):
    """
    Generate a marketing-ready property description.

    **Example:**
    ```json
    {
      "bedrooms": 3,
      "bathrooms": 2.5,
      "sqft": 1800,
      "property_type": "Single Family Home",
      "amenities": "Pool, Updated kitchen, Hardwood floors",
      "location": "Miami, FL"
    }
    ```

    **Returns:**
    Professional property description suitable for listings.
    """
    system_prompt = "You are a professional real estate copywriter. Create compelling property descriptions that highlight key features and appeal to potential buyers."

    prompt = f"""Create a property description for:
- Type: {request.property_type}
- Bedrooms: {request.bedrooms}
- Bathrooms: {request.bathrooms}
- Square Feet: {request.sqft:,}"""

    if request.location:
        prompt += f"\n- Location: {request.location}"

    if request.amenities:
        prompt += f"\n- Amenities: {request.amenities}"

    prompt += "\n\nWrite an engaging 2-3 paragraph description."

    result = await llm_service.generate(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=0.8,  # Higher creativity for marketing copy
        max_tokens=300,
        use_cache=True
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

# ================================
# ADVANCED REAL ESTATE ENDPOINTS
# ================================

@router.post("/analyze-market", response_model=GenerateResponse, tags=["llm", "real-estate"])
async def analyze_market_data(request: MarketAnalysisRequest):
    """
    Generate market analysis from data.

    **Use Cases:**
    - Summarize market trends
    - Identify investment opportunities
    - Compare market performance

    **Example:**
    ```json
    {
      "market_data": {
        "median_price": 450000,
        "price_change_yoy": 8.5,
        "inventory": 245,
        "days_on_market": 28,
        "absorption_rate": 3.2
      },
      "location": "Austin, TX",
      "analysis_focus": "Investment opportunities for multifamily"
    }
    ```
    """
    import json
    
    system_prompt = """You are a real estate market analyst with expertise in identifying trends,
opportunities, and risks. Provide data-driven insights and actionable recommendations."""

    prompt = f"""Analyze the following real estate market data for {request.location}:

{json.dumps(request.market_data, indent=2)}
"""

    if request.analysis_focus:
        prompt += f"\n\nSpecific focus: {request.analysis_focus}"

    prompt += "\n\nProvide a concise market analysis with key insights and recommendations."

    result = await llm_service.generate(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=0.4,  # Lower for analytical content
        max_tokens=400,
        use_cache=True
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


@router.post("/investment-recommendation", response_model=GenerateResponse, tags=["llm", "real-estate"])
async def generate_investment_recommendation(request: InvestmentRecommendationRequest):
    """
    Generate investment recommendation for a property.

    **Example:**
    ```json
    {
      "property_data": {
        "purchase_price": 500000,
        "estimated_noi": 42000,
        "cap_rate": 8.4,
        "cash_on_cash": 12.5,
        "property_type": "Multifamily",
        "units": 8,
        "location": "Phoenix, AZ"
      },
      "investor_profile": {
        "risk_tolerance": "moderate",
        "investment_horizon": "10 years",
        "target_return": 10
      }
    }
    ```

    **Returns:**
    Investment recommendation with pros, cons, and risk assessment.
    """
    import json
    
    system_prompt = """You are an experienced real estate investment advisor.
Provide balanced recommendations considering returns, risks, and market conditions."""

    prompt = f"""Analyze this investment opportunity:

Property Details:
{json.dumps(request.property_data, indent=2)}
"""

    if request.investor_profile:
        prompt += f"\n\nInvestor Profile:\n{json.dumps(request.investor_profile, indent=2)}"

    prompt += """

Provide:
1. Investment recommendation (Buy/Hold/Pass)
2. Key strengths
3. Main concerns
4. Risk factors
5. Expected performance"""

    result = await llm_service.generate(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=0.3,  # Very focused for financial advice
        max_tokens=500,
        use_cache=True
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


@router.post("/risk-assessment", response_model=GenerateResponse, tags=["llm", "real-estate"])
async def assess_property_risk(request: RiskAssessmentRequest):
    """
    Generate comprehensive risk assessment for a property or deal.

    **Example:**
    ```json
    {
      "property_info": {
        "property_type": "Office Building",
        "location": "Downtown Chicago",
        "vacancy_rate": 18,
        "tenant_concentration": "Top tenant is 40% of income",
        "deferred_maintenance": 150000,
        "market_outlook": "Declining demand for office space"
      },
      "risk_factors": ["tenant default", "market downturn", "capital expenditures"]
    }
    ```

    **Returns:**
    Detailed risk assessment with mitigation strategies.
    """
    import json
    
    system_prompt = """You are a real estate risk analyst. Identify and evaluate risks objectively,
providing specific mitigation strategies."""

    prompt = f"""Conduct a risk assessment for this property:

{json.dumps(request.property_info, indent=2)}
"""

    if request.risk_factors:
        prompt += f"\n\nFocus on these risk factors: {', '.join(request.risk_factors)}"

    prompt += """

Provide:
1. Risk level (High/Medium/Low)
2. Top 3-5 risk factors
3. Mitigation strategies
4. Red flags or deal breakers"""

    result = await llm_service.generate(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=0.3,
        max_tokens=450,
        use_cache=True
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


@router.post("/compare-properties", response_model=GenerateResponse, tags=["llm", "real-estate"])
async def compare_properties(request: ComparePropertiesRequest):
    """
    Compare multiple properties and provide analysis.

    **Example:**
    ```json
    {
      "properties": [
        {
          "name": "Property A",
          "price": 500000,
          "cap_rate": 7.5,
          "location": "Suburb",
          "condition": "Good"
        },
        {
          "name": "Property B",
          "price": 550000,
          "cap_rate": 8.2,
          "location": "Urban",
          "condition": "Needs work"
        }
      ],
      "comparison_criteria": ["ROI potential", "location", "risk level"]
    }
    ```

    **Returns:**
    Comparative analysis with pros/cons for each property.
    """
    import json
    
    system_prompt = """You are a real estate analyst specializing in property comparison and selection.
Provide objective comparisons highlighting trade-offs."""

    prompt = f"""Compare these {len(request.properties)} properties:

{json.dumps(request.properties, indent=2)}
"""

    if request.comparison_criteria:
        prompt += f"\n\nComparison criteria: {', '.join(request.comparison_criteria)}"

    prompt += """

Provide:
1. Side-by-side comparison
2. Best choice for different scenarios
3. Ranking with justification"""

    result = await llm_service.generate(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=0.4,
        max_tokens=500,
        use_cache=True
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


@router.post("/generate-deal-memo", response_model=GenerateResponse, tags=["llm", "real-estate"])
async def generate_deal_memo(request: DealMemoRequest):
    """
    Generate an investment memo for a deal.

    **Example:**
    ```json
    {
      "deal_data": {
        "property_name": "Sunset Apartments",
        "address": "123 Main St, Phoenix, AZ",
        "property_type": "Multifamily",
        "units": 24,
        "purchase_price": 3200000,
        "noi": 285000,
        "cap_rate": 8.9,
        "financing": "70% LTV, 5.5% rate",
        "value_add_strategy": "Unit renovations, rent increases",
        "exit_strategy": "5-year hold, projected sale"
      },
      "memo_sections": ["Executive Summary", "Investment Highlights", "Financial Analysis", "Risks"]
    }
    ```

    **Returns:**
    Professional investment memo suitable for presentation.
    """
    import json
    
    system_prompt = """You are an institutional real estate investment professional.
Write clear, professional investment memos that present opportunities objectively."""

    prompt = f"""Create an investment memo for this deal:

{json.dumps(request.deal_data, indent=2)}
"""

    if request.memo_sections:
        prompt += f"\n\nInclude these sections: {', '.join(request.memo_sections)}"
    else:
        prompt += """

Include these sections:
1. Executive Summary
2. Investment Highlights
3. Key Metrics
4. Strategy & Value Creation
5. Risk Factors"""

    result = await llm_service.generate(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=0.5,
        max_tokens=800,
        use_cache=True
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


@router.post("/analyze-lease", response_model=GenerateResponse, tags=["llm", "real-estate"])
async def analyze_lease_terms(request: LeaseAnalysisRequest):
    """
    Analyze lease terms and identify key considerations.

    **Example:**
    ```json
    {
      "lease_data": {
        "tenant": "TechCorp Inc.",
        "term": "10 years",
        "base_rent": 25.50,
        "rent_increases": "3% annually",
        "tenant_improvement_allowance": 50,
        "lease_type": "NNN",
        "renewal_options": "Two 5-year options",
        "termination_clause": "After year 7 with 12 month notice"
      },
      "tenant_info": {
        "credit_rating": "BBB+",
        "industry": "Technology",
        "financials": "Strong, profitable"
      }
    }
    ```

    **Returns:**
    Lease analysis with landlord/tenant perspectives.
    """
    import json
    
    system_prompt = """You are a commercial real estate leasing expert.
Analyze lease terms from both landlord and tenant perspectives."""

    prompt = f"""Analyze this lease:

Lease Terms:
{json.dumps(request.lease_data, indent=2)}
"""

    if request.tenant_info:
        prompt += f"\n\nTenant Information:\n{json.dumps(request.tenant_info, indent=2)}"

    prompt += """

Provide:
1. Key terms summary
2. Strengths (landlord perspective)
3. Concerns or risks
4. Market competitiveness
5. Negotiation points"""

    result = await llm_service.generate(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=0.4,
        max_tokens=500,
        use_cache=True
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


# ================================
# BATCH PROCESSING
# ================================

class BatchGenerateRequest(BaseModel):
    """Request model for batch text generation"""
    items: List[dict] = Field(..., min_items=1, max_items=10, description="Batch of items to process")
    operation: str = Field(..., description="Operation type: summarize, describe, analyze")
    common_params: Optional[dict] = Field(None, description="Common parameters for all items")


class BatchGenerateResponse(BaseModel):
    """Response model for batch generation"""
    results: List[GenerateResponse]
    total_items: int
    successful_items: int
    failed_items: int
    llm_available: bool


@router.post("/batch-generate", response_model=BatchGenerateResponse, tags=["llm", "batch"])
async def batch_generate(request: BatchGenerateRequest):
    """
    Process multiple items in batch for efficiency.

    **Supported Operations:**
    - `summarize`: Summarize multiple documents
    - `describe`: Generate property descriptions
    - `analyze`: Analyze multiple properties

    **Example:**
    ```json
    {
      "items": [
        {"text": "Long description 1..."},
        {"text": "Long description 2..."},
        {"text": "Long description 3..."}
      ],
      "operation": "summarize",
      "common_params": {
        "max_tokens": 100
      }
    }
    ```

    **Returns:**
    Results for each item with success/failure status.
    """
    import json
    
    results = []
    successful = 0
    failed = 0

    for item in request.items:
        # Merge common params with item-specific params
        params = {**(request.common_params or {}), **item}

        # Dispatch based on operation type
        if request.operation == "summarize":
            if "text" in params:
                result = await llm_service.generate(
                    prompt=f"Summarize: {params['text']}",
                    system_prompt="Provide concise summaries.",
                    temperature=0.3,
                    max_tokens=params.get("max_tokens", 150),
                    use_cache=True
                )
        elif request.operation == "describe":
            # Property description
            result = await llm_service.generate(
                prompt=f"Describe this property: {json.dumps(params)}",
                system_prompt="You are a real estate copywriter.",
                temperature=0.7,
                max_tokens=params.get("max_tokens", 300),
                use_cache=True
            )
        else:
            result = None

        if result:
            results.append(GenerateResponse(
                text=result["text"],
                available=True,
                model=result["model"],
                metadata=result.get("metadata")
            ))
            successful += 1
        else:
            results.append(GenerateResponse(
                text=None,
                available=False,
                model=None,
                metadata=None
            ))
            failed += 1

    return BatchGenerateResponse(
        results=results,
        total_items=len(request.items),
        successful_items=successful,
        failed_items=failed,
        llm_available=successful > 0
    )
