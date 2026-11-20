# Fragrance Recommender — Moteur de Recommandation Olfactive

Application interactive d'aide au choix de parfums développée en **Python**, **Pandas** et **Streamlit**, reposant sur une base structurée de **150 références** (Dupes, Designers et Haute Parfumerie / Niche).

## Fonctionnalités principales
- **Questionnaire olfactif guidé** : traduction de préférences utilisateur (gamme, budget, intensité, univers olfactif, occasion) en critères de filtrage et de scoring pondéré.
- **Algorithme de matching explicable** : calcul d'un score de compatibilité sur 100 % combinant adéquation olfactive, saisonnalité, occasion et performances (tenue et sillage).
- **Comparateur face-à-face** : analyse côte à côte de deux références (pyramides olfactives, prix, inspirations).
- **Catalogue interactif** : exploration et recherche plein texte sur les 150 parfums de la base de données.

## Stack Technique
- **Langage** : Python 3
- **Manipulation de données** : Pandas
- **Interface & Déploiement** : Streamlit / Streamlit Community Cloud

## Installation & Lancement
```bash
pip install -r requirements.txt
streamlit run app.py
