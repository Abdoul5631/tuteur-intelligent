from django.urls import path
from django.http import JsonResponse
import importlib
from functools import wraps, update_wrapper
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

# Helpers for lazy-loading views/classes to avoid import-time DRF access to settings
def lazy_view(view_name):
    """Import and return the view function or class directly without wrapping
    
    For class-based views, returns view.as_view()
    For functions, returns the function directly
    """
    try:
        module = importlib.import_module('core.views')
        view_obj = getattr(module, view_name)
        
        # Check if it's a class (specifically, a Django View class)
        if isinstance(view_obj, type) and hasattr(view_obj, 'as_view'):
            # It's a class-based view - return as_view()
            return view_obj.as_view()
        else:
            # It's a function - return directly
            return view_obj
            
    except (ImportError, AttributeError) as e:
        # Capture exception message before creating function (to avoid closure issues)
        error_msg = f'View "{view_name}" not found: {str(e)}'
        def error_view(request, *args, **kwargs):
            return JsonResponse({
                'error': error_msg
            }, status=500)
        return error_view

def lazy_class_view(module_name, class_name):
    def _view(request, *args, **kwargs):
        module = importlib.import_module(module_name)
        cls = getattr(module, class_name)
        # Create the view function and exempt it from CSRF to allow API clients
        view_func = cls.as_view()
        view_func = csrf_exempt(view_func)
        return view_func(request, *args, **kwargs)
    # Return the wrapper itself exempted so Django's CsrfViewMiddleware sees it
    return csrf_exempt(_view)

from .ia_endpoints import (
    chat_tuteur,
    historique_conversations,
    generer_exercices,
    analyser_reponse,
    recommandations_personnalisees,
    expliquer_concept,
    diagnostic_eleve,
)
from .ia_test_endpoints import (
    chat_test_mock,
    diagnostic_env,
)

# Create API view wrapper for profile that handles all methods
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class ProfilView(APIView):
    def get(self, request):
        try:
            from core.models import Utilisateur
            utilisateur = get_object_or_404(Utilisateur, user=request.user)
            # Construire un label lisible pour le niveau : préférer le niveau scolaire (ex: "Terminale"),
            # sinon tomber back sur le niveau global (débutant / intermédiaire / avancé)
            try:
                niveau_label = None
                if getattr(utilisateur, 'niveau_scolaire', None):
                    # get_FIELD_display disponible si le champ utilise des choices
                    niveau_label = utilisateur.get_niveau_scolaire_display()
                if not niveau_label and getattr(utilisateur, 'niveau_global', None):
                    niveau_label = utilisateur.get_niveau_global_display()
            except Exception:
                niveau_label = getattr(utilisateur, 'niveau_scolaire', None) or getattr(utilisateur, 'niveau_global', None)

            return Response({
                'id': utilisateur.id,
                'username': utilisateur.user.username,
                'email': utilisateur.user.email,
                'nom': utilisateur.nom,
                'prenom': utilisateur.prenom,
                # `niveau` : label lisible (préférer niveau scolaire),
                'niveau': niveau_label,
                # `niveau_code` : code stocké en base (ex: 'terminale', '6eme') si présent
                'niveau_code': getattr(utilisateur, 'niveau_scolaire', None),
                'niveau_global': getattr(utilisateur, 'niveau_global', None),
                'date_naissance': utilisateur.date_naissance,
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        try:
            from core.models import Utilisateur
            utilisateur = get_object_or_404(Utilisateur, user=request.user)
            
            # Update User model
            if 'email' in request.data:
                email = request.data.get('email', '').strip()
                if email:
                    request.user.email = email
                    request.user.save()
            
            # Update Utilisateur model
            if 'nom' in request.data:
                nom = request.data.get('nom', '').strip()
                if nom:
                    utilisateur.nom = nom
            
            if 'prenom' in request.data:
                prenom = request.data.get('prenom', '').strip()
                if prenom:
                    utilisateur.prenom = prenom
            
            if 'date_naissance' in request.data:
                date_naissance = request.data.get('date_naissance')
                if date_naissance:
                    utilisateur.date_naissance = date_naissance
            
            utilisateur.save()
            
            return Response({
                'id': utilisateur.id,
                'username': utilisateur.user.username,
                'email': utilisateur.user.email,
                'nom': utilisateur.nom,
                'prenom': utilisateur.prenom,
                # Retourner le label lisible pour `niveau` comme en GET
                'niveau': (utilisateur.get_niveau_scolaire_display() if getattr(utilisateur, 'niveau_scolaire', None) else (utilisateur.get_niveau_global_display() if getattr(utilisateur, 'niveau_global', None) else None)),
                'niveau_code': getattr(utilisateur, 'niveau_scolaire', None),
                'niveau_global': getattr(utilisateur, 'niveau_global', None),
                'date_naissance': utilisateur.date_naissance,
                'message': 'Profil mis à jour avec succès'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        # PATCH is same as PUT for profile
        return self.put(request)
    
    def options(self, request):
        return Response({})

profil_utilisateur_view = csrf_exempt(ProfilView.as_view())


# Preferences View wrapper
class PreferencesView(APIView):
    def get(self, request):
        try:
            from core.models import Utilisateur
            utilisateur = get_object_or_404(Utilisateur, user=request.user)
            return Response({
                'id': utilisateur.id,
                'notifications_actives': True,  # Par défaut
                'theme': 'light',  # Par défaut  
                'style_apprentissage': utilisateur.style_apprentissage or 'visuel',
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        try:
            from core.models import Utilisateur
            utilisateur = get_object_or_404(Utilisateur, user=request.user)
            
            if 'style_apprentissage' in request.data:
                utilisateur.style_apprentissage = request.data.get('style_apprentissage', '').strip()
            
            utilisateur.save()
            
            return Response({
                'id': utilisateur.id,
                'notifications_actives': True,
                'theme': 'light',
                'style_apprentissage': utilisateur.style_apprentissage or 'visuel',
                'message': 'Préférences mises à jour'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        return self.put(request)
    
    def options(self, request):
        return Response({})

preferences_utilisateur_view = csrf_exempt(PreferencesView.as_view())

def api_index(request):
    return JsonResponse({
        "message": "API root",
        "endpoints": {
            "register": "/api/auth/register/",
            "forgot_password": "/api/auth/forgot-password/",
            "reset_password": "/api/auth/reset-password/",
            "login": "/api/auth/login/",
            "refresh": "/api/auth/refresh/",
            "lessons": "/api/lecons/",
            "chat": "/api/ia/chat/"
        }
    })

urlpatterns = [
    # accueil de /api/
    path('', api_index, name='api-root'),

    # Auth
    path('auth/register/', lazy_view('register_user')),
    path('auth/forgot-password/', lazy_view('forgot_password')),
    path('auth/reset-password/', lazy_view('reset_password')),
    # JWT login / refresh (vue personnalisée supportant username ET email)
    path('auth/login/', lazy_view('login_user'), name='token_obtain_pair'),
    path('auth/refresh/', lazy_class_view('rest_framework_simplejwt.views', 'TokenRefreshView'), name='token_refresh'),
    
    # User
    path('me/', profil_utilisateur_view),
    path('me/update/', profil_utilisateur_view),  # Points to same view
    path('me/preferences/', preferences_utilisateur_view),
    path('me/change-password/', lazy_view('changer_mot_de_passe')),
    path('progression/', lazy_view('progression_utilisateur')),
    
    # Leçons et exercices (filtrés par niveau élève)
    path('niveaux/', lazy_view('niveaux_list')),
    path('matieres/', lazy_view('matieres_list')),
    path('eleve/matieres/', lazy_view('matieres_du_niveau_eleve')),
    path('lecons/', lazy_view('lecons_utilisateur')),
    path('lecons/<int:lecon_id>/', lazy_view('lecon_detail')),
    path('lecons/<int:lecon_id>/exercices/', lazy_view('exercices_par_lecon')),
    path('progression-eleve/', lazy_view('progression_eleve')),
    path('exercices/recommandations/', lazy_view('recommandations_exercices')),
    path('exercices/soumettre/', lazy_view('soumettre_reponse')),
    
    # Stats et leaderboard
    path('leaderboard/', lazy_view('leaderboard')),
    path('resultats/', lazy_view('resultats_detailles')),
    path('statistiques-lecons/', lazy_view('statistiques_lecons')),
    
    # 🤖 IA & TUTORING
    path('ia/chat/', chat_tuteur),
    path('ia/chat-test-mock/', chat_test_mock),  # Test endpoint (force mock)
    path('ia/diagnostic-env/', diagnostic_env),  # Show environment variables
    path('ia/historique-conversations/', historique_conversations),
    path('ia/generer-exercices/', generer_exercices),
    path('ia/analyser-reponse/', analyser_reponse),
    path('ia/recommandations/', recommandations_personnalisees),
    path('ia/expliquer/', expliquer_concept),
    path('ia/diagnostic/', diagnostic_eleve),
]
