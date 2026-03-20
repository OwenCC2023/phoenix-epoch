import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import useAuthStore from '../store/authStore';

export default function RegisterPage() {
  const register = useAuthStore((s) => s.register);
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await register(username, email, password, displayName || undefined);
      navigate('/login');
    } catch {
      setError('Registration failed. Username or email may already be taken.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0f0f0f] flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <h1 className="text-amber-500 text-3xl font-bold text-center mb-2 tracking-wide">
          Phoenix Epoch
        </h1>
        <p className="text-gray-500 text-center text-sm mb-8">
          Create your account and join the new world.
        </p>

        <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-6">
          <h2 className="text-gray-200 text-lg font-semibold mb-4">Register</h2>

          {error && (
            <div className="bg-red-500/10 border border-red-500/30 text-red-400 text-sm rounded p-3 mb-4">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-gray-400 text-sm mb-1">Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                autoFocus
                className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm focus:outline-none focus:border-amber-500/50"
              />
            </div>

            <div>
              <label className="block text-gray-400 text-sm mb-1">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm focus:outline-none focus:border-amber-500/50"
              />
            </div>

            <div>
              <label className="block text-gray-400 text-sm mb-1">Display Name</label>
              <input
                type="text"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                placeholder="Optional"
                className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm placeholder:text-gray-600 focus:outline-none focus:border-amber-500/50"
              />
            </div>

            <div>
              <label className="block text-gray-400 text-sm mb-1">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm focus:outline-none focus:border-amber-500/50"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-amber-600 text-white rounded py-2 text-sm font-medium hover:bg-amber-700 transition-colors disabled:opacity-50 cursor-pointer"
            >
              {loading ? 'Creating account...' : 'Create Account'}
            </button>
          </form>

          <p className="text-gray-500 text-sm text-center mt-4">
            Already have an account?{' '}
            <Link to="/login" className="text-amber-500 hover:text-amber-400">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
