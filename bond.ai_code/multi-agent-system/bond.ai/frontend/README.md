# Bond.AI Frontend

Professional and friendly React frontend for the Bond.AI platform - AI-powered connection intelligence.

## Features

- 🎨 **Modern Design**: Beautiful, professional UI with Tailwind CSS
- 🤖 **Welcoming Chatbot**: AI assistant to guide users
- 📱 **Responsive**: Works seamlessly on desktop, tablet, and mobile
- ⚡ **Fast**: Built with Vite for lightning-fast development
- 🔐 **Secure**: JWT authentication with protected routes
- 🔄 **Real-time**: WebSocket integration for instant notifications
- 🎭 **Animated**: Smooth animations with Framer Motion
- 📊 **Dashboard**: Comprehensive overview of matches and connections
- 🎯 **Onboarding**: Multi-step flow for needs and offerings
- 💬 **Chat**: Agent-to-agent negotiation interface

## Tech Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Routing**: React Router v6
- **State Management**: Zustand
- **Data Fetching**: TanStack Query (React Query)
- **Forms**: React Hook Form + Zod validation
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **WebSocket**: Socket.IO Client
- **Notifications**: React Hot Toast

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running (see `bond.ai/server/`)

### Installation

```bash
cd bond.ai/frontend
npm install
```

### Configuration

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
VITE_API_URL=http://localhost:3005
VITE_WS_URL=ws://localhost:3005
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
npm run preview  # Preview production build
```

## Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # Reusable components
│   │   └── ChatbotWidget.tsx
│   ├── pages/           # Page components
│   │   ├── LandingPage.tsx
│   │   ├── LoginPage.tsx
│   │   ├── SignupPage.tsx
│   │   ├── OnboardingPage.tsx
│   │   ├── DashboardPage.tsx
│   │   ├── MatchesPage.tsx
│   │   ├── ConnectionsPage.tsx
│   │   └── ProfilePage.tsx
│   ├── lib/             # Utilities and services
│   │   ├── api.ts       # API client
│   │   ├── socket.ts    # WebSocket service
│   │   └── utils.ts     # Utility functions
│   ├── store/           # State management
│   │   └── authStore.ts
│   ├── types/           # TypeScript types
│   │   └── index.ts
│   ├── App.tsx          # Main app component
│   ├── main.tsx         # Entry point
│   └── index.css        # Global styles
├── index.html
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── vite.config.ts
```

## Key Pages

### Landing Page
- Hero section with value proposition
- How it works section
- Features showcase
- Call-to-action

### Onboarding
- Multi-step form (4 steps)
- Basic info (name, bio, industry, location)
- Needs (what you're looking for)
- Offerings (what you can provide)
- Review and submit

### Dashboard
- Overview of matches and connections
- Stats cards
- Recent matches list
- Activity feed
- Agent status indicator

### Matches
- List of AI-curated matches
- Filter by status
- Search functionality
- Match score visualization
- Accept/reject actions

### Connections
- Active partnerships
- Agreed terms display
- Connection status
- Messaging interface

### Profile
- User information
- Needs and offerings display
- Edit profile link

## Components

### Chatbot Widget
- Floating chat button
- Minimizable chat window
- AI-powered responses
- Suggested questions
- Typing indicators
- Message history

### Features
- Responsive design (mobile-first)
- Smooth animations on scroll
- Loading states
- Error handling
- Toast notifications
- WebSocket real-time updates

## Styling

Uses Tailwind CSS with custom configuration:

- **Primary Colors**: Blue shades for main brand
- **Secondary Colors**: Purple/pink gradient for accents
- **Accent Colors**: Orange for highlights
- **Typography**: Inter font family
- **Custom Components**: Buttons, inputs, cards
- **Animations**: Fade-in, slide-up, scale-in

## API Integration

All API calls are in `src/lib/api.ts`:

- **Auth**: Register, login, logout
- **Profile**: Get/update profile, onboarding
- **Matching**: Get matches, accept/reject
- **Negotiations**: View proposals, respond
- **Connections**: Get connections
- **Notifications**: Get/mark read
- **LinkedIn**: OAuth integration
- **Chatbot**: Send messages

## State Management

- **Auth Store** (Zustand): User authentication state
- **React Query**: Server state caching and syncing
- **Local State**: Component-level state with useState

## Real-time Features

WebSocket events handled:
- `notification`: New notifications
- `match:update`: Match status changes
- `negotiation:update`: Negotiation updates

## Development Tips

1. **Hot Reload**: Vite provides instant HMR
2. **TypeScript**: Strict mode enabled for type safety
3. **Linting**: ESLint configured for code quality
4. **Code Organization**: Features grouped by domain

## Deployment

### Vercel (Recommended)
```bash
npm run build
# Deploy dist/ folder
```

### Netlify
```bash
npm run build
# Deploy dist/ folder with redirects for SPA
```

### Docker
```bash
docker build -t bond-ai-frontend .
docker run -p 5173:80 bond-ai-frontend
```

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers

## License

Proprietary - Bond.AI Platform

## Support

For issues or questions, contact the development team.
