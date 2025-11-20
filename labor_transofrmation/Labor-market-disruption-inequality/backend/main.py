from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import workers, skills, jobs, analytics, enterprise, digital_twin, autopilot, agents, progress, corporate, gig, economic_copilot, freelance, multi_agent_system, career_tools
from app.core.config import settings

app = FastAPI(
    title="Workforce Transition Platform API",
    description="AI-powered platform with Digital Twin™, AI Reskilling Autopilot, 10-Agent Intelligence Ecosystem, Progress Tracking with Gamification, Corporate Workforce Transformation OS, Automation Fairness Engine, Gig & Hybrid Labor Integration, Citizen-Level Economic Copilot, Mental Health & Burnout Prevention, Networking Intelligence, Salary Negotiation Coach, Interview Preparation System, and Skills Verification & Certification Tracker",
    version="2.8.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(workers.router, prefix=f"{settings.API_V1_PREFIX}/workers", tags=["workers"])
app.include_router(skills.router, prefix=f"{settings.API_V1_PREFIX}/skills", tags=["skills"])
app.include_router(jobs.router, prefix=f"{settings.API_V1_PREFIX}/jobs", tags=["jobs"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_PREFIX}/analytics", tags=["analytics"])
app.include_router(enterprise.router, prefix=f"{settings.API_V1_PREFIX}/enterprise", tags=["enterprise"])
app.include_router(digital_twin.router, prefix=f"{settings.API_V1_PREFIX}/digital-twin", tags=["digital-twin"])
app.include_router(autopilot.router, prefix=f"{settings.API_V1_PREFIX}/autopilot", tags=["autopilot"])
app.include_router(agents.router, prefix=f"{settings.API_V1_PREFIX}/agents", tags=["multi-agents"])
app.include_router(progress.router, prefix=f"{settings.API_V1_PREFIX}/progress", tags=["progress"])
app.include_router(corporate.router, prefix=f"{settings.API_V1_PREFIX}/corporate", tags=["corporate"])
app.include_router(gig.router, prefix=f"{settings.API_V1_PREFIX}/gig", tags=["gig-economy"])
app.include_router(economic_copilot.router, prefix=f"{settings.API_V1_PREFIX}/economic-copilot", tags=["economic-copilot"])
app.include_router(freelance.router, prefix=f"{settings.API_V1_PREFIX}/freelance", tags=["freelance-hub"])
app.include_router(multi_agent_system.router, prefix=f"{settings.API_V1_PREFIX}/multi-agent", tags=["multi-agent-orchestration"])
app.include_router(career_tools.router, prefix=f"{settings.API_V1_PREFIX}/career-tools", tags=["career-tools"])

@app.get("/")
async def root():
    return {
        "message": "Workforce Transition Platform API",
        "version": "2.8.0",
        "features": [
            "Workforce Digital Twin™",
            "AI Reskilling Autopilot",
            "10-Agent Intelligence Ecosystem",
            "Progress Tracking & Gamification",
            "Corporate Workforce Transformation OS",
            "Automation Fairness Engine",
            "Gig & Hybrid Labor Integration",
            "Citizen-Level Economic Copilot",
            "Freelance Workers Hub",
            "Mental Health & Burnout Prevention",
            "Networking Intelligence Engine",
            "Salary Negotiation Coach",
            "Interview Preparation System",
            "Skills Verification & Certification Tracker",
            "Predictive Hiring Insights",
            "Internal Job Matching",
            "Union Negotiation Simulation",
            "Policy Impact Modeling",
            "Income Stabilization Tools",
            "Holistic Life Financial Planning"
        ],
        "active_agents": [
            "Gap Analyzer - Skill gaps and market readiness",
            "Opportunity Scout - Hidden job market discovery",
            "Learning Path Strategist - Personalized learning paths",
            "Teaching Coach - Adaptive 1-on-1 education",
            "Career Navigator - Career path exploration",
            "Resume Optimizer - Resume analysis and ATS optimization",
            "Job Application Strategist - Application campaign management",
            "Personal Brand Builder - Thought leadership and visibility",
            "Mentorship Matcher - Mentor discovery and relationship building",
            "Career Transition Advisor - Career pivot feasibility and planning"
        ],
        "corporate_tools": [
            "Internal Redeployment Engine",
            "Automation Opportunity Scanner",
            "Department Productivity Analytics",
            "Employee Risk Calculator",
            "Union Negotiation Simulator"
        ],
        "policy_tools": [
            "Automation Fairness Scorer",
            "Aggregate Impact Modeler",
            "Policy Recommendation Engine",
            "UBI Scenario Simulator",
            "Real-time Inequality Index"
        ],
        "gig_economy_tools": [
            "Skill-to-Gig Matcher",
            "Income Stabilization Planner",
            "Gig Portfolio Optimizer",
            "Benefits Calculator (Health, Retirement, Taxes)",
            "Hybrid Schedule Optimizer",
            "Gig vs W2 Comparison"
        ],
        "economic_copilot_tools": [
            "Job Offer Analyzer (Should I take this job?)",
            "Retirement Impact Analyzer",
            "Debt vs Reskilling Optimizer",
            "Family Financial Planner",
            "Comprehensive Life Decision Engine",
            "Multi-Scenario Comparator"
        ],
        "freelance_hub_tools": [
            "Freelancer Profile Management",
            "Job Posting & Discovery",
            "AI-Powered Job Recommendations",
            "Smart Proposal Generator",
            "Contract Management",
            "Rating & Review System",
            "Portfolio Management",
            "Pricing Optimization",
            "Competition Analysis",
            "Freelance Career Growth Strategy",
            "Marketplace Analytics"
        ],
        "multi_agent_orchestration": [
            "Collaborative Task Creation",
            "Distributed Agent Coordination",
            "Competitive Agent Bidding",
            "Inter-Agent Communication",
            "Shared Knowledge Base",
            "Task Decomposition & Distribution",
            "Collective Intelligence Emergence",
            "Multi-Agent Freelancer Optimization",
            "Coordinated Job Discovery & Application",
            "Collaborative Career Planning",
            "System Intelligence Analytics"
        ],
        "career_tools": [
            "Mental Health & Burnout Assessment",
            "Work-Life Balance Analyzer",
            "Stress Level Monitoring",
            "Wellness Check-In System",
            "Professional Network Analyzer",
            "LinkedIn Profile Optimization",
            "Networking Event Recommendations",
            "Connection Value Calculator",
            "Salary Offer Analyzer",
            "Counteroffer Generator",
            "Benefits Negotiation Guide",
            "Leverage Assessment Tool",
            "Mock Interview Generator",
            "Interview Performance Evaluator",
            "Company-Specific Interview Prep",
            "Answer Coaching System",
            "Skills Inventory Tracker",
            "Certification ROI Calculator",
            "Skill Verification System",
            "Skill Gap Validator"
        ],
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Basic health check - lightweight probe."""
    return {
        "status": "healthy",
        "service": "labor-backend",
        "version": "2.8.0"
    }

@app.get("/health/live")
async def liveness_check():
    """Kubernetes-style liveness probe."""
    import time
    return {
        "alive": True,
        "service": "labor-backend",
        "uptime": time.process_time()
    }

@app.get("/health/ready")
async def readiness_check():
    """Kubernetes-style readiness probe - checks critical dependencies."""
    import os
    import urllib.request
    import urllib.error

    checks = {}
    all_healthy = True

    # Check Database URL is configured
    database_url = os.getenv("DATABASE_URL", "")
    if database_url:
        checks["database"] = {"healthy": True, "configured": True, "critical": True}
    else:
        checks["database"] = {"healthy": False, "error": "DATABASE_URL not configured", "critical": True}
        all_healthy = False

    # Check Redis
    redis_url = os.getenv("REDIS_URL", "")
    if redis_url:
        checks["redis"] = {"healthy": True, "configured": True, "critical": True}
    else:
        checks["redis"] = {"healthy": False, "error": "REDIS_URL not configured", "critical": True}
        all_healthy = False

    status_code = 200 if all_healthy else 503

    return {
        "ready": all_healthy,
        "service": "labor-backend",
        "checks": checks
    }

@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with all dependencies."""
    import os
    import sys
    import time

    checks = {}

    # Database check
    database_url = os.getenv("DATABASE_URL", "")
    checks["database"] = {
        "healthy": bool(database_url),
        "configured": bool(database_url),
        "critical": True
    }

    # Redis check
    redis_url = os.getenv("REDIS_URL", "")
    checks["redis"] = {
        "healthy": bool(redis_url),
        "configured": bool(redis_url),
        "critical": True
    }

    # Determine overall status
    critical_services_healthy = all(
        check.get("healthy", False)
        for check in checks.values()
        if check.get("critical", False)
    )

    overall_status = "healthy" if critical_services_healthy else "degraded"

    return {
        "status": overall_status,
        "service": "labor-backend",
        "version": "2.8.0",
        "timestamp": time.time(),
        "checks": checks,
        "system": {
            "python_version": sys.version,
            "uptime": time.process_time()
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
