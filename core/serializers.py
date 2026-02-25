from rest_framework import serializers
from .models import Lecon, Exercice, NiveauScolaire, Matiere


class NiveauScolaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = NiveauScolaire
        fields = ['id', 'code', 'libelle', 'ordre', 'cycle']


class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = ['id', 'nom', 'description', 'couleur_hex', 'icone']


class ExerciceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercice
        fields = "__all__"


class LeconSerializer(serializers.ModelSerializer):
    exercices = ExerciceSerializer(many=True, read_only=True)
    # champ alias utilisé par le frontend (valeur lisible)
    niveau = serializers.SerializerMethodField()

    class Meta:
        model = Lecon
        fields = [
            'id', 'titre', 'description', 'niveau_scolaire', 'niveau_global',
            'niveau', 'exercices', 'contenu_principal', 'contenu_simplifie',
            'contenu_approfondi', 'image', 'video_url', 'concepts_cles',
            'ordre', 'difficulte', 'temps_estime', 'date_creation', 'date_modification', 'matiere'
        ]

    def get_niveau(self, obj):
        # Prioriser niveau_global si présent, sinon niveau_scolaire
        val = getattr(obj, 'niveau_global', None) or getattr(obj, 'niveau_scolaire', None)
        if not val:
            return ''
        # Normaliser pour affichage: Débutant / Intermédiaire / Avancé
        mapping = {
            'débutant': 'Débutant',
            'intermédiaire': 'Intermédiaire',
            'avancé': 'Avancé',
            'cp1': 'CP1', 'cp2': 'CP2', 'ce1': 'CE1', 'ce2': 'CE2', 'cm1': 'CM1', 'cm2': 'CM2'
        }
        return mapping.get(val.lower(), str(val).capitalize())
