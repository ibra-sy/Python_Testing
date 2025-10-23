"""Configuration globale pour les tests du système GUDLFT."""

import pytest
import json
import tempfile
import os
from pathlib import Path


@pytest.fixture(scope="session")
def test_data_dir():
    """Fixture pour créer un répertoire temporaire pour les données de test."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def sample_clubs():
    """Fixture pour fournir des données de clubs de test."""
    return [
        {
            "name": "Test Club 1",
            "email": "test1@test.com",
            "points": 20
        },
        {
            "name": "Test Club 2", 
            "email": "test2@test.com",
            "points": 15
        }
    ]


@pytest.fixture
def sample_competitions():
    """Fixture pour fournir des données de compétitions de test."""
    return [
        {
            "name": "Test Competition 1",
            "date": "2024-01-01 10:00:00",
            "numberOfPlaces": 25,
            "bookings": {}
        },
        {
            "name": "Test Competition 2",
            "date": "2024-02-01 14:00:00", 
            "numberOfPlaces": 15,
            "bookings": {}
        }
    ]


@pytest.fixture
def mock_json_files(test_data_dir, sample_clubs, sample_competitions):
    """Fixture pour créer des fichiers JSON de test."""
    clubs_file = os.path.join(test_data_dir, "clubs.json")
    competitions_file = os.path.join(test_data_dir, "competitions.json")
    
    with open(clubs_file, 'w') as f:
        json.dump({"clubs": sample_clubs}, f)
    
    with open(competitions_file, 'w') as f:
        json.dump({"competitions": sample_competitions}, f)
    
    return {
        "clubs_file": clubs_file,
        "competitions_file": competitions_file
    }
