# 🎬 TUTORIEL - NOUVEAU SYSTÈME D'AUTHENTIFICATION

## DÉMO COMPLÈTE

---

## 📍 ÉTAPE 1: PAGE DE CONNEXION AMÉLIORÉE

### Ce que vous verriez à l'écran:

```
┌─────────────────────────────────────────────────────────┐
│  CÔTÉ GAUCHE (Desktp) │         CÔTÉ DROIT              │
│                       │                                  │
│ 🎓 TUTEUR INTELLIGENT │  ┌──────────────────────────┐   │
│                       │  │   Connexion              │   │
│ Bienvenue dans votre  │  └──────────────────────────┘   │
│ plateforme           │                                   │
│ d'apprentissage      │  Nom d'utilisateur *             │
│                       │  [  alice/bob/charlie  ]         │
│ 📚 Leçons adaptées    │                                  │
│ 🚀 Progression rapide │  Mot de passe *                  │
│ 🏆 Compétition        │  [     ••••••••       ]          │
│                       │                                  │
│                       │  ┌─ SE CONNECTER ──────┐        │
│                       │  │ (Gradient bleu)     │        │
│                       │  └─────────────────────┘        │
│                       │                                  │
│                       │  ┌─ MOT DE PASSE OUBLIÉ? ───┐   │
│                       │  │ (Lien texte)              │   │
│                       │  └──────────────────────────┘    │
│                       │                                  │
│                       │            OU                    │
│                       │                                  │
│                       │  ┌─ CRÉER UN COMPTE ────────┐   │
│                       │  │ (Bouton gris)            │   │
│                       │  └──────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

---

## 👤 ÉTAPE 2: CRÉER UN NOUVEAU COMPTE

### 2.1 Cliquer sur "✍️ Créer un compte"

```
┌────────────────────────────────────────────────┐
│ ✕ ✍️ Créer un compte                           │
├────────────────────────────────────────────────┤
│                                                │
│ 📱 IDENTIFIANTS                                │
│ ┌────────────────────────────────────────────┐│
│ │ Nom d'utilisateur *         │newuser      ││
│ │ Email *                     │new@mail.com  ││
│ └────────────────────────────────────────────┘│
│                                                │
│ 👤 INFORMATIONS PERSONNELLES                   │
│ ┌────────────────────────────────────────────┐│
│ │ Prénom *           │Tom                    ││
│ │ Nom *              │Dupont                 ││
│ │ Date de naissance* │15/05/2011             ││
│ │ Niveau *           │▼ Débutant             ││
│ └────────────────────────────────────────────┘│
│                                                │
│ 📞 INFORMATIONS ADDITIONNELLES                 │
│ ┌────────────────────────────────────────────┐│
│ │ Email parent (opt) │parent@mail.com        ││
│ │ Téléphone (opt)    │+33612345678           ││
│ └────────────────────────────────────────────┘│
│                                                │
│ 🔒 MOT DE PASSE                                │
│ ┌────────────────────────────────────────────┐│
│ │ Mot de passe *     │••••••••••             ││
│ │ Confirmer *        │••••••••••             ││
│ └────────────────────────────────────────────┘│
│                                                │
│ [Annuler]              [✅ Créer le compte]   │
│                                                │
│ * Champs obligatoires                          │
└────────────────────────────────────────────────┘
```

### 2.2 Actions possibles:

```
✅ Remplir tous les champs obligatoires
   → Prénom, Nom, Email, Mot de passe, Niveau

❌ Oublier un champ → Message d'erreur rouge
   "Le prénom est requis"

❌ Entrer un email invalide → Erreur
   "Email invalide"

❌ Mots de passe différents → Erreur
   "Les mots de passe ne correspondent pas"

❌ Mot de passe court → Erreur
   "Le mot de passe doit avoir au moins 6 caractères"

❌ Username déjà pris → Erreur
   "Cet utilisateur existe déjà"

✅ Tout correct → Message de succès VERT
   "✅ Compte créé avec succès!"
   → Modale se ferme
   → Vous êtes redirigé à la connexion
```

---

## 🔑 ÉTAPE 3: MOT DE PASSE OUBLIÉ

### 3.1 Cliquer sur "🔑 Mot de passe oublié?"

```
ÉTAPE 1: RÉCUPÉRATION
┌────────────────────────────────────┐
│ ✕ 🔑 Récupérer mon compte          │
├────────────────────────────────────┤
│                                    │
│ Entrez votre email pour recevoir   │
│ un lien de réinitialisation.       │
│                                    │
│ Email                              │
│ [  alice@test.com  ]               │
│                                    │
│ [Annuler]    [📧 Envoyer]          │
│                                    │
│ 💡 Astuce:                         │
│ Si vous avez accès à votre nom     │
│ d'utilisateur, vous pouvez...      │
└────────────────────────────────────┘

↓ APRÈS VALIDATION ↓

ÉTAPE 2: RÉINITIALISATION
┌────────────────────────────────────┐
│ ✕ 🔑 Récupérer mon compte          │
├────────────────────────────────────┤
│                                    │
│ Réinitialisez votre mot de passe   │
│ avec votre nom d'utilisateur.      │
│                                    │
│ Nom d'utilisateur                  │
│ [  alice  ]                        │
│                                    │
│ Nouveau mot de passe               │
│ [  •••••••••••  ]                  │
│                                    │
│ Confirmer le mot de passe          │
│ [  •••••••••••  ]                  │
│                                    │
│ [← Retour]   [🔓 Réinitialiser]    │
└────────────────────────────────────┘
```

### 3.2 Validation mot de passe oublié:

```
✅ Email fourni → Confirmation
   "Si ce compte existe, vous recevrez un email"

✅ Infos réinit complètes → Succès
   "✅ Mot de passe réinitialisé avec succès"
   → Modale se ferme

❌ Mots de passe ne correspondent pas → Erreur
   "Les mots de passe ne correspondent pas"

❌ Mot de passe court → Erreur
   "Le mot de passe doit avoir au moins 6 caractères"
```

---

## 🎯 ÉTAPE 4: SE CONNECTER AVEC LE NOUVEAU COMPTE

### 4.1 Sur la page principale:

```
Nom d'utilisateur: newuser
Mot de passe: (celui créé)

[🔓 SE CONNECTER]

↓

Redirected to dashboard ✅
```

---

## 📊 SCÉNARIOS DE TEST COMPLETS

### SCÉNARIO 1: Création de compte réussie

```
1. Cliquer "✍️ Créer un compte"
2. Remplir:
   - Prenom: Marie
   - Nom: Leblanc
   - Username: marielb
   - Email: marie@school.fr
   - Date naissance: 01/06/2012
   - Niveau: Intermédiaire
   - Parent email: parent@mail.com
   - Tel: +33699887766
   - Password: School123
   - Confirm: School123
3. Cliquer "✅ Créer le compte"
4. ✅ Message vert "Compte créé avec succès"
5. Se connecter avec marielb / School123
6. ✅ Dashboard affiche la bienvenue
```

### SCÉNARIO 2: Validation d'erreurs

```
1. Cliquer "✍️ Créer un compte"
2. Remplir:
   - Prenom: Jean
   - Email: invalidemail  (❌ EMAIL INVALIDE)
   - Password: 123       (❌ TROP COURT)
   - Confirm: 456        (❌ PAS ÉGAL)
3. Cliquer "✅ Créer le compte"
4. ❌ Affiche 3 erreurs:
   - "Email invalide"
   - "Le mot de passe doit avoir au moins 6 caractères"
   - "Les mots de passe ne correspondent pas"
5. Corriger les erreurs une par une
6. Remplir les champs obligatoires restants (prénom, nom, etc.)
7. Cliquer à nouveau
8. ✅ Réussi!
```

### SCÉNARIO 3: Récupération mot de passe oublié

```
1. Sur page connexion, cliquer "🔑 Mot de passe oublié?"
2. Étape 1: Entrer alice@test.com
3. ✅ Message: "Email envoyé..."
4. Étape 2 apparaît
5. Entrer username: alice
6. Nouveau mol de passe: NewPassword123
7. Confirmer: NewPassword123
8. Cliquer "🔓 Réinitialiser"
9. ✅ Message: "Mot de passe réinitialisé avec succès"
10. Retour page connexion
11. Se connecter: alice / NewPassword123
12. ✅ Accès au dashboard
```

### SCÉNARIO 4: Testez tous les comptes pré-créés

```
Compte 1: alice / 123456
   → Niveau: Débutant
   → Email: alice@test.com
   → Dashboard de débutant

Compte 2: bob / 123456
   → Niveau: Intermédiaire
   → Email: bob@test.com
   → Contenu intermédiaire

Compte 3: charlie / 123456
   → Niveau: Avancé
   → Email: charlie@test.com
   → Contenu avancé
```

---

## 🔍 VÉRIFICATIONS FINALES

### Checklist de Qualité:

- [ ] Connexion fonctionne avec les 3 comptes de test
- [ ] Création de compte sauvegarde tous les attributs
- [ ] Validation des erreurs affichées correctement
- [ ] Design responsive sur mobile
- [ ] Modales s'ouvrent et se ferment
- [ ] Messages d'erreur/succès visibles
- [ ] Redirection vers dashboard après connexion
- [ ] Niveau sélectionné apparaît dans le profil
- [ ] Email parent optionnel
- [ ] Mot de passe oublié réinitialise correctement

### Performance:

- [ ] Pas d'erreurs dans la console (F12)
- [ ] Pas d'erreurs dans le terminal backend
- [ ] Chargement < 2 secondes
- [ ] Réponses API < 1 seconde

---

## 🐛 TROUBLESHOOTING

### Problème: Page blanche

```
Solution:
1. Vérifier que npm run dev est lancé
2. Vérifier http://localhost:5174
3. Appuyer F5 pour rafraîchir
```

### Problème: "Impossible de se connecter au backend"

```
Solution:
1. Vérifier que python manage.py runserver est en cours
2. Vérifier http://127.0.0.1:8000/api/
3. Vérifier les CORS en settings.py
```

### Problème: "Compte déjà existant"

```
Solution:
- Utiliser un autre username
- Ou supprimer le compte via Django admin (/admin)
```

### Problème: Mot de passe oublié ne fonctionne pas

```
Solution:
1. Vérifier que le username est exact
2. Vérifier que les mots de passe correspondent
3. Vérifier que moti de passe ≥ 6 caractères
```

---

## 🎉 RÉSULTAT FINAL

✅ **Système d'authentification professionnel et complet**
✅ **Design moderne et réactif**
✅ **Validation complète des données**
✅ **Sécurité pour la compétition**
✅ **UX/UI exceptionnelle**

**Prêt pour la compétition! 🏆**

