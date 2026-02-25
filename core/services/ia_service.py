from core.models import Resultat, Exercice

def analyser_niveau(utilisateur):
    """
    Analyse les performances de l'élève et décide du niveau à proposer
    """
    resultats = Resultat.objects.filter(utilisateur=utilisateur)

    if resultats.count() == 0:
        return "debutant"

    moyenne = sum(r.score for r in resultats) / resultats.count()

    if moyenne < 50:
        return "debutant"
    elif moyenne < 75:
        return "intermediaire"
    else:
        return "avance"

def proposer_exercices(utilisateur, nombre=5):
    """
    Propose des exercices adaptés au niveau de l'élève
    - Evite les exercices déjà maîtrisés à 100%
    - Se concentre sur les exercices non maîtrisés
    """
    niveau = analyser_niveau(utilisateur)

    # Exclure les exercices déjà réussis à 100%
    exercices_maitrises_ids = Resultat.objects.filter(
        utilisateur=utilisateur, score=100
    ).values_list('exercice_id', flat=True)

    # Sélectionner les exercices du niveau correspondant
    exercices_disponibles = Exercice.objects.filter(
        niveau=niveau
    ).exclude(id__in=exercices_maitrises_ids)

    # Limiter le nombre d'exercices proposés
    exercices = exercices_disponibles[:nombre]

    return exercices
    
def progression_utilisateur(utilisateur):
    """
    Retourne les statistiques de progression d'un utilisateur
    """
    resultats = Resultat.objects.filter(utilisateur=utilisateur)

    if resultats.count() == 0:
        return {
            "niveau": "debutant",
            "moyenne": 0,
            "total_exercices": 0
        }

    total = resultats.count()
    moyenne = sum(r.score for r in resultats) / total
    niveau = analyser_niveau(utilisateur)

    return {
        "niveau": niveau,
        "moyenne": moyenne,
        "total_exercices": total
    }


def corriger_exercice(exercice, reponse):
    """
    Corrige un exercice et retourne (score, feedback IA)
    """

    if not reponse:
        return 0, "❌ Aucune réponse fournie."

    reponse_attendue = getattr(exercice, 'reponse_correcte', None) or getattr(exercice, 'reponse', None) or ''
    if reponse.strip().lower() == str(reponse_attendue).strip().lower():
        return 100, "✅ Bonne réponse ! Excellent travail."
    else:
        return 0, (
            "❌ Réponse incorrecte.\n"
            f"La bonne réponse était : {reponse_attendue}\n"
            "👉 Relis bien la leçon et réessaie."
        )
