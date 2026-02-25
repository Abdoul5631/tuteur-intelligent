"""
Nouveau service LLM unifié - IA pédagogique locale uniquement
Remplace OpenAI, Gemini, Mock par une IA locale intelligente
"""

import json
from typing import Optional, List, Dict, Any
from core.services.pedagogical_ai import get_pedagogical_ai


class LLMService:
    """Service LLM avec IA pédagogique locale"""
    
    def __init__(self, provider: str = "local"):
        """
        Initialiser le service LLM
        
        Args:
            provider: Toujours "local" - pas de dépendances externes
        """
        self.provider = "local"
        self.ai = get_pedagogical_ai()
    
    def chat_tuteur(
        self,
        message: str,
        conversation_history: List[Dict] = None,
        niveau: Optional[str] = None,
        matiere: str = "mathématiques",
        age: int = 10,
        strengths: str = "",
        weak_areas: str = "",
        lecon_titre: str = "",
        lecon_contenu: str = "",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Chat avec le tuteur IA (interface principale)
        
        Args:
            message: Message de l'élève
            conversation_history: Historique complet
            niveau: Niveau scolaire
            matiere: Matière
            age: Âge
            strengths: Points forts
            weak_areas: Points faibles
            lecon_titre: Titre de la leçon en cours
            lecon_contenu: Contenu de la leçon
        
        Returns:
            Dict avec réponse et exercices optionnels
        """
        # Appeler l'IA pédagogique
        result = self.ai.chat_tuteur(
            message=message,
            niveau=niveau,
            matiere=matiere,
            prenom="",
            niveau_scolaire=niveau or "CM1-CM2"
        )
        
        # Format de réponse compatible avec les endpoints (clés en français)
        return {
            "reponse": result.get("response", ""),
            "exercises": result.get("exercises", []),
            "confiance": result.get("confidence", 0.5),
            "type": result.get("type", "explication")
        }
    
    def generate_chat_response(
        self,
        message: str,
        conversation_history: List[Dict] = None,
        context: Dict = None,
        **kwargs
    ) -> str:
        """
        Générer une réponse chat simple (compatibilité)
        """
        result = self.chat_tuteur(message=message, **kwargs)
        return result.get("response", "")
    
    def generate_exercises(
        self,
        count: int = 2,
        nombre: int = None,  # Alias pour compatibilité
        niveau: Optional[str] = None,
        topic: Optional[str] = None,
        matiere: str = "mathématiques",
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Générer des exercices
        
        Args:
            count: Nombre d'exercices (nouveau format)
            nombre: Nombre d'exercices (ancien format, compatibilité)
            niveau: Niveau scolaire
            topic: Sujet (optionnel)
            matiere: Matière
        
        Returns:
            Liste d'exercices
        """
        # Support ancien format (nombre) et nouveau format (count)
        nb = nombre if nombre is not None else count
        
        result = self.ai.generate_exercises(
            count=max(1, nb),
            niveau=niveau,
            topic=topic,
            matiere=matiere
        )
        
        # Retourner seulement la liste d'exercices (ancien format)
        return result.get('exercises', [])
    
    # Alias pour compatibilité avec ancien code
    def generer_exercices(
        self,
        nombre: int = 2,
        niveau: Optional[str] = None,
        matiere: str = "mathématiques",
        topics: List[str] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Générer des exercices (ancien format)
        Compatibilité avec endpoints existants
        """
        topic = topics[0] if topics and topics[0] != "general" else None
        return self.generate_exercises(
            count=nombre,
            niveau=niveau,
            topic=topic,
            matiere=matiere
        )


def get_llm_service(provider: str = None) -> LLMService:
    """
    Obtenir le service LLM (toujours local)
    
    Args:
        provider: Ignoré (toujours local pour sécurité)
    
    Returns:
        Instance LLMService
    """
    return LLMService(provider="local")
