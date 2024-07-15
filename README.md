# Learn Anything

Learn Anything est un projet qui utilise l'intelligence artificielle pour générer des graphes interactifs à partir de données brutes. Il combine les capacités de DeepSeekCoder et de Claude 3.5 Sonnet pour analyser, structurer et visualiser des informations complexes.

## Fonctionnalités

* Analyse de données brutes et structuration en graphe
* Génération de code SVG et JavaScript pour des graphes interactifs
* Création et gestion d'images associées au graphe
* Optimisation des performances du code généré
* Vérification de la qualité du graphe final

## Prérequis

* Python 3.8+
* Compte GitHub (pour le stockage des images)
* Clés API pour DeepSeek et Claude

## Installation

1. Clonez le repository :

   ```
   git clone https://github.com/votre-username/Learn-Anything.git
   cd Learn-Anything
   ```

2. Créez un environnement virtuel et activez-le :

   ```
   python -m venv venv
   source venv/bin/activate  # Sur Windows, utilisez venv\Scripts\activate
   ```

3. Installez les dépendances :

   ```
   pip install -r requirements.txt
   ```

4. Copiez le fichier `.env.example` en `.env` et remplissez-le avec vos propres clés API :

   ```
   cp .env.example .env
   ```

## Configuration

Modifiez le fichier `.env` avec vos informations :

```
DEEPSEEK_API_KEY=votre_clé_api_deepseek
CLAUDE_API_KEY=votre_clé_api_claude
GITHUB_TOKEN=votre_token_github
REPO_NAME=votre-username/Learn-Anything
BRANCH_NAME=main
```

## Utilisation

Pour générer un graphe interactif, utilisez la commande suivante :

```
python src/cli.py chemin/vers/votre/fichier_entree.json --output chemin/vers/fichier_sortie.json
```

Options :
* `--output` : Spécifie le chemin du fichier de sortie (par défaut : `output.json`)
* `--max-iterations` : Définit le nombre maximum d'itérations pour chaque étape (par défaut : 3)

## Structure du projet

* `src/` : Contient le code source principal
   * `main.py` : Logique principale de génération de graphes
   * `cli.py` : Interface en ligne de commande
* `tests/` : Contient les tests unitaires et de performance
* `scripts/` : Scripts utilitaires, comme la génération de grands datasets
* `assets/` : Dossier pour stocker les images générées

## Tests

Pour exécuter les tests unitaires :

```
python -m unittest discover tests
```

Pour les tests de performance :

```
python -m unittest tests.test_performance
```

## Contribution

Les contributions sont les bienvenues ! Veuillez suivre ces étapes :

1. Forkez le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.

## Contact

Votre Nom - [@votre_twitter](https://twitter.com/votre_twitter) - email@example.com

Lien du projet : [https://github.com/votre-username/Learn-Anything](https://github.com/votre-username/Learn-Anything)
