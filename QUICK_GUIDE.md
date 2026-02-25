# 🚀 GUIDE RAPIDE - LANCER LE PROJET

## ⚡ EN 2 MINUTES

### Terminal 1 - Backend
```powershell
cd "d:\Documents\Tuteur intelligent"
python manage.py runserver
```

**Résultat attendu:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Terminal 2 - Frontend
```powershell
cd "d:\Documents\Tuteur intelligent\Frontend"
npm run dev
```

**Résultat attendu:**
```
  VITE v7.3.1  ready in 6 seconds
  ➜  Local:   http://localhost:5174/
```

---

## 🌐 ACCÉDER À L'APPLICATION

```
Frontend:  http://localhost:5174
Backend:   http://127.0.0.1:8000
Admin:     http://127.0.0.1:8000/admin
API:       http://127.0.0.1:8000/api/
```

---

## 🔑 PREMIERS PAS

### 1️⃣ SE CONNECTER
```
Username: alice
Password: 123456
→ Dashboard
```

### 2️⃣ CRÉER UN COMPTE
```
Cliquer "✍️ Créer un compte"
Remplir formulaire
Cliquer "✅ Créer le compte"
→ Compte créé!
```

### 3️⃣ MOT DE PASSE OUBLIÉ
```
Cliquer "🔑 Mot de passe oublié?"
Étape 1: Email
Étape 2: Username + nouveau MDP
→ Réinitialisé!
```

---

## ✨ NOUVEAUTÉS

✅ Page connexion rénovée
✅ Création de compte complète (7 attributs)
✅ Récupération mot de passe en 2 étapes
✅ Design moderne & responsive
✅ Validation d'erreurs
✅ 3 comptes de test pré-créés

---

## 📚 DOCUMENTATION

- [AUTHENTICATION_GUIDE.md](AUTHENTICATION_GUIDE.md) - Documentation technique complète
- [DEMO_GUIDE.md](DEMO_GUIDE.md) - Tutoriel et scénarios de test
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Résumé des changements
- [CHANGELOG.md](CHANGELOG.md) - Historique des versions

---

## 🔧 COMMANDES UTILES

### Créer des données de test ("Populate DB")
```bash
python manage.py populate_db
```

### Migrations de base de données
```bash
python manage.py makemigrations   # Créer migration
python manage.py migrate           # Appliquer migration
```

### Admin Django
```
URL: http://127.0.0.1:8000/admin
Username: admin
Password: admin
```

### Arrêter les serveurs
```
Backend:  Ctrl+C dans Terminal 1
Frontend: Ctrl+C dans Terminal 2
```

---

## ❓ BESOIN D'AIDE?

### Erreur: "Port déjà utilisé"
```bash
# Backend sur port 8000
python manage.py runserver 0.0.0.0:8001

# Frontend automatiquement sur 5174 si 5173 utilisé
```

### Erreur: "Module not found"
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

### Erreur: "Base de données"
```bash
python manage.py migrate
python manage.py populate_db
```

---

## ✅ CHECKLIST AVANT COMPÉTITION

- [ ] Backend tourne sur 127.0.0.1:8000
- [ ] Frontend tourne sur localhost:5174
- [ ] Se connecter avec alice/123456 fonctionne
- [ ] Créer un compte fonctionne
- [ ] Mot de passe oublié fonctionne
- [ ] Dashboard s'affiche après connexion
- [ ] Leçons visibles
- [ ] Exercices jouables
- [ ] Leaderboard marche
- [ ] Statistiques marche
- [ ] Pas d'erreurs console (F12)
- [ ] Pas d'erreurs dans les terminaux

---

**🎉 Vous êtes prêt pour la compétition!**

