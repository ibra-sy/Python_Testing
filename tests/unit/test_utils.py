"""
Tests unitaires pour les fonctions utilitaires du système GUDLFT.

Types de tests inclus :
- Tests des fonctions de chargement JSON
- Tests des fonctions de sauvegarde JSON
- Tests des fonctions de gestion des clubs
- Tests des fonctions de gestion des compétitions
- Tests avec mocks pour isoler les dépendances
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
import sys
import os

# Configuration du path pour permettre l'import du module server
# Nécessaire car les tests sont dans un sous-répertoire
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from server import load_json, save_json, load_clubs, load_competitions, save_clubs, save_competitions


class TestLoadJson:
    """
    Tests pour la fonction load_json.
    
    """
    
    def test_load_json_success(self):
        """
        Test du chargement réussi d'un fichier JSON.
        
        """
        # Données de test simulées
        test_data = {"clubs": [{"name": "Test Club", "email": "test@test.com"}]}
        mock_file_content = json.dumps(test_data)
        
        # Mock du système de fichiers pour simuler la lecture d'un fichier
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            with patch("pathlib.Path.__truediv__", return_value=Path("test.json")):
                # Teste le chargement des données
                result = load_json("test.json", "clubs")
                # Vérifie que les données sont correctement chargées
                assert result == [{"name": "Test Club", "email": "test@test.com"}]
    
    def test_load_json_file_not_found(self):
        """
        Test du comportement quand le fichier n'existe pas.
        
        """
        # Mock pour simuler un fichier inexistant
        with patch("builtins.open", side_effect=FileNotFoundError):
            # Vérifie que l'exception est levée correctement
            with pytest.raises(FileNotFoundError):
                load_json("nonexistent.json", "clubs")


class TestSaveJson:
    """
    Tests pour la fonction save_json.
    
    """
    
    def test_save_json_success(self):
        """
        Test de la sauvegarde réussie d'un fichier JSON.
        
        """
        # Données de test à sauvegarder
        test_data = [{"name": "Test Club", "email": "test@test.com"}]
        
        # Mock du système de fichiers pour simuler l'écriture d'un fichier
        with patch("builtins.open", mock_open()) as mock_file:
            with patch("pathlib.Path.__truediv__", return_value=Path("test.json")):
                # Teste la sauvegarde des données
                save_json("test.json", "clubs", test_data)
                
                # Vérifie que le fichier a été ouvert en mode écriture
                mock_file.assert_called_once()
                # Vérifie que le fichier a été ouvert avec les bons paramètres
                mock_file.assert_called_with(Path("test.json"), "w", encoding="utf-8")


class TestLoadClubs:
    """
    Tests pour la fonction load_clubs.
    
    """
    
    def test_load_clubs_success(self):
        """
        Test du chargement réussi des clubs.
        
        """
        # Données de test simulées pour les clubs
        test_clubs = [{"name": "Test Club", "email": "test@test.com", "points": 10}]
        mock_file_content = json.dumps({"clubs": test_clubs})
        
        # Mock du système de fichiers pour simuler la lecture du fichier clubs.json
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            with patch("pathlib.Path.__truediv__", return_value=Path("clubs.json")):
                # Teste le chargement des clubs
                result = load_clubs()
                # Vérifie que les données des clubs sont correctement chargées
                assert result == test_clubs


class TestLoadCompetitions:
    """
    Tests pour la fonction load_competitions.
    
    """
    
    def test_load_competitions_success(self):
        """
        Test du chargement réussi des compétitions.
        
        """
        # Données de test simulées pour les compétitions
        test_competitions = [{"name": "Test Competition", "date": "2024-01-01", "numberOfPlaces": 10}]
        mock_file_content = json.dumps({"competitions": test_competitions})
        
        # Mock du système de fichiers pour simuler la lecture du fichier competitions.json
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            with patch("pathlib.Path.__truediv__", return_value=Path("competitions.json")):
                # Teste le chargement des compétitions
                result = load_competitions()
                # Vérifie que les données des compétitions sont correctement chargées
                assert result == test_competitions


class TestSaveClubs:
    """
    Tests pour la fonction save_clubs.
    
    """
    
    def test_save_clubs_success(self):
        """
        Test de la sauvegarde réussie des clubs.
        
        """
        # Données de test à sauvegarder pour les clubs
        test_clubs = [{"name": "Test Club", "email": "test@test.com", "points": 10}]
        
        # Mock du système de fichiers pour simuler l'écriture du fichier clubs.json
        with patch("builtins.open", mock_open()) as mock_file:
            with patch("pathlib.Path.__truediv__", return_value=Path("clubs.json")):
                # Teste la sauvegarde des clubs
                save_clubs(test_clubs)
                # Vérifie que le fichier a été ouvert pour l'écriture
                mock_file.assert_called_once()


class TestSaveCompetitions:
    """
    Tests pour la fonction save_competitions.
    
    """
    
    def test_save_competitions_success(self):
        """
        Test de la sauvegarde réussie des compétitions.
        
        """
        # Données de test à sauvegarder pour les compétitions
        test_competitions = [{"name": "Test Competition", "date": "2024-01-01", "numberOfPlaces": 10}]
        
        # Mock du système de fichiers pour simuler l'écriture du fichier competitions.json
        with patch("builtins.open", mock_open()) as mock_file:
            with patch("pathlib.Path.__truediv__", return_value=Path("competitions.json")):
                # Teste la sauvegarde des compétitions
                save_competitions(test_competitions)
                # Vérifie que le fichier a été ouvert pour l'écriture
                mock_file.assert_called_once()