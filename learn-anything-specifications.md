# Cahier des charges - Learn Anything

## 1. src/main.py

Objectif : Contenir la logique principale de génération de graphes interactifs.

Responsabilités :
- Définir et initialiser les agents (Orchestrator, Data Analyzer, Graph Designer, etc.)
- Implémenter la fonction `generate_interactive_graph`
- Gérer les appels API à DeepSeek et Claude
- Gérer le stockage et la récupération des images sur GitHub
- Implémenter la gestion des erreurs avec la classe `LearnEverythingError`
- Fournir des fonctions de débogage

Interfaces :
- Exposer `generate_interactive_graph` pour être utilisé par d'autres modules
- Utiliser les API DeepSeek et Claude
- Interagir avec l'API GitHub pour la gestion des images

## 2. src/cli.py

Objectif : Fournir une interface en ligne de commande pour l'utilisateur.

Responsabilités :
- Parser les arguments de ligne de commande
- Charger les données d'entrée à partir d'un fichier
- Appeler la fonction `generate_interactive_graph` de main.py
- Sauvegarder les résultats dans un fichier de sortie
- Gérer les logs et les messages d'erreur pour l'utilisateur

Interfaces :
- Accepter des arguments en ligne de commande
- Utiliser `generate_interactive_graph` de main.py

## 3. tests/test_main.py

Objectif : Tester les fonctionnalités principales de main.py.

Responsabilités :
- Tester chaque agent individuellement
- Tester la fonction `generate_interactive_graph`
- Tester les fonctions de gestion des images
- Tester les appels API (avec des mocks)
- Tester la gestion des erreurs

## 4. tests/test_cli.py

Objectif : Tester l'interface en ligne de commande.

Responsabilités :
- Tester le parsing des arguments
- Tester le chargement des fichiers d'entrée
- Tester la sauvegarde des fichiers de sortie
- Tester la gestion des erreurs de l'interface CLI

## 5. tests/test_performance.py

Objectif : Tester les performances du système avec de grands ensembles de données.

Responsabilités :
- Générer ou charger de grands ensembles de données
- Mesurer le temps d'exécution pour différentes tailles de données
- Vérifier la qualité des résultats pour de grands ensembles de données
- Tester les limites du système en termes de taille de données

## 6. tests/test_end_to_end.py

Objectif : Tester le système de bout en bout.

Responsabilités :
- Simuler un scénario complet d'utilisation
- Vérifier que tous les composants fonctionnent ensemble correctement
- Tester l'intégration entre les différents agents et modules

## 7. scripts/generate_large_dataset.py

Objectif : Générer un grand ensemble de données réaliste pour les tests.

Responsabilités :
- Créer un dataset simulant un réseau social
- Générer des utilisateurs, des posts, des commentaires et des relations
- Sauvegarder le dataset dans un fichier JSON

## 8. .env

Objectif : Stocker les variables d'environnement sensibles.

Contenu :
- Clés API pour DeepSeek et Claude
- Token GitHub
- Autres configurations sensibles

## 9. requirements.txt

Objectif : Lister toutes les dépendances Python du projet.

Contenu :
- Noms et versions des packages Python requis

## 10. README.md

Objectif : Fournir une documentation générale du projet.

Contenu :
- Description du projet
- Instructions d'installation et de configuration
- Guide d'utilisation
- Structure du projet
- Instructions pour exécuter les tests
- Informations sur la contribution et la licence

