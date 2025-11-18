-- Seed Data for Advanced Features
-- Adds example decision templates, report templates, and industry insights

-- ============================================
-- DECISION TEMPLATES
-- ============================================

-- Product Launch Decision Template
INSERT INTO decision_templates (
  name, description, category, decision_context,
  recommended_agents, template_data, is_public
) VALUES (
  'Product Launch Decision Framework',
  'Comprehensive framework for deciding whether and when to launch a new product',
  'product',
  'STRATEGIC_PLANNING',
  ARRAY['jobs', 'musk', 'bezos', 'zuckerberg'],
  '{
    "questions": [
      {"id": "q1", "question": "What problem does this product solve?", "type": "text", "required": true},
      {"id": "q2", "question": "Who is the target customer?", "type": "text", "required": true},
      {"id": "q3", "question": "What is the estimated market size?", "type": "number", "unit": "dollars", "required": true},
      {"id": "q4", "question": "What is the competitive landscape?", "type": "textarea", "required": true},
      {"id": "q5", "question": "What are the key features?", "type": "list", "required": true},
      {"id": "q6", "question": "What is the proposed timeline?", "type": "date_range", "required": true},
      {"id": "q7", "question": "What is the budget?", "type": "number", "unit": "dollars", "required": true},
      {"id": "q8", "question": "What are the biggest risks?", "type": "list", "required": true}
    ],
    "criteria": [
      {"name": "Market Opportunity", "weight": 0.25},
      {"name": "Technical Feasibility", "weight": 0.2},
      {"name": "Competitive Advantage", "weight": 0.2},
      {"name": "Resource Availability", "weight": 0.15},
      {"name": "Strategic Fit", "weight": 0.2}
    ],
    "outcomes": ["Launch Q4 2025", "Launch Q1 2026", "Delay indefinitely", "Kill the project"],
    "follow_up_period_days": 90
  }'::jsonb,
  true
);

-- Hiring Decision Template
INSERT INTO decision_templates (
  name, description, category, decision_context,
  recommended_agents, template_data, is_public
) VALUES (
  'Executive Hiring Framework',
  'Framework for making critical hiring decisions for senior positions',
  'hiring',
  'TEAM_BUILDING',
  ARRAY['jobs', 'bezos', 'fink'],
  '{
    "questions": [
      {"id": "q1", "question": "What is the role?", "type": "text", "required": true},
      {"id": "q2", "question": "What are the must-have qualifications?", "type": "list", "required": true},
      {"id": "q3", "question": "What are the nice-to-have qualifications?", "type": "list", "required": false},
      {"id": "q4", "question": "Candidate previous companies", "type": "list", "required": true},
      {"id": "q5", "question": "Candidate key achievements", "type": "textarea", "required": true},
      {"id": "q6", "question": "Cultural fit assessment", "type": "rating", "max": 10, "required": true},
      {"id": "q7", "question": "Salary expectations", "type": "number", "unit": "dollars", "required": true},
      {"id": "q8", "question": "Start date availability", "type": "date", "required": true}
    ],
    "criteria": [
      {"name": "Experience & Skills", "weight": 0.3},
      {"name": "Cultural Fit", "weight": 0.25},
      {"name": "Leadership Ability", "weight": 0.2},
      {"name": "Growth Potential", "weight": 0.15},
      {"name": "Compensation Fit", "weight": 0.1}
    ],
    "outcomes": ["Hire immediately", "Hire after negotiation", "Keep in pipeline", "Reject"],
    "follow_up_period_days": 180
  }'::jsonb,
  true
);

-- Investment Decision Template
INSERT INTO decision_templates (
  name, description, category, decision_context,
  recommended_agents, template_data, is_public
) VALUES (
  'Investment Opportunity Evaluation',
  'Comprehensive framework for evaluating investment opportunities',
  'investment',
  'OPPORTUNITY_EVALUATION',
  ARRAY['fink', 'zell', 'bren'],
  '{
    "questions": [
      {"id": "q1", "question": "Investment type", "type": "select", "options": ["Stock", "Real Estate", "Startup", "Bond", "Other"], "required": true},
      {"id": "q2", "question": "Investment amount", "type": "number", "unit": "dollars", "required": true},
      {"id": "q3", "question": "Expected return", "type": "percentage", "required": true},
      {"id": "q4", "question": "Investment timeline", "type": "text", "required": true},
      {"id": "q5", "question": "Risk assessment", "type": "rating", "max": 10, "required": true},
      {"id": "q6", "question": "Liquidity needs", "type": "text", "required": true},
      {"id": "q7", "question": "Market conditions", "type": "textarea", "required": true},
      {"id": "q8", "question": "Alternative investments considered", "type": "list", "required": false}
    ],
    "criteria": [
      {"name": "Expected Returns", "weight": 0.3},
      {"name": "Risk Level", "weight": 0.25},
      {"name": "Liquidity", "weight": 0.15},
      {"name": "Market Timing", "weight": 0.15},
      {"name": "Diversification", "weight": 0.15}
    ],
    "outcomes": ["Invest full amount", "Invest partial amount", "Wait for better terms", "Decline"],
    "follow_up_period_days": 365
  }'::jsonb,
  true
);

-- M&A Decision Template
INSERT INTO decision_templates (
  name, description, category, decision_context,
  recommended_agents, template_data, is_public
) VALUES (
  'Merger & Acquisition Analysis',
  'Framework for evaluating potential acquisitions',
  'acquisition',
  'ACQUISITION',
  ARRAY['musk', 'bezos', 'fink', 'zuckerberg'],
  '{
    "questions": [
      {"id": "q1", "question": "Target company name", "type": "text", "required": true},
      {"id": "q2", "question": "Target valuation", "type": "number", "unit": "dollars", "required": true},
      {"id": "q3", "question": "Annual revenue", "type": "number", "unit": "dollars", "required": true},
      {"id": "q4", "question": "Growth rate (YoY)", "type": "percentage", "required": true},
      {"id": "q5", "question": "Strategic fit", "type": "textarea", "required": true},
      {"id": "q6", "question": "Technology/IP assets", "type": "textarea", "required": true},
      {"id": "q7", "question": "Team quality", "type": "rating", "max": 10, "required": true},
      {"id": "q8", "question": "Integration complexity", "type": "rating", "max": 10, "required": true},
      {"id": "q9", "question": "Cultural alignment", "type": "rating", "max": 10, "required": true}
    ],
    "criteria": [
      {"name": "Strategic Value", "weight": 0.3},
      {"name": "Financial Performance", "weight": 0.25},
      {"name": "Technology/IP", "weight": 0.2},
      {"name": "Team Quality", "weight": 0.15},
      {"name": "Integration Risk", "weight": 0.1}
    ],
    "outcomes": ["Acquire at asking price", "Negotiate lower price", "Strategic partnership instead", "Pass"],
    "follow_up_period_days": 180
  }'::jsonb,
  true
);

-- Crisis Management Template
INSERT INTO decision_templates (
  name, description, category, decision_context,
  recommended_agents, template_data, is_public
) VALUES (
  'Crisis Response Framework',
  'Rapid decision-making framework for crisis situations',
  'crisis',
  'CRISIS_MANAGEMENT',
  ARRAY['musk', 'trump', 'fink', 'zell'],
  '{
    "questions": [
      {"id": "q1", "question": "What is the nature of the crisis?", "type": "textarea", "required": true},
      {"id": "q2", "question": "Severity level", "type": "rating", "max": 10, "required": true},
      {"id": "q3", "question": "Stakeholders impacted", "type": "list", "required": true},
      {"id": "q4", "question": "Immediate risks", "type": "list", "required": true},
      {"id": "q5", "question": "Available resources", "type": "textarea", "required": true},
      {"id": "q6", "question": "Timeline for response", "type": "text", "required": true},
      {"id": "q7", "question": "Communication plan needed?", "type": "boolean", "required": true},
      {"id": "q8", "question": "Legal/regulatory considerations", "type": "textarea", "required": false}
    ],
    "criteria": [
      {"name": "Urgency", "weight": 0.35},
      {"name": "Impact Severity", "weight": 0.3},
      {"name": "Resource Availability", "weight": 0.15},
      {"name": "Stakeholder Concerns", "weight": 0.2}
    ],
    "outcomes": ["Immediate action", "Prepare and execute", "Monitor closely", "Limited intervention"],
    "follow_up_period_days": 30
  }'::jsonb,
  true
);

-- Market Expansion Template
INSERT INTO decision_templates (
  name, description, category, decision_context,
  recommended_agents, template_data, is_public
) VALUES (
  'Market Expansion Strategy',
  'Framework for evaluating new market entry opportunities',
  'expansion',
  'MARKET_EXPANSION',
  ARRAY['bezos', 'zuckerberg', 'musk'],
  '{
    "questions": [
      {"id": "q1", "question": "Target market/geography", "type": "text", "required": true},
      {"id": "q2", "question": "Market size estimate", "type": "number", "unit": "dollars", "required": true},
      {"id": "q3", "question": "Competition analysis", "type": "textarea", "required": true},
      {"id": "q4", "question": "Required investment", "type": "number", "unit": "dollars", "required": true},
      {"id": "q5", "question": "Time to profitability", "type": "text", "required": true},
      {"id": "q6", "question": "Regulatory barriers", "type": "textarea", "required": true},
      {"id": "q7", "question": "Local partnerships needed?", "type": "boolean", "required": true},
      {"id": "q8", "question": "Product/service adaptation needed", "type": "textarea", "required": false}
    ],
    "criteria": [
      {"name": "Market Potential", "weight": 0.3},
      {"name": "Competitive Position", "weight": 0.25},
      {"name": "Investment Required", "weight": 0.2},
      {"name": "Regulatory Risk", "weight": 0.15},
      {"name": "Strategic Fit", "weight": 0.1}
    ],
    "outcomes": ["Expand immediately", "Pilot program first", "Partner for entry", "Defer expansion"],
    "follow_up_period_days": 180
  }'::jsonb,
  true
);

-- ============================================
-- REPORT TEMPLATES
-- ============================================

-- Executive Summary Report
INSERT INTO report_templates (
  name, report_type, template_config, is_public
) VALUES (
  'Monthly Executive Summary',
  'executive_summary',
  '{
    "sections": [
      {
        "name": "Key Decisions Made",
        "type": "decision_summary",
        "config": {"limit": 10, "sort": "date_desc"}
      },
      {
        "name": "Top Performing Agents",
        "type": "agent_rankings",
        "config": {"metric": "success_rate", "limit": 5}
      },
      {
        "name": "Consultation Volume",
        "type": "chart",
        "config": {"chart_type": "line", "metric": "consultations_count"}
      },
      {
        "name": "Decision Outcomes",
        "type": "outcomes_analysis",
        "config": {"show_roi": true, "show_success_rate": true}
      },
      {
        "name": "Recommendations",
        "type": "insights",
        "config": {"auto_generate": true}
      }
    ],
    "format": "pdf",
    "include_charts": true,
    "date_range": "last_30_days"
  }'::jsonb,
  true
);

-- Agent Performance Report
INSERT INTO report_templates (
  name, report_type, template_config, is_public
) VALUES (
  'Agent Performance Analysis',
  'agent_performance',
  '{
    "sections": [
      {
        "name": "Overall Metrics",
        "type": "agent_metrics_summary",
        "config": {"include_all_agents": true}
      },
      {
        "name": "Success Rate by Context",
        "type": "success_by_context",
        "config": {"chart_type": "bar"}
      },
      {
        "name": "User Satisfaction",
        "type": "rating_analysis",
        "config": {"show_trends": true}
      },
      {
        "name": "Most Consulted Agents",
        "type": "usage_rankings",
        "config": {"limit": 8}
      },
      {
        "name": "Comparative Analysis",
        "type": "agent_comparison",
        "config": {"metrics": ["confidence", "success_rate", "avg_rating"]}
      }
    ],
    "format": "pdf",
    "include_charts": true,
    "date_range": "last_90_days"
  }'::jsonb,
  true
);

-- Decision History Report
INSERT INTO report_templates (
  name, report_type, template_config, is_public
) VALUES (
  'Decision History & Outcomes',
  'decision_history',
  '{
    "sections": [
      {
        "name": "Decisions Timeline",
        "type": "timeline",
        "config": {"include_outcomes": true}
      },
      {
        "name": "Success Metrics",
        "type": "success_analysis",
        "config": {"breakdown_by": ["category", "agent", "context"]}
      },
      {
        "name": "ROI Analysis",
        "type": "roi_summary",
        "config": {"show_total": true, "show_by_decision": true}
      },
      {
        "name": "Lessons Learned",
        "type": "insights_collection",
        "config": {"source": "consultation_outcomes"}
      }
    ],
    "format": "pdf",
    "include_charts": true,
    "date_range": "custom"
  }'::jsonb,
  true
);

-- ============================================
-- INDUSTRY INSIGHTS
-- ============================================

-- Technology Industry Insights
INSERT INTO industry_insights (
  industry, insight_type, title, description, supporting_data, confidence_score, source
) VALUES
(
  'technology',
  'trend',
  'AI Adoption Accelerating Across All Sectors',
  'Based on consultation patterns, there is a 300% increase in AI-related strategic decisions compared to last year. Companies are increasingly consulting about AI integration, talent acquisition, and competitive positioning.',
  '{
    "growth_rate": 3.0,
    "key_topics": ["AI integration", "Machine learning talent", "Competitive positioning"],
    "agent_insights": {
      "musk": "First principles approach to AI capabilities assessment",
      "bezos": "Customer-centric AI applications showing highest success",
      "zuckerberg": "Long-term AI infrastructure bets paying off"
    }
  }'::jsonb,
  0.85,
  'derived'
),
(
  'technology',
  'pattern',
  'Speed-to-Market vs. Quality Trade-offs',
  'Analysis of 500+ product launch decisions shows that companies consistently underestimate quality issues when prioritizing speed. Successful launches balanced both with phased rollouts.',
  '{
    "sample_size": 500,
    "success_rate_fast": 0.45,
    "success_rate_balanced": 0.78,
    "recommendation": "Implement phased rollout strategy"
  }'::jsonb,
  0.82,
  'derived'
);

-- Finance Industry Insights
INSERT INTO industry_insights (
  industry, insight_type, title, description, supporting_data, confidence_score, source
) VALUES
(
  'finance',
  'recommendation',
  'Diversification Strategies in Volatile Markets',
  'Based on investment consultations during market volatility, diversified portfolios with 30-40% alternative investments showed 25% better risk-adjusted returns.',
  '{
    "optimal_allocation": {
      "stocks": 0.35,
      "bonds": 0.25,
      "alternatives": 0.35,
      "cash": 0.05
    },
    "performance_improvement": 0.25,
    "volatility_reduction": 0.18
  }'::jsonb,
  0.78,
  'derived'
);

-- Real Estate Industry Insights
INSERT INTO industry_insights (
  industry, insight_type, title, description, supporting_data, confidence_score, source
) VALUES
(
  'real_estate',
  'trend',
  'Mixed-Use Development Outperforming Single-Purpose',
  'Analysis of real estate investment decisions shows mixed-use developments have 40% higher occupancy rates and 30% better ROI than single-purpose buildings.',
  '{
    "occupancy_rate_difference": 0.40,
    "roi_improvement": 0.30,
    "key_success_factors": [
      "Residential + retail combination",
      "Urban locations",
      "Transit-oriented development"
    ]
  }'::jsonb,
  0.75,
  'derived'
);

-- General Business Insights
INSERT INTO industry_insights (
  industry, insight_type, title, description, supporting_data, confidence_score, source
) VALUES
(
  'general',
  'pattern',
  'Data-Driven Decisions Have 65% Higher Success Rate',
  'Consultations that included quantitative data and metrics resulted in significantly better outcomes compared to those based primarily on intuition or qualitative factors.',
  '{
    "success_rate_data_driven": 0.73,
    "success_rate_intuition": 0.44,
    "improvement": 0.65,
    "key_metrics_used": [
      "Market size data",
      "Customer metrics",
      "Financial projections",
      "Competitive benchmarks"
    ]
  }'::jsonb,
  0.88,
  'derived'
);

-- ============================================
-- EXAMPLE WEBHOOKS (for documentation)
-- ============================================

COMMENT ON TABLE webhooks IS 'Example webhook events:
- consultation.completed
- debate.finished
- decision.made
- outcome.reported
- reminder.due
- report.generated
- agent.performance.updated
- team.member.added
';

-- ============================================
-- VIEWS FOR ANALYTICS
-- ============================================

-- Agent performance summary view
CREATE OR REPLACE VIEW agent_performance_summary AS
SELECT
  ba.id,
  ba.agent_key,
  ba.name,
  COUNT(ac.id) as total_consultations,
  AVG(ac.user_rating) as avg_rating,
  AVG(ac.confidence_score) as avg_confidence,
  COUNT(CASE WHEN co.success_level >= 4 THEN 1 END)::decimal /
    NULLIF(COUNT(co.id), 0) as success_rate,
  COUNT(CASE WHEN ac.created_at >= NOW() - INTERVAL '30 days' THEN 1 END) as last_30_days_count
FROM behavior_agents ba
LEFT JOIN agent_consultations ac ON ba.id = ac.agent_id
LEFT JOIN consultation_outcomes co ON ac.id = co.consultation_id
WHERE ba.is_active = true
GROUP BY ba.id, ba.agent_key, ba.name;

-- User engagement summary view
CREATE OR REPLACE VIEW user_engagement_summary AS
SELECT
  u.id,
  u.email,
  u.full_name,
  COUNT(DISTINCT ac.id) as total_conversations,
  COUNT(DISTINCT cons.id) as total_consultations,
  COUNT(DISTINCT di.id) as decisions_made,
  AVG(cons.user_rating) as avg_rating_given,
  MAX(ac.updated_at) as last_activity
FROM users u
LEFT JOIN agent_conversations ac ON u.id = ac.user_id
LEFT JOIN agent_consultations cons ON u.id = cons.user_id
LEFT JOIN decision_instances di ON u.id = di.user_id
GROUP BY u.id, u.email, u.full_name;

-- Decision template usage view
CREATE OR REPLACE VIEW decision_template_usage AS
SELECT
  dt.id,
  dt.name,
  dt.category,
  COUNT(di.id) as times_used,
  AVG(CASE WHEN di.success_rating >= 4 THEN 1.0 ELSE 0.0 END) as success_rate,
  COUNT(CASE WHEN di.created_at >= NOW() - INTERVAL '30 days' THEN 1 END) as last_30_days_usage
FROM decision_templates dt
LEFT JOIN decision_instances di ON dt.id = di.template_id
WHERE dt.is_public = true OR dt.user_id IS NOT NULL
GROUP BY dt.id, dt.name, dt.category;

COMMENT ON VIEW agent_performance_summary IS 'Aggregated agent performance metrics';
COMMENT ON VIEW user_engagement_summary IS 'User engagement and activity metrics';
COMMENT ON VIEW decision_template_usage IS 'Decision template usage and success metrics';
