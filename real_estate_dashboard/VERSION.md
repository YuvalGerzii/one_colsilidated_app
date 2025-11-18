# Version History

## Version 1.1.0 (2025-11-15)

### Design System Overhaul

**Added:**
- Created centralized design token system (`frontend/src/theme/designTokens.ts`)
  - 8px grid spacing system
  - Comprehensive color palette (brand, semantic, workspace, chart)
  - Typography scale with font sizes, weights, line heights
  - Border radius scale
  - Shadow definitions
  - Transition timing functions
  - Z-index scale
  - Responsive breakpoints
  - `alphaColor()` helper function for alpha transparency

- Created reusable `MetricCard` component (`frontend/src/components/ui/MetricCard.tsx`)
  - Supports loading states with skeleton screens
  - Trend indicators (up/down/neutral)
  - Icon badges with dynamic colors
  - Hover animations (transform + shadow)
  - Responsive font sizes
  - Gradient top border accent
  - Subtext support

**Redesigned:**
- `AnalysisInsightsHub.tsx` - Complete UI overhaul
  - Replaced accordion-based layout with tabbed navigation
  - Simplified hero header (reduced visual noise)
  - 7 organized tabs with cleaner 56px height design
  - Icons positioned beside labels (not above)
  - Tooltips for full tab descriptions
  - Dynamic gradient indicators based on active tab

- `CapitalAnalysis.tsx` - Standalone page for Capital & Structure workspace
  - Clean single-row hero header
  - Integrated MetricCard components for key metrics
  - Responsive grid layout (xs: 12, sm: 6, md: 3)
  - 5 tabs: Economic Overview, Financial Markets, Economic Forecasting, Historical Analysis, Correlations
  - All styling uses design tokens for consistency

- `OperateIntelligence.tsx` - Standalone page for Operate workspace
  - Clean single-row hero header matching design system
  - Integrated MetricCard components with real estate metrics
  - Responsive grid layout
  - 5 tabs: Market Overview, Market Insights, STR Analytics, Zoning Intelligence, Advanced Data
  - All styling uses design tokens for consistency

**Design Improvements:**
- Hero headers: Reduced gradient opacity (8% → 3%), simplified icon treatment
- Tab navigation: Reduced height (72px → 56px), improved hover states
- Metric cards: Better visual hierarchy with gradient accents and hover effects
- Loading states: Added skeleton screens to prevent layout shift
- Responsive design: Mobile-first approach with breakpoint-based spacing
- Accessibility: Added tooltips, proper ARIA labels, keyboard navigation support

**Architecture:**
- Separated financial/economic data into Capital & Structure page
- Separated real estate data into Operate page
- Self-contained pages with no routing back to Market Intelligence
- Updated routing in `App.tsx` and `NewLayout.tsx`

---

## Version 1.0.0 (Previous)

Initial release with Market Intelligence Dashboard and basic economics components.
