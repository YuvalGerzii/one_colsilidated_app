import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store/authStore';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import OnboardingPage from './pages/OnboardingPage';
import DashboardPage from './pages/DashboardPage';
import MatchesPage from './pages/MatchesPage';
import ConnectionsPage from './pages/ConnectionsPage';
import ProfilePage from './pages/ProfilePage';
import ChatbotWidget from './components/ChatbotWidget';

function App() {
  const { isAuthenticated, user } = useAuthStore();

  return (
    <>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={isAuthenticated ? <Navigate to="/dashboard" /> : <LoginPage />} />
        <Route path="/signup" element={isAuthenticated ? <Navigate to="/onboarding" /> : <SignupPage />} />

        {/* Protected routes */}
        <Route
          path="/onboarding"
          element={isAuthenticated ? <OnboardingPage /> : <Navigate to="/login" />}
        />
        <Route
          path="/dashboard"
          element={isAuthenticated ? <DashboardPage /> : <Navigate to="/login" />}
        />
        <Route
          path="/matches"
          element={isAuthenticated ? <MatchesPage /> : <Navigate to="/login" />}
        />
        <Route
          path="/connections"
          element={isAuthenticated ? <ConnectionsPage /> : <Navigate to="/login" />}
        />
        <Route
          path="/profile"
          element={isAuthenticated ? <ProfilePage /> : <Navigate to="/login" />}
        />

        {/* Catch all */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>

      {/* Global chatbot - shows on all pages */}
      <ChatbotWidget />
    </>
  );
}

export default App;
