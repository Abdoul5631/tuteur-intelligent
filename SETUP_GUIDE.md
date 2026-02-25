# 🎓 Guide de configuration - Tuteur Intelligent

## ✅ Qu'est-ce qui a été fait

J'ai restructuré et complété votre projet pour avoir une application fonctionnelle complète:

### Backend (Django + DRF)
- ✅ **API d'inscription**: Nouveau endpoint `/api/auth/register/` avec validation
- ✅ **Authentification JWT**: Configuration correcte dans `settings.py`
- ✅ **Endpoints utilisateur**: 
  - `/api/me/` - Profil utilisateur
  - `/api/progression/` - Progression et statistiques
  - `/api/exercices/recommandations/` - Exercices adaptés au niveau
- ✅ **Données de test**: Commande Django pour peupler la BD avec 5 leçons et 15 exercices

### Frontend (React + TypeScript)
- ✅ **Page SignUp**: Formulaire complet d'inscription avec validation
- ✅ **Dashboard**: Intégration API réelle, affichage progression
- ✅ **Page Leçons**: Affichage élégant des leçons avec navigation
- ✅ **Page Exercices**: Interface exercice par exercice avec feedback
- ✅ **Gestion JWT**: Interceptors pour refresh token automatique

### Configuration
- ✅ CORS activé pour communication client-serveur
- ✅ JWT par défaut pour authentification
- ✅ Routes alignées et testables

---

## 🚀 Lancer le projet

### 1️⃣ Backend - Configuration initiale (première fois seulement)

```bash
# Aller dans le répertoire backend
cd "d:\Documents\Tuteur intelligent"

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur (admin)
python manage.py createsuperuser
# Suivre les prompts (username, email, password)

# 🔥 PEUPLER LA BD AVEC LES DONNÉES DE TEST
python manage.py populate_db

# Lancer le serveur
python manage.py runserver
```

Backend tournera sur: **http://127.0.0.1:8000**

### 2️⃣ Frontend - Démarrer le serveur de développement

```bash
# Dans un AUTRE terminal, aller au dossier Frontend
cd "d:\Documents\Tuteur intelligent\Frontend"

# Installer les dépendances
npm install

# Lancer le serveur Vite
npm run dev
```

Frontend tournera sur: **http://localhost:5173** (ou affichera l'URL dans le terminal)

---

## 🧪 Tester l'application

### 1. Inscription
- Aller à `http://localhost:5173/auth/signup` (ou le lien dans le terminal)
- Créer un compte avec:
  - Username: `test_user`
  - Email: `test@example.com`
  - Password: `password123`
  - Niveau: `Débutant`

### 2. Connexion
- Vous êtes redirigé vers la page de login
- Entrer vos identifiants → vous êtes redirigé au Dashboard

### 3. Tester les fonctionnalités
- **Dashboard**: Voir progression, recommandations
- **Leçons**: Cliquer sur "Commencer cette leçon"
- **Exercices**: Répondre aux questions et voir les feedbacks
- **Résultats**: Voir le résumé à la fin

---

## 🔑 Comptes de test pré-créés

Après `populate_db`, vous pouvez tester avec:

- **alice** / `123456`
- **bob** / `123456`
- **charlie** / `123456`

Tous au niveau "Débutant"

---

## 📁 Structure des fichiers modifiés/créés

### Backend
```
core/
  ├── views.py ✏️ (ajout API inscription, profil, progression)
  ├── urls.py ✏️ (nouvelles routes)
  └── management/commands/
      └── populate_db.py ✨ (nouvelle commande de test)
backend/
  └── settings.py ✏️ (JWT + REST_FRAMEWORK config)
```

### Frontend
```
src/
  ├── pages/
  │   ├── Authentication/
  │   │   └── SignUp.tsx ✏️ (formulaire complet)
  │   ├── Dashboard/
  │   │   └── TuteurDashboard.tsx ✏️ (intégration API)
  │   ├── Lecons/
  │   │   └── Lecons.tsx ✏️ (UI améliorée)
  │   └── Exercices/
  │       └── Exercices.tsx ✏️ (UI complète + logic)
  ├── services/
  │   ├── api.ts ✏️ (JWT + refresh token interceptor)
  │   └── refreshToken.ts ✓
  └── App.tsx ✏️ (routes corrigées)
```

---

## 🐛 Dépannage

### Erreur: "Module not found" en backend
```bash
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
python manage.py migrate
```

### Erreur: "Cannot POST /api/auth/login/"
- Vérifier que le backend tourne: `python manage.py runserver`
- Vérifier les logs Django pour les erreurs

### Erreur: "CORS error" en frontend
- Vérifier `CORS_ALLOW_ALL_ORIGINS = True` dans `settings.py`
- Redémarrer le backend après modification

### Token invalide / Non authentifié
- Supprimer les tokens du localStorage (DevTools > Application > LocalStorage)
- Se reconnecter

---

## 📝 Fichier requirements.txt

Si vous n'avez pas ce fichier, créez-le avec:

```
Django==6.0.1
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.0
```

Puis:
```bash
pip install -r requirements.txt
```

---

## 🎉 C'est prêt!

L'application est maintenant **complète et fonctionnelle**. Tous les composants (inscription, authentification, leçons, exercices, progression) sont intégrés et testables.

**Suggestions pour la suite**:
1. Ajouter des vraies leçons avec du contenu pédagogique
2. Intégrer une vraie IA (OpenAI) pour la correction
3. Ajouter un système de badges/récompenses
4. Implémenter un système de notifications
5. Améliorer l'expérience utilisateur avec animations

Bon apprentissage! 🚀
