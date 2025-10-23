# Plan de Test - Système GUDLFT

## 1. Objectif
Tester la fonctionnalité complète du système de réservation GUDLFT (Great Udacity League Football Tournament) pour s'assurer que toutes les fonctionnalités critiques fonctionnent correctement.

## 2. Périmètre
- **Authentification des utilisateurs** : Connexion via email
- **Gestion des réservations** : Achat de places pour les compétitions
- **Gestion des points** : Déduction et affichage des points des clubs
- **Interface utilisateur** : Navigation et affichage des données

## 3. Critères de succès
-  L'utilisateur peut se connecter avec un email valide  OK
-  Un message d'erreur apparaît en cas d'email invalide  OK
-  Les réservations sont correctement traitées et validées  OK
-  Les points sont correctement déduits après réservation  OK
-  Les limites de réservation sont respectées (max 12 places par club)  OK
-  L'interface est accessible et fonctionnelle  OK

## 4. Structure des Tests

### 4.1 Tests Unitaires (60% des tests)
**Localisation** : `tests/unit/`
- **test_utils.py** : Tests des fonctions utilitaires (load_json, save_json, etc.)
- **test_business_logic.py** : Tests de la logique métier (validation, calculs)

### 4.2 Tests d'Intégration (20% des tests)
**Localisation** : `tests/integration/`
- **test_routes.py** : Tests des routes Flask et intégration avec les données

### 4.3 Tests Fonctionnels (20% des tests)
**Localisation** : `tests/functional/`
- **test_user_scenarios.py** : Tests des scénarios utilisateur complets

## 5. Matrice de Priorisation des Tests

| Fonctionnalité             | Probabilité d'échec | Impact   | Priorité       | Tests associés |
|----------------------------|---------------------|----------|----------------|----------------|
| **Connexion utilisateur**  | Élevée              | Critique | **Très Haute** | test_show_summary_valid_email<br>test_show_summary_invalid_email |
| **Réservation de places**  | Haute               | Critique | **Très Haute** | test_purchase_places_valid_booking<br>test_purchase_places_insufficient_points |
| **Validation des limites** | Haute               | Critique | **Très Haute** | test_validate_max_places_per_booking<br>test_purchase_places_exceed_max_per_booking |
| **Gestion des points**     | Moyenne             | Critique | **Haute**      | test_calculate_remaining_points<br>test_validate_club_points_sufficient |
| **Chargement des données** | Faible              | Moyen    | **Moyenne**    | test_load_clubs<br>test_load_competitions |
| **Sauvegarde des données** | Faible              | Moyen    | **Moyenne**    | test_save_clubs<br>test_save_competitions |
| **Interface utilisateur**  | Faible              | Mineur   | **Basse**      | test_points_dashboard<br>test_navigation_flow |

## 6. Outils de Test

### 6.1 Framework de Test
- **pytest** : Framework principal pour l'exécution des tests
- **pytest-flask** : Extension pour tester les applications Flask
- **pytest-cov** : Extension pour la couverture de code

### 6.2 Configuration
- **pytest.ini** : Configuration des tests
- **conftest.py** : Fixtures globales et configuration
- **run_tests.py** : Script d'exécution automatisée

### 6.3 Couverture de Code
- **Objectif** : Minimum 60% de couverture
- **Outils** : coverage.py, pytest-cov
- **Rapports** : HTML et terminal

## 7. Exécution des Tests

### 7.1 Commandes de Base
```bash
# Tous les tests
python -m pytest tests/ -v

# Tests unitaires uniquement
python -m pytest tests/unit/ -v

# Tests avec couverture
python -m pytest tests/ --cov=server --cov-report=html

# Script automatisé
python run_tests.py
```

### 7.2 Structure des Rapports
```
htmlcov/
├── index.html          # Rapport principal de couverture
├── server_py.html      # Détail de couverture pour server.py
└── ...
```

## 8. Critères d'Acceptation

### 8.1 Tests Unitaires
- OK Toutes les fonctions utilitaires sont testées
- OK Toute la logique métier est couverte
- OK Gestion des cas d'erreur validée

### 8.2 Tests d'Intégration
- OK Toutes les routes Flask sont testées
- OK Intégration avec les données JSON validée
- OK Gestion des erreurs HTTP testée

### 8.3 Tests Fonctionnels
- OK Parcours utilisateur complet validé
- OK Scénarios d'erreur testés
- OK Cohérence des données vérifiée

### 8.4 Couverture de Code
- OK Minimum 60% de couverture atteint
- OK Toutes les branches critiques couvertes
- OK Rapport de couverture généré

## 9. Maintenance des Tests

### 9.1 Ajout de Nouveaux Tests
- Suivre la structure existante (unit/integration/functional)
- Maintenir le ratio 60/20/20
- Documenter les nouveaux cas de test

### 9.2 Mise à Jour des Tests
- Adapter les tests lors de modifications du code
- Vérifier la couverture après chaque modification
- Maintenir la cohérence des données de test

## 10. Métriques de Qualité

| Métrique            | Objectif       | Actuel    |
|---------------------|----------------|-----------|
| Couverture de code  | ≥ 60%          | À mesurer |
| Tests unitaires     | ≥ 60% du total | OK        |
| Tests d'intégration | ≤ 20% du total | OK        |
| Tests fonctionnels  | ≤ 20% du total | OK        |
| Temps d'exécution   | < 30 secondes  | À mesurer |
