# HOTEL FINANCIAL MODEL - USER GUIDE

## 📊 **OVERVIEW**

The Hotel Financial Model is a comprehensive tool for analyzing hotel investments across all segments, from luxury to economy properties. Built on industry research from STR, HVS, CBRE, and CoStar (2024 data), this model provides professional-grade financial analysis for:

- **Development projects**: New construction hotels
- **Acquisition analysis**: Existing hotel valuations
- **Brand comparison**: Franchise vs. management company structures
- **Segment analysis**: Luxury, Upper Upscale, Upscale, Midscale, Economy

---

## ðŸ"‹ MODEL STRUCTURE

### Sheet 1: Executive Summary
**Purpose**: One-page dashboard showing all key metrics

**Key Metrics Displayed:**
- Property overview (name, type, rooms, brand)
- Year 1 performance (ADR, occupancy, RevPAR)
- Financial summary (revenue, GOP, margins)
- Investment returns (IRR, equity multiple, exit value)

**How to Use:**
- View as "investor presentation" page
- Print/PDF for pitch decks
- Quick health check of investment
- All values auto-update from other sheets (green = linked)

---

### Sheet 2: Inputs
**Purpose**: Central hub for ALL model assumptions

**CRITICAL**: Only change **BLUE** cells with **YELLOW** backgrounds

#### PROPERTY INFORMATION (Rows 4-9)

```
Property Name: Your hotel name
Hotel Type: Luxury | Upper Upscale | Upscale | Midscale | Economy
Location: City/market location
Opening Date: Project opening date
Number of Rooms: Total guest rooms (50-1,000+)
Average Room Size (SF): Square footage per room (250-700)
```

**Industry Standards by Type:**
- **Luxury**: 500-700 SF, $500k-$1M+ per room
- **Upper Upscale**: 450-550 SF, $350k-$500k per room
- **Upscale**: 400-450 SF, $250k-$350k per room
- **Midscale**: 300-400 SF, $150k-$250k per room
- **Economy**: 250-350 SF, $80k-$150k per room

#### REVENUE ASSUMPTIONS (Rows 11-50)

**Rooms Revenue (Rows 13-17)**
```
Year 1 ADR: Starting average daily rate
Stabilized Occupancy: Target occupancy after ramp-up (60-75%)
Ramp-Up Period: Months to reach stabilization (12-24 typical)
ADR Growth Rate: Annual rate increase (2-4% typical)
```

**2024 ADR Benchmarks by Segment:**
- **Luxury**: $300-$500
- **Upper Upscale**: $200-$300 (US average: $227)
- **Upscale**: $120-$200 (US average: $186)
- **Midscale**: $70-$120
- **Economy**: $50-$90

**Brand/Franchise Structure (Rows 19-25)**

Choose between two operating models:

**1. Franchise Model (Owner-Operated)**
- You own and operate the hotel
- Pay franchise fees for brand usage
- Lower operating costs
- More control over operations

**2. Management Agreement Model**
- Brand manages the hotel for you
- Pay base + incentive management fees
- Higher fees but professional management
- Common for luxury properties

**Typical Franchise Fees (% of rooms revenue):**
```
Royalty Fee: 4-6% (brand usage)
Marketing/Reservation Fee: 2-4% (central reservations, marketing)
Technology/Distribution Fee: 1-2% (PMS, booking systems)
Total: 7-12% of rooms revenue
```

**Major Brands by Segment:**
- **Luxury**: Ritz-Carlton, Four Seasons, St. Regis, Waldorf Astoria
- **Upper Upscale**: Marriott, Hilton, Hyatt Regency, Westin
- **Upscale**: Courtyard, Hilton Garden Inn, Hyatt Place, Aloft
- **Midscale**: Hampton Inn, Fairfield Inn, Holiday Inn Express, Comfort Inn
- **Economy**: Super 8, Days Inn, Motel 6, Red Roof Inn

**F&B Revenue (Rows 27-31)**
```
Restaurant/Outlet Revenue per Room per Day: $15-$80 depending on segment
Banquet/Catering Revenue per Group Room Night: $30-$200 depending on segment
Group Business % of Total Rooms: 25-40% typical
F&B Revenue Growth Rate: 3-4% typical
```

**F&B Benchmarks by Segment (per STR, CBRE 2024):**
- **Luxury**: $50-$80/room/day outlet, $150-$200/group room catering
- **Upper Upscale**: $35-$50/room/day outlet, $90-$120/group room catering
- **Upscale**: $25-$40/room/day outlet, $50-$80/group room catering
- **Midscale**: $15-$25/room/day outlet, $30-$50/group room catering
- **Economy**: Minimal to no F&B operations

**Key F&B Insights:**
- Catering/banquet is 55-60% of F&B revenue at luxury/upper upscale
- Food accounts for 57-59% of C&B revenue
- Beverage accounts for 6-10% of C&B revenue
- F&B margins are 25-35% (lower than rooms at 70-80%)

**Other Operated Departments (Rows 33-37)**
```
Meeting Room Rental: $800-$2,500 per room per year
Parking: $600-$1,200 per room per year
Spa/Fitness: $200-$800 per room per year
Other Revenue: $400-$800 per room per year (AV, business center, etc.)
```

#### OPERATING EXPENSES (Rows 39-50)

**Department Operating Expenses**
```
Rooms Dept OpEx: 18-35% of rooms revenue (higher in luxury)
F&B Dept OpEx: 60-75% of F&B revenue
Other Dept OpEx: 30-40% of other revenue
```

**Undistributed Operating Expenses (per room per year)**
```
Administrative & General: $6,000-$12,000
Property Operations & Maintenance: $2,500-$4,000
Utilities: $2,000-$3,500
```

**Fixed Charges (% of total revenue)**
```
Insurance: 1.0-2.0%
Property Tax: 2.5-4.5%
Expense Growth Rate: 2.5-3.5% annually
```

**GOP Margin Benchmarks by Segment:**
- **Luxury**: 35-45% (highest rates but also highest costs)
- **Upper Upscale**: 35-42%
- **Upscale**: 30-40%
- **Midscale**: 25-35%
- **Economy**: 20-30% (lowest costs but compressed rates)

#### DEVELOPMENT COSTS (Rows 52-60)

```
Land Cost: Market value (varies widely by location)
Hard Costs per Room: Construction costs ($80k-$1M per room)
Soft Costs: 15-25% of hard costs (architecture, engineering, permits)
FF&E per Room: $5k-$75k (furniture, fixtures, equipment)
Pre-Opening Expenses: $6k-$10k per room (marketing, training, inventory)
Contingency: 3-7% of total development cost
```

**Development Cost Benchmarks (2024):**
- **Luxury Urban**: $700k-$1.2M per room
- **Upper Upscale Urban**: $400k-$600k per room
- **Upscale Suburban**: $200k-$350k per room
- **Midscale**: $120k-$200k per room
- **Economy**: $70k-$120k per room

**Example Development Budget (300-room Upper Upscale):**
```
Land: $15,000,000
Hard Costs: $105,000,000 (300 rooms × $350,000)
Soft Costs: $21,000,000 (20% of hard costs)
FF&E: $7,500,000 (300 rooms × $25,000)
Pre-Opening: $2,400,000 (300 rooms × $8,000)
Franchise Fee: $75,000
Contingency: $7,548,750 (5%)
TOTAL: $158,523,750 ($528,413 per room)
```

#### FINANCING (Rows 62-67)

```
Loan-to-Cost (LTC): 55-70% (lender will provide this % of total cost)
Interest Rate: Current market rate (6.0-7.5% typical in 2024)
Loan Term: 5-30 years
Amortization: 25-30 years
```

**Typical Financing Terms:**
- **Construction Loan**: 65-75% LTC, floating rate (SOFR + 250-400bps)
- **Permanent Loan**: 60-70% LTC, fixed rate, 10-30 year term
- **Mezzanine/Preferred Equity**: 10-15% of stack at 12-15% return

#### EXIT ASSUMPTIONS (Rows 69-73)

```
Hold Period: Investment horizon (5-10 years typical)
Exit Cap Rate: Market cap rate at sale (6.0-9.0% depending on segment)
Selling Costs: 2.0-3.0% of sale price
```

**Exit Cap Rate Benchmarks (2024):**
- **Luxury**: 6.0-7.5% (lower = higher value)
- **Upper Upscale**: 6.5-7.5%
- **Upscale**: 7.0-8.0%
- **Midscale**: 7.5-8.5%
- **Economy**: 8.0-9.0%

---

### Sheet 3: Pro Forma
**Purpose**: 10-year revenue and expense projections

**Key Sections:**

#### Operating Statistics (Rows 8-15)
- Available rooms and room nights
- Occupancy rate (ramp-up in Year 1, stabilized thereafter)
- Occupied room nights
- Group room nights (% of total)

**Understanding Ramp-Up:**
- Year 1 occupancy is reduced based on ramp-up period
- Formula: Stabilized Occ × 12 / (12 + Ramp Months/12)
- Example: 70% stabilized with 18-month ramp = 58.3% Year 1
- Year 2+ reaches full stabilization

#### Revenue Breakdown (Rows 17-42)

**Rooms Revenue** - Largest revenue source (55-95% of total)
- ADR grows annually at ADR growth rate
- RevPAR = ADR × Occupancy (key industry metric)
- Total Rooms Revenue = Occupied Nights × ADR

**F&B Revenue** - Second largest (0-35% of total)
- Outlet revenue from restaurants, bars, room service
- Banquet/catering from meetings and events
- Grows at F&B growth rate

**Other Revenue** - Ancillary sources (5-10% of total)
- Meeting room rental
- Parking
- Spa/fitness
- Other (business center, AV, laundry, etc.)

#### Operating Expenses (Rows 44-71)

**Department Expenses** - Variable with revenue
- Rooms: 18-35% of rooms revenue
- F&B: 60-75% of F&B revenue (food cost, labor, supplies)
- Other: 30-40% of other revenue

**Undistributed Expenses** - Semi-fixed per room
- Administrative & General (accounting, HR, IT)
- Property Operations & Maintenance (engineering, grounds)
- Utilities (electric, gas, water)

**Fixed Charges** - Based on total revenue
- Franchise/brand fees (7-12% of rooms revenue)
- Insurance (1-2% of total revenue)
- Property taxes (2.5-4.5% of total revenue)

#### Profitability Metrics (Rows 73-76)

**GOP (Gross Operating Profit)**
- Revenue - Operating Expenses
- Key metric for hotel valuation
- Typically 25-45% of revenue depending on segment

**GOP Margin**
- GOP / Total Revenue
- Measures operational efficiency
- Compare to industry benchmarks in Segment Benchmarks sheet

**NOI (Net Operating Income)**
- For this model, NOI = GOP (simplified)
- In detailed models, would include management fees, FF&E reserve
- Used for valuation (NOI / Cap Rate = Value)

---

### Sheet 4: Cash Flow Analysis
**Purpose**: Investment-level cash flows and debt service

#### Sources & Uses (Rows 5-14)
Shows how the project is capitalized:

**Sources:**
- Equity Investment: Your capital (30-45% typical)
- Debt Financing: Lender capital (55-70% typical)

**Uses:**
- Total Development Cost (from Inputs sheet)

**Example (300-room hotel, $158.5M total cost):**
```
SOURCES:
Equity (35%): $55.5M
Debt (65%): $103.0M
TOTAL: $158.5M

USES:
Development Cost: $158.5M
TOTAL: $158.5M
```

#### Operating Cash Flow (Row 18)
- Links to NOI from Pro Forma sheet
- Shows annual operating profit

#### Debt Service (Row 21)
- Annual debt service calculated using PMT function
- Based on loan amount, interest rate, and amortization period
- Formula: =PMT(rate, nper, -loan amount)

**Example Debt Service Calculation:**
- Loan Amount: $103M
- Interest Rate: 6.5%
- Amortization: 30 years
- Annual Payment: $7.8M

#### Cash Flow Before Tax (Row 25)
- NOI - Debt Service
- Shows cash available to equity investors before tax

#### Capital Expenditures (Row 28)
- FF&E Reserve: 4% of total revenue (industry standard)
- Funds periodic renovations and equipment replacement
- Typical cycle: Rooms every 5-7 years, public spaces every 7-10 years

#### Net Operating Cash Flow (Row 32)
- Cash Flow Before Tax - FF&E Reserve
- This is the cash distributed to equity investors each year

**Year 0:** Shows negative equity investment (cash outflow)
**Years 1-10:** Shows annual cash distributions

---

### Sheet 5: Returns Analysis
**Purpose**: Investment returns and exit value

#### Exit Assumptions (Rows 3-12)

**Exit Value Calculation:**
```
1. Exit Year NOI: Year 10 NOI from Pro Forma
2. Exit Cap Rate: Market cap rate (from Inputs)
3. Estimated Value: NOI / Cap Rate
4. Less: Selling Costs (2.5% of value)
5. Less: Loan Balance (remaining debt)
6. = Net Sale Proceeds to Equity
```

**Example Exit Calculation:**
```
Year 10 NOI: $13.5M
Exit Cap Rate: 7.0%
Estimated Value: $13.5M / 7.0% = $192.9M
Selling Costs: ($4.8M)
Loan Balance: ($103.0M)
Net Proceeds: $85.0M
```

#### Return Metrics (Rows 18-29)

**Levered IRR (Internal Rate of Return)**
- Measures annualized return on equity investment
- Accounts for timing of cash flows
- Formula: IRR of (Year 0 equity + Years 1-9 cash flows + Year 10 exit proceeds)

**Interpretation:**
- 15-18% IRR: Acceptable for core investments
- 18-22% IRR: Good for value-add investments
- 22%+ IRR: Excellent, typical for opportunistic deals

**Equity Multiple**
- Total cash returned / Total equity invested
- Simple measure of money made
- Formula: (Sum of distributions + Exit proceeds) / Initial equity

**Interpretation:**
- 1.5x - 2.0x: Conservative stabilized asset over 5-7 years
- 2.0x - 2.5x: Value-add project over 5-7 years
- 2.5x+ : High-return opportunistic deal

**Yield Metrics:**
- Year 1 Yield on Cost: Year 1 NOI / Total development cost
- Stabilized Yield (Year 2): Year 2 NOI / Total development cost
- Cash-on-Cash Return: Year 2 cash flow / Equity invested

**Interpretation:**
- Yield on Cost should exceed equity cap rate by 100-200 bps
- Example: If exit cap is 7%, target 8-9% stabilized yield on cost

---

### Sheet 6: Segment Benchmarks
**Purpose**: Industry reference data for all hotel segments

**2024 Industry Data from:**
- STR (Smith Travel Research)
- HVS (Hotel Valuation Services)
- CBRE Hotels Research
- CoStar

**Sections:**

#### Rate & Occupancy Benchmarks (Rows 6-9)
- ADR ranges by segment
- Typical occupancy levels
- RevPAR expectations

**Use Case:** Compare your assumptions to industry norms

#### Revenue Mix (Rows 11-14)
- What % of revenue comes from rooms vs. F&B vs. other
- Luxury hotels: 30-35% F&B
- Economy hotels: 0-5% F&B

**Use Case:** Ensure your revenue mix is realistic for your segment

#### Operating Margins (Rows 16-20)
- Department expense ratios
- GOP margins
- Net profit margins

**Use Case:** Benchmark your expense assumptions

#### Development Costs (Rows 22-25)
- Cost per room ranges
- FF&E per room
- Typical room sizes

**Use Case:** Validate your development budget

#### Franchise/Brand Fees (Rows 27-30)
- Royalty fee ranges
- Marketing fee ranges
- Total brand cost

**Use Case:** Check if your franchise fees are in line with market

#### F&B Operations (Rows 32-35)
- Outlet revenue benchmarks
- Banquet revenue per group room night
- Meeting space per room

**Use Case:** Set realistic F&B revenue targets

#### Key Financial Ratios (Rows 37-40)
- Labor cost % of revenue
- Flow-through percentages
- Exit cap rates

**Use Case:** Validate your operating model

#### Major Brands (Row 42-43)
- Examples of brands in each segment

**Use Case:** Understand competitive set

---

## 🎯 STEP-BY-STEP USAGE GUIDE

### BASIC SETUP (15 minutes)

1. **Open the model** and save a copy with your project name

2. **Go to Inputs sheet** and update property information:
   - Property name
   - Hotel type (select from benchmarks)
   - Location
   - Number of rooms

3. **Set revenue assumptions** based on market research:
   - Research comparable hotels in your market
   - Check ADR on STR reports or OTA websites
   - Look at group demand for your location
   - Review Segment Benchmarks sheet for guidance

4. **Choose operating structure:**
   - Franchise: Lower fees, more control
   - Management agreement: Higher fees, professional operations

5. **Review expense assumptions:**
   - Compare to Segment Benchmarks
   - Adjust for local labor costs and taxes
   - Consider energy costs in your market

6. **Input development costs:**
   - Get bids from contractors for hard costs
   - Research land values in your area
   - Add local permit/fee costs to soft costs

7. **Set financing terms:**
   - Talk to lenders about available terms
   - Input LTC, rate, and amortization

8. **Review results:**
   - Check Executive Summary for key metrics
   - Look at Pro Forma for detailed projections
   - Analyze Returns Analysis for IRR and exit value

### ADVANCED ANALYSIS

#### Sensitivity Analysis
Test how changes impact returns:

1. **ADR Sensitivity:**
   - Change ADR by ±10% in Inputs
   - Note impact on IRR in Returns Analysis
   - Repeat for ±20%

2. **Occupancy Sensitivity:**
   - Change stabilized occupancy by ±5 points
   - Note impact on Year 2 NOI

3. **Exit Cap Rate Sensitivity:**
   - Change exit cap by ±0.5%
   - Note impact on exit value and IRR

4. **Development Cost Sensitivity:**
   - Increase hard costs by 10-20% (typical overruns)
   - See impact on yields and returns

#### Scenario Planning
Create multiple versions:

**Base Case:** Most likely scenario
- Use median market assumptions
- Conservative ramp-up

**Upside Case:** Optimistic scenario
- ADR at market peak
- Strong occupancy
- Fast ramp-up

**Downside Case:** Stress test
- ADR 15% below market
- Lower occupancy
- Extended ramp-up

#### Optimization
Improve returns:

1. **Increase ADR:**
   - Add premium amenities
   - Improve location
   - Upgrade brand

2. **Reduce Development Costs:**
   - Value engineer design
   - Competitive bidding
   - Efficient layout

3. **Improve Operating Efficiency:**
   - Reduce labor costs per room
   - Negotiate better franchise fees
   - Implement energy-saving systems

---

## 📊 KEY METRICS EXPLAINED

### ADR (Average Daily Rate)
**Formula:** Total Room Revenue / Rooms Sold
**What it measures:** Average price achieved per occupied room
**Why it matters:** Primary indicator of pricing power

**2024 US Average:** $159 (all segments)
**Luxury Average:** $380
**Upper Upscale Average:** $227
**Upscale Average:** $186
**Midscale Average:** $95
**Economy Average:** $70

### Occupancy Rate
**Formula:** Rooms Sold / Rooms Available
**What it measures:** How full the hotel is
**Why it matters:** Utilization of inventory

**2024 US Average:** 63.0%
**Luxury Average:** 70.0%
**Upper Upscale Average:** 70.0%
**Upscale Average:** 69.0%
**Midscale Average:** 61.0%
**Economy Average:** 58.0%

**Urban hotels:** 65-75%
**Suburban hotels:** 60-70%
**Interstate/highway hotels:** 55-65%

### RevPAR (Revenue Per Available Room)
**Formula:** ADR × Occupancy (or Room Revenue / Available Rooms)
**What it measures:** Revenue productivity per room
**Why it matters:** Combines rate and occupancy into single metric

**2024 US Average:** $100
**Luxury Average:** $262
**Upper Upscale Average:** $160
**Upscale Average:** $132
**Midscale Average:** $58
**Economy Average:** $40

**Best Markets (2024):**
- New York City: $350+ RevPAR
- San Francisco: $250+ RevPAR
- Boston: $220+ RevPAR

### GOP (Gross Operating Profit)
**Formula:** Total Revenue - Operating Expenses
**What it measures:** Operating profitability
**Why it matters:** Used for hotel valuation

**GOP Margin Benchmarks:**
- Luxury: 35-45%
- Upper Upscale: 35-42%
- Upscale: 30-40%
- Midscale: 25-35%
- Economy: 20-30%

### GOPPAR (GOP Per Available Room)
**Formula:** GOP / Total Rooms Available
**What it measures:** Profit per room
**Why it matters:** Efficiency of profit generation

### IRR (Internal Rate of Return)
**Formula:** IRR function on cash flows
**What it measures:** Annualized return on investment
**Why it matters:** Time value of money

**Target IRRs by Strategy:**
- Core (stabilized): 12-15%
- Core-Plus (minor value-add): 15-18%
- Value-Add (renovation): 18-22%
- Opportunistic (development): 20-25%+

### Equity Multiple
**Formula:** Total Cash Returned / Equity Invested
**What it measures:** Total profit multiple
**Why it matters:** Simple return measure

**Target Multiples:**
- 5-year hold: 1.5x-2.0x
- 7-year hold: 2.0x-2.5x
- 10-year hold: 2.5x-3.0x+

---

## 🚨 COMMON MISTAKES TO AVOID

### 1. Unrealistic Revenue Assumptions
❌ **Don't:** Use peak ADR as Year 1 assumption
✅ **Do:** Start conservative, ramp to stabilized

❌ **Don't:** Assume 85% occupancy for new hotel
✅ **Do:** Use 70-75% stabilized, lower in Year 1

### 2. Underestimating Operating Expenses
❌ **Don't:** Use 20% rooms department expense at luxury hotel
✅ **Do:** Use 30-35% to account for high service levels

❌ **Don't:** Forget about franchise fees in operating expenses
✅ **Do:** Include 7-12% of rooms revenue for brand fees

### 3. Ignoring Ramp-Up Period
❌ **Don't:** Show full occupancy in Year 1
✅ **Do:** Model 12-24 month ramp-up period

### 4. Incorrect Exit Value
❌ **Don't:** Use Year 1 NOI for exit value
✅ **Do:** Use Year 10 NOI (or year after exit)

❌ **Don't:** Forget to subtract loan balance from exit proceeds
✅ **Do:** Show net proceeds to equity after loan payoff

### 5. Development Budget Gaps
❌ **Don't:** Forget FF&E, pre-opening, franchise fees
✅ **Do:** Include all project costs in development budget

❌ **Don't:** Omit contingency (overruns happen!)
✅ **Do:** Include 5% minimum contingency

---

## 💡 BEST PRACTICES

### Market Research
1. **ADR Research:**
   - Check STR reports for your market
   - Review OTA prices for competitive set
   - Analyze historical ADR trends
   - Account for seasonality

2. **Occupancy Research:**
   - Get STR market penetration data
   - Understand demand generators (convention center, airport, business district)
   - Look at hotel supply pipeline
   - Consider market seasonality

3. **F&B Potential:**
   - Assess group demand in market
   - Size meeting space appropriately
   - Don't overinvest in F&B for midscale/economy

### Financial Modeling
1. **Conservative Base Case:**
   - Use 25th-50th percentile assumptions
   - Model realistic ramp-up
   - Don't underestimate expenses

2. **Scenario Testing:**
   - Create upside, base, downside cases
   - Test sensitivity to key variables
   - Understand break-even points

3. **Market Comparison:**
   - Benchmark against comparable hotels
   - Validate assumptions with operators
   - Check against industry reports

### Investment Analysis
1. **Risk Assessment:**
   - Higher yields for higher risk
   - Development > Value-add > Stabilized
   - Consider market cycle timing

2. **Return Targets:**
   - Match return targets to risk profile
   - Account for market conditions
   - Consider opportunity cost

3. **Exit Strategy:**
   - Plan exit timing (market peak vs. hold to maturity)
   - Consider buyer pool
   - Model multiple exit scenarios

---

## 📈 HOTEL INVESTMENT STRATEGIES

### Development (Ground-Up)
**Risk Level:** Highest
**Return Target:** 20-25%+ IRR
**Hold Period:** 7-10 years

**Key Considerations:**
- Entitlement risk (zoning, permits)
- Construction cost risk (overruns)
- Lease-up risk (slower ramp)
- Highest potential returns

**Best For:**
- Experienced developers
- Strong markets with undersupply
- Long-term investment horizon

### Value-Add (Renovation)
**Risk Level:** Moderate-High
**Return Target:** 18-22% IRR
**Hold Period:** 5-7 years

**Key Considerations:**
- Capital improvement needs
- Revenue growth potential
- Market repositioning
- Flag conversion opportunities

**Best For:**
- Operators with hotel experience
- Markets with strong fundamentals
- Assets with clear improvement path

### Core (Stabilized)
**Risk Level:** Low-Moderate
**Return Target:** 12-15% IRR
**Hold Period:** 5-10 years

**Key Considerations:**
- Stable cash flow
- Lower leverage (50-60% LTV)
- Quality location and brand
- Defensive investment

**Best For:**
- Income-focused investors
- Portfolio diversification
- Defensive allocations

---

## 🌟 SUCCESS METRICS

### Operating Metrics
- **ADR Index:** Your ADR / Comp set ADR (target: 100-110%)
- **Occupancy Index:** Your Occ / Comp set Occ (target: 100-105%)
- **RevPAR Index:** Your RevPAR / Comp set RevPAR (target: 100-110%)
- **GOP Margin:** GOP / Revenue (compare to segment benchmarks)

### Investment Metrics
- **Yield on Cost:** NOI / Total development cost (target: exit cap + 100-200bps)
- **Cash-on-Cash:** Annual cash flow / Equity invested (target: 8-12%)
- **Levered IRR:** Internal rate of return (target: 15-25% depending on risk)
- **Equity Multiple:** Total return / Equity invested (target: 2.0-3.0x)

---

## 📚 ADDITIONAL RESOURCES

### Industry Organizations
- **STR** (Smith Travel Research): Hotel benchmarking data
- **AHLA** (American Hotel & Lodging Association): Industry advocacy and research
- **HFTP** (Hospitality Financial & Technology Professionals): Standards and education
- **HVS** (Hotel Valuation Services): Valuation and consulting

### Market Data Sources
- **CoStar**: Hotel performance data
- **STR Reports**: Market benchmarking
- **CBRE Hotels Research**: Trends and forecasts
- **JLL Hotels & Hospitality**: Market intelligence

### Brand Websites
- **Marriott International**: Franchise information
- **Hilton Worldwide**: Development opportunities
- **IHG Hotels & Resorts**: Brand portfolio
- **Hyatt Hotels**: Franchise options
- **Wyndham Hotels & Resorts**: Midscale brands

---

## ❓ FREQUENTLY ASKED QUESTIONS

**Q: What's a good stabilized occupancy for a new hotel?**
A: 68-75% depending on segment and market. Luxury and upper upscale target 70-75%, midscale 65-70%, economy 60-65%.

**Q: How long does it take a new hotel to stabilize?**
A: 12-24 months typically. Urban full-service hotels may take 18-24 months, select-service hotels 12-18 months.

**Q: What's the difference between franchise and management agreement?**
A: Franchise: You operate, pay 7-12% fees for brand. Management agreement: They operate, pay 12-20%+ fees including incentive.

**Q: Should I include an FF&E reserve in operating expenses?**
A: Yes, 4% of revenue is industry standard. Hotels require periodic renovation every 5-7 years for rooms, 7-10 years for public spaces.

**Q: How do I value a hotel?**
A: NOI / Cap Rate = Value. Cap rates range from 6.0% (luxury gateway) to 9.0% (economy secondary market).

**Q: What's a good GOP margin for my hotel type?**
A: See Segment Benchmarks sheet. Luxury: 35-45%, Upper Upscale: 35-42%, Upscale: 30-40%, Midscale: 25-35%, Economy: 20-30%.

**Q: How much equity do I need?**
A: Construction: 25-35% equity. Acquisition: 30-40% equity. Value-add: 35-45% equity. Stabilized: 40-50% equity.

**Q: What return should I target?**
A: Development: 20-25%, Value-add: 18-22%, Core-plus: 15-18%, Core: 12-15%. Higher risk requires higher returns.

**Q: How do group vs. transient segments differ?**
A: Group (35-50% of mix): Lower ADR but higher F&B spend. Transient: Higher ADR but lower F&B. Mix affects total revenue.

**Q: What's the impact of brand vs. independent?**
A: Branded: +10-20% ADR, +5-10% occupancy, but costs 7-12% of rooms revenue. ROI positive in most markets.

---

## 🎓 APPENDIX: HOTEL TERMINOLOGY

**ADR**: Average Daily Rate - average room revenue per occupied room

**Comp Set**: Competitive set - hotels you compete with

**GOP**: Gross Operating Profit - profit before fixed charges

**GOPPAR**: GOP Per Available Room - profit efficiency metric

**IRR**: Internal Rate of Return - time-adjusted return on investment

**LTC**: Loan-to-Cost - loan amount as % of total development cost

**NOI**: Net Operating Income - income before debt service

**OTA**: Online Travel Agency - Booking.com, Expedia, etc.

**PMS**: Property Management System - hotel operating software

**RevPAR**: Revenue Per Available Room - key performance metric

**RevPAS**: Revenue Per Available Square Foot - meeting space metric

**STR**: Smith Travel Research - leading hotel data provider

**TRevPAR**: Total Revenue Per Available Room - includes all revenue sources

**Yield Management**: Dynamic pricing strategy to maximize revenue

---

## 📞 SUPPORT & UPDATES

This model is based on 2024 industry data and best practices. Market conditions change, so always validate assumptions with current market research.

**Model Version:** 1.0
**Last Updated:** November 2025
**Industry Data:** 2024 calendar year

For questions about the model, consult with hotel finance professionals, appraisers, or investment advisors familiar with your specific market.

---

**DISCLAIMER**: This model is for educational and analytical purposes. All investment decisions should be made with professional advice and thorough due diligence. Past performance does not guarantee future results. Hotel investments carry significant risk including market, operating, and financial risks.
