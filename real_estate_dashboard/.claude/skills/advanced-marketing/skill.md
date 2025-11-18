---
name: Advanced Marketing Expert
description: Develops comprehensive marketing strategies, growth frameworks, and data-driven campaigns for real estate technology products and services
---

# Advanced Marketing Expert

## Overview

This skill enables Claude to develop and execute sophisticated marketing strategies that drive user acquisition, engagement, and retention. It combines growth marketing frameworks, data analytics, content strategy, and conversion optimization to build successful real estate technology brands.

## When to Use This Skill

Invoke this skill when:
- Developing go-to-market strategies
- Planning marketing campaigns
- Optimizing conversion funnels
- Creating content marketing strategies
- Analyzing user acquisition and retention metrics
- Designing growth experiments
- Building brand positioning and messaging
- Implementing SEO and SEM strategies
- Creating email marketing campaigns
- Developing social media strategies
- Planning product launches
- Optimizing landing pages and user onboarding

## Core Marketing Frameworks

### 1. Growth Marketing Funnel (AARRR Metrics)

**Acquisition → Activation → Retention → Revenue → Referral**

```typescript
interface GrowthMetrics {
  acquisition: {
    channels: {
      organic: number;          // SEO, direct traffic
      paid: number;             // PPC, paid social
      referral: number;         // Word of mouth, affiliate
      social: number;           // Social media organic
      email: number;            // Email campaigns
    };
    metrics: {
      traffic: number;          // Total visitors
      cac: number;              // Customer Acquisition Cost
      cpv: number;              // Cost Per Visitor
      uniqueVisitors: number;
    };
  };

  activation: {
    signupRate: number;         // % of visitors who sign up
    timeToValue: number;        // Minutes to first value
    onboardingCompletion: number; // % completing onboarding
    featureAdoption: {
      [feature: string]: number; // % using key features
    };
  };

  retention: {
    dau: number;                // Daily Active Users
    wau: number;                // Weekly Active Users
    mau: number;                // Monthly Active Users
    churnRate: number;          // % churning per period
    retentionCohorts: {
      day1: number;
      day7: number;
      day30: number;
      day90: number;
    };
  };

  revenue: {
    mrr: number;                // Monthly Recurring Revenue
    arr: number;                // Annual Recurring Revenue
    arpu: number;               // Average Revenue Per User
    ltv: number;                // Customer Lifetime Value
    ltvCacRatio: number;        // LTV / CAC (should be > 3)
    paybackPeriod: number;      // Months to recover CAC
  };

  referral: {
    nps: number;                // Net Promoter Score
    viralCoefficient: number;   // K-factor (> 1 = viral)
    referralRate: number;       // % of users who refer
    invitesPerUser: number;
    inviteConversion: number;   // % of invites that convert
  };
}
```

### 2. Marketing Strategy Framework

**Positioning Statement:**
```
For [target customer]
Who [statement of need or opportunity]
Our [product/service name] is a [product category]
That [key benefit, reason to buy]
Unlike [primary competitive alternative]
Our product [statement of primary differentiation]
```

**Example for Real Estate Dashboard:**
```
For real estate investors and property managers
Who need to track portfolio performance and make data-driven investment decisions
Our Real Estate Dashboard is a comprehensive analytics platform
That provides real-time insights, predictive analytics, and automated reporting
Unlike traditional spreadsheets or basic property management software
Our product delivers institutional-grade analytics with an intuitive, modern interface
```

### 3. Content Marketing Strategy

**Content Pillars:**
```typescript
interface ContentStrategy {
  pillars: {
    educational: {
      topics: string[];         // "Real Estate Investing 101", "Cap Rate Explained"
      formats: string[];        // Blog posts, guides, webinars
      goal: 'awareness' | 'consideration';
    };

    thought_leadership: {
      topics: string[];         // Market trends, industry insights
      formats: string[];        // Whitepapers, research reports
      goal: 'authority' | 'trust';
    };

    product_focused: {
      topics: string[];         // Feature highlights, use cases
      formats: string[];        // Case studies, tutorials, demos
      goal: 'consideration' | 'conversion';
    };

    customer_success: {
      topics: string[];         // Success stories, testimonials
      formats: string[];        // Video testimonials, written case studies
      goal: 'conversion' | 'retention';
    };
  };

  seo: {
    targetKeywords: {
      keyword: string;
      searchVolume: number;
      difficulty: number;
      intent: 'informational' | 'navigational' | 'transactional';
    }[];

    contentClusters: {
      pillarPage: string;       // Main comprehensive page
      clusterContent: string[]; // Supporting articles
    }[];
  };
}
```

**Content Calendar:**
```typescript
interface ContentCalendar {
  month: string;
  themes: string[];
  pieces: {
    title: string;
    type: 'blog' | 'video' | 'infographic' | 'guide' | 'case_study';
    pillar: string;
    keywords: string[];
    distribution: string[];     // Channels for distribution
    cta: string;               // Call to action
    publishDate: Date;
  }[];
}
```

### 4. Campaign Planning Framework

**Campaign Structure:**
```typescript
interface MarketingCampaign {
  name: string;
  objective: 'awareness' | 'consideration' | 'conversion' | 'retention';

  targeting: {
    demographics: {
      age?: [number, number];
      income?: [number, number];
      occupation?: string[];
      location?: string[];
    };
    psychographics: {
      interests?: string[];
      behaviors?: string[];
      painPoints?: string[];
    };
    firmographics?: {         // For B2B
      companySize?: string;
      industry?: string[];
      revenue?: [number, number];
    };
  };

  channels: {
    channel: 'email' | 'social' | 'ppc' | 'content' | 'display' | 'seo';
    budget: number;
    expectedReach: number;
    expectedConversion: number;
  }[];

  messaging: {
    headline: string;
    subheadline: string;
    valueProps: string[];
    cta: string;
    socialProof?: string;
  };

  budget: {
    total: number;
    byChannel: { [channel: string]: number };
    cac_target: number;
    roi_target: number;
  };

  timeline: {
    start: Date;
    end: Date;
    milestones: {
      date: Date;
      deliverable: string;
    }[];
  };

  kpis: {
    metric: string;
    target: number;
    actual?: number;
  }[];
}
```

### 5. Conversion Rate Optimization (CRO)

**Landing Page Optimization:**
```tsx
// High-converting landing page structure
const LandingPageTemplate = () => (
  <>
    {/* Hero Section - Above the fold */}
    <Hero>
      <Headline>
        {/* Clear value proposition in < 10 words */}
        Transform Your Real Estate Portfolio Management
      </Headline>
      <Subheadline>
        {/* Expand on value prop, address pain point */}
        Stop wasting hours in spreadsheets. Get real-time insights,
        predictive analytics, and automated reporting in one platform.
      </Subheadline>
      <CTAButton primary size="large">
        Start Free Trial
      </CTAButton>
      <TrustIndicators>
        {/* Social proof */}
        Join 10,000+ investors managing $2B+ in assets
      </TrustIndicators>
      <HeroImage>
        {/* Product screenshot or demo */}
      </HeroImage>
    </Hero>

    {/* Social Proof */}
    <LogoBar>
      {/* Customer logos, press mentions */}
    </LogoBar>

    {/* Features / Benefits */}
    <Features>
      {/* Focus on outcomes, not features */}
      <FeatureCard
        icon={<Chart />}
        title="Make Smarter Investments"
        description="Analyze deals in seconds with AI-powered valuation models"
      />
    </Features>

    {/* How It Works */}
    <HowItWorks>
      {/* 3-step process to reduce perceived complexity */}
    </HowItWorks>

    {/* Testimonials */}
    <Testimonials>
      {/* Video testimonials > written */}
      {/* Include specific results and metrics */}
    </Testimonials>

    {/* Pricing */}
    <Pricing>
      {/* Clear, transparent pricing */}
      {/* Highlight most popular plan */}
    </Pricing>

    {/* FAQ */}
    <FAQ>
      {/* Address common objections */}
    </FAQ>

    {/* Final CTA */}
    <FinalCTA>
      <CTAButton>Start Free Trial - No Credit Card Required</CTAButton>
    </FinalCTA>
  </>
);
```

**CRO Testing Framework:**
```typescript
interface ABTest {
  hypothesis: string;          // "Changing CTA from 'Sign Up' to 'Start Free Trial' will increase conversions"
  variant_a: string;           // Control
  variant_b: string;           // Test
  metric: string;              // Primary metric to measure
  sample_size_required: number; // Statistical significance
  confidence_level: number;    // Typically 95%
  expected_lift: number;       // Expected improvement %

  results?: {
    variant_a_conversion: number;
    variant_b_conversion: number;
    statistical_significance: boolean;
    winner: 'a' | 'b' | 'inconclusive';
  };
}
```

### 6. Email Marketing Strategy

**Email Sequences:**
```typescript
// Onboarding email sequence
const onboardingSequence = [
  {
    day: 0,
    subject: "Welcome to [Product] - Let's get you started",
    goal: "Complete profile setup",
    cta: "Complete Your Profile",
    content: {
      sections: [
        "Welcome message",
        "Quick start guide (3 steps)",
        "Video tutorial link",
        "Support resources"
      ]
    }
  },
  {
    day: 2,
    subject: "Quick win: Add your first property in 2 minutes",
    goal: "Add first property",
    cta: "Add Your First Property",
    content: {
      sections: [
        "Benefit of adding properties",
        "Step-by-step guide",
        "Success story example"
      ]
    }
  },
  {
    day: 5,
    subject: "You're missing out on these powerful features",
    goal: "Feature discovery",
    cta: "Explore Advanced Analytics",
    content: {
      sections: [
        "Feature highlights",
        "Use case examples",
        "Video demo"
      ]
    }
  },
  {
    day: 10,
    subject: "How [Customer Name] increased ROI by 23% using [Product]",
    goal: "Social proof / retention",
    cta: "Read Full Case Study",
    content: {
      sections: [
        "Customer success story",
        "Specific results and metrics",
        "How they did it"
      ]
    }
  }
];

// Re-engagement sequence (for inactive users)
const reengagementSequence = [
  {
    trigger: "No login in 14 days",
    subject: "We miss you! Here's what's new",
    goal: "Re-activate user",
    incentive: "Exclusive feature preview",
  },
  {
    trigger: "No login in 30 days",
    subject: "Your portfolio data is waiting for you",
    goal: "Highlight value",
    incentive: "New market insights available",
  },
  {
    trigger: "No login in 60 days",
    subject: "Last chance: Keep your account active",
    goal: "Prevent churn",
    incentive: "30-day extension offer",
  }
];
```

**Email Best Practices:**
```typescript
interface EmailBestPractices {
  subject_line: {
    max_length: 50;              // Characters
    personalization: true;       // Use recipient name
    avoid: ['URGENT', 'FREE', 'Click here']; // Spam triggers
    test_emojis: boolean;        // A/B test emoji usage
  };

  preview_text: {
    length: 90;                  // Characters (visible in inbox)
    complement_subject: true;    // Don't repeat subject line
  };

  body: {
    paragraphs: 'short';         // 2-3 sentences max
    cta_buttons: 1-2;            // Primary and optional secondary
    images: {
      use_alt_text: true;
      optimize_size: true;       // < 200KB total
    };
    personalization_tokens: ['first_name', 'company', 'property_count'];
  };

  timing: {
    optimal_days: ['Tuesday', 'Wednesday', 'Thursday'];
    optimal_times: ['10:00 AM', '2:00 PM'];  // Recipient timezone
    frequency: 'weekly_max: 2'; // Don't overwhelm
  };

  metrics: {
    open_rate_target: 0.25;      // 25%
    click_rate_target: 0.05;     // 5%
    unsubscribe_threshold: 0.005; // < 0.5%
  };
}
```

### 7. SEO Strategy

**On-Page SEO Checklist:**
```typescript
interface SEOOptimization {
  technical: {
    page_speed: 'Target < 3s load time';
    mobile_friendly: boolean;
    https: boolean;
    structured_data: ['Organization', 'Product', 'Review', 'FAQ'];
    sitemap: boolean;
    robots_txt: boolean;
  };

  on_page: {
    title_tag: {
      length: [50, 60];          // Characters
      includes_keyword: boolean;
      format: 'Primary Keyword | Brand Name';
    };
    meta_description: {
      length: [150, 160];
      includes_keyword: boolean;
      includes_cta: boolean;
    };
    headings: {
      h1: 1;                     // One H1 per page
      keyword_in_h1: boolean;
      h2_h3_structure: boolean;  // Logical hierarchy
    };
    content: {
      word_count: 1500;          // Minimum for pillar content
      keyword_density: [0.01, 0.02]; // 1-2%
      internal_links: 3;         // Minimum
      external_links: 2;         // To authoritative sources
      images_optimized: boolean; // Alt text, compressed
    };
  };

  off_page: {
    backlinks: {
      target_da: 50;             // Domain Authority
      target_count: number;
      diversity: boolean;        // From multiple domains
      anchor_text_variety: boolean;
    };
  };

  local_seo: {                   // For real estate businesses
    google_business_profile: boolean;
    local_citations: string[];   // Yelp, Zillow, etc.
    location_pages: boolean;     // For each market
  };
}
```

**Keyword Strategy:**
```typescript
// Target keyword clusters
const keywordClusters = {
  high_intent: {
    keywords: [
      'real estate portfolio management software',
      'property investment analytics platform',
      'real estate dashboard for investors'
    ],
    monthly_searches: [1000, 800, 500],
    difficulty: 'high',
    priority: 'high',           // High intent = high priority
    content_type: 'product_page'
  },

  informational: {
    keywords: [
      'how to calculate cap rate',
      'real estate investment metrics',
      'property ROI calculator'
    ],
    monthly_searches: [5000, 3000, 2000],
    difficulty: 'medium',
    priority: 'medium',          // Drive traffic, build authority
    content_type: 'blog_post'
  },

  long_tail: {
    keywords: [
      'best real estate portfolio tracker for multifamily',
      'how to analyze rental property cash flow'
    ],
    monthly_searches: [100, 150],
    difficulty: 'low',
    priority: 'medium',          // Easier to rank, qualified traffic
    content_type: 'blog_post'
  }
};
```

### 8. Paid Advertising Strategy

**Google Ads Campaign Structure:**
```typescript
interface GoogleAdsCampaign {
  campaign_name: string;
  campaign_type: 'search' | 'display' | 'video' | 'shopping';
  budget: {
    daily: number;
    monthly: number;
  };

  ad_groups: {
    name: string;
    keywords: {
      keyword: string;
      match_type: 'exact' | 'phrase' | 'broad';
      max_cpc: number;
    }[];

    ads: {
      headline_1: string;        // 30 chars max
      headline_2: string;
      headline_3: string;
      description_1: string;     // 90 chars max
      description_2: string;
      final_url: string;
      display_path: string;
    }[];

    bid_strategy: 'manual_cpc' | 'target_cpa' | 'maximize_conversions';
    target_cpa?: number;
  }[];

  targeting: {
    locations: string[];
    languages: string[];
    demographics: {
      age: string[];
      household_income: string[];
    };
    audiences: string[];
  };

  tracking: {
    conversion_actions: string[];
    utm_parameters: boolean;
    call_tracking: boolean;
  };
}
```

**Social Media Ads:**
```typescript
// Facebook/Instagram ad campaign
const socialAdCampaign = {
  objective: 'conversions',     // vs. awareness, traffic, etc.

  audience: {
    targeting: {
      age: [30, 55],
      interests: ['Real Estate', 'Investing', 'Property Management'],
      behaviors: ['Real estate investors', 'Small business owners'],
      lookalike: {
        source: 'existing_customers',
        percentage: 1              // 1% = most similar
      }
    },
    exclusions: ['Existing customers', 'Job seekers']
  },

  creative: {
    format: 'carousel' | 'video' | 'single_image',
    primary_text: string;        // 125 chars recommended
    headline: string;            // 40 chars max
    description: string;         // 30 chars max
    cta_button: 'Learn More' | 'Sign Up' | 'Get Started',
    media: {
      images: string[];          // 1080x1080 recommended
      videos: string[];          // 15-60 seconds
    }
  },

  budget: {
    daily: number;
    bid_strategy: 'lowest_cost' | 'cost_cap' | 'bid_cap',
    optimization_goal: 'conversions' | 'landing_page_views'
  },

  placement: {
    platforms: ['facebook', 'instagram'],
    positions: ['feed', 'stories', 'reels', 'right_column']
  }
};
```

### 9. Analytics and Attribution

**Marketing Attribution Model:**
```typescript
interface AttributionModel {
  type: 'first_touch' | 'last_touch' | 'linear' | 'time_decay' | 'position_based';

  // Example: Position-based (40% first, 40% last, 20% middle)
  position_based: {
    first_touch: 0.40,
    last_touch: 0.40,
    middle_touches: 0.20
  };

  touchpoints: {
    timestamp: Date;
    channel: string;
    source: string;
    medium: string;
    campaign: string;
    content: string;
  }[];

  conversion: {
    timestamp: Date;
    value: number;
    type: string;
  };

  attribution_credit: {
    [channel: string]: {
      credit: number;            // Attribution percentage
      roi: number;               // Return on investment
      influenced_conversions: number;
    };
  };
}
```

**Dashboard Metrics:**
```typescript
interface MarketingDashboard {
  overview: {
    total_traffic: number;
    conversion_rate: number;
    cac: number;                 // Customer Acquisition Cost
    ltv: number;                 // Lifetime Value
    ltv_cac_ratio: number;       // Should be > 3
    roas: number;                // Return on Ad Spend
  };

  by_channel: {
    channel: string;
    traffic: number;
    conversions: number;
    conversion_rate: number;
    cost: number;
    revenue: number;
    roi: number;
  }[];

  cohort_analysis: {
    cohort_month: string;
    users: number;
    retention: {
      month_0: number;
      month_1: number;
      month_3: number;
      month_6: number;
      month_12: number;
    };
    ltv: number;
  }[];

  funnel_metrics: {
    stage: string;
    users: number;
    conversion_rate: number;     // To next stage
    dropoff_rate: number;
  }[];
}
```

## Best Practices

### ✅ DO:

1. **Focus on Metrics That Matter**
   - Track LTV:CAC ratio (target > 3:1)
   - Monitor cohort retention
   - Measure time to value
   - Calculate payback period

2. **Test Everything**
   - A/B test landing pages
   - Test email subject lines
   - Experiment with ad creative
   - Validate messaging with customers

3. **Segment Your Audience**
   - Create buyer personas
   - Segment by behavior and engagement
   - Personalize messaging by segment
   - Target high-value cohorts

4. **Build for the Long Term**
   - Invest in SEO and content
   - Build email lists
   - Focus on retention, not just acquisition
   - Create compounding growth channels

5. **Leverage Data**
   - Use analytics to drive decisions
   - Track full-funnel metrics
   - Implement proper attribution
   - Monitor competitor strategies

6. **Optimize the Entire Funnel**
   - Don't just focus on top of funnel
   - Improve activation and onboarding
   - Reduce churn
   - Increase referrals

### ❌ DON'T:

1. **Vanity Metrics**
   - Don't celebrate traffic without conversions
   - Avoid focusing solely on follower counts
   - Look beyond open rates to click-through and conversions

2. **Spray and Pray**
   - Don't try every channel at once
   - Avoid spreading budget too thin
   - Focus on channels that work

3. **Ignore Existing Customers**
   - Don't only focus on acquisition
   - Retention is more cost-effective than acquisition
   - Upsell and cross-sell to existing base

4. **Set and Forget**
   - Marketing requires continuous optimization
   - Monitor performance regularly
   - Adapt to changing market conditions

## Execution Instructions

When this skill is invoked:

1. **Understand Business Context**
   - Clarify marketing objectives
   - Identify target audience
   - Review existing strategies and results
   - Understand budget and resources

2. **Develop Strategy**
   - Define positioning and messaging
   - Select appropriate channels
   - Plan campaigns and content
   - Set KPIs and targets

3. **Create Campaign Plan**
   - Develop detailed execution plan
   - Create content and creative assets
   - Set up tracking and analytics
   - Define success metrics

4. **Execute and Monitor**
   - Launch campaigns
   - Track performance metrics
   - Monitor budget pacing
   - Gather user feedback

5. **Analyze and Optimize**
   - Review performance data
   - Identify opportunities
   - Run A/B tests
   - Iterate and improve

6. **Report and Recommend**
   - Summarize results
   - Calculate ROI
   - Provide actionable recommendations
   - Plan next steps

## Integration with Other Skills

- **Data Analysis**: Analyze marketing metrics and attribution
- **Data Science**: Build predictive models for user behavior
- **UI Design**: Create high-converting landing pages
- **Finance**: Calculate ROI and budget allocation
- **Manager/CEO**: Align marketing with business strategy

## Deliverable Checklist

Before completing marketing task:
- [ ] Clear objectives and KPIs defined
- [ ] Target audience identified and segmented
- [ ] Messaging and positioning validated
- [ ] Channel strategy optimized for ROI
- [ ] Content calendar planned
- [ ] Tracking and analytics implemented
- [ ] Budget allocated efficiently
- [ ] A/B testing framework in place
- [ ] Success metrics baseline established
- [ ] Reporting dashboard created

