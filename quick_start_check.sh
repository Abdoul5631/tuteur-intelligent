#!/bin/bash

# 🚀 QUICK START - TUTEUR INTELLIGENT IA
# Exécutez ce script pour vérifier que tout fonctionne

echo "🎓 Tuteur Intelligent - IA Integration Quick Start"
echo "=================================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# Fonction pour tester
check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
        ERRORS=$((ERRORS+1))
    fi
}

check_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    WARNINGS=$((WARNINGS+1))
}

# ========================================
# 1. VÉRIFICATIONS SYSTÈME
# ========================================
echo "1️⃣ Vérification du système..."
echo "---"

# Python
python --version > /dev/null 2>&1
check "Python installé"

# Node
node --version > /dev/null 2>&1
check "Node.js installé"

# npm
npm --version > /dev/null 2>&1
check "npm installé"

# Django
python -c "import django; print(django.get_version())" > /dev/null 2>&1
check "Django installé"

# React
cd Frontend 2>/dev/null && npm list react > /dev/null 2>&1
check "React installé"
cd ..

echo ""

# ========================================
# 2. VÉRIFICATIONS FICHIERS
# ========================================
echo "2️⃣ Vérification des fichiers créés..."
echo "---"

# Backend
[ -f "core/services/llm_service.py" ]
check "Service LLM créé (llm_service.py)"

[ -f "core/ia_endpoints.py" ]
check "Endpoints IA créés (ia_endpoints.py)"

[ -f "core/migrations/0007_ia_integration.py" ]
check "Migration IA créée (0007_ia_integration.py)"

# Frontend
[ -f "Frontend/src/components/Chat/ChatIA.tsx" ]
check "Composant Chat créé (ChatIA.tsx)"

[ -f "Frontend/src/pages/Tuteur/TuteurIA.tsx" ]
check "Page Tuteur créée (TuteurIA.tsx)"

[ -f "Frontend/src/services/iaService.ts" ]
check "Service IA créé (iaService.ts)"

# Documentation
[ -f "IA_INTEGRATION_PLAN.md" ]
check "Plan d'intégration (IA_INTEGRATION_PLAN.md)"

[ -f "IMPLEMENTATION_IA_COMPLETE.md" ]
check "Implementation guide (IMPLEMENTATION_IA_COMPLETE.md)"

[ -f "FILES_STRUCTURE.md" ]
check "Structure fichiers (FILES_STRUCTURE.md)"

[ -f "DELIVERABLE_IA.md" ]
check "Deliverable document (DELIVERABLE_IA.md)"

echo ""

# ========================================
# 3. VÉRIFICATIONS DÉPENDANCES
# ========================================
echo "3️⃣ Vérification des dépendances..."
echo "---"

python -c "import openai" > /dev/null 2>&1 && check "OpenAI package" || check_warning "OpenAI pas installé (pip install openai)"

python -c "import google.generativeai" > /dev/null 2>&1 && check "Gemini package" || check_warning "Gemini pas installé (pip install google-generativeai)"

python -c "import pydantic" > /dev/null 2>&1 && check "Pydantic package"

python -c "import aiohttp" > /dev/null 2>&1 && check "Aiohttp package"

python -c "from dotenv import load_dotenv" > /dev/null 2>&1 && check "Python-dotenv package"

echo ""

# ========================================
# 4. VÉRIFICATIONS CONFIGURATION
# ========================================
echo "4️⃣ Vérification de la configuration..."
echo "---"

if [ -f ".env" ]; then
    echo -e "${GREEN}✅ Fichier .env trouvé${NC}"
    if grep -q "OPENAI_API_KEY\|GEMINI_API_KEY\|IA_PROVIDER" .env; then
        echo -e "${GREEN}✅ Configuration IA trouvée dans .env${NC}"
    else
        echo -e "${YELLOW}⚠️  Pas de configuration IA dans .env${NC}"
        WARNINGS=$((WARNINGS+1))
    fi
else
    echo -e "${YELLOW}⚠️  Fichier .env non trouvé - Mode mock utilisé${NC}"
    WARNINGS=$((WARNINGS+1))
    echo "   Pour utiliser une vraie IA, créez .env avec:"
    echo "   echo 'OPENAI_API_KEY=sk-...' > .env"
    echo "   OU"
    echo "   echo 'GEMINI_API_KEY=...' > .env"
fi

echo ""

# ========================================
# 5. VÉRIFICATIONS CODE
# ========================================
echo "5️⃣ Vérification du code..."
echo "---"

# Vérifier les imports clés
grep -q "class LLMService" core/services/llm_service.py
check "LLMService class dans llm_service.py"

grep -q "@api_view" core/ia_endpoints.py
check "API views dans ia_endpoints.py"

grep -q "export const ChatIA" Frontend/src/components/Chat/ChatIA.tsx
check "ChatIA component exporté"

grep -q "export default function TuteurIA" Frontend/src/pages/Tuteur/TuteurIA.tsx
check "TuteurIA page créée"

grep -q "class IAService" Frontend/src/services/iaService.ts
check "IAService class créée"

echo ""

# ========================================
# 6. VÉRIFICATIONS ROUTES
# ========================================
echo "6️⃣ Vérification des routes..."
echo "---"

grep -q "'/api/ia/chat/'" core/urls.py
check "Route /api/ia/chat/"

grep -q "'/api/ia/generer-exercices/'" core/urls.py
check "Route /api/ia/generer-exercices/"

grep -q "'/api/ia/analyser-reponse/'" core/urls.py
check "Route /api/ia/analyser-reponse/"

grep -q "'/api/ia/recommandations/'" core/urls.py
check "Route /api/ia/recommandations/"

grep -q "path='/tuteur'" Frontend/src/App.tsx 2>/dev/null || grep -q "'/tuteur'" Frontend/src/App.tsx
check "Route /tuteur dans frontend"

echo ""

# ========================================
# 7. RÉSUMÉ
# ========================================
echo "=========================================="
echo "📊 RÉSUMÉ DE VÉRIFICATION"
echo "=========================================="
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ TOUT EST PRÊT!${NC}"
    echo ""
    echo "Prochaines étapes:"
    echo "1. Lancer le backend:  python manage.py migrate && python manage.py runserver"
    echo "2. Lancer le frontend: cd Frontend && npm run dev"
    echo "3. Accéder à:          http://localhost:5174"
    echo "4. Aller à:            Menu -> Tuteur IA"
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  PRÊT AVEC AVERTISSEMENTS (${WARNINGS})${NC}"
    echo ""
    echo "Vous avez $WARNINGS avertissement(s) - revoir ci-dessus"
    echo ""
else
    echo -e "${RED}❌ ${ERRORS} erreur(s) trouvée(s)${NC}"
    echo ""
    echo "Accélération issues:"
    [ $ERRORS -gt 1 ] && echo "- Reinstaller dépendances: pip install -r requirements.txt"
    [ ! -f "core/ia_endpoints.py" ] && echo "- Fichiers backend non trouvés - vérifier répertoire courante"
    [ ! -f "Frontend/src/components/Chat/ChatIA.tsx" ] && echo "- Fichiers frontend non trouvés - vérifier répertoire courante"
fi

echo ""
echo "=========================================="
echo "📚 Documentation Disponible:"
echo "=========================================="
echo "- IA_INTEGRATION_PLAN.md"
echo "- IMPLEMENTATION_IA_COMPLETE.md"
echo "- FILES_STRUCTURE.md"
echo "- DELIVERABLE_IA.md"
echo ""
echo "🎓 Tuteur Intelligent - IA Integration"
echo "=========================================="
