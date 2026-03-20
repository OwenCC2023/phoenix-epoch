import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import LobbyListPage from './pages/LobbyListPage';
import GameLobbyPage from './pages/GameLobbyPage';
import NationCreatePage from './pages/NationCreatePage';
import GameDashboardPage from './pages/GameDashboardPage';
import AdminPanelPage from './pages/AdminPanelPage';
import ProtectedRoute from './components/ProtectedRoute';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/games"
          element={
            <ProtectedRoute>
              <LobbyListPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/games/:id"
          element={
            <ProtectedRoute>
              <GameLobbyPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/games/:gameId/create-nation"
          element={
            <ProtectedRoute>
              <NationCreatePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/games/:gameId/dashboard"
          element={
            <ProtectedRoute>
              <GameDashboardPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/games/:gameId/admin"
          element={
            <ProtectedRoute>
              <AdminPanelPage />
            </ProtectedRoute>
          }
        />
        <Route path="/" element={<Navigate to="/games" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
