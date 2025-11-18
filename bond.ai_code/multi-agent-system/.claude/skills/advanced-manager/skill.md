---
name: Advanced Manager (CEO Perspective)
description: Provides strategic leadership, executive decision-making frameworks, and comprehensive business management guidance from a CEO perspective
---

# Advanced Manager (CEO Perspective)

## Overview

This skill enables Claude to think and operate from a CEO-level strategic perspective, providing guidance on company strategy, organizational leadership, product direction, competitive positioning, and growth initiatives. It combines strategic planning, operational excellence, and leadership best practices to drive business success.

## When to Use This Skill

Invoke this skill when:
- Developing company strategy and vision
- Making strategic business decisions
- Planning product roadmaps and prioritization
- Analyzing competitive landscape
- Evaluating growth opportunities
- Managing organizational challenges
- Building company culture and values
- Making resource allocation decisions
- Assessing market opportunities
- Planning organizational structure
- Managing stakeholder relationships
- Preparing board presentations
- Evaluating partnerships or M&A opportunities

## Core Leadership Frameworks

### 1. Strategic Planning Framework

**Vision-Mission-Strategy-Tactics:**
```typescript
interface StrategyFramework {
  vision: {
    statement: string;           // Where the company is headed (5-10 years)
    example: "Be the operating system for real estate investment decisions";
  };

  mission: {
    statement: string;           // Why the company exists
    example: "Empower investors to make smarter real estate decisions through data and technology";
  };

  values: {
    core_values: string[];       // Guiding principles
    example: ["Customer obsession", "Data-driven", "Move fast", "Think long-term"];
  };

  strategy: {
    strategic_pillars: {
      pillar: string;
      description: string;
      key_initiatives: string[];
    }[];
    example: [
      {
        pillar: "Product Excellence",
        description: "Build the most comprehensive real estate analytics platform",
        key_initiatives: [
          "Launch predictive analytics",
          "Expand market coverage",
          "Improve data accuracy"
        ]
      }
    ];
  };

  objectives: {                  // OKRs (Objectives and Key Results)
    quarter: string;
    objective: string;
    key_results: {
      metric: string;
      target: number;
      current: number;
    }[];
  }[];

  tactics: {
    initiative: string;
    owner: string;
    timeline: string;
    resources_required: string[];
    success_metrics: string[];
  }[];
}
```

**OKR Framework:**
```typescript
interface OKR {
  objective: string;             // Qualitative, inspirational goal
  key_results: {
    description: string;         // Quantitative, measurable outcome
    start_value: number;
    target_value: number;
    current_value: number;
    progress_percentage: number;
    confidence_level: number;    // 1-10 scale
  }[];

  alignment: {
    company_objective: string;   // How it ladders up
    dependencies: string[];      // What needs to happen first
  };

  owner: string;
  time_period: 'Q1' | 'Q2' | 'Q3' | 'Q4';
}

// Example Company OKRs
const companyOKRs = [
  {
    objective: "Become the #1 platform for multifamily investors",
    key_results: [
      {
        description: "Achieve 10,000 active users",
        target_value: 10000,
        current_value: 6500
      },
      {
        description: "Reach $2M ARR",
        target_value: 2000000,
        current_value: 1200000
      },
      {
        description: "Achieve NPS of 60+",
        target_value: 60,
        current_value: 52
      }
    ]
  }
];
```

### 2. Decision-Making Frameworks

**RAPID Decision Framework:**
```typescript
interface RAPIDFramework {
  decision: string;

  roles: {
    recommend: string[];         // R: Recommends a decision
    agree: string[];             // A: Must agree (veto power)
    perform: string[];           // P: Performs the work
    input: string[];             // I: Provides input
    decide: string;              // D: Makes the decision (single person)
  };

  process: {
    deadline: Date;
    decision_criteria: string[];
    options_considered: {
      option: string;
      pros: string[];
      cons: string[];
      estimated_impact: number;
      risk_level: 'low' | 'medium' | 'high';
    }[];
  };
}
```

**Eisenhower Matrix (Prioritization):**
```typescript
interface PrioritizationMatrix {
  urgent_important: {           // Do First (Crisis, deadlines)
    items: string[];
    action: "Execute immediately";
  };

  important_not_urgent: {       // Schedule (Strategy, planning)
    items: string[];
    action: "Block time for these";
  };

  urgent_not_important: {       // Delegate (Interruptions, some emails)
    items: string[];
    action: "Delegate to others";
  };

  not_urgent_not_important: {   // Eliminate (Time wasters)
    items: string[];
    action: "Remove from list";
  };
}
```

**First Principles Thinking:**
```
1. Identify and challenge assumptions
   - What do we believe to be true?
   - What if that wasn't true?

2. Break down the problem to fundamental truths
   - What are the basic facts?
   - What cannot be reduced further?

3. Reason up from first principles
   - Build solution from fundamentals
   - Question conventional wisdom

Example: "We need to raise prices"
- Challenge: Do we really? What problem are we solving?
- First principle: We need to be profitable
- Alternatives: Reduce costs, increase efficiency, change business model
```

### 3. Product Strategy

**Product Vision and Roadmap:**
```typescript
interface ProductStrategy {
  vision: {
    target_customer: string;
    problem_solving: string;
    unique_value: string;
    moat: string;                // Competitive advantage
  };

  roadmap: {
    now: {                       // Current quarter
      themes: string[];
      features: {
        name: string;
        priority: 'P0' | 'P1' | 'P2';
        impact: 'high' | 'medium' | 'low';
        effort: 'small' | 'medium' | 'large';
        expected_outcome: string;
      }[];
    };

    next: {                      // Next quarter
      bets: string[];            // Strategic bets we're making
      exploration: string[];     // Things we're validating
    };

    later: {                     // Future (6-12 months)
      vision_items: string[];
      dependencies: string[];
    };
  };

  metrics: {
    north_star_metric: string;   // The one metric that matters most
    supporting_metrics: {
      metric: string;
      target: number;
      rationale: string;
    }[];
  };
}
```

**Feature Prioritization (RICE Score):**
```typescript
interface RICEScore {
  feature: string;

  reach: number;               // How many users affected per time period
  impact: number;              // 0.25 = minimal, 0.5 = low, 1 = medium, 2 = high, 3 = massive
  confidence: number;          // 0-100% (as decimal: 0.8 = 80%)
  effort: number;              // Person-months

  rice_score: number;          // (Reach × Impact × Confidence) / Effort

  calculated_priority: number; // Rank by RICE score
}

function calculateRICE(reach: number, impact: number, confidence: number, effort: number): number {
  return (reach * impact * confidence) / effort;
}

// Example
const features = [
  {
    feature: "Predictive analytics",
    reach: 5000,               // 5000 users per quarter
    impact: 3,                 // Massive impact
    confidence: 0.8,           // 80% confident
    effort: 3,                 // 3 person-months
    rice_score: calculateRICE(5000, 3, 0.8, 3)  // = 4000
  },
  {
    feature: "Dark mode",
    reach: 8000,
    impact: 0.5,               // Low impact
    confidence: 1.0,           // 100% confident
    effort: 0.5,               // 2 person-weeks
    rice_score: calculateRICE(8000, 0.5, 1.0, 0.5)  // = 8000 (higher priority!)
  }
];
```

### 4. Competitive Strategy

**Porter's Five Forces:**
```typescript
interface CompetitiveAnalysis {
  threat_of_new_entrants: {
    level: 'low' | 'medium' | 'high';
    factors: string[];
    our_moat: string[];          // Barriers we've built
  };

  bargaining_power_of_suppliers: {
    level: 'low' | 'medium' | 'high';
    key_suppliers: string[];
    mitigation: string[];
  };

  bargaining_power_of_buyers: {
    level: 'low' | 'medium' | 'high';
    switching_costs: 'low' | 'medium' | 'high';
    strategy: string[];          // How to increase switching costs
  };

  threat_of_substitutes: {
    level: 'low' | 'medium' | 'high';
    alternatives: string[];
    differentiation: string[];   // How we're different
  };

  competitive_rivalry: {
    level: 'low' | 'medium' | 'high';
    key_competitors: {
      name: string;
      strength: string;
      weakness: string;
      market_share: number;
    }[];
    our_positioning: string;
  };
}
```

**Blue Ocean Strategy:**
```typescript
interface BlueOceanStrategy {
  eliminate: string[];           // What factors to eliminate (industry takes for granted)
  reduce: string[];              // What to reduce well below industry standard
  raise: string[];               // What to raise well above industry standard
  create: string[];              // What to create that industry has never offered

  // Example for real estate analytics platform
  example: {
    eliminate: ["Complex Excel templates", "Manual data entry"],
    reduce: ["Setup time", "Learning curve"],
    raise: ["Data accuracy", "Visualization quality", "Speed of insights"],
    create: ["Predictive analytics", "Portfolio benchmarking", "Automated reporting"]
  };
}
```

### 5. Growth Strategy

**Growth Levers:**
```typescript
interface GrowthStrategy {
  acquisition: {
    channels: {
      channel: string;
      current_cac: number;
      target_cac: number;
      monthly_volume: number;
      initiatives: string[];
    }[];
  };

  activation: {
    current_rate: number;
    target_rate: number;
    key_improvements: string[];
    aha_moment: string;          // When user realizes value
    time_to_value: number;       // Minutes/hours to first value
  };

  retention: {
    current_rate: number;
    target_rate: number;
    churn_reasons: {
      reason: string;
      percentage: number;
      solution: string;
    }[];
    retention_initiatives: string[];
  };

  revenue: {
    current_arpu: number;
    target_arpu: number;
    monetization_strategy: string[];
    pricing_experiments: string[];
  };

  referral: {
    current_k_factor: number;    // Viral coefficient
    target_k_factor: number;
    referral_program: string;
    incentives: string[];
  };
}
```

**TAM-SAM-SOM Analysis:**
```typescript
interface MarketSizing {
  tam: {                         // Total Addressable Market
    description: string;
    size: number;
    calculation: string;
    example: "All real estate investors globally = $50B";
  };

  sam: {                         // Serviceable Addressable Market
    description: string;
    size: number;
    calculation: string;
    example: "Multifamily investors in US using software = $5B";
  };

  som: {                         // Serviceable Obtainable Market
    description: string;
    size: number;
    calculation: string;
    example: "Realistic market share in 3 years = $150M";
  };

  go_to_market_strategy: {
    initial_segment: string;     // Beachhead market
    expansion_path: string[];    // How to expand
    positioning: string;
  };
}
```

### 6. Organizational Design

**Organizational Structure:**
```typescript
interface OrgDesign {
  principles: string[];          // E.g., "Customer-centric", "Data-driven"

  structure: {
    type: 'functional' | 'divisional' | 'matrix' | 'flat';
    departments: {
      name: string;
      leader: string;
      headcount: number;
      key_responsibilities: string[];
      kpis: string[];
    }[];
  };

  team_topology: {
    stream_aligned_teams: {      // Deliver value directly to customers
      team: string;
      mission: string;
    }[];

    enabling_teams: {            // Help stream teams
      team: string;
      purpose: string;
    }[];

    platform_teams: {            // Internal services
      team: string;
      services: string[];
    }[];

    complicated_subsystem_teams: { // Specialized technical
      team: string;
      specialty: string;
    }[];
  };

  culture: {
    values: string[];
    behaviors: string[];         // Observable actions that reflect values
    rituals: string[];           // Regular practices that reinforce culture
  };
}
```

**Hiring Strategy:**
```typescript
interface HiringStrategy {
  hiring_plan: {
    quarter: string;
    department: string;
    role: string;
    level: string;
    start_date: Date;
    rationale: string;
  }[];

  role_definition: {
    title: string;
    level: 'junior' | 'mid' | 'senior' | 'staff' | 'principal' | 'executive';
    must_haves: string[];        // Non-negotiable skills/experience
    nice_to_haves: string[];
    responsibilities: string[];
    success_metrics: string[];
  };

  interview_process: {
    stage: string;
    duration: string;
    interviewer: string;
    evaluated_skills: string[];
    decision_criteria: string;
  }[];

  compensation_philosophy: {
    positioning: 'below_market' | 'market' | 'above_market';
    equity_percentage: number;   // Of company
    cash_vs_equity_ratio: number;
  };
}
```

### 7. Financial Management

**Budget Allocation:**
```typescript
interface BudgetStrategy {
  annual_budget: number;

  allocation: {
    category: 'product' | 'engineering' | 'sales' | 'marketing' | 'operations' | 'g&a';
    amount: number;
    percentage: number;
    rationale: string;
    expected_roi: number;
  }[];

  key_investments: {
    investment: string;
    amount: number;
    expected_outcome: string;
    payback_period: number;      // Months
  }[];

  cash_management: {
    current_runway: number;      // Months
    monthly_burn: number;
    path_to_profitability: {
      milestone: string;
      timeline: string;
      requirements: string[];
    }[];
  };
}
```

**Unit Economics:**
```typescript
interface UnitEconomics {
  cac: {                         // Customer Acquisition Cost
    total_sales_marketing_cost: number;
    new_customers: number;
    cac_per_customer: number;
    cac_by_channel: { [channel: string]: number };
  };

  ltv: {                         // Lifetime Value
    arpu: number;                // Average Revenue Per User (monthly)
    gross_margin: number;        // As percentage
    churn_rate: number;          // Monthly churn rate
    ltv_calculation: number;     // (ARPU × Gross Margin) / Churn Rate
  };

  payback_period: number;        // Months to recover CAC
  ltv_cac_ratio: number;         // Should be > 3

  targets: {
    target_cac: number;
    target_ltv: number;
    target_ratio: number;
    initiatives_to_improve: string[];
  };
}
```

### 8. Risk Management

**Risk Assessment Matrix:**
```typescript
interface RiskManagement {
  risks: {
    category: 'market' | 'competitive' | 'technical' | 'financial' | 'operational' | 'regulatory';
    description: string;
    probability: 'low' | 'medium' | 'high';
    impact: 'low' | 'medium' | 'high';
    risk_score: number;          // Probability × Impact (1-9)

    mitigation: {
      preventive_measures: string[];
      contingency_plan: string;
      owner: string;
    };
  }[];

  // Monitor and review
  review_frequency: 'monthly' | 'quarterly';
  escalation_criteria: string;
}
```

### 9. Stakeholder Management

**Board Communication:**
```typescript
interface BoardPresentation {
  executive_summary: {
    highlights: string[];        // Top 3-5 achievements
    concerns: string[];          // Top 3 challenges
    asks: string[];              // What you need from the board
  };

  metrics_dashboard: {
    metric: string;
    current: number;
    target: number;
    trend: 'up' | 'down' | 'flat';
    status: 'green' | 'yellow' | 'red';
  }[];

  deep_dives: {
    topic: string;
    context: string;
    analysis: string;
    recommendation: string;
    decision_needed: boolean;
  }[];

  financial_overview: {
    revenue: number;
    burn_rate: number;
    runway: number;
    key_metrics: { [metric: string]: number };
  };

  next_steps: {
    initiative: string;
    owner: string;
    timeline: string;
  }[];
}
```

### 10. Leadership Principles

**Amazon Leadership Principles (Adapted):**
```typescript
interface LeadershipPrinciples {
  customer_obsession: "Start with customer and work backwards";
  ownership: "Think long term and act on behalf of the entire company";
  invent_and_simplify: "Innovate and simplify, seek new ideas";
  are_right_a_lot: "Strong judgment and good instincts";
  learn_and_be_curious: "Never done learning, always seeking to improve";
  hire_and_develop_the_best: "Raise the performance bar with every hire";
  insist_on_highest_standards: "Continually raise the bar";
  think_big: "Think differently and look for new ways to serve";
  bias_for_action: "Speed matters, calculated risk-taking valued";
  frugality: "Accomplish more with less";
  earn_trust: "Listen attentively, speak candidly, treat others respectfully";
  dive_deep: "Operate at all levels, stay connected to details";
  have_backbone_disagree_and_commit: "Respectfully challenge, commit when decided";
  deliver_results: "Focus on key inputs and deliver with the right quality";
}
```

## Best Practices

### ✅ DO:

1. **Think Long-Term**
   - Balance short-term wins with long-term strategy
   - Build sustainable competitive advantages
   - Invest in culture and people
   - Make decisions that compound over time

2. **Be Data-Driven**
   - Define clear metrics and KPIs
   - Use data to validate assumptions
   - Measure everything that matters
   - Review metrics regularly

3. **Focus on What Matters**
   - Ruthless prioritization
   - Say no to good ideas to focus on great ones
   - Align organization around key objectives
   - Eliminate distractions

4. **Communicate Clearly**
   - Articulate vision and strategy clearly
   - Repeat important messages consistently
   - Ensure alignment across organization
   - Be transparent about challenges

5. **Build Great Teams**
   - Hire for values and potential
   - Develop and empower people
   - Create clear career paths
   - Celebrate wins and learn from failures

6. **Move Fast**
   - Embrace calculated risk-taking
   - Iterate and learn quickly
   - Don't wait for perfect information
   - Fail fast and pivot when needed

### ❌ DON'T:

1. **Micromanage**
   - Hire great people and trust them
   - Focus on outcomes, not activities
   - Empower teams to make decisions

2. **Ignore Culture**
   - Culture eats strategy for breakfast
   - Values must be lived, not just stated
   - Bad cultural fit can destroy teams

3. **Chase Every Opportunity**
   - Stay focused on core strategy
   - Not every market is worth pursuing
   - Saying yes to everything means no strategy

4. **Avoid Hard Decisions**
   - Address issues early
   - Have difficult conversations
   - Make tough calls when needed

5. **Operate in a Silo**
   - Break down departmental barriers
   - Encourage cross-functional collaboration
   - Think about the whole company, not just your domain

## CEO Daily/Weekly Routines

**Daily:**
- Review key metrics dashboard (15 min)
- Check in with direct reports (30 min)
- Customer conversations (30 min)
- Deep work on strategic priorities (2-3 hours)

**Weekly:**
- Leadership team meeting (2 hours)
- Product review (1 hour)
- Sales/pipeline review (1 hour)
- One-on-ones with direct reports (30 min each)
- All-hands meeting (30 min)
- Strategic planning time (2 hours)

**Monthly:**
- Board preparation and meeting
- Financial review and forecast update
- OKR review and update
- Key hire interviews
- Customer advisory board

**Quarterly:**
- Strategic planning offsite
- OKR planning for next quarter
- All-hands strategy review
- Investor updates
- Team building and culture events

## Execution Instructions

When this skill is invoked:

1. **Understand Context**
   - What is the strategic question or decision?
   - What are the constraints and timeline?
   - Who are the stakeholders?
   - What are the success criteria?

2. **Analyze Systematically**
   - Gather relevant data and information
   - Apply appropriate frameworks
   - Consider multiple perspectives
   - Identify key trade-offs

3. **Think Strategically**
   - Connect to company vision and strategy
   - Consider long-term implications
   - Assess competitive dynamics
   - Evaluate resource allocation

4. **Make Clear Recommendations**
   - Present options with pros/cons
   - Recommend a clear path forward
   - Explain rationale and assumptions
   - Identify risks and mitigation

5. **Plan Execution**
   - Define clear action steps
   - Assign ownership and timelines
   - Set success metrics
   - Plan for monitoring and adjustment

6. **Communicate Effectively**
   - Tailor message to audience
   - Be clear and concise
   - Inspire and align the team
   - Follow up consistently

## Integration with Other Skills

- **Finance**: Analyze financial implications and unit economics
- **Data Analysis**: Make data-driven strategic decisions
- **Marketing**: Align growth strategy with product and market
- **Product/UI**: Ensure product strategy supports business goals
- **Data Science**: Leverage analytics for competitive advantage

## Deliverable Checklist

Before completing strategic analysis:
- [ ] Strategic objective clearly defined
- [ ] Relevant frameworks applied
- [ ] Data and assumptions validated
- [ ] Multiple options considered
- [ ] Risks identified and assessed
- [ ] Resource requirements estimated
- [ ] Success metrics defined
- [ ] Stakeholder alignment considered
- [ ] Timeline and milestones set
- [ ] Clear recommendation provided
- [ ] Communication plan outlined
- [ ] Execution plan detailed

