"""
Service d'intégration LLM (Large Language Model)
Gère OpenAI, Gemini et autres providers
"""

import os
import json
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from enum import Enum

from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Pour suppression : from openai import OpenAI
# Pour suppression : import google.generativeai as genai

# Défensifs : éviter que Pylance signale les imports manquants en l'éditeur
try:
    from pydantic import BaseModel  # pragma: no cover
except Exception:  # pragma: no cover
    class BaseModel:  # simple stub pour l'éditeur / tests légers
        pass

try:
    from dotenv import load_dotenv  # pragma: no cover
except Exception:  # pragma: no cover
    def load_dotenv():  # stub
        return None

try:
    import openai  # pragma: no cover
except Exception:  # pragma: no cover
    openai = None

import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=FutureWarning)
    try:
        import google.generativeai as generativeai  # pragma: no cover
        from google.generativeai import types as generative_types  # pragma: no cover
    except Exception:  # pragma: no cover
        generativeai = None
        generative_types = None

load_dotenv()


class LLMProvider(str, Enum):
    """Providers disponibles"""
    OPENAI = "openai"
    GEMINI = "gemini"
    OLLAMA = "ollama"  # Local


class NiveauScolaire(str, Enum):
    """Niveaux scolaires"""
    CP1 = "cp1"
    CP2 = "cp2"
    CE1 = "ce1"
    CE2 = "ce2"
    CM1 = "cm1"
    CM2 = "cm2"
    SIXIEME = "6eme"
    CINQUIEME = "5eme"
    QUATRIEME = "4eme"
    TROISIEME = "3eme"
    SECONDE = "seconde"
    PREMIERE = "1ere"
    TERMINALE = "terminale"


class Matiere(str, Enum):
    """Matières disponibles"""
    MATHEMATIQUES = "mathematiques"
    FRANCAIS = "francais"
    HISTOIRE_GEO = "histoire_geo"
    SCIENCES = "sciences"
    ANGLAIS = "anglais"
    SCIENCES_VIE = "sciences_vie"
    PHYSIQUE_CHIMIE = "physique_chimie"
    TECHNOLOGIE = "technologie"
    EPS = "eps"
    ARTS = "arts"


class ExerciseType(str, Enum):
    """Types d'exercices"""
    CHOIX_MULTIPLE = "choix_multiple"
    REPONSE_COURTE = "reponse_courte"
    REDACTION = "redaction"
    CALCUL = "calcul"
    VRAI_FAUX = "vrai_faux"
    MATCHING = "matching"


# ========================
# PROMPT TEMPLATES
# ========================

SYSTEM_PROMPT_TUTEUR = """Tu es un tuteur intelligent et bienveillant pour élèves de primaire et secondaire.

**Contexte Pédagogique:**
- Niveau scolaire: {niveau}
- Matière: {matiere}
- Âge estimé: {age} ans
- Points forts de l'élève: {strengths}
- Points à améliorer: {weak_areas}
- Leçon en cours (si l'élève est sur une leçon): {lecon_titre}
- Contenu de la leçon (extrait pour contextualiser): {lecon_contenu}

**Directives Essentielles:**
1. 🎯 ADAPTE ton langage au niveau de l'élève:
   - CP1-CE2: Très simple, mots courants, phrases courtes
   - CM1-CM2: Langage clair, quelques termes techniques avec explications
   - 6ème-3ème: Plus détaillé, définitions précises
   - Lycée: Technique, nuancé, approfondi

2. 💡 Utilise des analogies et exemples concrets:
   - Pour la fraction: "C'est comme un gâteau divisé"
   - Pour les verbes: "C'est l'action que fait quelqu'un"

3. ✅ Soit encourageant et positif TOUJOURS

4. ❓ Pose des questions pour vérifier la compréhension

5. ⚠️ N'utilise PAS de jargon technique pas expliqué pour niveaux bas

6. 📝 Structure tes réponses clairement:
   - Salutation courte
   - Explication simple
   - Exemple(s) concret(s)
   - Vérification compréhension
   - Suggestion d'exercice si pertinent

7. 🎓 Adapte à son style d'apprentissage

**Réponse attendue (JSON):**
{{
    "reponse": "...",
    "type": "explication|question|exercice|feedback",
    "niveau_adapte": true,
    "confiance": 0.95
}}
"""

SYSTEM_PROMPT_EXERCICE_GENERATOR = """Tu es un générateur d'exercices pédagogiques intelligent.

**Contexte:**
- Niveau: {niveau}
- Matière: {matiere}
- Nombre d'exercices à générer: {nombre}
- Topics: {topics}
- Difficultés antérieures: {difficulty_history}

**Règles de génération:**
1. Génère des exercices variés et intéressants
2. Adapte la difficulté au niveau de l'élève
3. Basé sur les lacunes identifiées
4. Inclus des problèmes du monde réel quand possible
5. Pour chaque exercice, fournis:
   - Question claire
   - Options (si choix multiple)
   - Réponse correcte
   - 2-3 erreurs courantes possibles
   - Explication détaillée

**Format de réponse (JSON):**
{{
    "exercices": [
        {{
            "id": 1,
            "type": "choix_multiple|reponse_courte|calcul",
            "question": "...",
            "options": ["a", "b", "c"],  // optionnel
            "reponse": "...",
            "explication": "...",
            "erreurs_courantes": ["...", "..."],
            "difficulte": 5,
            "temps_estime": 180,
            "points": 10
        }}
    ],
    "note_generation": {{
        "qualite": 0.95,
        "adaptation": "bonne",
        "variete": "excellente"
    }}
}}
"""

SYSTEM_PROMPT_ANALYSIS = """Tu es un analyste pédagogique IA.

Analyse la réponse de l'élève et fournis un feedback détaillé.

**Réponse attendue:**
{{
    "correct": true|false,
    "score": 0-100,
    "feedback_positif": "...",
    "raison_erreur": "...",
    "explication": "...",
    "prochaine_etape": {{
        "type": "exercice_similaire|lecon_preparatoire|approfondissement",
        "titre": "..."
    }},
    "encouragement": "..."
}}
"""


# ========================
# MODELS PYDANTIC
# ========================

class ChatMessage(BaseModel):
    """Modèle pour message de chat"""
    role: str = Field(..., description="user ou assistant")
    content: str = Field(..., description="Contenu du message")


class GeneratedExercise(BaseModel):
    """Modèle pour exercice généré"""
    type: ExerciseType
    question: str
    options: Optional[List[str]] = None
    reponse: str
    explication: str
    erreurs_courantes: List[str]
    difficulte: int = Field(ge=1, le=10)
    temps_estime: int = Field(description="en secondes")
    points: int = Field(default=10)


class AnalysisResult(BaseModel):
    """Modèle pour analyse de réponse"""
    correct: bool
    score: int = Field(ge=0, le=100)
    feedback_positif: str
    raison_erreur: Optional[str] = None
    explication: str
    prochaine_etape: Optional[Dict[str, str]] = None
    encouragement: str


# ========================
# BASE SERVICE
# ========================

class BaseLLMService(ABC):
    """Service LLM abstrait"""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    def chat(self, messages: List[ChatMessage], system_prompt: str) -> str:
        """Chat avec le modèle"""
        pass

    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """Générer du texte"""
        pass


# ========================
# OPENAI SERVICE (EN ATTENTE DE CLÉ API)
# ========================

class OpenAIService(BaseLLMService):
    """Service OpenAI (nécessite clé API)"""
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        if not api_key:
            # Pour respecter l'exigence: le backend doit appeler OpenAI à chaque réponse.
            # Si la clé n'est pas fournie, on lève une erreur lors de l'initialisation pour forcer la configuration.
            raise EnvironmentError("OPENAI_API_KEY non configurée. Définissez la variable d'environnement OPENAI_API_KEY.")

        try:
            from openai import OpenAI
        except Exception as e:
            raise ImportError("Package 'openai' requis mais non installé: pip install openai") from e

        # Utiliser la nouvelle API OpenAI v1.0.0+ (initialiser sans proxies)
        self.client = OpenAI(api_key=api_key)

    def chat(self, messages: List[Dict], system_prompt: str) -> str:
        """Chat avec OpenAI en envoyant un system prompt puis les messages fournis.

        Retourne la chaîne de texte produite par le modèle. Le modèle est encouragé
        à produire du JSON conforme aux prompts systèmes (`SYSTEM_PROMPT_TUTEUR` / `SYSTEM_PROMPT_EXERCICE_GENERATOR`).
        """
        # Construire la liste de messages au format API OpenAI
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})

        # Messages doivent être des dicts {role, content}
        for m in messages:
            # Normaliser les rôles en 'user' ou 'assistant'
            role = m.get('role', 'user')
            content = m.get('content', '')
            full_messages.append({"role": role, "content": content})

        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                temperature=0.3,
                max_tokens=1500
            )
            # Nouvelle API retourne un objet avec .content
            return resp.choices[0].message.content
        except Exception as e:
            # Ne jamais renvoyer l'input utilisateur en cas d'erreur
            raise RuntimeError(f"Erreur OpenAI: {e}") from e

    def generate_text(self, prompt: str) -> str:
        return self.chat([{"role": "user", "content": prompt}], "")


# ========================
# GEMINI SERVICE (EN ATTENTE DE CLÉ API)
# ========================

class GeminiService(BaseLLMService):
    """Service Google Gemini (nécessite clé API)"""

    def __init__(self, api_key: Optional[str] = None):
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            self.available = False
            print("⚠️ GEMINI_API_KEY non configurée - Mode démo")
        else:
            self.available = True
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-pro')
            except ImportError:
                print("⚠️ Package 'google-generativeai' non installé")
                self.available = False

    def chat(self, messages: List[Dict], system_prompt: str) -> str:
        """Chat avec Gemini"""
        if not self.available:
            return self._mock_response()

        try:
            from google.generativeai.types import ContentType

            conversation = self.model.start_chat()
            
            # Préparer le contexte
            context = f"{system_prompt}\n\nConversation:\n"
            for msg in messages[:-1]:
                role = "User" if msg["role"] == "user" else "AI"
                context += f"{role}: {msg['content']}\n"

            response = conversation.send_message(
                messages[-1]["content"] if messages else "Bonjour"
            )
            return response.text
        except Exception as e:
            print(f"❌ Erreur Gemini: {e}")
            return self._mock_response()

    def generate_text(self, prompt: str) -> str:
        """Générer du texte"""
        if not self.available:
            return self._mock_response()
        return self.chat([{"role": "user", "content": prompt}], "")

    def _mock_response(self) -> str:
        """Réponse mock pour démo"""
        return json.dumps({
            "reponse": "Réponse en mode démo (configurez GEMINI_API_KEY)",
            "type": "explication",
            "niveau_adapte": True,
            "confiance": 0.5
        })


# ========================
# MOCK SERVICE (POUR TESTS)
# ========================

class MockLLMService(BaseLLMService):
    """Service Mock intelligent pour tests et démo - VRAIE logique pédagogique"""

    def __init__(self):
        self.conversation_history = {}
        
        # Contenu pédagogique intelligent par niveau et matière
        self.explications = {
            "CM1-CM2": {
                "mathématiques": {
                    "fraction": "Une fraction, c'est comme diviser quelque chose en parts égales. Par exemple, si tu coupes un gâteau en 4 parts égales et tu en prends 1, tu as 1/4 du gâteau!",
                    "périmètre": "Le périmètre, c'est la distance autour d'une forme. Imagine du scotch qui entoure un carré: la longueur du scotch, c'est le périmètre!",
                    "aire": "L'aire, c'est l'espace à l'intérieur d'une forme. Imagine peindre le sol d'une pièce: la quantité de peinture dépend de l'aire!",
                    "décimales": "Les décimales, ce sont les chiffres après la virgule. Comme l'argent: 2,50€, c'est 2 euros et 50 centimes!"
                },
                "français": {
                    "verbe": "Un verbe, c'est un mot qui montre une action. Courir, sauter, manger, lire... ce sont des verbes!",
                    "adjectif": "Un adjectif décrit une personne ou une chose. Grand, petit, bleu, heureux... ce sont des adjectifs!",
                    "accord": "L'accord, c'est faire en sorte que les mots 'se parlent' entre eux. Si tu dis 'un chat noir', 'noir' s'accorde avec 'chat'!",
                    "homophones": "Ce sont des mots qui se prononcent pareil mais n'ont pas le même sens. Exemple: 'est' (verbe être) et 'et' (conjonction)!"
                }
            },
            "6ème-3ème": {
                "mathématiques": {
                    "équation": "Une équation, c'est trouver la valeur mystérieuse (souvent x). Par exemple: 2x + 3 = 7. On doit trouver x!",
                    "théorème": "Un théorème, c'est une règle mathématique importante. Pythagore, c'est un exemple célèbre!",
                    "probabilité": "La probabilité mesure la chance qu'un événement arrive. Entre 0 (impossible) et 1 (certain).",
                    "fonction": "Une fonction, c'est une machine: tu rentre un nombre, elle te ressort un autre nombre suivant une règle."
                },
                "français": {
                    "subordonnée": "Une proposition subordonnée dépend d'une propositionprincipale. Elle commence souvent par 'qui', 'que', 'parce que'...",
                    "conjugaison": "Changer la forme du verbe selon la personne et le temps. Je suis, Tu es, Il est...",
                    "analyse": "Étudier chaque mot pour comprendre la structure d'une phrase ou l'intention d'un auteur.",
                    "littérature": "L'étude des œuvres écrites pour les analyser et les interpréter!"
                }
            },
            "2nde-Tle": {
                "mathématiques": {
                    "dérivée": "La dérivée mesure comment une fonction change. C'est la pente de la courbe à un point donné.",
                    "intégrale": "L'intégrale calcule l'aire sous une courbe. C'est l'inverse de la dérivée!",
                    "logarithme": "Le log sert à résoudre des équations exponentielles: log(a^x) = x * log(a).",
                    "limite": "La limite c'est vers quel nombre on tend quand on s'approche d'un point."
                },
                "philosophie": {
                    "épistémologie": "C'est l'étude de comment on connaît les choses. Qu'est-ce que la science?",
                    "morale": "L'étude du bien et du mal, de comment on doit se comporter.",
                    "logique": "L'art de raisonner correctement: prémisses → conclusion.",
                    "métapysique": "L'étude de la réalité ultime: qu'est-ce qui existe vraiment?"
                }
            }
        }

    def _analyser_historique(self, messages: List[Dict], niveau: str, matiere: str) -> Dict[str, Any]:
        """
        Analyser l'historique de conversation pour extraire le contexte
        Détecte : était-ce une question? une demande d'exercice? etc.
        """
        contexte = {
            "est_reponse_question": False,
            "question_precedente": None,
            "contexte_matiere_identifie": False,
            "nombre_echanges": len(messages),
            "concepts_mentionnes": []
        }
        
        if len(messages) < 2:
            return contexte
        
        # Analyser les messages précédents pour trouver la question posée
        for i in range(len(messages) - 2, -1, -1):  # De l'avant-avant-dernier vers le début
            msg = messages[i]
            if msg.get("role") == "assistant":
                # Chercher si c'était une question à l'utilisateur
                contenu = msg.get("content", "").lower()
                if any(word in contenu for word in ["veux-tu", "veux tu", "?", "veux"]):
                    contexte["est_reponse_question"] = True
                    contexte["question_precedente"] = msg.get("content", "")
                    break
        
        return contexte

    def _generer_reponse_intelligente(
        self,
        message_courant: str,
        contexte: Dict[str, Any],
        niveau: str,
        matiere: str,
        system_prompt: str
    ) -> str:
        """Générer une réponse vraiment intelligente basée sur le contexte réel"""
        
        # Si c'est une réponse positive ou négative
        prompt_lower = message_courant.lower().strip()
        
        if prompt_lower in ["oui", "ouais", "yep", "yes", "d'accord", "ok", "ok!", "oki"]:
            # Analyser ce qu'on proposait dans le message précédent
            prev_question = contexte.get("question_precedente", "").lower()
            
            if any(word in prev_question for word in ["exercice", "s'entraîner", "pratiquer"]):
                n = 2
                exercices = self._generer_exercices_contextuels(n, niveau, matiere)
                return json.dumps({
                    "exercices": exercices,
                    "reponse": f"🎯 Parfait! Voici {n} exercices sur {matiere} adaptés au niveau {niveau}:",
                    "type": "exercice",
                    "niveau_adapte": True,
                    "confiance": 0.95
                })
            
            elif any(word in prev_question for word in ["continuer", "plusque", "suite", "approfondir"]):
                return json.dumps({
                    "reponse": f"Excellent! On va approfondir {matiere}. Dis-moi sur quel concept tu aimerais que je t'aide: fractions, équations, littérature... ?",
                    "type": "explication",
                    "niveau_adapte": True,
                    "confiance": 0.9
                })
            else:
                return json.dumps({
                    "reponse": f"Super! Je suis ravi que le soit compris. On va continuer? Tu peux me demander une explication, un exercice, ou m'aider sur un concept précis en {matiere}.",
                    "type": "explication",
                    "niveau_adapte": True,
                    "confiance": 0.85
                })
        
        elif prompt_lower in ["non", "non pas", "nope", "non merci", "non!", "pas"]:
            return json.dumps({
                "reponse": "D'accord! Pas de problème. Qu'est-ce que je peux faire pour t'aider? Je peux expliquer un concept, te proposer un exercice différent, ou même une révision.",
                "type": "explication",
                "niveau_adapte": True,
                "confiance": 0.85
            })
        
        # Fallback
        return json.dumps({
            "reponse": f"Je vois. En {matiere}, je peux t'aider avec des explications, des exercices, ou des révisions. Qu'est-ce que tu préfères?",
            "type": "explication",
            "niveau_adapte": True,
            "confiance": 0.8
        })

    def _extraire_niveau_depuis_prompt(self, prompt: str) -> str:
        """Extraire le niveau depuis le system prompt"""
        if "CP1" in prompt or "CE" in prompt or "CM" in prompt:
            if "CM1" in prompt or "CM2" in prompt:
                return "CM1-CM2"
            return "CP1-CE2"
        elif "6" in prompt and "ème" in prompt or "3" in prompt and "ème" in prompt:
            return "6ème-3ème"
        elif "2nde" in prompt or "Tale" in prompt or "Lycée" in prompt:
            return "2nde-Tle"
        return "CM1-CM2"  # défaut

    def _extraire_matiere_depuis_prompt(self, prompt: str) -> str:
        """Extraire la matière depuis le system prompt"""
        matiere_map = {
            "mathématiques": "mathématiques",
            "math": "mathématiques",
            "français": "français",
            "francais": "français",
            "français": "français",
            "svt": "svt",
            "sciences": "svt",
            "physique": "physique",
            "chimie": "physique",
            "philosophie": "philosophie",
            "philo": "philosophie",
            "histoire": "histoire",
            "geo": "histoire"
        }
        prompt_lower = prompt.lower()
        for mot, matiere in matiere_map.items():
            if mot in prompt_lower:
                return matiere
        return "général"

    def chat(self, messages: List[Dict], system_prompt: str) -> str:
        """Chat intelligent avec contexte pédagogique réel et historique de conversation"""
        
        if not messages:
            return json.dumps({
                "reponse": "Bonjour! Je suis ton tuteur intelligent. Je m'adapte à ton niveau et je suis là pour clarifier tes doutes. Qu'est-ce que tu aimerais apprendre?",
                "type": "salutation",
                "niveau_adapte": True,
                "confiance": 0.95
            })

        # 🔥 Récupérer le dernier message (message courant de l'utilisateur)
        last_msg = messages[-1].get("content", "").strip() if messages else ""
        prompt_lower = last_msg.lower()
        
        # Extraire le contexte pédagogique du system prompt
        niveau = self._extraire_niveau_depuis_prompt(system_prompt)
        matiere = self._extraire_matiere_depuis_prompt(system_prompt)

        # 🔥 NOUVEAU : Analyser l'historique complet pour mieux comprendre le contexte
        contexte_conversation = self._analyser_historique(messages, niveau, matiere)

        # ============ SALUTATION / SIMPLE REFLEXE ==============
        if len(messages) == 1:  # Premier message
            if any(word in prompt_lower for word in ["bonjour", "hello", "salut", "coucou", "hi"]):
                return json.dumps({
                    "reponse": f"Salut! Bienvenue! Je suis ton tuteur en {matiere}. Je suis là pour t'aider à mieux comprendre. Qu'est-ce que tu aimerais apprendre ou dont tu as besoin d'aide?",
                    "type": "salutation",
                    "niveau_adapte": True,
                    "confiance": 0.95
                })

        # ============ RÉPONSE À UNE QUESTION PRÉCÉDENTE ==============
        # Si contexte_conversation a identifié qu'on répond à une question
        if contexte_conversation.get("est_reponse_question"):
            return self._generer_reponse_intelligente(
                last_msg,
                contexte_conversation,
                niveau,
                matiere,
                system_prompt
            )

        # ============ GESTION EXPLICITE DE CONCEPTS ==============
        for concept_key, explications_dict in self.explications.get(niveau, {}).get(matiere, {}).items():
            if concept_key in prompt_lower:
                return json.dumps({
                    "reponse": f"Bonne question sur {concept_key}! {explications_dict}\n\nMaintenant que tu comprends ça, tu veux essayer un exercice?",
                    "type": "explication",
                    "niveau_adapte": True,
                    "confiance": 0.95
                })

        # ============ GÉNÉRATION D'EXERCICES INTELLIGENTS ==============
        import re
        
        if any(word in prompt_lower for word in ["exercice", "exercices", "génèr", "genere", "gen", "entrainement", "entraînement", "pratique"]):
            m = re.search(r"(\d+)", last_msg)
            n = int(m.group(1)) if m else 3
            n = min(10, max(1, n))
            
            exercices = self._generer_exercices_contextuels(n, niveau, matiere)
            
            return json.dumps({
                "exercices": exercices,
                "note_generation": {
                    "qualite": 0.95,
                    "adaptation": f"adapté au niveau {niveau}",
                    "nombre": n,
                    "matiere": matiere
                }
            })

        # ============ ANALYSE DE RÉPONSE INTELLIGENTE ==============
        
        if any(word in prompt_lower for word in ["corrig", "analyse", "reponse", "réponse", "verifi", "juste", "faux"]):
            est_correcte = self._evaluer_reponse_basique(last_msg, prompt_lower)
            score = 85 if est_correcte else 35
            
            return json.dumps({
                "correct": est_correcte,
                "score": score,
                "feedback_positif": "✓ Tu as fait un bonne effort!" if est_correcte else "Tu es sur la bonne voie, mais il manque quelque chose.",
                "raison_erreur": None if est_correcte else "Attention à la méthode - relis le concept clé.",
                "explication": "Tu as bien appliqué la méthode!" if est_correcte else "Essaie de vérifier chaque étape de ton raisonnement.",
                "prochaine_etape": {
                    "type": "approfondissement" if est_correcte else "exercice_similaire",
                    "titre": "Exercice d'approfondissement" if est_correcte else "Exercice de révision"
                },
                "encouragement": "Excellent! Prêt pour plus difficile?" if est_correcte else "Continue à t'entraîner, tu vas y arriver!"
            })

        # ============ CHAT GÉNÉRIQUE CONTEXTUEL ==============
        
        # 🔥 NOUVEAU : Répondre différemment selon le contexte réel de conversation
        if contexte_conversation.get("question_precedente"):
            prev_question = contexte_conversation["question_precedente"]
            
            # Si l'utilisateur dit "oui" après une question
            if last_msg in ["oui", "ouais", "yep", "yes", "d'accord", "ok", "ok!"]:
                # Répondre avec l'action proposée
                if "exercice" in prev_question.lower():
                    n = 2
                    exercices = self._generer_exercices_contextuels(n, niveau, matiere)
                    return json.dumps({
                        "exercices": exercices,
                        "reponse": f"Super! Voici {n} exercices adaptés à ton niveau pour pratiquer:",
                        "type": "exercice",
                        "niveau_adapte": True,
                        "confiance": 0.95
                    })
                elif "expliquer" in prev_question.lower() or "comprendre" in prev_question.lower():
                    return json.dumps({
                        "reponse": "Parfait! Dis-moi quel concept tu aimerais que j'explique plus en détail.",
                        "type": "explication",
                        "niveau_adapte": True,
                        "confiance": 0.9
                    })
                else:
                    # Réponse générique mais contextuelle
                    return json.dumps({
                        "reponse": "Excellent! Je suis ravi. Qu'est-ce que tu aimerais faire maintenant? Tu peux me demander une explication, un exercice, ou une aide spécifique.",
                        "type": "explication",
                        "niveau_adapte": True,
                        "confiance": 0.85
                    })
            
            # Si l'utilisateur dit "non"
            elif last_msg in ["non", "non pas", "nope", "non merci", "non!"]:
                return json.dumps({
                    "reponse": "D'accord! Qu'est-ce que je peux faire pour t'aider alors? Je peux expliciter un concept, tester ta compréhension, ou te proposer une autre activité.",
                    "type": "explication",
                    "niveau_adapte": True,
                    "confiance": 0.85
                })

        # Réponse adaptée au niveau et contexte
        reponses_reflexes = {
            "salut": "Salut! Que puis-je t'expliquer en {matiere} pour le niveau {niveau}?",
            "merci": "De rien! N'hésite pas à demander si tu as d'autres questions!",
            "comment": "C'est une excellente question! Dans {matiere}, voici comment on pense à ça...",
            "pourquoi": "Très bonne question! La raison c'est que...",
            "difficile": "C'est normal que ce soit difficile! Tous les élèves trouvent ça complexe au début. Décomposons-le étape par étape.",
            "facile": "Bravo! Tu progresses bien. Veux-tu passer à quelque chose de plus difficile?",
            "comprends pas": "Ne t'inquiète pas, je vais te l'expliquer différemment. Dis-moi ce que tu as compris..."
        }

        reponse_base = f"C'est une bonne question! En {matiere.capitalize()} au niveau {niveau}, voici comment on peut l'aborder:"
        
        for trigger, response_template in reponses_reflexes.items():
            if trigger in prompt_lower:
                reponse_base = response_template
                break

        reponse = reponse_base.format(matiere=matiere.capitalize(), niveau=niveau)

        return json.dumps({
            "reponse": reponse + "\n\nVeux-tu un exercice pour pratiquer, on tu as d'autres questions?",
            "type": "explication",
            "niveau_adapte": True,
            "confiance": 0.88
        })

    def _generer_exercices_contextuels(self, n: int, niveau: str, matiere: str) -> List[Dict]:
        """Générer des exercices vraiment contextuels"""
        
        # Banque d'exercices par niveau et matière
        banques = {
            "CM1-CM2": {
                "mathématiques": [
                    {"type": "num", "question": "Quel est le double de 25?", "options": ["50", "45", "52", "55"], "reponse": "50", "explication": "25 × 2 = 50"},
                    {"type": "num", "question": "Divise 48 par 6", "options": ["6", "8", "7", "9"], "reponse": "8", "explication": "48 ÷ 6 = 8"},
                    {"type": "choix", "question": "Quelle est la fraction for 0.5?", "options": ["1/2", "1/3", "2/3", "1/4"], "reponse": "1/2", "explication": "0.5 = 50/100 = 1/2"},
                    {"type": "calcul", "question": "Calcule: 234 + 567", "options": ["801", "800", "802", "799"], "reponse": "801", "explication": "234 + 567 = 801"},
                    {"type": "prob", "question": "Quel est le périmètre d'un carré de 5cm?", "options": ["20cm", "15cm", "25cm", "10cm"], "reponse": "20cm", "explication": "Périmètre = 4 × côté = 4 × 5 = 20cm"}
                ],
                "français": [
                    {"type": "gram", "question": "Quel est le verbe dans: 'Je suis heureux'?", "options": ["Je", "suis", "heureux", ""], "reponse": "suis", "explication": "'Suis' est le verbe (être)"},
                    {"type": "gram", "question": "Accorde: 'Un chat (noir)'", "options": ["noir", "noirs", "noiré", "noire"], "reponse": "noir", "explication": "Adjectif masculin singulier: noir"},
                    {"type": "ortho", "question": "Complète: 'C\\'est / C'est / Sait'", "options": ["C'est", "C\\'est", "Sait", "Sé"], "reponse": "C'est", "explication": "Contraction de 'ce est' = c'est"},
                    {"type": "conj", "question": "Conjugue 'avoir' au présent (je)", "options": ["ai", "ais", "è", "h"], "reponsa": "ai", "explication": "Je ai = j'ai"}
                ]
            },
            "6ème-3ème": {
                "mathématiques": [
                    {"type": "algebra", "question": "Résous: 2x + 5 = 13", "options": ["4", "3", "5", "6"], "reponse": "4", "explication": "2x = 13 - 5 = 8, donc x = 4"},
                    {"type": "geo", "question": "Quel est le carré de 7?", "options": ["49", "48", "50", "64"], "reponsa": "49", "explication": "7² = 7 × 7 = 49"},
                    {"type": "prob", "question": "Proba de tirer un as dans un jeu de 52 cartes?", "options": ["4/52", "1/13", "1/4", "4/48"], "reponse": "4/52", "explication": "Il y a 4 as sur 52 cartes"}
                ],
                "français": [
                    {"type": "gram", "question": "Type: 'Le chat que J'ai vu'", "options": ["principale", "subordonnée", "simple", "composée"], "reponse": "subordonnée", "explication": "'que j'ai vu' dépend de 'le chat'"},
                    {"type": "lit", "question": "Victor Hugo a écrit?", "options": ["Phèdre", "Les Misérables", "Candide", "Dom Juan"], "reponse": "Les Misérables", "explication": "Victor Hugo (1802-1885) a écrit Les Misérables"}
                ]
            },
            "2nde-Tle": {
                "mathématiques": [
                    {"type": "calc", "question": "Dérivée de x² + 3x est?", "options": ["2x + 3", "2x + 1", "x + 3", "2x"], "reponse": "2x + 3", "explication": "d/dx(x²) = 2x, d/dx(3x) = 3"},
                    {"type": "log", "question": "log(100) en base 10 est?", "options": ["2", "3", "1", "4"], "reponse": "2", "explication": "10² = 100"}
                ],
                "philosophie": [
                    {"type": "philo", "question": "Descartes dit: 'Je pense donc...'", "options": ["je doute", "je suis", "je crois", "je peux"], "reponse": "je suis", "explication": "'Cogito ergo sum' - cela prouve l'existence de la conscience"},
                    {"type": "ethique", "question": "Utilitarisme = maximiser le?", "options": ["bonheur", "profit", "ordre", "pouvoir"], "reponsa": "bonheur", "explication": "L'utilitarisme cherche le plus grand bien pour le plus grand nombre"}
                ]
            }
        }

        # Récupérer la banque appropriée
        exercises = banques.get(niveau, {}).get(matiere, [])
        
        if not exercises:
            # Fallback générique mais réaliste
            exercises = [
                {
                    "type": "general",
                    "question": f"Question de révision #{i} en {matiere}",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "reponse": "Option A",
                    "explication": "Explication pédagogique"
                }
                for i in range(1, 4)
            ]

        # Sélectionner et formater
        result = []
        for i, ex in enumerate(exercises[:n], 1):
            result.append({
                "id": i,
                "type": ex.get("type", "choix_multiple"),
                "question": ex["question"],
                "options": ex.get("options", ["A", "B", "C", "D"]),
                "reponse": ex.get("reponse", ex.get("reponsa", "A")),
                "explication": ex.get("explication", "Voir le cours"),
                "erreurs_courantes": ["Confusion conceptuelle", "Erreur de calcul"],
                "difficulte": {"CM1-CM2": 3, "6ème-3ème": 5, "2nde-Tle": 8}.get(niveau, 5),
                "temps_estime": 120,
                "points": 10
            })
        
        return result

    def _evaluer_reponse_basique(self, reponse: str, prompt: str) -> bool:
        """Éval basique mais intelligente"""
        # Mots-clés positifs
        positifs = ["correct", "juste", "bon", "exact", "vrai", "bien", "parfait"]
        negatifs = ["faux", "incorrec", "mauvais", "non", "erreur", "faux"]
        
        reponse_lower = reponse.lower()
        
        score_positif = sum(1 for p in positifs if p in reponse_lower)
        score_negatif = sum(1 for n in negatifs if n in reponse_lower)
        
        # Si c'est une réponse chiffrée, tester cohérence basique
        if any(char.isdigit() for char in reponse):
            return True  # optimiste pour démo
        
        return score_positif > score_negatif

    def generate_text(self, prompt: str) -> str:
        """Générer du texte contextualisé"""
        # Pour un vrai prompt, extraire des concepts et donner explica
        if "explication" in prompt.lower() or "explique" in prompt.lower():
            return "Bien sûr! Voici une explication détaillée et adaptée à ton niveau..."
        elif "recommanda" in prompt.lower():
            return json.dumps({
                "recommandations": [
                    "Exercice 1: Pratiquer les concepts clés",
                    "Exercice 2: Appliquer à des cas réels",
                    "Projet: Intégrer plusieurs concepts"
                ],
                "note": "Basé sur ta progression actuelle"
            })
        
        return "Texte généré intelligemment par ton tuteur."


# ========================
# MAIN LLM SERVICE
# ========================

class LLMService:
    """Service principal d'intégration LLM"""

    def __init__(self, provider: str = None):
        """
        Initialiser le service LLM

        Args:
            provider: "openai", "gemini", ou "mock"
        """
        # Déterminer le provider à partir de la variable d'environnement ou du paramètre
        self.provider_name = provider or os.getenv("IA_PROVIDER", "openai")

        if self.provider_name == "openai":
            # OpenAIService lève une exception si la clé n'est pas configurée
            self.service = OpenAIService()
        elif self.provider_name == "gemini":
            self.service = GeminiService()
        else:
            # Pour sécurité, permettre explicitement mock mais ne pas l'utiliser par défaut
            self.service = MockLLMService()

    # ========================
    # TUTORING
    # ========================

    def chat_tuteur(
        self,
        message: str,
        niveau: str,
        matiere: str,
        age: int = 10,
        strengths: str = "aucune identifiée",
        weak_areas: str = "aucune identifiée",
        lecon_titre: str = "",
        lecon_contenu: str = "",
        conversation_history: List[Dict] = None,  # 🔥 NOUVEAU : Historique de conversation
    ) -> Dict[str, Any]:
        """
        Chat avec le tuteur IA. Utilise le niveau, la matière et optionnellement la leçon en cours.
        
        Args:
            conversation_history: Liste complète des messages antérieurs pour contexte
        """
        system = SYSTEM_PROMPT_TUTEUR.format(
            niveau=niveau or "non précisé",
            matiere=matiere or "général",
            age=age,
            strengths=strengths,
            weak_areas=weak_areas,
            lecon_titre=lecon_titre or "aucune (conversation générale)",
            lecon_contenu=(lecon_contenu or "—")[:500],
        )

        # 🔥 Utiliser l'historique complet si disponible
        if conversation_history:
            messages = conversation_history
        else:
            messages = [{"role": "user", "content": message}]
            
        response = self.service.chat(messages, system)

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Défensif: si le service renvoie du texte brut, éviter d'echoer le message utilisateur
            raw = (response or "").strip()
            last_msg = (messages[-1].get('content') if messages else message) or message
            last_lower = (last_msg or "").lower()

            # Intent minimal: formule / volume
            if "volume" in last_lower or ("formule" in last_lower and "volume" in last_lower):
                reponse = (
                    "La formule du volume dépend de la forme. Par exemple:\n"
                    "- Sphère: V = 4/3 × π × r³\n"
                    "- Cylindre: V = π × r² × h\n"
                    "Souhaites-tu un exercice pour t'entraîner ?"
                )
                return {
                    "reponse": reponse,
                    "type": "explication",
                    "niveau_adapte": True,
                    "confiance": 0.95
                }

            # Salutation
            if any(w in last_lower for w in ["bonjour", "salut", "hello", "coucou"]):
                return {
                    "reponse": "Salut! Je suis ton tuteur. Dis-moi sur quel sujet tu veux travailler.",
                    "type": "salutation",
                    "niveau_adapte": True,
                    "confiance": 0.95
                }

            # Demande d'exercice -> tenter de générer au moins 1 exercice
            if any(w in last_lower for w in ["exercice", "exercices", "entraîne", "entrainement", "pratique", "génèr", "genere"]):
                # Essayer d'utiliser le service interne si disponible
                try:
                    if hasattr(self.service, '_generer_exercices_contextuels'):
                        exercices = self.service._generer_exercices_contextuels(1, niveau or 'CM1-CM2', matiere or 'général')
                        return {
                            "exercices": exercices,
                            "reponse": f"Voici {len(exercices)} exercice(s) pour pratiquer.",
                            "type": "exercice",
                            "niveau_adapte": True,
                            "confiance": 0.95
                        }
                except Exception:
                    pass

            # Fallback: ne jamais renvoyer l'input brut. Fournir une réponse générique utile.
            fallback = (
                "Je n'ai pas compris complètement ta demande. Peux-tu préciser ? Par exemple: 'explique les fractions', 'génère des exercices', ou 'donne la formule du volume'."
            )
            return {
                "reponse": fallback,
                "type": "explication",
                "niveau_adapte": True,
                "confiance": 0.6
            }

    # ========================
    # EXERCICES
    # ========================

    def generer_exercices(
        self,
        nombre: int,
        niveau: str,
        matiere: str,
        topics: List[str],
        difficulty_history: str = "débutant"
    ) -> List[Dict[str, Any]]:
        """
        Générer des exercices

        Args:
            nombre: Nombre d'exercices à générer
            niveau: Niveau scolaire
            matiere: Matière
            topics: Topics à couvrir
            difficulty_history: Historique de difficulté

        Returns:
            Liste d'exercices générés
        """
        system = SYSTEM_PROMPT_EXERCICE_GENERATOR.format(
            niveau=niveau,
            matiere=matiere,
            nombre=nombre,
            topics=", ".join(topics),
            difficulty_history=difficulty_history
        )

        prompt = f"Génère {nombre} exercices pour {matiere} au niveau {niveau} sur {', '.join(topics)}"
        messages = [{"role": "user", "content": prompt}]

        response = self.service.chat(messages, system)
        try:
            data = json.loads(response)
            exercices = data.get("exercices", [])
            # Garantir au moins 1 exercice
            if not exercices:
                raise ValueError("Aucun exercice retourné par le modèle")
            return exercices
        except (json.JSONDecodeError, ValueError):
            # Tentative de secours: utiliser le générateur interne si disponible
            try:
                if hasattr(self.service, '_generer_exercices_contextuels'):
                    return self.service._generer_exercices_contextuels(max(1, nombre), niveau or 'CM1-CM2', matiere or 'général')
            except Exception:
                pass
            # Fallback final: générer un exercice générique simple
            return [
                {
                    "id": 1,
                    "type": "general",
                    "question": f"Exercice de révision en {matiere} (niveau {niveau}) : Donne un exemple.",
                    "options": [],
                    "reponse": "Exemple attendu",
                    "explication": "Ceci est un exercice généré par le système car le service LLM n'a pas renvoyé d'exercices."
                }
            ]

    # ========================
    # ANALYSE
    # ========================

    def analyser_reponse(
        self,
        question: str,
        reponse_donnee: str,
        reponse_correcte: str,
        concept: str,
        niveau: str
    ) -> Dict[str, Any]:
        """
        Analyser une réponse intelligemment

        Args:
            question: Question posée
            reponse_donnee: Réponse donnée par l'élève
            reponse_correcte: Réponse correcte
            concept: Concept enseigné
            niveau: Niveau de l'élève

        Returns:
            Analyse détaillée
        """
        system = SYSTEM_PROMPT_ANALYSIS

        prompt = f"""
        Question: {question}
        Concept: {concept}
        
        Réponse de l'élève: {reponse_donnee}
        Réponse correcte: {reponse_correcte}
        
        Niveau de l'élève: {niveau}
        
        Analyse cette réponse et fournis un feedback détaillé et encourageant.
        """

        messages = [{"role": "user", "content": prompt}]
        response = self.service.chat(messages, system)

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "correct": reponse_donnee.strip().lower() == reponse_correcte.strip().lower(),
                "score": 100 if reponse_donnee.strip().lower() == reponse_correcte.strip().lower() else 0,
                "feedback_positif": "Bonne tentative!",
                "explication": f"La réponse correcte était: {reponse_correcte}",
                "encouragement": "Continue à progresser!"
            }

    # ========================
    # EXPLICATIONS
    # ========================

    def expliquer_concept(
        self,
        concept: str,
        niveau: str,
        matiere: str,
        style: str = "analogie"  # analogie, exemple, technique
    ) -> str:
        """
        Expliquer un concept

        Args:
            concept: Concept à expliquer
            niveau: Niveau de l'élève
            matiere: Matière
            style: Style d'explication

        Returns:
            Explication adaptée
        """
        prompt = f"""
        Explique le concept '{concept}' en {matiere} pour un élève de niveau {niveau}.
        Style d'explication: {style} (utilise des analogies, des exemples concrets, ou des détails techniques).
        Sois clair et adapté au niveau de l'élève.
        """

        return self.service.generate_text(prompt)

    # ========================
    # RECOMMANDATIONS
    # ========================

    def recommander_contenu(
        self,
        niveau: str,
        matiere: str,
        weak_areas: List[str],
        strengths: List[str]
    ) -> Dict[str, Any]:
        """
        Recommander du contenu personnalisé

        Args:
            niveau: Niveau de l'élève
            matiere: Matière
            weak_areas: Domaines faibles
            strengths: Points forts

        Returns:
            Recommandations
        """
        prompt = f"""
        Pour un élève de niveau {niveau} en {matiere}:
        - Points forts: {', '.join(strengths)}
        - A améliorer: {', '.join(weak_areas)}
        
        Recommande:
        1. Les 3 prochaines leçons à étudier
        2. 2 exercices complémentaires
        3. 1 projet d'approfondissement
        """

        response = self.service.generate_text(prompt)

        return {
            "recommandations": response,
            "generated_at": None
        }


# ========================
# SINGLETON GLOBAL
# ========================

_llm_service_cache = {}


def get_llm_service(provider: str = None) -> LLMService:
    """Obtenir le service LLM correspondant au provider (relire IA_PROVIDER à chaque appel)"""
    provider = provider or os.getenv("IA_PROVIDER", "openai")
    
    # Cacher une instance par provider, mais relire IA_PROVIDER chaque fois
    if provider not in _llm_service_cache:
        _llm_service_cache[provider] = LLMService(provider)
    return _llm_service_cache[provider]
