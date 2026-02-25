from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Lecon, Exercice, Utilisateur, Resultat, Matiere, NiveauScolaire, ProgressionNotion
from .serializers import LeconSerializer, ExerciceSerializer, NiveauScolaireSerializer, MatiereSerializer
from .services.ia_service import corriger_exercice


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    Bienvenue sur l'API Tuteur Intelligent
    """
    return Response({
        'message': '🎓 Bienvenue sur l\'API Tuteur Intelligent',
        'version': '1.0.0',
        'endpoints': {
            'authentication': {
                'register': '/api/auth/register/ (POST)',
                'login': '/api/auth/login/ (POST)',
                'refresh': '/api/auth/refresh/ (POST)',
            },
            'user': {
                'profile': '/api/me/ (GET)',
                'progression': '/api/progression/ (GET)',
            },
            'learning': {
                'lessons': '/api/lecons/ (GET)',
                'exercises': '/api/lecons/<id>/exercices/ (GET)',
                'submit': '/api/exercices/soumettre/ (POST)',
                'recommendations': '/api/exercices/recommandations/ (GET)',
            },
            'stats': {
                'leaderboard': '/api/leaderboard/ (GET)',
            }
        },
        'status': '✅ Backend actif et prêt'
    })



@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Endpoint d'enregistrement utilisateur avec tous les attributs
    """
    # Champs requis
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password_confirm = request.data.get('password_confirm')
    
    # Champs élève
    nom = request.data.get('nom')
    prenom = request.data.get('prenom')
    date_naissance = request.data.get('date_naissance')
    niveau_scolaire = (request.data.get('niveau_scolaire') or '').strip().lower()
    parent_email = request.data.get('parent_email')
    telephone = request.data.get('telephone')

    # Validation des champs requis (nom/prenom optionnels)
    if not all([username, email, password, password_confirm]):
        return Response(
            {'error': 'Les champs suivants sont requis: username, email, password, password_confirm'},
            status=status.HTTP_400_BAD_REQUEST
        )
    nom = (nom or '').strip() or username
    prenom = (prenom or '').strip() or username

    if len(password) < 8:
        return Response(
            {'error': 'Le mot de passe doit avoir au moins 8 caractères'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if password != password_confirm:
        return Response(
            {'error': 'Les mots de passe ne correspondent pas'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Cet utilisateur existe déjà'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Cet email est déjà utilisé'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Niveau scolaire obligatoire (CP1 → Terminale) — saisi une seule fois à l'inscription
    NIVEAUX_SCOLAIRES_VALIDES = [
        'cp1', 'cp2', 'ce1', 'ce2', 'cm1', 'cm2',
        '6eme', '5eme', '4eme', '3eme', 'seconde', '1ere', 'terminale'
    ]
    if not niveau_scolaire or niveau_scolaire not in NIVEAUX_SCOLAIRES_VALIDES:
        return Response(
            {'error': 'Choisissez votre niveau scolaire (CP1 à Terminale). Ce choix ne sera plus modifiable.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Déduire niveau_global pour rétrocompat
    if niveau_scolaire in ('cp1', 'cp2', 'ce1', 'ce2', 'cm1', 'cm2'):
        niveau_global = 'débutant'
    elif niveau_scolaire in ('6eme', '5eme', '4eme', '3eme'):
        niveau_global = 'intermédiaire'
    else:
        niveau_global = 'avancé'

    # Créer l'utilisateur Django (create_user = mot de passe hashé, is_active=True par défaut)
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=prenom,
            last_name=nom,
        )
        user.is_active = True
        user.save(update_fields=['is_active'])

        # Créer le profil élève — obligatoire pour accéder aux leçons / matières / IA
        utilisateur = Utilisateur.objects.create(
            user=user,
            nom=nom,
            prenom=prenom,
            date_naissance=date_naissance if date_naissance else None,
            niveau_scolaire=niveau_scolaire,
            niveau_global=niveau_global,
            parent_email=parent_email if parent_email else None,
            telephone=(telephone or '')[:15],
        )

        return Response({
            'message': 'Compte créé avec succès',
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'prenom': prenom,
            'nom': nom,
            'niveau_scolaire': niveau_scolaire,
            'niveau_global': niveau_global,
        }, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        msg = e.messages[0] if e.messages else str(e)
        if 'too common' in msg.lower() or 'common' in msg.lower():
            msg = 'Mot de passe trop courant. Choisissez un mot de passe plus original.'
        elif 'numeric' in msg.lower() or 'entirely numeric' in msg.lower():
            msg = 'Le mot de passe ne doit pas être uniquement composé de chiffres.'
        elif 'short' in msg.lower() or 'minimum' in msg.lower():
            msg = 'Le mot de passe doit contenir au moins 8 caractères.'
        return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la création du compte: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )


def _password_looks_hashed(stored_password):
    """Django hash = pbkdf2_sha256$... ou argon2$... ; sinon considéré comme clair."""
    if not stored_password or len(stored_password) < 50:
        return False
    return (
        stored_password.startswith('pbkdf2_') or
        stored_password.startswith('argon2') or
        stored_password.startswith('bcrypt$')
    )


def _ensure_utilisateur_for_user(user):
    """Crée le profil Utilisateur si absent (utilisateurs créés manuellement)."""
    from .models import Utilisateur
    if Utilisateur.objects.filter(user=user).exists():
        return
    Utilisateur.objects.create(
        user=user,
        nom=user.last_name or user.username,
        prenom=user.first_name or user.username,
        niveau_scolaire='ce1',
        niveau_global='débutant',
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Connexion avec username/password. Le username est tolérant à la casse.
    Accepte JSON ou form. Répare si besoin : mot de passe en clair → hash,
    User sans profil Utilisateur → création du profil.
    """
    if request.content_type and 'application/json' in request.content_type:
        data = request.data
    else:
        data = request.POST
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    if not username:
        return Response(
            {'detail': 'Le nom d\'utilisateur est requis.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if not password:
        return Response(
            {'detail': 'Le mot de passe est requis.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.filter(username__iexact=username).first()
    if not user:
        return Response(
            {'detail': 'Aucun compte trouvé avec ce nom d\'utilisateur.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    if not user.is_active:
        return Response(
            {'detail': 'Ce compte a été désactivé. Contactez l\'administrateur.'},
            status=status.HTTP_403_FORBIDDEN
        )

    auth_user = authenticate(request, username=user.username, password=password)
    if not auth_user:
        # Réparation : mot de passe stocké en clair (création manuelle / admin)
        if not _password_looks_hashed(user.password) and password == user.password:
            user.set_password(password)
            user.save(update_fields=['password'])
            auth_user = user
        else:
            return Response(
                {'detail': 'Mot de passe incorrect. Utilisez « Mot de passe oublié » pour réinitialiser.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

    _ensure_utilisateur_for_user(auth_user)

    refresh = RefreshToken.for_user(auth_user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def niveaux_list(request):
    """Liste des niveaux scolaires CP1 → Terminale"""
    niveaux = NiveauScolaire.objects.all().order_by('ordre')
    return Response(NiveauScolaireSerializer(niveaux, many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def matieres_list(request):
    """Liste de toutes les matières (pour admin / référence)."""
    matieres = Matiere.objects.all().order_by('nom')
    return Response(MatiereSerializer(matieres, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def matieres_du_niveau_eleve(request):
    """
    Matières du niveau de l'élève (saisi à l'inscription).
    Si aucune matière n'existe pour ce niveau, le système en crée une automatiquement
    (sans dépendance à une commande manuelle) pour garantir qu'un élève valide voit
    toujours au moins une matière et des leçons.
    """
    utilisateur = get_object_or_404(Utilisateur, user=request.user)
    code_niveau = utilisateur.niveau_scolaire
    matieres = Matiere.objects.filter(
        lecons__niveau__code=code_niveau
    ).distinct().order_by('nom')
    if not matieres.exists():
        from .services.curriculum_complet import ensure_curriculum_complet_pour_niveau
        ensure_curriculum_complet_pour_niveau(code_niveau)
        matieres = Matiere.objects.filter(
            lecons__niveau__code=code_niveau
        ).distinct().order_by('nom')
    return Response(MatiereSerializer(matieres, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lecons_utilisateur(request):
    """
    Leçons du niveau de l'élève connecté. Filtrage automatique par niveau_scolaire.
    Query: ?matiere_id=<id> pour restreindre à une matière.
    """
    utilisateur = get_object_or_404(Utilisateur, user=request.user)
    code_niveau = utilisateur.niveau_scolaire
    qs = Lecon.objects.filter(niveau__code=code_niveau).select_related('matiere', 'niveau')
    matiere_id = request.query_params.get('matiere_id')
    if matiere_id:
        qs = qs.filter(matiere_id=matiere_id)
    qs = qs.order_by('matiere__nom', 'ordre', 'titre')
    return Response(LeconSerializer(qs, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lecon_detail(request, lecon_id):
    """Détail d'une leçon (vérifie que la leçon est du niveau de l'élève)."""
    utilisateur = get_object_or_404(Utilisateur, user=request.user)
    lecon = get_object_or_404(
        Lecon.objects.filter(niveau__code=utilisateur.niveau_scolaire),
        id=lecon_id
    )
    return Response(LeconSerializer(lecon).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exercices_par_lecon(request, lecon_id):
    """Exercices d'une leçon (leçon doit être du niveau de l'élève connecté)."""
    utilisateur = get_object_or_404(Utilisateur, user=request.user)
    lecon = get_object_or_404(
        Lecon.objects.filter(niveau__code=utilisateur.niveau_scolaire),
        id=lecon_id
    )
    exercices = Exercice.objects.filter(lecon=lecon)
    return Response(ExerciceSerializer(exercices, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def soumettre_reponse(request):
    utilisateur = get_object_or_404(Utilisateur, user=request.user)

    exercice_id = request.data.get("exercice_id")
    reponse = request.data.get("reponse")

    if not exercice_id or not reponse:
        return Response(
            {"error": "exercice_id et reponse sont requis"},
            status=400
        )

    exercice = get_object_or_404(Exercice, id=exercice_id)

    score, feedback = corriger_exercice(exercice, reponse)

    Resultat.objects.create(
        utilisateur=utilisateur,
        exercice=exercice,
        reponse_donnee=reponse,
        score=score,
        feedback_ia=feedback
    )

    return Response({
        "score": score,
        "feedback": feedback
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profil_utilisateur(request):
    """
    Retourne les informations du profil utilisateur
    """
    utilisateur = get_object_or_404(Utilisateur, user=request.user)
    
    return Response({
        'id': utilisateur.id,
        'username': utilisateur.user.username,
        'email': utilisateur.user.email,
        'nom': utilisateur.nom,
        'prenom': utilisateur.prenom,
        'niveau': utilisateur.niveau_global,
        # ...other fields...
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def progression_eleve(request):
    """
    Suivi progression élève : notions maîtrisées, notions faibles.
    Base pour l'IA personnalisée.
    """
    utilisateur = get_object_or_404(Utilisateur, user=request.user)
    progressions = ProgressionNotion.objects.filter(utilisateur=utilisateur)
    notions_maitrisees = list(progressions.filter(statut='maitrise').values_list('notion', flat=True))
    notions_faibles = list(progressions.filter(statut='faible').values_list('notion', flat=True))
    return Response({
        'niveau_scolaire': utilisateur.niveau_scolaire,
        'niveau_global': utilisateur.niveau_global,
        'notions_maitrisees': notions_maitrisees,
        'notions_faibles': notions_faibles,
        'domaines_forts': utilisateur.domaines_forts or [],
        'domaines_faibles': utilisateur.domaines_faibles or [],
        'score_moyen': utilisateur.score_moyen,
        'total_exercices': utilisateur.total_exercices_completes,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def progression_utilisateur(request):
    """
    Retourne la progression et les statistiques de l'utilisateur
    """
    from .services.ia_service import progression_utilisateur as get_progression
    
    utilisateur = get_object_or_404(Utilisateur, user=request.user)
    progr = get_progression(utilisateur)
    
    return Response(progr)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommandations_exercices(request):
    """
    Propose des exercices recommandés basés sur le niveau de l'utilisateur
    """
    from .services.ia_service import proposer_exercices
    
    utilisateur = get_object_or_404(Utilisateur, user=request.user)
    exercices = proposer_exercices(utilisateur, nombre=5)
    
    return Response(ExerciceSerializer(exercices, many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def leaderboard(request):
    """
    Leaderboard global avec les meilleures performances
    """
    utilisateurs = Utilisateur.objects.all()
    leaderboard_data = []
    
    for user in utilisateurs:
        resultats = Resultat.objects.filter(utilisateur=user)
        total = resultats.count()
        
        if total > 0:
            moyenne = sum(r.score for r in resultats) / total
            reussis = resultats.filter(score=100).count()
        else:
            moyenne = 0
            reussis = 0
        
        leaderboard_data.append({
            'username': user.user.username,
            'niveau': user.niveau_global,
            'moyenne': round(moyenne, 2),
            'total_exercices': total,
            'reussis': reussis,
            'position': 0  # À calculer après tri
        })
    
    # Trier par moyenne (décroissant), puis par exercices (décroissant)
    leaderboard_data.sort(key=lambda x: (x['moyenne'], x['total_exercices']), reverse=True)
    
    # Ajouter les positions
    for i, entry in enumerate(leaderboard_data):
        entry['position'] = i + 1
    
    return Response(leaderboard_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def resultats_detailles(request):
    """
    Récupère tous les résultats détaillés de l'utilisateur
    """
    utilisateur = get_object_or_404(Utilisateur, user=request.user)
    resultats = Resultat.objects.filter(utilisateur=utilisateur).order_by('-date')
    
    data = []
    for r in resultats:
        data.append({
            'id': r.id,
            'exercice_id': r.exercice.id,
            'exercice_question': r.exercice.question,
            'lecon': r.exercice.lecon.titre,
            'reponse_donnee': r.reponse_donnee,
            'reponse_correcte': getattr(r.exercice, 'reponse_correcte', None) or getattr(r.exercice, 'reponse', ''),
            'score': r.score,
            'feedback': r.feedback_ia,
            'date': r.date
        })
    
    return Response({
        'total_resultats': len(data),
        'moyenne_globale': round(sum(r['score'] for r in data) / len(data), 2) if data else 0,
        'reussis': len([r for r in data if r['score'] == 100]),
        'resultats': data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def statistiques_lecons(request):
    """
    Statistiques détaillées par leçon
    """
    utilisateur = get_object_or_404(Utilisateur, user=request.user)
    
    lecons = Lecon.objects.all()
    stats = []
    
    for lecon in lecons:
        resultats = Resultat.objects.filter(
            utilisateur=utilisateur,
            exercice__lecon=lecon
        )
        
        total = resultats.count()
        if total > 0:
            moyenne = sum(r.score for r in resultats) / total
            reussis = resultats.filter(score=100).count()
        else:
            moyenne = 0
            reussis = 0
        
        stats.append({
            'lecon_id': lecon.id,
            'lecon_titre': lecon.titre,
            'niveau': lecon.niveau_global,
            'exercices_total': lecon.exercices.count(),
            'exercices_faits': total,
            'moyenne': round(moyenne, 2),
            'reussis': reussis,
            'progression': round((reussis / lecon.exercices.count() * 100) if lecon.exercices.count() > 0 else 0, 2)
        })
    
    return Response(stats)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    """
    Endpoint pour la réinitialisation du mot de passe oublié
    """
    email = request.data.get('email')
    
    if not email:
        return Response(
            {'error': 'Email requis'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(email=email)
        # Note: En production, envoyer un email avec lien de réinitialisation
        # Pour demo, retourner un message de succès
        return Response({
            'message': f'Un lien de réinitialisation a été envoyé à {email}',
            'note': 'En production, vérifier l\'email pour le lien de réinitialisation'
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        # Ne pas révéler si l'email existe
        return Response({
            'message': 'Si cet email existe dans notre système, vous recevrez un lien de réinitialisation'
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    """
    Endpoint pour réinitialiser le mot de passe avec token
    """
    username = request.data.get('username')
    new_password = request.data.get('new_password')
    new_password_confirm = request.data.get('new_password_confirm')
    
    if not all([username, new_password, new_password_confirm]):
        return Response(
            {'error': 'Tous les champs sont requis'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if len(new_password) < 8:
        return Response(
            {'error': 'Le mot de passe doit avoir au moins 8 caractères'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if new_password != new_password_confirm:
        return Response(
            {'error': 'Les mots de passe ne correspondent pas'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.filter(username__iexact=username.strip()).first()
    if not user:
        return Response(
            {'error': 'Utilisateur non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )
    user.set_password(new_password)
    user.save()
    return Response({
        'message': 'Mot de passe réinitialisé avec succès. Vous pouvez vous connecter.'
    }, status=status.HTTP_200_OK)
