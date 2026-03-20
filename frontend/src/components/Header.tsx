import { Link, useNavigate } from 'react-router-dom';
import useAuthStore from '../store/authStore';

export default function Header() {
  const { user, isAuthenticated, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="bg-[#1a1a1a] border-b border-[#2a2a2a]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-8">
            <Link to="/games" className="text-amber-500 font-bold text-xl tracking-wide">
              Phoenix Epoch
            </Link>
            {isAuthenticated && (
              <nav className="flex gap-4">
                <Link
                  to="/games"
                  className="text-gray-400 hover:text-amber-500 transition-colors text-sm font-medium"
                >
                  Games
                </Link>
              </nav>
            )}
          </div>

          {isAuthenticated && user && (
            <div className="flex items-center gap-4">
              <span className="text-gray-300 text-sm">
                {user.display_name || user.username}
              </span>
              <button
                onClick={handleLogout}
                className="text-gray-400 hover:text-amber-500 transition-colors text-sm font-medium cursor-pointer"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
