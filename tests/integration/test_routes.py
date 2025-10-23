"""
Tests d'intégration pour les routes Flask du système GUDLFT.


Types de tests inclus :
- Tests des routes GET et POST
- Validation des paramètres d'entrée
- Gestion des erreurs et cas limites
- Vérification des codes de statut HTTP
- Tests de redirection
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


class TestIndexRoute:
    """
    Tests pour la route d'accueil.
    
    """
    
    def test_index_get(self, client):
        """
        Test de l'accès à la page d'accueil.
        
        """
        # Teste l'accès à la route racine
        response = client.get('/')
        assert response.status_code == 200
        # Vérifie que le message de bienvenue s'affiche
        assert b'Welcome to the GUDLFT Registration Portal!' in response.data


class TestShowSummaryRoute:
    """
    Tests pour la route de connexion.
    
    """
    
    def test_show_summary_valid_email(self, client):
        """
        Test de connexion avec un email valide.
        
        """
        # Teste la connexion avec un email valide
        response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
        assert response.status_code == 200
        # Vérifie que le message de bienvenue personnalisé s'affiche
        assert b'Welcome, Simply Lift!' in response.data
    
    def test_show_summary_invalid_email(self, client):
        """
        Test de connexion avec un email invalide.
        
        """
        # Teste la connexion avec un email inexistant
        response = client.post('/showSummary', data={'email': 'invalid@email.com'})
        # L'application doit rediriger vers la page d'accueil
        assert response.status_code == 302
    
    def test_show_summary_empty_email(self, client):
        """
        Test de connexion avec un email vide.
        
        """
        # Teste la connexion avec un email vide
        response = client.post('/showSummary', data={'email': ''})
        # L'application doit rediriger vers la page d'accueil
        assert response.status_code == 302
    
    def test_show_summary_no_email(self, client):
        """
        Test de connexion sans email.
        
        """
        # Teste la connexion sans fournir d'email
        response = client.post('/showSummary')
        # L'application doit rediriger vers la page d'accueil
        assert response.status_code == 302


class TestBookRoute:
    """
    Tests pour la route de réservation.
    
    """
    
    def test_book_valid_competition_and_club(self, client):
        """
        Test de réservation avec une compétition et un club valides.
        
        """
        # Teste l'accès à la page de réservation avec des paramètres valides
        response = client.get('/book/Spring Festival/Simply Lift')
        assert response.status_code == 200
        # Vérifie que la page de réservation s'affiche correctement
        assert b'Book Places' in response.data
    
    def test_book_invalid_competition(self, client):
        """
        Test de réservation avec une compétition invalide.
        
        """
        # Teste l'accès avec un nom de compétition inexistant
        response = client.get('/book/Invalid Competition/Simply Lift')
        # L'application doit rediriger vers la page d'accueil
        assert response.status_code == 302
    
    def test_book_invalid_club(self, client):
        """
        Test de réservation avec un club invalide.
        
        """
        # Teste l'accès avec un nom de club inexistant
        response = client.get('/book/Spring Festival/Invalid Club')
        # L'application doit rediriger vers la page d'accueil
        assert response.status_code == 302


class TestPurchasePlacesRoute:
    """
    Tests pour la route d'achat de places.
    
    """
    
    def test_purchase_places_valid_booking(self, client):
        """
        Test d'achat de places valide.
        
        """
        # Teste une réservation avec des données valides
        response = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Spring Festival',
            'places': '2'
        })
        assert response.status_code == 200
        # Vérifie que la réservation a été confirmée
        assert b'Great! Booking complete.' in response.data
    
    def test_purchase_places_insufficient_points(self, client):
        """
        Test d'achat avec points insuffisants.
        
        """
        # Teste une réservation avec un club ayant peu de points
        response = client.post('/purchasePlaces', data={
            'club': 'Iron Temple',  # Club avec seulement 4 points
            'competition': 'Spring Festival',
            'places': '10'  # Plus que les points disponibles (4)
        })
        assert response.status_code == 200
        # Vérifie que l'application affiche le message d'erreur approprié
        assert b'Not enough points' in response.data
    
    def test_purchase_places_insufficient_places(self, client):
        """
        Test d'achat avec places insuffisantes dans la compétition.
        
        """
        # Teste une réservation avec plus de places que disponibles
        response = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Fall Classic',  # Compétition avec seulement 9 places
            'places': '15'  # Plus que les places disponibles (9)
        })
        assert response.status_code == 200
        # Vérifie que l'application affiche le message d'erreur approprié
        assert b'You cannot book more than 12 places' in response.data
    
    def test_purchase_places_zero_places(self, client):
        """
        Test d'achat avec zéro place.

        """
        # Teste une réservation avec zéro place
        response = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Spring Festival',
            'places': '0'
        })
        assert response.status_code == 200
        # Vérifie que l'application affiche le message d'erreur approprié
        assert b'You must book at least 1 place' in response.data
    
    def test_purchase_places_negative_places(self, client):
        """
        Test d'achat avec un nombre négatif de places.
        
        """
        # Teste une réservation avec un nombre négatif de places
        response = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Spring Festival',
            'places': '-1'
        })
        assert response.status_code == 200
        # Vérifie que l'application affiche le message d'erreur approprié
        assert b'You must book at least 1 place' in response.data
    
    def test_purchase_places_invalid_number(self, client):
        """
        Test d'achat avec un nombre invalide.
        
        """
        # Teste une réservation avec un nombre invalide (texte au lieu de nombre)
        response = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Spring Festival',
            'places': 'abc'  # Nombre invalide
        })
        assert response.status_code == 200
        # Vérifie que l'application affiche le message d'erreur approprié
        assert b'Invalid number of places provided' in response.data


class TestPointsRoute:
    """
    Tests pour la route des points.
    
    """
    
    def test_points_dashboard(self, client):
        """
        Test de l'affichage du tableau de bord des points.
        
        """
        # Teste l'accès à la page des points
        response = client.get('/points')
        assert response.status_code == 200
        # Vérifie que le titre de la page s'affiche
        assert b'Clubs Points & Bookings' in response.data


class TestLogoutRoute:
    """
    Tests pour la route de déconnexion.
    
    """
    
    def test_logout(self, client):
        """
        Test de déconnexion.
        
        """
        # Teste la déconnexion
        response = client.get('/logout')
        # Vérifie que la déconnexion redirige vers la page d'accueil
        assert response.status_code == 302  # Redirection
        assert response.location.endswith('/')


class TestBookingAliasRoute:
    """
    Tests pour la route d'alias de réservation.
    
    """
    
    def test_booking_alias(self, client):
        """
        Test de la route d'alias de réservation.
        
        """
        # Teste l'accès à la route d'alias
        response = client.get('/booking')
        # Vérifie que la route redirige vers la page d'accueil
        assert response.status_code == 302  # Redirection
        assert response.location.endswith('/')