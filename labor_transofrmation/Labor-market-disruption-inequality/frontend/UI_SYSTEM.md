# UI System Documentation

## Overview

Comprehensive UI system for the Workforce Transition Platform, designed by AI agents and built with React + Material-UI.

## 🎨 Design System

### Color Palette

**Primary (Professional Blue)**
- Main: `#2196F3` - Conveys trust, stability, professionalism
- Used for: CTAs, primary actions, navigation, links

**Secondary (Modern Purple)**
- Main: `#9C27B0` - Represents innovation, creativity
- Used for: Accents, highlights, special features

**Semantic Colors**
- Success: `#4CAF50` (Green)
- Warning: `#FF9800` (Orange)
- Error: `#F44336` (Red)
- Info: `#03A9F4` (Light Blue)

### Typography

**Font Families:**
- **Primary (Body)**: Inter - Clean, readable, optimized for screens
- **Headings**: Poppins - Geometric, friendly, attention-grabbing
- **Monospace**: Fira Code - For code and data displays

**Type Scale:**
```
xs:   12px (0.75rem)
sm:   14px (0.875rem)
base: 16px (1rem)
lg:   18px (1.125rem)
xl:   20px (1.25rem)
2xl:  24px (1.5rem)
3xl:  30px (1.875rem)
4xl:  36px (2.25rem)
5xl:  48px (3rem)
6xl:  60px (3.75rem)
7xl:  72px (4.5rem)
```

### Spacing System

Consistent 4px base unit:
```
1:  4px
2:  8px
3:  12px
4:  16px
5:  20px
6:  24px
8:  32px
10: 40px
12: 48px
16: 64px
20: 80px
24: 96px
```

### Component Tokens

**Buttons:**
- Small: 32px height, 8px/16px padding
- Medium: 40px height, 12px/24px padding
- Large: 48px height, 16px/32px padding
- Border Radius: 8px

**Input Fields:**
- Small: 36px height
- Medium: 44px height
- Large: 52px height
- Border Radius: 6px

**Cards:**
- Padding: 24px
- Border Radius: 12px
- Shadow: md (4px blur)

## 📁 Component Library

### Layout Components

#### `Navigation.jsx`
**Purpose:** Main sidebar navigation with collapsible menu

**Features:**
- Responsive (drawer on mobile, permanent on desktop)
- Expandable submenus
- Active state highlighting
- User profile section
- Gradient background (#1976D2 → #1565C0)

**Props:**
```jsx
<Navigation
  open={boolean}              // Navigation expanded state
  onToggle={() => {}}         // Toggle handler
  currentPath={string}        // Current route
  onNavigate={(path) => {}}   // Navigation handler
/>
```

**Navigation Structure:**
1. Overview (Dashboard)
2. Workforce Digital Twin (5 subpages)
3. AI Agents (5 specialized agents)
4. Study Buddy (7 subpages) [NEW badge]
5. Economic Copilot (5 tools)
6. Gig Economy (5 features)
7. Corporate Tools (7 enterprise features)
8. Progress & Goals
9. Analytics

### Dashboard Components

#### `MetricCard.jsx`
**Purpose:** Display key metrics with trends and sparklines

**Features:**
- Animated hover effect (translateY -4px)
- Trend indicators (up/down arrows)
- Icon with colored background
- Sparkline visualization
- Tooltip for more info

**Props:**
```jsx
<MetricCard
  title="Automation Risk"
  value="42"
  unit="%"
  trend="down"
  trendValue={-8}
  icon={TrendingDown}
  color="success"
  subtitle="Lower is better"
  sparklineData={[45, 48, 44, 43, 42]}
/>
```

**Visual States:**
- Default: Clean card with shadow
- Hover: Elevated (-4px) with increased shadow
- Loading: Skeleton animation

### Study Buddy Components

#### Components to Build:
1. **ResourceCard** - Learning resource display
2. **LearningPathTimeline** - Visual progress tracker
3. **ContributorProfile** - Expert profiles
4. **StudyGroupCard** - Group information
5. **QAThreadCard** - Question/Answer display
6. **LearningCurveChart** - Proficiency over time
7. **CreditBalance** - Earnings dashboard

### Digital Twin Components

#### Components to Build:
1. **MarketHeatmap** - Geographic risk visualization
2. **DisplacementChart** - Occupation predictions
3. **RiskGauge** - Visual risk score (0-100)
4. **ScenarioComparison** - Side-by-side modeling
5. **TrendLineChart** - Historical + projected data

### Economic Copilot Components

#### Components to Build:
1. **JobOfferComparison** - Multi-dimensional analysis
2. **RetirementProjection** - Timeline with milestones
3. **DebtVsReskilling** - ROI visualization
4. **FamilyImpactCard** - Whole-family view
5. **DecisionMatrix** - Weighted factor display

### Gig Economy Components

#### Components to Build:
1. **GigOpportunityCard** - Platform matching
2. **IncomeOptimizer** - Visual scheduler
3. **PortfolioBreakdown** - Earnings by source
4. **BenefitsCalculator** - Cost comparison
5. **ScheduleVisualization** - Hours allocation

### Corporate Components

#### Components to Build:
1. **TransformationDashboard** - Executive overview
2. **JobMatchingTable** - Employee-position pairs
3. **AutomationROI** - Financial impact
4. **RiskHeatmap** - Employee risk scores
5. **UnionSimulator** - Scenario outcomes
6. **FairnessScorecard** - 5-dimension analysis

## 🎯 UI/UX Principles

### 1. Accessibility First (WCAG 2.1 AA)
- 4.5:1 contrast ratio for text
- 3px focus rings on all interactive elements
- Keyboard navigation support
- Screen reader compatibility
- Skip navigation links
- ARIA labels on icons

### 2. Responsive Design
**Breakpoints:**
- xs: 320px (mobile)
- sm: 640px (large mobile)
- md: 768px (tablet)
- lg: 1024px (desktop)
- xl: 1280px (large desktop)
- 2xl: 1536px (ultra-wide)

**Mobile-First Approach:**
- Navigation collapses to drawer
- Cards stack vertically
- Tables become scrollable
- Charts adapt to viewport

### 3. Performance
- Code splitting by route
- Lazy loading for heavy components
- Image optimization with WebP
- Skeleton screens for loading states
- Virtualized lists for large data sets

### 4. Animation Guidelines
- **Fast:** 150ms - Instant feedback (hover, focus)
- **Normal:** 300ms - Standard transitions
- **Slow:** 500ms - Page transitions

**Easing:**
- `ease-out` for entrances
- `ease-in` for exits
- `ease-in-out` for movement

**Honor:** `prefers-reduced-motion` for accessibility

### 5. Progressive Disclosure
- Show essential info first
- Use expand/collapse for details
- Tooltips for additional context
- Step-by-step wizards for complex flows

## 🔧 Implementation Guide

### Setup

```bash
# Install dependencies
npm install @mui/material @mui/icons-material @emotion/react @emotion/styled

# Install additional libraries
npm install recharts axios react-router-dom
```

### Theme Configuration

```jsx
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { designSystem } from './theme/designSystem';

const theme = createTheme({
  palette: {
    primary: {
      main: designSystem.colors.primary[500],
    },
    secondary: {
      main: designSystem.colors.secondary[500],
    },
  },
  typography: {
    fontFamily: designSystem.typography.fontFamily.primary,
  },
  shape: {
    borderRadius: 8,
  },
  shadows: Object.values(designSystem.shadows),
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      {/* Your app */}
    </ThemeProvider>
  );
}
```

### Routing Structure

```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';

<BrowserRouter>
  <Routes>
    <Route path="/" element={<Dashboard />} />

    {/* Digital Twin */}
    <Route path="/digital-twin" element={<DigitalTwinLayout />}>
      <Route path="market" element={<MarketOverview />} />
      <Route path="risk" element={<RiskAssessment />} />
      {/* ... */}
    </Route>

    {/* Study Buddy */}
    <Route path="/study-buddy" element={<StudyBuddyLayout />}>
      <Route path="library" element={<KnowledgeLibrary />} />
      <Route path="paths" element={<LearningPaths />} />
      {/* ... */}
    </Route>

    {/* More routes */}
  </Routes>
</BrowserRouter>
```

### API Integration

```jsx
// services/api.js
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api/v1';

export const api = {
  // Digital Twin
  getMarketRisk: () => axios.get(`${API_BASE}/digital-twin/macro-risk-index`),

  // Study Buddy
  getRecommendations: (userId, params) =>
    axios.post(`${API_BASE}/study-buddy/recommendations/content?user_id=${userId}`, params),

  // Economic Copilot
  analyzeJobOffer: (data) =>
    axios.post(`${API_BASE}/economic-copilot/analyze-job-offer`, data),

  // Gig Economy
  matchGigs: (skills) =>
    axios.post(`${API_BASE}/gig/match-skills-to-gigs`, skills),
};
```

## 📊 Component Examples

### Dashboard Page

```jsx
import MetricCard from './components/Dashboard/MetricCard';
import { Assessment, School, TrendingUp, AttachMoney } from '@mui/icons-material';

<Grid container spacing={3}>
  <Grid item xs={12} sm={6} lg={3}>
    <MetricCard
      title="Automation Risk"
      value="42"
      unit="%"
      trend="down"
      trendValue={-8}
      icon={Assessment}
      color="success"
      sparklineData={[45, 48, 44, 43, 42]}
    />
  </Grid>

  <Grid item xs={12} sm={6} lg={3}>
    <MetricCard
      title="Skills Mastered"
      value="12"
      trend="up"
      trendValue={15}
      icon={School}
      color="primary"
    />
  </Grid>

  <Grid item xs={12} sm={6} lg={3}>
    <MetricCard
      title="Learning Streak"
      value="23"
      unit="days"
      trend="up"
      trendValue={12}
      icon={TrendingUp}
      color="warning"
    />
  </Grid>

  <Grid item xs={12} sm={6} lg={3}>
    <MetricCard
      title="Credits Earned"
      value="$1,250"
      trend="up"
      trendValue={28}
      icon={AttachMoney}
      color="success"
    />
  </Grid>
</Grid>
```

## 🎨 Figma Design Files

**Design System:** [View Figma File](#)
- Color palette swatches
- Typography scale
- Component library with all states
- Iconography set
- Layout templates

**Prototypes:** [View Interactive Prototype](#)
- Full user flows
- Microinteractions
- Responsive breakpoints
- Accessibility annotations

## 🚀 Next Steps

### Phase 1: Core Components (Week 1-2)
- [x] Navigation system
- [x] Metric cards
- [ ] Data tables
- [ ] Chart components (Recharts)
- [ ] Form inputs
- [ ] Modal dialogs

### Phase 2: Feature Pages (Week 3-4)
- [ ] Dashboard home
- [ ] Digital Twin pages
- [ ] Study Buddy platform
- [ ] Economic Copilot tools
- [ ] Gig economy features

### Phase 3: Interactions (Week 5-6)
- [ ] Agent chat interface
- [ ] Real-time notifications
- [ ] Progress animations
- [ ] Gamification elements
- [ ] Social features

### Phase 4: Polish (Week 7-8)
- [ ] Performance optimization
- [ ] Accessibility audit
- [ ] Cross-browser testing
- [ ] Mobile refinement
- [ ] Documentation completion

## 📚 Resources

- **Material-UI Docs:** https://mui.com
- **Design System:** `frontend/src/theme/designSystem.js`
- **Figma Templates:** [Link to designs]
- **Component Storybook:** [Link when built]
- **API Documentation:** `README.md` sections 40-50

---

**Built with ❤️ using AI-designed systems**
*UI Designer Agent + Marketing Agent + Design Tokens*
