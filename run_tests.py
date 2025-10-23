#!/usr/bin/env python3
"""Script pour lancer tous les tests avec couverture de code."""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Exécute une commande et affiche le résultat."""
    print(f"\n{'='*60}")
    print(f" {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("ERREURS:")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Erreur lors de l'exécution: {e}")
        return False


def main():
    """Fonction principale pour lancer tous les tests."""
    print("🧪 LANCEMENT DES TESTS POUR LE SYSTÈME GUDLFT")
    print("=" * 60)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists("server.py"):
        print("❌ Erreur: Le fichier server.py n'est pas trouvé.")
        print("   Assurez-vous d'être dans le répertoire Python_Testing")
        sys.exit(1)
    
    # 1. Tests unitaires
    print("\n📋 1. TESTS UNITAIRES")
    success_unit = run_command(
        "python -m pytest tests/unit/ -v --tb=short",
        "Tests unitaires"
    )
    
    # 2. Tests d'intégration  
    print("\n📋 2. TESTS D'INTÉGRATION")
    success_integration = run_command(
        "python -m pytest tests/integration/ -v --tb=short",
        "Tests d'intégration"
    )
    
    # 3. Tests fonctionnels
    print("\n📋 3. TESTS FONCTIONNELS")
    success_functional = run_command(
        "python -m pytest tests/functional/ -v --tb=short", 
        "Tests fonctionnels"
    )
    
    # 4. Tous les tests avec couverture
    print("\n📋 4. TOUS LES TESTS AVEC COUVERTURE")
    success_coverage = run_command(
        "python -m pytest tests/ -v --cov=server --cov-report=html --cov-report=term",
        "Tests avec couverture de code"
    )
    
    # 5. Résumé
    print("\n" + "="*60)
    print(" RÉSUMÉ DES TESTS")
    print("="*60)
    
    results = [
        ("Tests unitaires", success_unit),
        ("Tests d'intégration", success_integration), 
        ("Tests fonctionnels", success_functional),
        ("Couverture de code", success_coverage)
    ]
    
    all_passed = True
    for test_type, success in results:
        status = "✅ RÉUSSI" if success else "❌ ÉCHEC"
        print(f"{test_type:20} : {status}")
        if not success:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
        print("📁 Rapport de couverture généré dans: htmlcov/index.html")
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("   Vérifiez les messages d'erreur ci-dessus")
    
    print("="*60)
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
