import { NavLink } from 'react-router-dom';
import type { FC, ReactNode } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';

interface SidebarProps {
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
}

const Sidebar: FC<SidebarProps> = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    const confirm = window.confirm('Voulez‑vous vraiment vous déconnecter ?');
    if (!confirm) return;

    logout();
    navigate('/auth/signin');
  };

  return (
    <aside className="hidden h-screen w-64 bg-slate-900 text-white lg:flex flex-col">
      {/* ===== Logo ===== */}
      <div className="px-6 py-6 text-xl font-bold border-b border-slate-700">
        🎓 Tuteur Intelligent
      </div>

      {/* ===== Menu ===== */}
      <nav className="flex-1 px-4 py-6 space-y-6">
        {/* ===== Navigation ===== */}
        <div>
          <p className="mb-3 text-xs uppercase text-slate-400">Navigation</p>

          <SidebarLink
            to="/"
            icon={<span>🏠</span>}
            label="Dashboard"
          />

          <SidebarLink
            to="/lecons"
            icon={<span>📘</span>}
            label="Leçons"
          />

          <SidebarLink
            to="/leaderboard"
            icon={<span>🏆</span>}
            label="Classement"
          />

          <SidebarLink
            to="/statistiques"
            icon={<span>📊</span>}
            label="Statistiques"
          />
        </div>

        {/* ===== Compte ===== */}
        <div>
          <p className="mb-3 text-xs uppercase text-slate-400">Compte</p>

          <SidebarLink
            to="/profile"
            icon={<span>👤</span>}
            label="Profil"
          />

          <SidebarLink
            to="/settings"
            icon={<span>⚙️</span>}
            label="Paramètres"
          />
        </div>

        {/* ===== Authentification ===== */}
        <div>
          <p className="mb-3 text-xs uppercase text-slate-400">Authentification</p>

          <button
  onClick={handleLogout}
  className="flex w-full items-center gap-3 rounded-lg px-4 py-2.5 text-sm font-medium text-slate-300 transition hover:bg-slate-800 hover:text-white"
>
  <span>🔓</span>
  Déconnexion
</button>

        </div>
      </nav>
    </aside>
  );
};

export default Sidebar;

/* ===== Composant lien ===== */
interface SidebarLinkProps {
  to: string;
  icon: ReactNode;
  label: string;
}

const SidebarLink: FC<SidebarLinkProps> = ({ to, icon, label }) => {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `flex items-center gap-3 rounded-lg px-4 py-2.5 text-sm font-medium transition
        ${
          isActive
            ? 'bg-primary text-white'
            : 'text-slate-300 hover:bg-slate-800 hover:text-white'
        }`
      }
    >
      {icon}
      {label}
    </NavLink>
  );
};
