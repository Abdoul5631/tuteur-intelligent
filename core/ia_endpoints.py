"""
API Endpoints pour l'intégration IA
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # pour l'éditeur / type checker uniquement
    from rest_framework.decorators import api_view, permission_classes  # type: ignore[reportMissingImports]
    from rest_framework.permissions import IsAuthenticated  # type: ignore[reportMissingImports]
    from rest_framework.response import Response  # type: ignore[reportMissingImports]
    from rest_framework import status  # type: ignore[reportMissingImports]
else:
    try:
        from rest_framework.decorators import api_view, permission_classes
        from rest_framework.permissions import IsAuthenticated
        from rest_framework.response import Response
        from rest_framework import status
    except Exception:
        # fallback léger pour supprimer les erreurs d'éditeur si les paquets ne sont pas installés.
        # Installez les dépendances réelles dans votre venv (voir commande dans le terminal).
        def api_view(_):
            def dec(f): return f
            return dec
        def permission_classes(_):
            def dec(f): return f
            return dec
        class IsAuthenticated: pass
        class Response:
            def __init__(self, data=None, status=None):
                self.data = data
                self.status_code = status
        status = type('status', (), {
            'HTTP_200_OK': 200,
            'HTTP_201_CREATED': 201,
            'HTTP_400_BAD_REQUEST': 400,
            'HTTP_404_NOT_FOUND': 404,
            'HTTP_500_INTERNAL_SERVER_ERROR': 500
        })

from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta

from core.models import (
    Utilisateur, Matiere, Lecon, Exercice, Resultat,
    ConversationIA, ConversationMessage
)
from core.services.llm_service import get_llm_service


# ========================
# CHAT TUTEUR
# ========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_tuteur(request):
    try:
        utilisateur = get_object_or_404(Utilisateur, user=request.user)
    except:
        return Response({"error": "Profil utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    message = request.data.get('message', '').strip()
    matiere_id = request.data.get('matiere_id')
    lecon_id = request.data.get('lecon_id')

    if not message:
        return Response({"error": "Message vide"}, status=status.HTTP_400_BAD_REQUEST)

    matiere = None
    lecon = None
    if matiere_id:
        matiere = get_object_or_404(Matiere, id=matiere_id)
    if lecon_id:
        lecon = get_object_or_404(Lecon, id=lecon_id)

    conversation = ConversationIA.objects.filter(utilisateur=utilisateur, date_fin__isnull=True).first()

    if not conversation:
        conversation = ConversationIA.objects.create(
            utilisateur=utilisateur,
            matiere=matiere,
            lecon=lecon,
            contexte={
                "niveau_scolaire": getattr(utilisateur, 'niveau_scolaire', None),
                "niveau_global": getattr(utilisateur, 'niveau_global', None),
            }
        )

    user_message = ConversationMessage.objects.create(
        conversation=conversation,
        role='user',
        type_message='question',
        contenu=message
    )

    try:
        llm_service = get_llm_service()
        lecon_titre = lecon.titre if lecon else None
        lecon_contenu = (lecon.contenu_principal or '')[:800] if lecon else None

        # 🔥 CORRECTION CRITIQUE: Récupérer tout l'historique de la conversation
        # pour que l'IA ait le contexte complet et puisse vraiment comprendre
        historique_messages = list(
            conversation.messages.exclude(id=user_message.id)  # Exclure le message qu'on vient de créer
            .values('role', 'contenu', 'timestamp')
            .order_by('timestamp')
        )
        
        # Convertir au format attendu par le service IA
        messages_contexte = [
            {"role": msg['role'], "content": msg['contenu'], "timestamp": str(msg['timestamp'])}
            for msg in historique_messages
        ]
        
        # Ajouter le message utilisateur courant à la fin
        messages_contexte.append({
            "role": "user",
            "content": message,
            "timestamp": str(user_message.timestamp)
        })

        response_data = llm_service.chat_tuteur(
            message=message,  # Message courant pour compatibilité
            conversation_history=messages_contexte,  # 🔥 NOUVEAU : Historique complet
            niveau=getattr(utilisateur, 'niveau_scolaire', None),
            matiere=(matiere.get_nom_display() if matiere and hasattr(matiere, 'get_nom_display') else (matiere.nom if matiere else 'général')),
            age=getattr(utilisateur, 'age', None) or 10,
            strengths=", ".join(getattr(utilisateur, 'domaines_forts', []) or []),
            weak_areas=", ".join(getattr(utilisateur, 'domaines_faibles', []) or []),
            lecon_titre=lecon_titre,
            lecon_contenu=lecon_contenu,
        )

        response_text = response_data.get('reponse', '')
        response_type = response_data.get('type', 'explication')
        exercises = response_data.get('exercises', [])

        assistant_message = ConversationMessage.objects.create(
            conversation=conversation,
            role='assistant',
            type_message=response_type,
            contenu=response_text
        )

        conversation.nombre_messages = (conversation.nombre_messages or 0) + 2
        conversation.save()

        return Response({
            'id': assistant_message.id,
            'response': response_text,
            'type': response_type,
            'conversation_id': conversation.id,
            'timestamp': assistant_message.timestamp,
            'confiance': response_data.get('confiance', 0.8),
            'exercises': exercises
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Erreur IA: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ========================
# HISTORIQUE CHAT
# ========================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def historique_conversations(request):
    try:
        utilisateur = get_object_or_404(Utilisateur, user=request.user)
    except:
        return Response({"error": "Profil utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    limit = int(request.query_params.get('limit', 10))
    matiere_id = request.query_params.get('matiere_id')

    conversations = ConversationIA.objects.filter(utilisateur=utilisateur)
    if matiere_id:
        conversations = conversations.filter(matiere_id=matiere_id)

    conversations = conversations[:limit]

    result = []
    for conv in conversations:
        messages = list(conv.messages.values('role', 'contenu', 'timestamp')) if hasattr(conv, 'messages') else []
        result.append({
            'id': conv.id,
            'matiere': (conv.matiere.get_nom_display() if getattr(conv, 'matiere', None) and hasattr(conv.matiere, 'get_nom_display') else (conv.matiere.nom if getattr(conv, 'matiere', None) else 'Général')),
            'lecon': conv.lecon.titre if getattr(conv, 'lecon', None) else None,
            'date_debut': conv.date_debut,
            'date_fin': conv.date_fin,
            'nombre_messages': conv.nombre_messages,
            'resume': conv.resume,
            'messages': messages
        })

    # Retourner sous forme d'objet pour stabilité côté client
    return Response({
        'conversations': result
    }, status=status.HTTP_200_OK)


# ========================
# GÉNÉRER EXERCICES
# ========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generer_exercices(request):
    try:
        utilisateur = get_object_or_404(Utilisateur, user=request.user)
    except:
        return Response({"error": "Profil utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    nombre = int(request.data.get('nombre', 3))
    matiere_id = request.data.get('matiere_id')
    topics = request.data.get('topics', [])
    difficulte = request.data.get('difficulte', 'adapte')

    if nombre < 1 or nombre > 10:
        return Response({"error": "Nombre d'exercices doit être entre 1 et 10"}, status=status.HTTP_400_BAD_REQUEST)

    if not matiere_id:
        return Response({"error": "matiere_id requis"}, status=status.HTTP_400_BAD_REQUEST)

    matiere = get_object_or_404(Matiere, id=matiere_id)

    try:
        llm_service = get_llm_service()

        exercices_data = llm_service.generer_exercices(
            nombre=nombre,
            niveau=getattr(utilisateur, 'niveau_scolaire', None),
            matiere=(matiere.nom if hasattr(matiere, 'nom') else None),
            topics=topics if topics else ["general"],
            difficulty_history=getattr(utilisateur, 'niveau_global', None)
        )

        exercices_sauvegardes = []

        lecon_default, _ = Lecon.objects.get_or_create(
            titre=f"Exercices Générés - {(matiere.get_nom_display() if hasattr(matiere, 'get_nom_display') else getattr(matiere, 'nom', 'Général'))}",
            matiere=matiere,
            defaults={
                'niveau_global': getattr(utilisateur, 'niveau_global', None),
                'niveau_scolaire': getattr(utilisateur, 'niveau_scolaire', None),
                'contenu_principal': "Exercices générés automatiquement par l'IA"
            }
        )

        for data in exercices_data:
            exercice = Exercice.objects.create(
                lecon=lecon_default,
                matiere=matiere,
                question=data.get('question', ''),
                type_exercice=data.get('type', 'choix_multiple'),
                reponse_correcte=data.get('reponse', ''),
                options=data.get('options', []),
                explication_bonne_reponse=data.get('explication', ''),
                erreurs_courantes=data.get('erreurs_courantes', []),
                niveau=getattr(utilisateur, 'niveau_global', None),
                difficulte=data.get('difficulte', 5),
                points_valeur=data.get('points', 10),
                temps_estime=data.get('temps_estime', 300),
                concepts_evalues=data.get('concepts', [])
            )
            exercices_sauvegardes.append(exercice)

        return Response({
            'nombre_genere': len(exercices_sauvegardes),
            'exercices': [
                {
                    'id': ex.id,
                    'question': ex.question,
                    'type': ex.type_exercice,
                    'options': ex.options,
                    'difficulte': ex.difficulte,
                    'points': ex.points_valeur,
                    'temps_estime': ex.temps_estime
                }
                for ex in exercices_sauvegardes
            ]
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": f"Erreur génération: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ========================
# ANALYSER RÉPONSE
# ========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyser_reponse(request):
    try:
        utilisateur = get_object_or_404(Utilisateur, user=request.user)
    except:
        return Response({"error": "Profil utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    exercice_id = request.data.get('exercice_id')
    reponse_donnee = request.data.get('reponse_donnee', '').strip()
    temps_resolution = request.data.get('temps_resolution')

    if not exercice_id:
        return Response({"error": "exercice_id requis"}, status=status.HTTP_400_BAD_REQUEST)

    exercice = get_object_or_404(Exercice, id=exercice_id)

    try:
        llm_service = get_llm_service()

        analysis = llm_service.analyser_reponse(
            question=exercice.question,
            reponse_donnee=reponse_donnee,
            reponse_correcte=exercice.reponse_correcte,
            concept=", ".join(exercice.concepts_evalues or []),
            niveau=getattr(utilisateur, 'niveau_global', None)
        )

        score = analysis.get('score', 0)
        correct = analysis.get('correct', False)

        tentative_num = Resultat.objects.filter(utilisateur=utilisateur, exercice=exercice).count() + 1

        resultat = Resultat.objects.create(
            utilisateur=utilisateur,
            exercice=exercice,
            reponse_donnee=reponse_donnee,
            score=score,
            numero_tentative=tentative_num,
            temps_resolution=temps_resolution,
            feedback_ia=analysis.get('feedback_positif', ''),
            feedback_detaille=analysis.get('explication', ''),
            encouragement=analysis.get('encouragement', ''),
            analyse_erreur={'type': 'auto_analysis'}
        )

        utilisateur.total_exercices_completes = (utilisateur.total_exercices_completes or 0) + 1
        utilisateur.derniere_activite = timezone.now()

        total_results = Resultat.objects.filter(utilisateur=utilisateur)
        if total_results.exists():
            utilisateur.score_moyen = sum(r.score for r in total_results) / total_results.count()

        utilisateur.save()

        return Response({
            'correct': correct,
            'score': score,
            'feedback_positif': analysis.get('feedback_positif', ''),
            'explication': analysis.get('explication', ''),
            'encouragement': analysis.get('encouragement', ''),
            'resultat_id': resultat.id,
            'prochaine_etape': analysis.get('prochaine_etape'),
            'tentative_num': tentative_num
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": f"Erreur analyse: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ========================
# RECOMMANDATIONS
# ========================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommandations_personnalisees(request):
    try:
        utilisateur = get_object_or_404(Utilisateur, user=request.user)
    except:
        return Response({"error": "Profil utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    matiere_id = request.query_params.get('matiere_id')

    resultats = Resultat.objects.filter(utilisateur=utilisateur)

    exercices_faibles = resultats.filter(score__lt=70).values_list('exercice__concepts_evalues', flat=True)

    weak_concepts = set()
    for concepts in exercices_faibles:
        weak_concepts.update(concepts or [])

    if matiere_id:
        lecons = Lecon.objects.filter(matiere_id=matiere_id, niveau_global=getattr(utilisateur, 'niveau_global', None))
    else:
        lecons = Lecon.objects.filter(niveau_global=getattr(utilisateur, 'niveau_global', None))

    lecons_recommandees = lecons[:5]

    exercices_recommandes = Exercice.objects.filter(
        difficulte__gte=(getattr(utilisateur, 'score_moyen', 0) / 20) - 1,
        difficulte__lte=(getattr(utilisateur, 'score_moyen', 0) / 20) + 1,
        actif=True
    )[:3]

    return Response({
        'lecons_recommandees': [
            {
                'id': l.id,
                'titre': l.titre,
                'matiere': (l.matiere.get_nom_display() if hasattr(l.matiere, 'get_nom_display') else getattr(l.matiere, 'nom', None)),
                'difficulte': l.difficulte,
                'temps_estime': l.temps_estime
            }
            for l in lecons_recommandees
        ],
        'exercices_bonus': [
            {
                'id': e.id,
                'question': (e.question[:50] if e.question else ''),
                'difficulte': e.difficulte,
                'points': e.points_valeur
            }
            for e in exercices_recommandes
        ],
        'prochaine_etape': 'Continuer avec les exercices recommandés',
        'areas_to_improve': list(weak_concepts)[:5],
        'progress_score': getattr(utilisateur, 'score_moyen', 0)
    }, status=status.HTTP_200_OK)


# ========================
# EXPLIQUER CONCEPT
# ========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def expliquer_concept(request):
    try:
        utilisateur = get_object_or_404(Utilisateur, user=request.user)
    except:
        return Response({"error": "Profil utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    concept = request.data.get('concept', '').strip()
    matiere_id = request.data.get('matiere_id')
    style = request.data.get('style', 'analogie')

    if not concept:
        return Response({"error": "concept requis"}, status=status.HTTP_400_BAD_REQUEST)

    if not matiere_id:
        return Response({"error": "matiere_id requis"}, status=status.HTTP_400_BAD_REQUEST)

    matiere = get_object_or_404(Matiere, id=matiere_id)

    try:
        llm_service = get_llm_service()

        explication = llm_service.expliquer_concept(
            concept=concept,
            niveau=getattr(utilisateur, 'niveau_scolaire', None),
            matiere=(matiere.nom if hasattr(matiere, 'nom') else None),
            style=style
        )

        return Response({'concept': concept, 'explication': explication, 'style': style}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Erreur explication: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ========================
# DIAGNOSTIC
# ========================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def diagnostic_eleve(request):
    try:
        utilisateur = get_object_or_404(Utilisateur, user=request.user)
    except:
        return Response({"error": "Profil utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    resultats = Resultat.objects.filter(utilisateur=utilisateur)
    total = resultats.count()

    if total == 0:
        return Response({'score_moyen': 0, 'total_exercices': 0, 'progression': 'debut', 'recommendations': 'Commencez par une leçon'}, status=status.HTTP_200_OK)

    resultats_par_matiere = {}
    for resultat in resultats:
        matiere_nom = (resultat.exercice.matiere.get_nom_display() if hasattr(resultat.exercice.matiere, 'get_nom_display') else getattr(resultat.exercice.matiere, 'nom', None))
        if matiere_nom not in resultats_par_matiere:
            resultats_par_matiere[matiere_nom] = []
        resultats_par_matiere[matiere_nom].append(resultat.score)

    scores_par_matiere = {m: sum(s) / len(s) for m, s in resultats_par_matiere.items()}

    resultats_tries = resultats.order_by('date')
    if resultats_tries.count() > 5:
        premiers = list(resultats_tries[:5])
        derniers = list(resultats_tries.reverse()[:5])
        progression_debut = sum(r.score for r in premiers) / 5
        progression_fin = sum(r.score for r in derniers) / 5
        progression = 'bonne' if progression_fin > progression_debut else 'stagnante'
    else:
        progression = 'insuffisant'

    return Response({
        'score_moyen': getattr(utilisateur, 'score_moyen', 0),
        'total_exercices': total,
        'niveaux_maitrise': scores_par_matiere,
        'domaines_forts': getattr(utilisateur, 'domaines_forts', []),
        'domaines_faibles': getattr(utilisateur, 'domaines_faibles', []),
        'progression': progression,
        'nombre_conversations': getattr(utilisateur, 'conversations_ia', []).count() if hasattr(utilisateur, 'conversations_ia') else 0,
        'niveau_actuel': getattr(utilisateur, 'niveau_global', None),
        'niveau_scolaire': getattr(utilisateur, 'niveau_scolaire', None)
    }, status=status.HTTP_200_OK)
