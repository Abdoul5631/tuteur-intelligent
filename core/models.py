from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import json


# ========================
# NIVEAU SCOLAIRE (CP1 → Terminale)
# ========================

class NiveauScolaire(models.Model):
    """Niveaux du programme francophone : CP1 à Terminale"""
    CYCLE_CHOICES = [
        ('primaire', 'Primaire'),
        ('college', 'Collège'),
        ('lycee', 'Lycée'),
    ]
    code = models.CharField(max_length=20, unique=True)  # cp1, ce1, 6eme, seconde...
    libelle = models.CharField(max_length=50)  # CP1, CE1, 6ème, Seconde...
    ordre = models.IntegerField(default=0)  # 1=CP1, 2=CP2, ... 13=Terminale
    cycle = models.CharField(max_length=20, choices=CYCLE_CHOICES)

    class Meta:
        ordering = ['ordre']
        verbose_name_plural = "Niveaux scolaires"

    def __str__(self):
        return self.libelle


# ========================
# MATIÈRE
# ========================

class Matiere(models.Model):
    """Matières disponibles dans l'application"""
    
    MATIERE_CHOICES = [
        ('mathematiques', 'Mathématiques'),
        ('francais', 'Français'),
        ('lecture', 'Lecture'),
        ('ecriture', 'Écriture'),
        ('education_civique', 'Éducation civique'),
        ('histoire_geo', 'Histoire-Géographie'),
        ('sciences', 'Sciences'),
        ('anglais', 'Anglais'),
        ('sciences_vie', 'Sciences de la Vie et de la Terre'),
        ('physique', 'Physique'),
        ('chimie', 'Chimie'),
        ('physique_chimie', 'Physique-Chimie'),
        ('technologie', 'Technologie'),
        ('eps', 'EPS'),
        ('arts', 'Arts Plastiques'),
        ('musique', 'Musique'),
        ('ses', 'Sciences Économiques et Sociales'),
        ('philosophie', 'Philosophie'),
        ('espagnol', 'Espagnol'),
        ('allemand', 'Allemand'),
    ]
    
    nom = models.CharField(max_length=100, choices=MATIERE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    couleur_hex = models.CharField(max_length=7, default="#3B82F6")
    icone = models.CharField(max_length=50, default="📚")
    
    class Meta:
        verbose_name_plural = "Matières"
    
    def __str__(self):
        return self.get_nom_display()


# ========================
# UTILISATEUR (AMÉLIORÉ)
# ========================

class Utilisateur(models.Model):
    """Profil d'élève avec support complet de l'IA"""
    
    NIVEAU_SCOLAIRE_CHOICES = [
        ('cp1', 'CP1'),
        ('cp2', 'CP2'),
        ('ce1', 'CE1'),
        ('ce2', 'CE2'),
        ('cm1', 'CM1'),
        ('cm2', 'CM2'),
        ('6eme', '6ème'),
        ('5eme', '5ème'),
        ('4eme', '4ème'),
        ('3eme', '3ème'),
        ('seconde', 'Seconde'),
        ('1ere', '1ère'),
        ('terminale', 'Terminale'),
    ]
    
    NIVEAU_GLOBAL_CHOICES = [
        ('débutant', 'Débutant'),
        ('intermédiaire', 'Intermédiaire'),
        ('avancé', 'Avancé'),
    ]
    
    STYLE_APPRENTISSAGE_CHOICES = [
        ('visuel', 'Visuel'),
        ('auditif', 'Auditif'),
        ('kinesthesique', 'Kinesthésique'),
        ('lecture_ecriture', 'Lecture-Écriture'),
    ]
    
    # Relations
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Infos personnelles
    nom = models.CharField(max_length=100, blank=True)
    prenom = models.CharField(max_length=100, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    
    # Niveaux
    niveau_scolaire = models.CharField(
        max_length=50, 
        choices=NIVEAU_SCOLAIRE_CHOICES, 
        default='cp1'
    )
    niveau_global = models.CharField(
        max_length=50,
        choices=NIVEAU_GLOBAL_CHOICES,
        default='débutant'
    )
    
    # Matières
    matiere_principale = models.ForeignKey(
        Matiere,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='utilisateurs_principaux'
    )
    matieres_disponibles = models.ManyToManyField(
        Matiere,
        blank=True,
        related_name='utilisateurs'
    )
    
    # Apprentissage
    style_apprentissage = models.CharField(
        max_length=50,
        choices=STYLE_APPRENTISSAGE_CHOICES,
        null=True,
        blank=True
    )
    
    # Domaines
    domaines_forts = models.JSONField(default=list, blank=True)  # ["fractions", "conjugaison"]
    domaines_faibles = models.JSONField(default=list, blank=True)  # ["proportions"]
    
    # Parent
    parent_email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=15, blank=True)
    
    # Statistiques
    total_exercices_completes = models.IntegerField(default=0)
    score_moyen = models.FloatField(default=0.0)
    temps_total_apprentissage = models.IntegerField(default=0)  # en minutes
    derniere_activite = models.DateTimeField(null=True, blank=True)
    
    # Dates
    date_inscription = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}" if self.prenom or self.nom else self.user.username
    
    @property
    def age(self):
        """Calculer l'âge de l'élève"""
        from datetime import date
        if self.date_naissance:
            today = date.today()
            return today.year - self.date_naissance.year
        return None


# ========================
# LEÇON (AMÉLIORÉE)
# ========================

class Lecon(models.Model):
    """Leçon avec contenu adaptatif - compatible IA explication, exercices, suivi"""
    
    matiere = models.ForeignKey(
        Matiere,
        on_delete=models.CASCADE,
        related_name='lecons'
    )
    niveau = models.ForeignKey(
        NiveauScolaire,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lecons'
    )
    
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Niveaux (legacy, pour rétrocompat)
    niveau_scolaire = models.CharField(max_length=50, blank=True)
    niveau_global = models.CharField(max_length=50, blank=True)
    
    # Contenu
    contenu_principal = models.TextField(blank=True)
    contenu_simplifie = models.TextField(blank=True)  # Pour niveaux bas
    contenu_approfondi = models.TextField(blank=True)  # Pour niveaux avancés
    
    # Médias
    image = models.URLField(blank=True)
    video_url = models.URLField(blank=True)
    
    # Métadonnées
    concepts_cles = models.JSONField(default=list, blank=True)  # ["fraction", "numerateur"]
    prerequis = models.ManyToManyField('self', symmetrical=False, blank=True)
    ordre = models.IntegerField(default=0)
    difficulte = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    temps_estime = models.IntegerField(default=20)  # en minutes
    
    # Dates
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['ordre', 'titre']
        verbose_name_plural = "Leçons"

    def __str__(self):
        return self.titre
    
    def get_contenu_pour_niveau(self, niveau):
        """Retourner le contenu adapté au niveau"""
        if niveau == 'débutant' and self.contenu_simplifie:
            return self.contenu_simplifie
        elif niveau == 'avancé' and self.contenu_approfondi:
            return self.contenu_approfondi
        return self.contenu_principal


# ========================
# EXERCICE (AMÉLIORÉ)
# ========================

class Exercice(models.Model):
    """Exercices avec types variés et feedback riche"""
    
    TYPE_EXERCICE_CHOICES = [
        ('choix_multiple', 'Choix Multiple'),
        ('reponse_courte', 'Réponse Courte'),
        ('redaction', 'Rédaction'),
        ('calcul', 'Calcul'),
        ('vrai_faux', 'Vrai/Faux'),
        ('matching', 'Appariement'),
    ]
    
    # Relations
    lecon = models.ForeignKey(
        Lecon,
        on_delete=models.CASCADE,
        related_name='exercices'
    )
    matiere = models.ForeignKey(
        Matiere,
        on_delete=models.CASCADE,
        related_name='exercices'
    )
    
    # Contenu
    question = models.TextField()
    type_exercice = models.CharField(
        max_length=50,
        choices=TYPE_EXERCICE_CHOICES,
        default='choix_multiple'
    )
    
    # Réponses
    reponse_correcte = models.TextField()
    options = models.JSONField(
        default=list,
        blank=True,
        help_text="Pour choix multiple"
    )
    erreurs_courantes = models.JSONField(
        default=list,
        blank=True
    )
    
    # Explications
    explication_bonne_reponse = models.TextField(blank=True)
    explication_detaillee = models.TextField(blank=True)
    solution_etape_par_etape = models.JSONField(default=dict, blank=True)
    
    # Niveaux
    niveau = models.CharField(max_length=50)
    difficulte = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    points_valeur = models.IntegerField(default=10)
    
    # Temps
    temps_estime = models.IntegerField(default=300)  # en secondes
    
    # Métadonnées
    concepts_evalues = models.JSONField(default=list, blank=True)
    ordre = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)
    
    # Dates
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['ordre', 'id']

    def __str__(self):
        return self.question[:50]


# ========================
# RÉSULTAT (AMÉLIORÉ)
# ========================

class Resultat(models.Model):
    """Résultats enrichis avec analyses IA"""
    
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='resultats'
    )
    exercice = models.ForeignKey(
        Exercice,
        on_delete=models.CASCADE,
        related_name='resultats'
    )
    
    # Réponse
    reponse_donnee = models.TextField()
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Tentatives
    numero_tentative = models.IntegerField(default=1)
    temps_resolution = models.IntegerField(null=True, blank=True)  # en secondes
    
    # Feedback IA
    feedback_ia = models.TextField(blank=True)
    feedback_detaille = models.TextField(blank=True)
    encouragement = models.TextField(blank=True)
    
    # Analyse
    analyse_erreur = models.JSONField(default=dict, blank=True)
    suggestion_amelioration = models.TextField(blank=True)
    
    # Dates
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Résultats"

    def __str__(self):
        return f"{self.utilisateur} - {self.exercice} ({self.score}%)"


# ========================
# PROGRESSION ÉLÈVE (base pour IA personnalisée)
# ========================

class ProgressionNotion(models.Model):
    """Suivi par notion/concept : maîtrisé ou faible"""
    MAITRISE_CHOICES = [
        ('faible', 'À revoir'),
        ('encours', 'En cours'),
        ('maitrise', 'Maîtrisé'),
    ]
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='progression_notions'
    )
    notion = models.CharField(max_length=100)  # ex: "fractions", "conjugaison passé"
    matiere = models.ForeignKey(
        Matiere,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='progression_notions'
    )
    statut = models.CharField(
        max_length=20,
        choices=MAITRISE_CHOICES,
        default='encours'
    )
    score_moyen = models.FloatField(default=0.0)
    nb_tentatives = models.IntegerField(default=0)
    derniere_tentative = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = [['utilisateur', 'notion']]
        verbose_name_plural = "Progression par notion"

    def __str__(self):
        return f"{self.utilisateur} - {self.notion} ({self.statut})"


# ========================
# CONVERSATION IA
# ========================

class ConversationIA(models.Model):
    """Conversation avec le tuteur IA"""
    
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='conversations_ia'
    )
    
    matiere = models.ForeignKey(
        Matiere,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    lecon = models.ForeignKey(
        Lecon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Métadonnées
    titre = models.CharField(max_length=200, blank=True)
    contexte = models.JSONField(default=dict, blank=True)
    
    # Dates
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    
    # Résumé IA
    resume = models.TextField(blank=True)
    points_cles_identifies = models.JSONField(default=list, blank=True)
    
    # Statistiques
    nombre_messages = models.IntegerField(default=0)
    tokens_utilises = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date_debut']

    def __str__(self):
        return f"{self.utilisateur} - {self.date_debut}"


# ========================
# MESSAGE IA
# ========================

class ConversationMessage(models.Model):
    """Messages individuels dans une conversation IA"""
    
    ROLE_CHOICES = [
        ('user', 'Utilisateur'),
        ('assistant', 'Assistant IA'),
    ]
    
    TYPE_MESSAGE_CHOICES = [
        ('question', 'Question'),
        ('explication', 'Explication'),
        ('exercice', 'Exercice'),
        ('feedback', 'Feedback'),
        ('encouragement', 'Encouragement'),
        ('autre', 'Autre'),
    ]
    
    conversation = models.ForeignKey(
        ConversationIA,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    type_message = models.CharField(
        max_length=50,
        choices=TYPE_MESSAGE_CHOICES,
        default='autre'
    )
    
    contenu = models.TextField()
    
    # Métadonnées
    tokens = models.IntegerField(default=0)
    
    # Dates
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.role} - {self.timestamp}"
