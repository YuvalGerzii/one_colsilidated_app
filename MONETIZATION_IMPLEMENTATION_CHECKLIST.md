# MONETIZATION IMPLEMENTATION CHECKLIST
## Technical Requirements & Priority Matrix

---

## PHASE 1: FOUNDATION (Months 1-2)

### Database Schema Updates
- [ ] Add `subscription_tier` column to User/Company tables (all platforms)
  - [ ] Finance: User.subscription_tier (ENUM: basic, pro, enterprise)
  - [ ] Real Estate: Company.subscription_tier
  - [ ] Bond.AI: User.subscription_tier
  - [ ] Legacy Systems: Organization.subscription_tier
  - [ ] Labor: Existing, ensure consistency

- [ ] Add billing fields
  - [ ] stripe_customer_id (VARCHAR)
  - [ ] subscription_expires (DATETIME)
  - [ ] next_billing_date (DATETIME)
  - [ ] billing_cycle_day (INT)
  - [ ] auto_renew (BOOLEAN)

- [ ] Create new tables
  ```sql
  CREATE TABLE subscriptions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    stripe_subscription_id VARCHAR UNIQUE,
    tier VARCHAR NOT NULL,
    status VARCHAR,  -- active, canceled, past_due
    current_period_start DATETIME,
    current_period_end DATETIME,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW()
  );

  CREATE TABLE api_keys (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    key_hash VARCHAR UNIQUE NOT NULL,
    name VARCHAR,
    last_used DATETIME,
    created_at DATETIME DEFAULT NOW(),
    deleted_at DATETIME  -- soft delete
  );

  CREATE TABLE usage_metrics (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    api_calls INT DEFAULT 0,
    backtest_runs INT DEFAULT 0,
    analyses_run INT DEFAULT 0,
    documents_processed INT DEFAULT 0,
    period_start DATETIME,
    period_end DATETIME,
    created_at DATETIME DEFAULT NOW()
  );

  CREATE TABLE billing_events (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    type VARCHAR,  -- charge, refund, overage
    amount DECIMAL(10, 2),
    currency VARCHAR DEFAULT 'USD',
    description TEXT,
    stripe_event_id VARCHAR UNIQUE,
    created_at DATETIME DEFAULT NOW()
  );
  ```

### Stripe Integration
- [ ] Set up Stripe account (if not exists)
  - [ ] Get API keys (test + live)
  - [ ] Configure webhook endpoints
  - [ ] Create products and price objects in Stripe dashboard

- [ ] Create Stripe products (one per tier, per platform)
  ```
  Finance Platform:
    - Product: "Finance Basic"
      - Price: $99/month (recurring)
    - Product: "Finance Professional"
      - Price: $499/month (recurring)
    - Product: "Finance Enterprise"
      - Price: $2,999/month (recurring)
  
  (Repeat for all platforms)
  ```

- [ ] Install Stripe Python/JS SDK
  ```bash
  pip install stripe  # Python backends
  npm install stripe  # Node backends
  ```

- [ ] Create Stripe service module (`app/services/stripe_service.py`)
  ```python
  class StripeService:
      def create_customer(user_email, user_id)
      def create_subscription(customer_id, price_id)
      def update_subscription(subscription_id, new_price_id)
      def cancel_subscription(subscription_id)
      def get_usage()
      def process_webhook(event)
  ```

- [ ] Webhook endpoint implementation
  - [ ] POST `/api/v1/webhooks/stripe`
  - [ ] Verify webhook signature
  - [ ] Handle events:
    - `customer.subscription.created`
    - `customer.subscription.updated`
    - `customer.subscription.deleted`
    - `invoice.payment_succeeded`
    - `invoice.payment_failed`
  - [ ] Update subscription status in database

### Authentication & Authorization
- [ ] Configure Keycloak RBAC
  - [ ] Create client roles
    - `admin`, `manager`, `user`, `viewer`
  - [ ] Create scope mappings
  - [ ] Configure role-based JWT claims

- [ ] Implement RBAC middleware (all backends)
  ```python
  @require_role(['admin', 'manager'])
  async def protected_endpoint(request: Request):
      pass
  ```

### Rate Limiter Configuration
- [ ] Extend rate limiter per tier
  ```python
  # app/core/rate_limiter.py
  TIER_LIMITS = {
      'basic': {'capacity': 100, 'window_seconds': 60},
      'professional': {'capacity': 1000, 'window_seconds': 60},
      'enterprise': {'capacity': 10000, 'window_seconds': 60}
  }
  ```

- [ ] Apply per-platform
  - [ ] Finance: Backtest operations (10, 50, unlimited per tier)
  - [ ] Real Estate: Model calculations (5, 20, unlimited)
  - [ ] Labor: API calls (500, 2000, unlimited)
  - [ ] Bond.AI: Recommendations (100, 1000, unlimited)

- [ ] Switch from IP-based to user-based rate limiting
  - [ ] Get user_id from auth token
  - [ ] Look up subscription tier
  - [ ] Apply tier-specific limits

---

## PHASE 2: CORE MONETIZATION (Months 3-4)

### Feature Flag System
- [ ] Implement feature flags (recommended: LaunchDarkly or custom)
  ```python
  # app/core/feature_flags.py
  class FeatureFlags:
      @staticmethod
      def is_enabled(feature: str, user_id: str, tier: str):
          flags = {
              'dcf_modeling': ['professional', 'enterprise'],
              'extreme_events': ['professional', 'enterprise'],
              'api_access': ['professional', 'enterprise'],
          }
          return tier in flags.get(feature, [])
  ```

- [ ] Create feature mapping per platform:
  
  **Finance:**
  ```
  basic:
    - Single agent only
    - 100 backtests/month
  professional:
    - 5 concurrent agents
    - Unlimited backtests
    - API access (100 calls/min)
    - Alerts & webhooks
  enterprise:
    - Unlimited everything
    - Custom agents
    - White-labeling
  ```

  **Real Estate:**
  ```
  basic:
    - Property management
    - Basic tax calculator
    - Max 2 users
  professional:
    - DCF/LBO modeling
    - Advanced tax strategies
    - Deal pipeline with AI
    - Max 5 users
  enterprise:
    - Everything
    - Unlimited users
    - Compliance suite
    - White-labeling
  ```

- [ ] API route-level guards
  ```python
  @router.post("/dcf-analysis")
  @require_tier(['professional', 'enterprise'])
  async def create_dcf():
      pass
  ```

- [ ] UI-level feature gating
  - [ ] Hide/disable buttons based on tier
  - [ ] Show "Upgrade to Professional" prompts
  - [ ] Display tier badges

### Usage Metering System
- [ ] Create usage tracking middleware
  ```python
  @track_usage(metric='api_calls', amount=1)
  async def api_endpoint():
      pass
  ```

- [ ] Implement quota enforcement
  ```python
  async def check_quota(user_id, metric, tier):
      limits = {
          'basic': {'backtest_runs': 100},
          'professional': {'backtest_runs': float('inf')},
      }
      usage = get_current_month_usage(user_id, metric)
      limit = limits[tier][metric]
      if usage >= limit and tier != 'enterprise':
          raise QuotaExceededException()
  ```

- [ ] Create usage dashboard
  - [ ] Show current month usage
  - [ ] Show limits per tier
  - [ ] Show overage charges
  - [ ] Forecast end-of-month usage

### API Key Management
- [ ] Create API key generation endpoint
  ```
  POST /api/v1/auth/api-keys
  {
    "name": "My Integration",
    "tier": "professional"  # optional, use subscription tier if not provided
  }
  
  Response:
  {
    "api_key": "sk_live_xyz123",  # masked after creation
    "created_at": "2025-11-18T12:00:00Z"
  }
  ```

- [ ] Create API key management UI
  - [ ] List active keys
  - [ ] Revoke keys
  - [ ] View usage per key
  - [ ] Rotate keys

- [ ] API key authentication middleware
  ```python
  async def verify_api_key(request: Request):
      key = request.headers.get('X-API-Key')
      api_key = db.query(APIKey).filter(APIKey.key_hash == hash(key)).first()
      if not api_key:
          raise AuthenticationError()
      request.state.user_id = api_key.user_id
      request.state.tier = get_user_tier(api_key.user_id)
  ```

### Subscription Management UI
- [ ] Create subscription portal pages
  - [ ] `/settings/subscription`
  - [ ] Current tier display
  - [ ] Features per tier table
  - [ ] "Upgrade" / "Downgrade" / "Cancel" buttons

- [ ] Implement upgrade flow
  ```
  1. User clicks "Upgrade"
  2. Show tier comparison modal
  3. Redirect to Stripe Checkout
  4. On success, update tier in database
  5. Show confirmation & new features
  ```

- [ ] Implement downgrade flow
  - [ ] Warning: Feature loss
  - [ ] Proration calculation
  - [ ] Effective date (end of cycle or immediate)

- [ ] Implement cancellation flow
  - [ ] Cancellation reason survey
  - [ ] Retention offers
  - [ ] Data export option
  - [ ] Confirmation email

### Billing History
- [ ] Create billing history page
  - [ ] Display all invoices
  - [ ] Download PDF invoices
  - [ ] View charges and credits
  - [ ] Payment method management

---

## PHASE 3: ENTERPRISE FEATURES (Months 5-6)

### Multi-Tenancy Isolation
- [ ] Database-level isolation
  - [ ] Add company_id (UUID FK) to all major tables
  - [ ] Create RLS (Row Level Security) policies
  ```sql
  ALTER TABLE properties ENABLE ROW LEVEL SECURITY;
  CREATE POLICY company_isolation ON properties
    USING (company_id = current_user_company_id());
  ```

- [ ] Query-level filtering
  ```python
  @require_company_access
  async def list_properties(company_id: UUID):
      # Automatically filter by company_id
      pass
  ```

- [ ] Implement company context in requests
  - [ ] Extract company_id from JWT token
  - [ ] Pass as request.state.company_id
  - [ ] All queries filtered by this

### SSO/SAML Implementation
- [ ] Configure Keycloak SAML
  - [ ] Create SAML client in Keycloak
  - [ ] Generate SAML metadata
  - [ ] Set up assertion consumer service (ACS)

- [ ] Implement SAML endpoint
  ```
  POST /api/v1/auth/saml/acs
  - Verify SAML assertion
  - Create/update user
  - Issue JWT token
  ```

- [ ] Enterprise SSO onboarding
  - [ ] Show SAML configuration instructions
  - [ ] Validate SAML setup
  - [ ] Test login flow

- [ ] SCIM protocol (optional but enterprise-expected)
  - [ ] GET /scim/v2/users
  - [ ] POST /scim/v2/users (create)
  - [ ] PATCH /scim/v2/users/{id} (update)
  - [ ] DELETE /scim/v2/users/{id} (deactivate)

### White-Labeling
- [ ] Create branding configuration table
  ```sql
  CREATE TABLE brand_configs (
    id UUID PRIMARY KEY,
    company_id UUID REFERENCES companies(id),
    logo_url VARCHAR,
    primary_color VARCHAR,
    secondary_color VARCHAR,
    favicon_url VARCHAR,
    custom_domain VARCHAR,
    enable_powered_by BOOLEAN DEFAULT TRUE,
    created_at DATETIME
  );
  ```

- [ ] Implement logo/color customization
  - [ ] UI theme configuration
  - [ ] Email template customization
  - [ ] Frontend logo replacement

- [ ] Custom domain support
  - [ ] DNS CNAME setup
  - [ ] SSL certificate provisioning (Let's Encrypt)
  - [ ] Routing based on Host header

### Audit Logging
- [ ] Create audit log table
  ```sql
  CREATE TABLE audit_logs (
    id UUID PRIMARY KEY,
    company_id UUID,
    user_id UUID,
    action VARCHAR,  -- create, update, delete, login, export
    resource_type VARCHAR,  -- property, user, deal, etc
    resource_id VARCHAR,
    changes JSON,  -- {old_value, new_value} diffs
    ip_address VARCHAR,
    user_agent TEXT,
    created_at DATETIME
  );
  ```

- [ ] Implement audit middleware
  ```python
  @audit_log(action='create_property')
  async def create_property(data: PropertyCreate):
      pass
  ```

- [ ] Create audit log viewer
  - [ ] Filter by user, action, date range
  - [ ] Export to CSV/JSON
  - [ ] Real-time activity stream (optional)

---

## PHASE 4: ADVANCED (Months 7-8)

### Marketplace Integration
- [ ] Create integration directory
  - [ ] List available integrations
  - [ ] Installation instructions
  - [ ] OAuth flow for integrations

- [ ] Implement webhook system
  - [ ] User can set custom webhooks
  - [ ] Event types per platform
  - [ ] Retry logic for failed webhooks
  - [ ] Webhook testing tool

### Analytics & Reporting
- [ ] Create metrics dashboard
  - [ ] Active subscriptions by tier
  - [ ] MRR (Monthly Recurring Revenue)
  - [ ] Churn rate
  - [ ] Usage trends

- [ ] Export usage analytics
  - [ ] CSV/JSON exports
  - [ ] Customer usage reports
  - [ ] Billing forecast

---

## VALIDATION CHECKLIST

### Security
- [ ] All secrets in environment variables (not in code)
- [ ] Stripe API keys rotated monthly
- [ ] CORS configured for production domains only
- [ ] CSRF tokens on all forms
- [ ] SQL injection prevention (use parameterized queries)
- [ ] XSS prevention (sanitize user input)
- [ ] Rate limiting prevents abuse
- [ ] API keys cannot be exposed in logs

### Compliance
- [ ] PCI DSS compliance (if handling cards)
  - [ ] Never log card numbers
  - [ ] Use Stripe for tokenization
  - [ ] Annual security audit
- [ ] GDPR compliance
  - [ ] Right to data deletion
  - [ ] Data export in standard formats
  - [ ] Privacy policy updated
- [ ] Terms of Service
  - [ ] Subscription terms defined
  - [ ] Refund policy documented
  - [ ] Data retention policy

### Testing
- [ ] Unit tests for tier enforcement
- [ ] Integration tests for Stripe webhooks
- [ ] End-to-end tests for subscription flows
- [ ] Load testing for rate limiter
- [ ] Security penetration testing

### Operations
- [ ] Monitoring for webhook failures
- [ ] Alert on failed charges
- [ ] Backup & recovery procedures
- [ ] Incident response plan
- [ ] Customer communication templates

---

## MIGRATION STRATEGY

### For Existing Users
- [ ] Grandfather free access for 30 days
- [ ] Email notification of pricing (30 days before)
- [ ] Special lifetime discount offer (first 100 users)
- [ ] Dedicated onboarding call for Enterprise users

### Data Migration
- [ ] Assign existing users to appropriate tier
  - Finance: All → Basic tier free for 30 days
  - Real Estate: All → Professional tier (if power users) or Basic
  - Labor: All → Free tier, opt-in to paid tiers
  - Legacy Systems: All → Professional (limited to 90 days)

- [ ] Create trial subscriptions
  - [ ] Generate Stripe customers (no payment method required)
  - [ ] Set subscription to active until end of grace period
  - [ ] Auto-upgrade to paid if user activates payment method

---

## MONITORING & METRICS

### Key Metrics to Track
- Subscription conversion rate (free → paid)
- Monthly Recurring Revenue (MRR)
- Customer Acquisition Cost (CAC)
- Lifetime Value (LTV)
- Churn rate
- Usage per tier
- Revenue per user

### Dashboard Setup
- [ ] Create metrics database
- [ ] Real-time dashboards (Grafana)
- [ ] Daily email digest to leadership
- [ ] Monthly business reviews

---

## ESTIMATED EFFORT

| Task | Effort | Dependencies |
|------|--------|--------------|
| Database schema | 40 hours | None |
| Stripe integration | 60 hours | DB schema |
| Rate limiter extension | 20 hours | DB schema |
| Feature flag system | 30 hours | None |
| Usage metering | 40 hours | DB schema, feature flags |
| API key management | 30 hours | DB schema |
| Subscription UI | 50 hours | Stripe integration |
| SSO/SAML | 50 hours | Keycloak setup |
| White-labeling | 40 hours | UI components |
| Audit logging | 30 hours | DB schema |
| Testing & QA | 100 hours | All above |
| Documentation | 30 hours | All above |
| **TOTAL** | **520 hours** | ~3 months with team of 4 |

