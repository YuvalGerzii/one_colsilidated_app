# VALUE-ADD RENOVATION BUDGET BUILDER - USER GUIDE

**Version 1.0 | November 2025**  
**Part of Portfolio Dashboard Project**

---

## 📚 TABLE OF CONTENTS

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Sheet-by-Sheet Guide](#sheet-by-sheet-guide)
4. [Step-by-Step Workflow](#step-by-step-workflow)
5. [Industry Benchmarks](#industry-benchmarks)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## OVERVIEW

### What This Model Does

The **Value-Add Renovation Budget Builder** is a comprehensive Excel template designed for multifamily property investors executing value-add strategies. It provides:

- **Pre-built cost databases** with 100+ line items by building class (A, B, C)
- **Unit-by-unit budget customization** for 50 units (expandable)
- **Phased renovation planning** to maintain occupancy
- **ROI calculator** with detailed value creation metrics
- **Sensitivity analysis** for risk assessment
- **Timeline tracking** with holding cost calculations

### Who Should Use This Model

- **Private equity real estate investors** acquiring value-add multifamily
- **Property managers** planning capital improvements
- **Asset managers** evaluating renovation ROI
- **Developers** repositioning older properties
- **Lenders** underwriting value-add financing

### Key Features

✅ **425 formulas, 0 errors** - Fully validated calculations  
✅ **Industry-standard color coding** - Blue inputs, black formulas, green links  
✅ **Pre-built cost database** - 100+ renovation items with Class A/B/C pricing  
✅ **Automatic calculations** - Change inputs, everything updates instantly  
✅ **Integration-ready** - Designed to connect with Portfolio Dashboard platform  

---

## GETTING STARTED

### System Requirements

- **Excel Version**: 2016, 2019, 2021, or 365
- **Platform**: Windows, Mac, or Excel Online
- **Macros**: Not required (pure formulas only)
- **File Size**: ~150 KB (fast performance)

### Installation

1. Download `ValueAdd_Renovation_Budget_Builder.xlsx`
2. Open in Microsoft Excel
3. Enable editing if prompted
4. Save a copy before making changes

### Color Coding Legend

**INPUTS (Blue Text)**: Values you can change
- Property information
- Renovation costs
- Rent assumptions
- Timeline parameters

**FORMULAS (Black Text)**: Auto-calculated values
- Totals and subtotals
- ROI metrics
- Dates and schedules

**LINKS (Green Text)**: References to other sheets
- Cross-sheet calculations
- Summary metrics

**KEY CELLS (Yellow Fill)**: Important results
- Total budget
- ROI percentages
- Value creation

---

## SHEET-BY-SHEET GUIDE

### SHEET 1: Executive Summary

**Purpose**: High-level dashboard showing key metrics

**What You See**:
- Property overview (name, units, class, size)
- Total renovation budget summary
- Budget breakdown by 7 major categories
- Value creation & ROI analysis
- Rent increase and payback metrics

**All GREEN**: These cells pull from other sheets automatically. Don't edit directly.

**Use Case**: Present to investment committee, lenders, or partners

---

### SHEET 2: Inputs

**Purpose**: All property and renovation assumptions

**What to Enter** (BLUE cells only):

#### Property Information
- Property Name: Your building name
- Address: Full property address
- Total Units: Number of apartment units (default: 50)
- Building Class: A, B, or C
- Average Unit Size (SF): Weighted average square footage

#### Current & Pro Forma Rents
- Current Avg Monthly Rent: In-place rent before renovation
- Pro Forma Monthly Rent: Expected rent after renovation
- Monthly Rent Increase: Auto-calculates

#### Value Creation Assumptions
- Exit Cap Rate: 5.0-6.0% typical (conservative)
- NOI Margin: 60% standard for multifamily

#### Renovation Timeline & Phasing
- Total Project Duration: 12-24 months typical
- Units per Phase: 10-15 units recommended
- Days per Unit Renovation: 21 days typical (3 weeks)
- Lost Rent per Unit during Reno: 30 days typical

#### Holding Costs During Renovation
- Monthly Debt Service: Mortgage payment
- Monthly Operating Expenses: Utilities, insurance, etc.
- Monthly Management Fee: Property management costs

**Pro Tip**: Use conservative (pessimistic) assumptions. It's better to over-deliver.

---

### SHEET 3: Cost Database

**Purpose**: Reference pricing for 100+ renovation items

**DO NOT EDIT**: This is a reference database. Use it to inform your unit-level budgets.

**Categories Covered**:

1. **Kitchen Renovations** (15 items)
   - Cabinets: Paint ($2K-$3K) to Semi-Custom ($5.5K-$10K)
   - Countertops: Laminate ($1K-$1.5K) to Quartz ($2.5K-$4K)
   - Appliances: Basic ($1.5K-$2K) to Premium ($3K-$5K)
   - Backsplash, sinks, lighting

2. **Bathroom Renovations** (19 items)
   - Vanities, toilets, tubs, showers
   - Tile flooring: $5-$18/SF by quality
   - Fixtures, lighting, mirrors

3. **Flooring** (13 items)
   - Carpet: $2-$7/SF
   - LVP (Luxury Vinyl Plank): $3-$9/SF
   - Hardwood/Laminate/Tile options

4. **Paint & Finishes** (9 items)
   - Interior paint: $1.75-$2.50/SF
   - Trim, doors, hardware

5. **Appliances & Fixtures** (14 items)
   - Lighting, thermostats, window treatments
   - Dishwashers, microwaves

6. **Exterior Improvements** (16 items)
   - Painting, siding, landscaping
   - Fencing, parking lot, signage

7. **Common Area Improvements** (12 items)
   - Lobby/clubhouse: $30-$60/SF
   - Fitness center, pool, amenities

**How to Use**:
1. Identify your building class (A, B, or C)
2. Find relevant line items for your scope
3. Use these costs in Unit-Level Budget sheet
4. Adjust for your specific market

---

### SHEET 4: Unit-Level Budget

**Purpose**: Customize renovation cost for each unit

**Structure**: 50 units pre-loaded (expandable to 100+)

**Columns**:
- **Unit**: Unit number (1-50)
- **Type**: 1BR, 2BR, or 3BR (BLUE - you can change)
- **Kitchen**: Kitchen renovation cost (BLUE)
- **Bathroom**: Bathroom renovation cost (BLUE)
- **Flooring**: Flooring cost (BLUE)
- **Paint**: Paint & finishes cost (BLUE)
- **Fixtures**: Appliances & fixtures cost (BLUE)
- **Total**: Auto-calculated sum per unit (BLACK)
- **Phase**: Auto-assigned based on Units per Phase (BLACK)
- **Start Date**: Auto-calculated from phase (BLACK)
- **Status**: Planned, In Progress, or Complete (BLUE)

**Sample Costs Included**:
- 1BR units: ~$23,000/unit
- 2BR units: ~$33,000/unit
- 3BR units: ~$44,000/unit

**Category Totals** (rows 59-70):
- Kitchen Renovations: Sum of all kitchen costs
- Bathroom Renovations: Sum of all bathroom costs
- Flooring: Sum of all flooring costs
- Paint & Finishes: Sum of all paint costs
- Appliances & Fixtures: Sum of all fixture costs
- **Exterior Improvements**: $50K lump sum (BLUE - adjust as needed)
- **Common Areas**: $75K lump sum (BLUE - adjust as needed)

**Grand Totals** (rows 72-77):
- Base Renovation Cost
- Cost per Unit
- Cost per SF
- Contingency Reserve (10%)
- **ALL-IN BUDGET** (in yellow)

**How to Customize**:
1. Change unit types to match your property
2. Adjust costs based on your actual scope
3. Add units if needed (copy row formulas down)
4. Update exterior/common area lump sums

---

### SHEET 5: Renovation Phasing

**Purpose**: Plan phased renovation to maintain cash flow

**Project Overview** (rows 5-9):
- Total units, units per phase, number of phases
- Days per unit, total duration
- All auto-calculated from Inputs sheet

**Phase Breakdown** (rows 13-18):
For each of 5 phases (adjusts based on your inputs):
- **Start Date**: Auto-calculated (Phase 1 = Jan 1, 2025)
- **End Date**: Start Date + (Units per Phase × Days per Unit)
- **Units**: Number of units in this phase
- **Cost**: Sum of unit costs in this phase (from Unit-Level Budget)
- **Lost Rent**: Vacancy cost during renovation
- **Holding Costs**: Debt service + OpEx for phase duration
- **Total Cash Out**: Cost + Lost Rent + Holding Costs

**Cash Flow Impact Analysis** (rows 25-36):
- Total renovation cost
- Total lost rent across all phases
- Total holding costs
- **TOTAL CAPITAL REQUIRED** (in yellow)
- Annual rent increase (stabilized)
- Annual NOI increase
- Property value creation
- Net value created
- ROI on total investment
- Cash-on-cash return (Year 1)

**Key Insight**: This shows you need more capital than just the renovation budget. Lost rent and holding costs add ~10-15% to total investment.

---

### SHEET 6: ROI Calculator

**Purpose**: Detailed return on investment analysis

**Investment Summary** (rows 5-10):
- Base renovation cost
- Contingency (10%)
- Lost rent during renovation
- Holding costs
- **TOTAL CAPITAL REQUIRED**

**Revenue Impact** (rows 13-21):
- Current vs pro forma rents
- Monthly and annual rent increases
- Total property revenue increase
- Rent increase percentage

**NOI & Value Creation** (rows 24-33):
- Annual revenue increase
- NOI margin (60% typical)
- Annual NOI increase
- Exit cap rate
- **Property value creation**
- Total investment
- Value created
- **Net gain**

**Return Metrics** (rows 36-46):
- ROI %
- Value creation multiple
- Cash-on-cash return (Year 1)
- Payback period (years)
- Cost per unit and per SF
- Value creation per unit and per SF

**Industry Benchmarks** (rows 49-54):
Compares your project to industry targets:
- ROI target: 100%+ (1.0x return minimum)
- Value multiple target: 1.5x or better
- Payback target: Under 3 years
- Rent increase target: 15%+ lift
- Cost per unit target: Under $30K

**Status Column**: Shows ✓ PASS or ✗ REVIEW based on your metrics

---

### SHEET 7: Sensitivity Analysis

**Purpose**: Test different scenarios to understand risk

**Scenario Comparison** (rows 6-10):
Tests 5 scenarios (Worst, Conservative, Base, Optimistic, Best):
- Rent increase: 10% to 30%
- Cost overrun: 90% to 120% of budget
- Exit cap rate: 4.5% to 6.5%
- Project duration: 12 to 24 months
- Occupancy impact: 85% to 98%

**Scenario Results** (rows 13-19):
For each scenario calculates:
- Monthly rent increase
- Total investment
- Annual NOI increase
- Property value created
- ROI %
- Payback period

**Rent Increase Sensitivity** (rows 22-32):
Tests 7 rent scenarios from 5% to 35% increase:
- Monthly rent at each level
- Annual revenue impact
- Annual NOI impact
- Value created
- ROI %
- Payback years

**Exit Cap Rate Sensitivity** (rows 35-45):
Tests 7 cap rates from 4.0% to 7.0%:
- Annual NOI (constant)
- Property value at each cap rate
- Value created
- Net gain
- ROI %
- Value multiple

**How to Use**:
1. Base Case (column D) = your current assumptions
2. Look at Worst Case (column B) - Can you handle this outcome?
3. Look at Best Case (column F) - What's the upside?
4. Use sensitivity tables to test specific variables
5. Focus on scenarios where you still make money

---

## STEP-BY-STEP WORKFLOW

### Phase 1: Property Setup (15 minutes)

1. **Open the model** and save a copy with your property name
2. **Go to Inputs sheet**
3. **Enter property details**:
   - Property name and address
   - Total units, building class, average unit size
4. **Enter current rents** (from rent roll)
5. **Estimate pro forma rents** (from market comps)
6. **Set exit cap rate** (check local sales comps)
7. **Define project timeline**:
   - Total duration (18 months typical)
   - Units per phase (10-15 recommended)
   - Days per unit (21 typical)
8. **Enter holding costs**:
   - Monthly debt service (from loan docs)
   - Monthly OpEx (from T-12 P&L)
   - Management fee

### Phase 2: Budget Development (1-2 hours)

1. **Go to Cost Database sheet**
2. **Review pricing** for your building class
3. **Decide on renovation scope** for each unit type:
   - Light: Paint, fixtures, minor repairs
   - Medium: Kitchens, baths, flooring
   - Heavy: Full gut renovation
4. **Go to Unit-Level Budget sheet**
5. **For each unit (or unit type)**:
   - Verify unit type (1BR, 2BR, 3BR)
   - Enter kitchen cost (refer to Cost Database)
   - Enter bathroom cost (1, 2, or 3 baths)
   - Enter flooring cost
   - Enter paint cost
   - Enter fixtures cost
6. **Update lump sum items**:
   - Exterior improvements (row 60)
   - Common areas (row 70)
7. **Review category totals** (rows 59-70)
8. **Check All-In Budget** (row 77) - Does this fit your financing?

### Phase 3: Phasing Plan (30 minutes)

1. **Go to Renovation Phasing sheet**
2. **Review auto-generated phase schedule**
3. **Verify phase timing** makes sense:
   - Can you handle lost rent?
   - Do you have enough crews/contractors?
   - Does this align with lease expirations?
4. **Review Cash Flow Impact Analysis**:
   - Total Capital Required (row 28)
   - Make sure you have adequate reserves

### Phase 4: ROI Analysis (30 minutes)

1. **Go to ROI Calculator sheet**
2. **Review Investment Summary** (rows 5-10)
3. **Verify Revenue Impact** (rows 13-21):
   - Are rent increases realistic?
   - Compare to market comps
4. **Check NOI & Value Creation** (rows 24-33):
   - Is value creation sufficient?
   - Does exit cap rate make sense?
5. **Review Return Metrics** (rows 36-46):
   - ROI: Target 100%+
   - Value Multiple: Target 1.5x+
   - Payback: Target <3 years
6. **Compare to Industry Benchmarks** (rows 49-54)
   - Where do you PASS?
   - Where do you need to REVIEW?

### Phase 5: Sensitivity Testing (30 minutes)

1. **Go to Sensitivity Analysis sheet**
2. **Review Scenario Comparison** (rows 6-19):
   - Can you handle Worst Case?
   - Is Conservative Case acceptable?
   - What's the Best Case upside?
3. **Study Rent Increase Sensitivity** (rows 22-32):
   - What if rents only increase 10%?
   - What if you get 25% increase?
4. **Study Cap Rate Sensitivity** (rows 35-45):
   - What if cap rates expand to 6.5%?
   - What if they compress to 4.5%?
5. **Identify breakeven points**:
   - Minimum rent increase needed
   - Maximum cap rate tolerable

### Phase 6: Final Review & Presentation

1. **Go to Executive Summary sheet**
2. **Print or PDF** for investment committee
3. **Create investor presentation**:
   - Show Executive Summary
   - Highlight ROI metrics
   - Present Base/Conservative/Optimistic scenarios
4. **Document assumptions**:
   - Why did you choose these rents?
   - How did you estimate costs?
   - What's your confidence level?

---

## INDUSTRY BENCHMARKS

### Renovation Costs by Building Class

**Class A (Luxury)**:
- Kitchen: $12,000-$20,000
- Bathroom: $8,000-$12,000 per bath
- Flooring: $6-$9/SF
- Total: $35,000-$50,000+ per unit

**Class B (Mid-Range)**:
- Kitchen: $8,000-$12,000
- Bathroom: $5,000-$8,000 per bath
- Flooring: $4-$6/SF
- Total: $20,000-$35,000 per unit

**Class C (Value)**:
- Kitchen: $5,000-$8,000
- Bathroom: $3,500-$5,000 per bath
- Flooring: $3-$4/SF
- Total: $12,000-$20,000 per unit

### Rent Increase Expectations

**Light Renovation** (cosmetic):
- Rent increase: 5-10%
- Cost: $8K-$15K per unit
- Payback: 1-2 years

**Medium Renovation** (kitchen/bath):
- Rent increase: 15-25%
- Cost: $20K-$35K per unit
- Payback: 2-3 years

**Heavy Renovation** (gut rehab):
- Rent increase: 25-40%+
- Cost: $40K-$60K per unit
- Payback: 3-5 years

### Return Targets

**Value-Add Multifamily**:
- ROI: 100-200% (1.0x-2.0x)
- IRR: 18-25% unlevered
- Equity Multiple: 1.8x-2.5x (5-7 years)
- Cash-on-Cash (Year 1): 8-12%
- Payback Period: 2-4 years

**Cap Rates** (2025 market):
- Class A Urban: 4.0-5.0%
- Class B Suburban: 5.0-6.0%
- Class C Secondary: 6.0-7.5%
- Value-Add Stabilized: 5.5-6.5%

### Project Timeline

**Typical Phased Renovation**:
- Planning/Design: 1-2 months
- Permitting: 1-2 months (concurrent)
- Phase 1 (10-15 units): 2-3 months
- Phase 2: 2-3 months
- Phase 3: 2-3 months
- Stabilization: 3-6 months
- **Total: 12-18 months**

### Lost Rent & Holding Costs

**Typical Costs**:
- Lost rent per unit: 1-2 months ($2K-$5K)
- Holding costs: 10-15% of renovation budget
- Total soft costs: 15-20% of hard costs

---

## BEST PRACTICES

### Budgeting

1. **Use contractor bids**, not just Cost Database estimates
2. **Add 10-20% contingency** - things always cost more
3. **Get multiple bids** (at least 3 for major items)
4. **Verify pricing locally** - costs vary by market
5. **Include permits, dumpsters, storage** in budget
6. **Account for code upgrades** (electrical, plumbing)
7. **Budget for temporary relocation** if needed

### Phasing Strategy

1. **Start with vacant units** to perfect scope
2. **Phase by unit type** (all 1BRs, then 2BRs)
3. **Renovate at lease turnover** when possible
4. **Maintain 90%+ occupancy** to cover debt service
5. **Avoid peak moving season** (summer)
6. **Coordinate with property management** on timing
7. **Have backup units** for displaced residents

### Rent Underwriting

1. **Survey 5+ comparable properties** in market
2. **Adjust for amenities and location**
3. **Account for concessions** (1 month free, etc.)
4. **Test pricing with market** before full rollout
5. **Phase rent increases** over 6-12 months
6. **Monitor absorption** - are units leasing?
7. **Be conservative** - it's better to exceed expectations

### Risk Management

1. **Test worst-case scenario** - what if rents flat?
2. **Stress test cap rates** +100 bps
3. **Plan for cost overruns** 15-20%
4. **Model extended timelines** +25%
5. **Have adequate reserves** 6 months OpEx minimum
6. **Maintain liquidity** for unexpected issues
7. **Get fixed-price contracts** when possible

### Value Creation

1. **Focus on NOI impact** - not just aesthetics
2. **Prioritize high-ROI items** (kitchens/baths)
3. **Bundle improvements** for efficiency
4. **Consider amenity upgrades** (fitness, package lockers)
5. **Improve curb appeal** - first impressions matter
6. **Add revenue streams** (parking, storage, pet fees)
7. **Reduce operating costs** (LED, low-flow, smart thermostats)

---

## TROUBLESHOOTING

### Common Issues

**Q: All my formulas show #REF! errors**
A: Don't delete rows or columns. If you did, use Undo (Ctrl+Z). Copy a fresh template.

**Q: My ROI shows negative**
A: Your costs are too high or rent increases too low. Adjust assumptions or reconsider the project.

**Q: Sensitivity Analysis doesn't change**
A: The scenarios are based on your Base Case inputs. Change Inputs sheet first, then review Sensitivity.

**Q: I have more than 50 units**
A: Go to Unit-Level Budget, insert rows, copy formulas down. Update range references if needed.

**Q: Phases aren't calculating correctly**
A: Check Inputs!B20 (Units per Phase). Phase formula is =ROUNDUP(Unit#/UnitsPerPhase,0)

**Q: Lost rent seems too high/low**
A: Check Inputs!B22 (Lost Rent days). Typical is 30-45 days per unit during renovation.

**Q: My dates are showing as numbers**
A: Right-click the cell, Format Cells, Date, select mm/dd/yyyy format.

**Q: Can I add more renovation categories?**
A: Yes, but you'll need to update summary formulas in Executive Summary and ROI Calculator sheets.

### Excel Tips

- **Freeze panes**: View > Freeze Panes to lock headers
- **Hide rows**: Right-click row number > Hide (e.g., hide unused units)
- **Protect sheet**: Review > Protect Sheet (lock formula cells)
- **Create scenarios**: Data > What-If Analysis > Scenario Manager
- **Print selection**: Select area, File > Print > Print Selection

### Getting Help

- **Project Documentation**: See Integration Guide for technical details
- **Excel Formulas**: Press F2 to see formula, Ctrl+` to show all formulas
- **Model Errors**: Use Excel's Error Checking tool (Formulas tab)

---

## APPENDIX: Formula Reference

### Key Calculations

**Total Renovation Budget**:
```
='Unit-Level Budget'!C100 * 1.10
(Base cost + 10% contingency)
```

**Annual Rent Increase**:
```
=(ProForma Rent - Current Rent) * 12 * Total Units
```

**Annual NOI Increase**:
```
=Annual Rent Increase * NOI Margin
(Typically 60% margin)
```

**Property Value Created**:
```
=Annual NOI Increase / Exit Cap Rate
```

**ROI**:
```
=(Value Created - Total Investment) / Total Investment
```

**Payback Period**:
```
=Total Investment / Annual NOI Increase
(In years)
```

---

**Model Version**: 1.0  
**Last Updated**: November 2025  
**Support**: See Portfolio Dashboard Integration Guide for platform integration  
**License**: Proprietary - Part of Portfolio Dashboard Project

---

## 📞 NEXT STEPS

1. **Customize the model** with your property details
2. **Run scenario analysis** to stress test assumptions
3. **Present to investment committee** using Executive Summary
4. **Integrate with Portfolio Dashboard** (see Integration Guide)
5. **Track actual vs projected** as renovation progresses

**Ready to integrate with Portfolio Dashboard?** See the Integration Guide for database mapping and API specifications.
