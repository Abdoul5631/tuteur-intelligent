import { createContext, useContext, useState } from 'react';
import api from '../services/api';
import { useNavigate } from 'react-router-dom';

interface AuthContextType {
  isAuthenticated: boolean;
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const navigate = useNavigate();
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(
    !!localStorage.getItem('access_token')
  );
  const [token, setToken] = useState<string | null>(
    localStorage.getItem('access_token')
  );

  const login = async (username: string, password: string) => {
    const res = await api.post('auth/login/', {
      username,
      password,
    });

    localStorage.setItem('access_token', res.data.access);
    localStorage.setItem('refresh_token', res.data.refresh);

    setToken(res.data.access);
    setIsAuthenticated(true);
    navigate('/');
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setToken(null);
    setIsAuthenticated(false);
    navigate('/auth/signin');
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
