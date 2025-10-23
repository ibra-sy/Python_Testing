"""
Tests fonctionnels pour les scénarios utilisateur du système GUDLFT.

Types de tests inclus :
- Parcours de réservation complet
- Gestion des erreurs et cas limites
- Cohérence des données
- Interface utilisateur et navigation
"""
import pytest
import json
from flask import Flask
import sys
import os
from server import app

# Configuration du path pour permettre l'import du module server
# Nécessaire car les tests sont dans un sous-répertoire
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


@pytest.fixture
def client():
    """
    Fixture pour créer un client de test Flask.
    Returns:
        Flask test client: Client de test pour effectuer des requêtes HTTP
    """
    # Configuration de l'application en mode test
    app.config['TESTING'] = True
    # Création du client de test avec gestion automatique du contexte
    with app.test_client() as client:
        yield client

class TestCompleteUserJourney:
    """
    Tests pour le parcours utilisateur complet.
    """
    def test_successful_booking_journey(self, client):
        """
        Test du parcours complet de réservation réussie.
        """
        # Étape 1: Accès à la page d'accueil
        # Vérifie que l'application répond correctement à la requête GET
        response = client.get('/')
        assert response.status_code == 200
        # Étape 2: Connexion avec un email valide
        # Teste l'authentification utilisateur avec un email existant
        response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
        assert response.status_code == 200
        # Vérifie que le message de bienvenue contient le nom du club
        assert b'Welcome, Simply Lift!' in response.data
        # Étape 3: Accès à la page de réservation
        # Teste la navigation vers la page de réservation pour une compétition spécifique
        response = client.get('/book/Spring Festival/Simply Lift')
        assert response.status_code == 200
        # Vérifie que la page de réservation s'affiche correctement
        assert b'Book Places' in response.data
        
        # Étape 4: Réservation de places
        # Teste le processus de réservation avec des données valides
        # Utilise un club avec suffisamment de points pour éviter les erreurs
        response = client.post('/purchasePlaces', data={
            'club': 'She Lifts',  # Club avec 12 points disponibles
            'competition': 'Summer Cup',
            'places': '2'
        })
        assert response.status_code == 200
        # Vérifie que la réservation a été confirmée
        assert b'Great! Booking complete.' in response.data
    def test_failed_login_journey(self, client):
        """
        Test du parcours avec échec de connexion.
        
        """
        # Étape 1: Accès à la page d'accueil
        # Vérifie que l'application est accessible
        response = client.get('/')
        assert response.status_code == 200
        
        # Étape 2: Tentative de connexion avec un email invalide
        # Teste la gestion des erreurs d'authentification
        response = client.post('/showSummary', data={'email': 'invalid@email.com'})
        # L'application doit rediriger vers la page d'accueil (code 302)
        assert response.status_code == 302
        
        # Étape 3: Suivre la redirection
        # Vérifie que l'utilisateur est bien redirigé vers la page d'accueil
        response = client.get('/')
        assert response.status_code == 200
        # Vérifie que le message d'accueil s'affiche (pas de message d'erreur visible)
        assert b'Welcome to the GUDLFT Registration Portal!' in response.data
    def test_booking_with_insufficient_points(self, client):
        """
        Test de réservation avec points insuffisants.
        """
        # Étape 1: Connexion avec un club ayant peu de points
        # Utilise Iron Temple qui n'a que 4 points disponibles
        response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
        assert response.status_code == 200
        
        # Étape 2: Tentative de réservation avec plus de points que disponibles
        # Teste la validation des points disponibles avant la réservation
        response = client.post('/purchasePlaces', data={
            'club': 'Iron Temple',
            'competition': 'Spring Festival',
            'places': '10'  # Iron Temple n'a que 4 points, donc 10 > 4
        })
        assert response.status_code == 200
        # Vérifie que l'application affiche le message d'erreur approprié
        assert b'Not enough points' in response.data
    def test_multiple_bookings_same_competition(self, client):
        """
        Test de plusieurs réservations pour la même compétition.
        
        """
        # Étape 1: Première réservation avec un club qui a suffisamment de points
        # Utilise She Lifts qui a 12 points disponibles
        response = client.post('/purchasePlaces', data={
            'club': 'She Lifts',  # Club avec 12 points
            'competition': 'Summer Cup',
            'places': '5'
        })
        assert response.status_code == 200
        assert b'Great! Booking complete.' in response.data
        
        # Étape 2: Deuxième réservation (devrait échouer car dépasse la limite de 12)
        # Teste la validation de la limite totale de 12 places par club par compétition
        response = client.post('/purchasePlaces', data={
            'club': 'She Lifts',
            'competition': 'Summer Cup',
            'places': '10'  # 5 + 10 = 15 > 12 (limite dépassée)
        })
        assert response.status_code == 200
        # Vérifie que l'application rejette la réservation qui dépasse la limite
        assert b'Booking exceeds limit' in response.data

class TestDataConsistency:
    """
    Tests pour la cohérence des données.
    
    """
    def test_points_deduction_after_booking(self, client):
        """
        Test de la déduction des points après réservation.
        
        """
        # Vérifier les points initiaux du club
        response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
        assert response.status_code == 200
        
        # Effectuer une réservation avec un club qui a suffisamment de points
        # Utilise She Lifts qui a 12 points disponibles
        response = client.post('/purchasePlaces', data={
            'club': 'She Lifts',  # Club avec 12 points
            'competition': 'Summer Cup',
            'places': '2'
        })
        assert response.status_code == 200
        # Vérifie que la réservation a été effectuée avec succès
        assert b'Great! Booking complete.' in response.data
    def test_competition_places_reduction(self, client):
        """
        Test de la réduction des places disponibles après réservation.
        
        """
        # Utiliser un club différent pour éviter les conflits avec les tests précédents
        # Iron Temple a 4 points, donc peut réserver 1 place
        response = client.post('/purchasePlaces', data={
            'club': 'Iron Temple',  # Club avec 4 points
            'competition': 'Winter Classic',
            'places': '1'
        })
        assert response.status_code == 200
        # Vérifie que la réservation a été effectuée avec succès
        assert b'Great! Booking complete.' in response.data

class TestErrorHandling:
    """
    Tests pour la gestion des erreurs.
    
    """
    def test_handling_missing_form_data(self, client):
        """
        Test de gestion des données de formulaire manquantes.
        
        """
        # Teste la réservation avec des données incomplètes (competition manquante)
        response = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            # 'competition' manquant - champ obligatoire
            'places': '2'
        })
        # L'application doit rediriger vers la page d'accueil en cas d'erreur
        assert response.status_code == 302
    def test_handling_invalid_competition_name(self, client):
        """
        Test de gestion d'un nom de compétition invalide.
        
        """
        # Teste la réservation avec un nom de compétition inexistant
        response = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Invalid Competition',  # Compétition inexistante
            'places': '2'
        })
        # L'application doit rediriger vers la page d'accueil
        assert response.status_code == 302 
    def test_handling_invalid_club_name(self, client):
        """
        Test de gestion d'un nom de club invalide.
        
        """
        # Teste la réservation avec un nom de club inexistant
        response = client.post('/purchasePlaces', data={
            'club': 'Invalid Club',  # Club inexistant
            'competition': 'Spring Festival',
            'places': '2'
        })
        # L'application doit rediriger vers la page d'accueil
        assert response.status_code == 302

class TestUserInterface:
    """
    Tests pour l'interface utilisateur.
    
    """
    def test_points_dashboard_accessibility(self, client):
        """
        Test de l'accessibilité du tableau de bord des points.
        
        """
        # Accès à la page des points
        response = client.get('/points')
        assert response.status_code == 200
        # Vérifie que le titre de la page s'affiche
        assert b'Clubs Points & Bookings' in response.data
        
        # Vérifier que tous les clubs sont affichés dans le tableau de bord
        assert b'Simply Lift' in response.data
        assert b'Iron Temple' in response.data
        assert b'She Lifts' in response.data
    def test_logout_functionality(self, client):
        """
        Test de la fonctionnalité de déconnexion.
        
        """
        # Étape 1: Se connecter d'abord
        response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
        assert response.status_code == 200
        
        # Étape 2: Se déconnecter
        response = client.get('/logout')
        # Vérifie que la déconnexion redirige vers la page d'accueil
        assert response.status_code == 302  # Redirection
        assert response.location.endswith('/')
    def test_navigation_flow(self, client):
        """
        Test du flux de navigation.
        """
        # Étape 1: Accès à la page d'accueil
        response = client.get('/')
        assert response.status_code == 200
        
        # Étape 2: Connexion utilisateur
        response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
        assert response.status_code == 200
        
        # Étape 3: Navigation vers la page de réservation
        response = client.get('/book/Spring Festival/Simply Lift')
        assert response.status_code == 200
        
        # Étape 4: Retour au tableau de bord des points
        response = client.get('/points')
        assert response.status_code == 200
