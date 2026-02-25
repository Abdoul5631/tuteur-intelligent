from django.contrib import admin
from .models import Utilisateur, Lecon, Exercice, Resultat

admin.site.register(Utilisateur)
admin.site.register(Lecon)
admin.site.register(Exercice)
admin.site.register(Resultat)


# Register your models here.
