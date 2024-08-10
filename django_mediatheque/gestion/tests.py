from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from gestion.models import Emprunteur, Livre, DVD, CD, Emprunt


class BibliothecaireTests(TestCase):

    def setUp(self):
        # Créer un utilisateur bibliothécaire et se connecter
        self.bibliothecaire = User.objects.create_user(username='biblio', password='password123')
        bibliothecaire_group = Group.objects.create(name='Bibliothécaires')
        self.bibliothecaire.groups.add(bibliothecaire_group)
        self.client.login(username='biblio', password='password123')

        # Créer un emprunteur
        self.emprunteur = Emprunteur.objects.create(name='Test Emprunteur')

        # Créer des médias
        self.livre = Livre.objects.create(name="Livre Test", auteur="Auteur Test")
        self.dvd = DVD.objects.create(name="DVD Test", realisateur="Realisateur Test")
        self.cd = CD.objects.create(name="CD Test", artiste="Artiste Test")

    def test_bibliothecaire_home_view(self):
        """Test que la vue d'accueil du bibliothécaire se charge correctement"""
        response = self.client.get(reverse('gestion:bibliothecaire_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bienvenue Bibliothécaire")

    def test_gestion_emprunteurs_view(self):
        """Test que la vue de gestion des emprunteurs se charge correctement"""
        response = self.client.get(reverse('gestion:liste_membres'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Liste des Membres")

    def test_create_emprunt_view(self):
        """Test que la vue de création d'emprunt fonctionne correctement"""
        response = self.client.post(reverse('gestion:create_emprunt'), {
            'emprunteur': self.emprunteur.id,
            'livre': self.livre.id,
        })
        self.assertEqual(response.status_code, 302)  # Redirection après création
        emprunt = Emprunt.objects.get(emprunteur=self.emprunteur, livre=self.livre)
        self.assertIsNotNone(emprunt)

    def test_list_emprunteurs_view(self):
        """Test que la vue de liste des emprunteurs se charge correctement"""
        Emprunt.objects.create(emprunteur=self.emprunteur, livre=self.livre)
        response = self.client.get(reverse('gestion:liste_membres'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.emprunteur.name)

    def test_add_media_view(self):
        """Test que la vue d'ajout de média fonctionne correctement"""
        response = self.client.post(reverse('gestion:add_media'), {
            'media_type': 'livre',
            'name': 'Test Livre',
            'auteur': 'Auteur Test',
            'disponible': True
        })
        self.assertEqual(response.status_code, 302)  # Redirection après création
        livre = Livre.objects.get(name='Test Livre')
        self.assertIsNotNone(livre)

    def test_list_medias_view(self):
        """Test que la vue de liste des médias se charge correctement"""
        response = self.client.get(reverse('gestion:list_medias'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.livre.name)

    def test_emprunt_marked_in_media_list(self):
        # Create an emprunt to mark a book as borrowed
        self.livre.disponible = False
        self.livre.save()

        response = self.client.get(reverse('gestion:list_medias'))

        # Check if the media list reflects the borrowed status
        self.assertContains(response, f"{self.livre.name} - {self.livre.auteur} (Emprunté)")
