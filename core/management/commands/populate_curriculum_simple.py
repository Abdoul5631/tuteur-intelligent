"""
Management command (SIMPLE) pour peupler le curriculum complet
"""

from django.core.management.base import BaseCommand
from core.models import Matiere, Lecon, Exercice


class Command(BaseCommand):
    help = 'Peupler le curriculum complet avec données réalistes'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Début du peuplement du curriculum...\n")
        
        # Mapping simple: (niveau_code, matiere_code, nom_affichage)
        curriculum = [
            # CM1
            ("cm1", "mathematiques", "Mathématiques CM1", [
                ("Les fractions simples", "Une fraction représente une partie d'un tout.", "1/2 = moitié, 1/4 quart", "Numérateur, dénominateur"),
                ("Multiplication et division", "Multiplicer = addition répétée", "3 × 4 = 12", "Tables multiplication"),
            ]),
            ("cm1", "francais", "Français CM1", [
                ("Les verbes", "Un verbe exprime une action", "courir, sauter, manger", "Présent, passé, futur"),
                ("L'accord des adjectifs", "L'adjectif s'accorde avec le nom", "un chat noir, une maison blanche", "Genre et nombre"),
            ]),
            
            # 6ème
            ("6eme", "mathematiques", "Mathématiques 6ème", [
                ("Nombres décimaux", "Les décimaux ont une virgule", "3,14", "Comparaison, opérations"),
                ("Équations simples", "Résouver 2x + 5 = 13", "Isoler x", "Vérification"),
            ]),
            ("6eme", "francais", "Français 6ème", [
                ("La phrase complexe", "Principale + subordinée", "Qui, que, parce que", "Ponctuation"),
                ("Homophones", "Mots qui sonnent pareil", "a/à, c'est/ces", "Stratégies"),
            ]),
            
            # 3ème  
            ("3eme", "mathematices", "Mathématiques 3ème", [
                ("Théorème de Pythagore", "a² + b² = c²", "3² + 4² = 25", "Réciproque"),
                ("Probabilités", "Chance qu'un événement arrive", "Dé: 1/6", "Événements"),
            ]),
            ("3eme", "francais", "Français 3ème", [
                ("Analyse littéraire", "Qui? Quand? Pourquoi?", "Auteur, contexte", "Figures style"),
            ]),
            
            # 2nde
            ("seconde", "mathematices", "Mathématiques 2nde", [
                ("Fonctions", "f(x) = ax + b", "Graphique = droite", "Pente, ordonnée"),
                ("Statistiques", "Moyenne, médiane", "Somme / nombre", "Variance"),
            ]),
            ("seconde", "francais", "Français 2nde", [
                ("Approches littéraires", "Étudier un texte", "Analyse", "Interprétation"),
            ]),
        ]
        
        matieres_created = 0
        lecons_created = 0
        
        for niveau_code, matiere_code, matiere_display, lecons_data in curriculum:
            # Créer la matière
            matiere, created = Matiere.objects.get_or_create(
                nom=matiere_code,
                niveau_scolaire=niveau_code,
                defaults={"description": f"{matiere_display}"}
            )
            
            if created:
                matieres_created += 1
                self.stdout.write(f"  ✓ {matiere_display}")
            
            # Créer les leçons
            for titre, contenu_principal, contenu_simplifie, contenu_approfondi in lecons_data:
                lecon, created = Lecon.objects.get_or_create(
                    titre=titre,
                    matiere=matiere,
                    defaults={
                        "contenu_principal": contenu_principal,
                        "contenu_simplifie": contenu_simplifie,
                        "contenu_approfondi": contenu_approfondi,
                    }
                )
                
                if created:
                    lecons_created += 1
                    self.stdout.write(f"    └─ {titre}")
                    
                    # Créer des exercices pour cette leçon
                    for i in range(3):
                        exercice, _ = Exercice.objects.get_or_create(
                            lecon=lecon,
                            question=f"Exercice {i+1}: {titre}?",
                            defaults={
                                "reponse": f"Réponse {i+1}",
                                "type": "choix_multiple",
                            }
                        )

        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS(f"""
✅ CURRICULUM PEUPLÉ!

📊 Créé:
   • Matières: {matieres_created}
   • Leçons: {lecons_created}
   • Exercices: {lecons_created * 3}

🎓 Niveaux: CM1, 6ème, 3ème, 2nde
💡 Prêt pour test!
        """))
        self.stdout.write("="*60)
