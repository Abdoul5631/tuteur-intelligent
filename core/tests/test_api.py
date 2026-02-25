"""
Tests minimaux API : leçons, auth, gestion des erreurs.
Lancer : python manage.py test core.tests.test_api
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from core.models import Utilisateur, Lecon, Matiere, Exercice, NiveauScolaire


class ApiRootTest(TestCase):
    """Vérifie que l'API répond et expose les bons endpoints."""

    def setUp(self):
        self.client = APIClient()

    def test_api_root_returns_200(self):
        r = self.client.get('/api/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        self.assertIn('endpoints', data)
        endpoints = data['endpoints']
        self.assertIn('login', endpoints)
        self.assertIn('lessons', endpoints)


class LeconsAccessTest(TestCase):
    """Vérifie que les leçons se chargent (filtrées par niveau élève, auth requise)."""

    def setUp(self):
        self.client = APIClient()
        self.matiere = Matiere.objects.create(nom='mathematiques', description='Maths')
        ns = NiveauScolaire.objects.filter(code='ce1').first()
        if not ns:
            ns = NiveauScolaire.objects.create(
                code='ce1', libelle='CE1', ordre=2, cycle='primaire'
            )
        self.lecon = Lecon.objects.create(
            titre='Test Leçon',
            matiere=self.matiere,
            niveau_global='débutant',
            niveau=ns,
        )

    def test_lecons_list_without_auth_returns_401(self):
        """Sans token : GET /api/lecons/ retourne 401."""
        r = self.client.get('/api/lecons/')
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lecons_list_with_auth_returns_filtered_by_niveau(self):
        """Avec token + profil élève : leçons filtrées par niveau_scolaire."""
        user = User.objects.create_user('testuser', 'test@test.com', 'pass123')
        Utilisateur.objects.create(
            user=user,
            nom='Test',
            prenom='User',
            niveau_scolaire='ce1',
            niveau_global='débutant',
        )
        self.client.force_authenticate(user=user)
        r = self.client.get('/api/lecons/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        self.assertIsInstance(data, list)
        for item in data:
            self.assertEqual(item.get('niveau_global'), 'débutant')

    def test_lecons_list_with_auth_no_profile_returns_404(self):
        """Utilisateur authentifié sans profil : 404 (get_object_or_404 Utilisateur)."""
        user = User.objects.create_user('noprofile', 'nop@test.com', 'pass123')
        self.client.force_authenticate(user=user)
        r = self.client.get('/api/lecons/')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)


class ExercicesByLeconTest(TestCase):
    """Vérifie l'accès aux exercices d'une leçon."""

    def setUp(self):
        self.client = APIClient()
        self.matiere = Matiere.objects.create(nom='mathematiques', description='Maths')
        ns = NiveauScolaire.objects.filter(code='ce1').first()
        if not ns:
            ns = NiveauScolaire.objects.create(
                code='ce1', libelle='CE1', ordre=2, cycle='primaire'
            )
        self.lecon = Lecon.objects.create(
            titre='Leçon avec exercices',
            matiere=self.matiere,
            niveau_global='débutant',
            niveau=ns,
        )
        Exercice.objects.create(
            lecon=self.lecon,
            matiere=self.matiere,
            question='2 + 2 ?',
            reponse_correcte='4',
        )

    def test_exercices_by_lecon_requires_auth(self):
        """GET /api/lecons/<id>/exercices/ requiert authentification."""
        r = self.client.get(f'/api/lecons/{self.lecon.id}/exercices/')
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_exercices_by_lecon_with_auth_returns_200(self):
        """GET /api/lecons/<id>/exercices/ avec auth et leçon du niveau élève."""
        user = User.objects.create_user('elev', 'e@t.com', 'pass123')
        Utilisateur.objects.create(user=user, nom='E', prenom='L', niveau_scolaire='ce1', niveau_global='débutant')
        self.client.force_authenticate(user=user)
        r = self.client.get(f'/api/lecons/{self.lecon.id}/exercices/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertIn('question', data[0])


class AuthTest(TestCase):
    """Login, register, et gestion des erreurs API."""

    def setUp(self):
        self.client = APIClient()
        User.objects.create_user('alice', 'alice@test.com', '123456')

    def test_login_success_returns_tokens(self):
        """POST /api/auth/login/ avec bons identifiants retourne access + refresh."""
        r = self.client.post('/api/auth/login/', {
            'username': 'alice',
            'password': '123456',
        }, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        self.assertIn('access', data)
        self.assertIn('refresh', data)

    def test_login_bad_credentials_returns_401(self):
        """Mauvais identifiants : 401."""
        r = self.client.post('/api/auth/login/', {
            'username': 'alice',
            'password': 'wrong',
        }, format='json')
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_minimal_returns_201(self):
        """Inscription avec niveau scolaire (CP1→Terminale) obligatoire."""
        r = self.client.post('/api/auth/register/', {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'TestPass123!Abc',
            'password_confirm': 'TestPass123!Abc',
            'niveau_scolaire': 'ce1',
        }, format='json')
        self.assertEqual(
            r.status_code, status.HTTP_201_CREATED,
            msg=r.json() if r.content else r.content
        )
        data = r.json()
        self.assertEqual(data.get('username'), 'newuser')
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Utilisateur.objects.filter(user__username='newuser').exists())

    def test_register_validation_errors_return_400(self):
        """Inscription sans password_confirm ou mots de passe différents : 400."""
        r = self.client.post('/api/auth/register/', {
            'username': 'other',
            'email': 'other@test.com',
            'password': 'short',
            'password_confirm': 'short',
        }, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)


class ProtectedEndpointsTest(TestCase):
    """Endpoints protégés : 401 sans token."""

    def setUp(self):
        self.client = APIClient()

    def test_me_without_token_returns_401(self):
        r = self.client.get('/api/me/')
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_progression_without_token_returns_401(self):
        r = self.client.get('/api/progression/')
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
