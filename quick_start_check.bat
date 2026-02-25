@echo off
REM 🚀 QUICK START - TUTEUR INTELLIGENT IA (Windows)
REM Exécutez ce script pour vérifier que tout fonctionne

echo.
echo 🎓 Tuteur Intelligent - IA Integration Quick Start
echo ==================================================
echo.

setlocal enabledelayedexpansion
set ERRORS=0
set WARNINGS=0

REM ========================================
REM 1. VÉRIFICATIONS SYSTÈME
REM ========================================
echo 1️⃣ Vérification du système...
echo ---

REM Python
python --version > nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✅ Python installé
) else (
    echo ❌ Python installé
    set /a ERRORS+=1
)

REM Node
node --version > nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✅ Node.js installé
) else (
    echo ❌ Node.js installé
    set /a ERRORS+=1
)

REM npm
npm --version > nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✅ npm installé
) else (
    echo ❌ npm installé
    set /a ERRORS+=1
)

REM Django
python -c "import django; print(django.get_version())" > nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✅ Django installé
) else (
    echo ❌ Django pas installé
    set /a ERRORS+=1
)

echo.

REM ========================================
REM 2. VÉRIFICATIONS FICHIERS
REM ========================================
echo 2️⃣ Vérification des fichiers créés...
echo ---

if exist "core\services\llm_service.py" (
    echo ✅ Service LLM créé
) else (
    echo ❌ Service LLM manquant
    set /a ERRORS+=1
)

if exist "core\ia_endpoints.py" (
    echo ✅ Endpoints IA créés
) else (
    echo ❌ Endpoints IA manquants
    set /a ERRORS+=1
)

if exist "core\migrations\0007_ia_integration.py" (
    echo ✅ Migration IA créée
) else (
    echo ❌ Migration IA manquante
    set /a ERRORS+=1
)

if exist "Frontend\src\components\Chat\ChatIA.tsx" (
    echo ✅ Composant Chat créé
) else (
    echo ❌ Composant Chat manquant
    set /a ERRORS+=1
)

if exist "Frontend\src\pages\Tuteur\TuteurIA.tsx" (
    echo ✅ Page Tuteur créée
) else (
    echo ❌ Page Tuteur manquante
    set /a ERRORS+=1
)

if exist "Frontend\src\services\iaService.ts" (
    echo ✅ Service IA créé
) else (
    echo ❌ Service IA manquant
    set /a ERRORS+=1
)

if exist "IA_INTEGRATION_PLAN.md" (
    echo ✅ Plan d'intégration trouvé
) else (
    echo ❌ Plan manquant
    set /a ERRORS+=1
)

echo.

REM ========================================
REM 3. VÉRIFICATIONS DÉPENDANCES
REM ========================================
echo 3️⃣ Vérification des dépendances...
echo ---

python -c "import openai" > nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✅ OpenAI package
) else (
    echo ⚠️  OpenAI pas installé (pip install openai)
    set /a WARNINGS+=1
)

python -c "import pydantic" > nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✅ Pydantic package
) else (
    echo ❌ Pydantic pas installé
    set /a ERRORS+=1
)

python -c "from dotenv import load_dotenv" > nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✅ Python-dotenv package
) else (
    echo ❌ Python-dotenv pas installé
    set /a ERRORS+=1
)

echo.

REM ========================================
REM 4. VÉRIFICATIONS CONFIGURATION
REM ========================================
echo 4️⃣ Vérification de la configuration...
echo ---

if exist ".env" (
    echo ✅ Fichier .env trouvé
    findstr /m "OPENAI_API_KEY\|GEMINI_API_KEY\|IA_PROVIDER" .env > nul
    if %ERRORLEVEL% equ 0 (
        echo ✅ Configuration IA trouvée
    ) else (
        echo ⚠️  Pas de configuration IA dans .env
        set /a WARNINGS+=1
    )
) else (
    echo ⚠️  Fichier .env non trouvé - Mode mock utilisé
    set /a WARNINGS+=1
    echo    Pour utiliser une vraie IA, créez .env avec:
    echo    OPENAI_API_KEY=sk-...
)

echo.

REM ========================================
REM 5. RÉSUMÉ
REM ========================================
echo ====================
echo 📊 RÉSUMÉ
echo ====================
echo.

if %ERRORS% equ 0 (
    if %WARNINGS% equ 0 (
        echo ✅ TOUT EST PRÊT!
        echo.
        echo Prochaines étapes:
        echo 1. Lancer le backend:
        echo    python manage.py migrate
        echo    python manage.py runserver
        echo.
        echo 2. Lancer le frontend (terminal 2):
        echo    cd Frontend
        echo    npm run dev
        echo.
        echo 3. Accéder à: http://localhost:5174
        echo.
    ) else (
        echo ⚠️  PRÊT AVEC AVERTISSEMENTS (%WARNINGS%)
        echo.
        echo Voir les avertissements ci-dessus
    )
) else (
    echo ❌ %ERRORS% erreur(s) trouvée(s)
    echo.
    echo Solutions:
    echo - Reinstaller dépendances: pip install -r requirements.txt
    echo - npm install dans Frontend/
    echo - Vérifier que vous êtes dans le bon répertoire
)

echo.
echo ========================================
echo 📚 Documentation Disponible:
echo ========================================
echo - IA_INTEGRATION_PLAN.md
echo - IMPLEMENTATION_IA_COMPLETE.md
echo - FILES_STRUCTURE.md
echo - DELIVERABLE_IA.md
echo.
echo 🎓 Tuteur Intelligent - IA Integration
echo ========================================
echo.

pause
