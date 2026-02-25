"""
Endpoint test rapide pour bypasser les problèmes d'environnement
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from core.models import Utilisateur, ConversationIA, ConversationMessage
from core.services.llm_service import LLMService, get_llm_service
import os


@api_view(['GET'])
@permission_classes([AllowAny])
def diagnostic_env(request):
    """Affiche l'état actuel de IA_PROVIDER et autres infos"""
    return Response({
        "IA_PROVIDER_env": os.getenv("IA_PROVIDER", "NOT SET"),
        "OPENAI_API_KEY_set": bool(os.getenv("OPENAI_API_KEY")),
        "current_service": type(get_llm_service()).__name__,
        "service_provider": getattr(get_llm_service(), 'provider', 'unknown'),
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_test_mock(request):
    """Test chat endpoint qui force le mock, sans dépendre de IA_PROVIDER"""
    try:
        utilisateur = get_object_or_404(Utilisateur, user=request.user)
    except:
        return Response({"error": "Profil utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    message = request.data.get('message', '').strip()
    if not message:
        return Response({"error": "Message vide"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Force mock provider explicitement
        llm_service = LLMService(provider='mock')
        
        response_data = llm_service.chat_tuteur(
            message=message,
            conversation_history=[
                {"role": "user", "content": message, "timestamp": "just_now"}
            ],
            niveau=getattr(utilisateur, 'niveau_scolaire', 'beginner'),
            matiere='test',
            age=getattr(utilisateur, 'age', 10) or 10,
            strengths='',
            weak_areas=''
        )

        return Response({
            "response": response_data.get('response', ''),
            "exercises": response_data.get('exercises', []),
            "provider": "mock (forced)",
            "status": "success"
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            "error": f"Erreur chat mock: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
