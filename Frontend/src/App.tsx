import { useEffect, useState } from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';

import Loader from './common/Loader';

import SignIn from './pages/Authentication/SignIn';
import SignUp from './pages/Authentication/SignUp';

import TuteurDashboard from './pages/Dashboard/TuteurDashboard';
import TuteurIA from './pages/Tuteur/TuteurIA';
import Profile from './pages/Prolife/Profile';
import Settings from './pages/Settings';
import Statistiques from './pages/Statistiques/Statistiques';

import Lecons from './pages/Lecons';
import LeconDetail from './pages/Lecons/LeconDetail';
import Exercices from './pages/Exercices/Exercices';
import ExerciceDetail from './pages/Exercices/ExerciceDetail';
import Leaderboard from './pages/Leaderboard/Leaderboard';

import DefaultLayout, { AuthLayout } from './layout/DefaultLayout';

function App() {
  const [loading, setLoading] = useState(true);
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 800);
    return () => clearTimeout(timer);
  }, []);

  if (loading) return <Loader />;

  return (
    <Routes>

      {/* AUTH */}
      <Route element={<AuthLayout />}>
        <Route path="/auth/signin" element={<SignIn />} />
        <Route path="/auth/signup" element={<SignUp />} />
      </Route>

      {/* APP */}
      <Route element={<DefaultLayout />}>
        <Route index element={<TuteurDashboard />} />
        <Route path="/tuteur" element={<TuteurIA />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/statistiques" element={<Statistiques />} />

        <Route path="/lecons" element={<Lecons />} />
        <Route path="/lecons/:id" element={<LeconDetail />} />

        {/* Routes exercices */}
        <Route path="/exercices/:leconId" element={<Exercices />} />
        <Route path="/exercices/:id" element={<ExerciceDetail />} />

        {/* Leaderboard */}
        <Route path="/leaderboard" element={<Leaderboard />} />
      </Route>

    </Routes>
  );
}

export default App;


