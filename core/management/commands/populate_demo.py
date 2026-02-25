"""
Management command: Peupler curriculum simple
"""

from django.core.management.base import BaseCommand
from core.models import Matiere, Lecon, Exercice


class Command(BaseCommand):
    help = 'Peupler le curriculum avec donnees demo'

    def handle(self, *args, **options):
        self.stdout.write("Debut du peuplement du curriculum...\n")
        
        # Matiere et lecons simples
        data = [
            ("mathematiques", "Mathematiques", [
                ("Fractions", "Une fraction = partie d'un tout", "1/2 = moitie", "Numerateur/denominateur"),
                ("Multiplication", "Mult = addition repetee", "3 x 4 = 12", "Tables"),
                ("Equations", "Trouver x", "2x + 5 = 13 -> x = 4", "Isoler la variable"),
            ]),
            ("francais", "Francais", [
                ("Verbes", "Mot d'action", "courir, sauter", "Conjugaison"),
                ("Adjectifs", "Decrit le nom", "grand, bleu", "Accord genre/nombre"),
                ("Litterature", "Etude de textes", "Auteur, contexte", "Analyse"),
            ]),
            ("sciences", "Sciences", [
                ("Cycle de l'eau", "Evaporation -> Condensation", "Pluie", "Etats matiere"),
                ("Cellule", "Unite vivante", "Noyau, cytoplasme", "Biologie"),
            ]),
        ]
        
        total_lecons = 0
        total_exercices = 0
        
        for matiere_code, matiere_display, lecons in data:
            # Obtenir ou creer la matiere
            matiere, created = Matiere.objects.get_or_create(
                nom=matiere_code,
                defaults={'description': matiere_display}
            )
            
            self.stdout.write(f"  . Matiere: {matiere_display}")
            
            # Creer les lecons
            for titre, principal, simple, approfondi in lecons:
                lecon, created = Lecon.objects.get_or_create(
                    titre=titre,
                    matiere=matiere,
                    defaults={
                        "contenu_principal": principal,
                        "contenu_simplifie": simple,
                        "contenu_approfondi": approfondi,
                    }
                )
                
                if created:
                    total_lecons += 1
                    self.stdout.write(f"    |- {titre}")
                
                # Creer exercices par lecon
                for i in range(1, 3):
                    ex, _ = Exercice.objects.get_or_create(
                        lecon=lecon,
                        question=f"Question {i} sur {titre.lower()}",
                        defaults={
                            "reponse_correcte": f"Reponse correcte a {titre.lower()} numero {i}",
                            "type_exercice": "choix_multiple",
                            "matiere": matiere,
                        }
                    )
                    total_exercices += 1

        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(self.style.SUCCESS(f"""
CURRICULUM POPULATE AVEC SUCCES!

Contenu cree:
   - Matieres: {len(data)}
   - Lecons: {total_lecons}
   - Exercices: {total_exercices}

Matieres incluses:
   - Mathematiques
   - Francais  
   - Sciences

Pret a tester la platform!
        """))
        self.stdout.write("="*60)
