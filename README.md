# WordPress Markdown Publisher

Publie automatiquement un fichier Markdown sur WordPress via REST API.

## Installation

```bash
# 1. Créer environnement virtuel
python -m venv venv

# 2. Activer (Windows)
venv\Scripts\activate

# 3. Installer dépendances
pip install requests markdown python-dotenv
```

# Sitegrow - Markdown to WordPress Publisher (REST API)

Petit script qui prend un fichier Markdown (.md) et le publie automatiquement comme article WordPress via l’API REST (Application Password).

## Prérequis

- Python 3.10+ (3.11 recommandé)
- Une instance WordPress (LocalWP, Docker, ou serveur distant)
- Un compte admin WordPress + Application Password activé

## 1) Préparer WordPress (LocalWP recommandé)

1. Créer un site WordPress dans LocalWP (ex: sitegrow-test)
2. Ouvrir WP Admin
3. Créer un Application Password :
   - Users -> Profile -> Application Passwords
   - Name: sitegrow-bot
   - Add New Application Password
   - Copier le mot de passe généré

Important : si tu utilises LocalWP en "Localhost routing", ton URL ressemble à http://localhost:10004

## 2) Configuration du projet

Cloner le repo puis se placer dans le dossier :

```bash
git clone https://github.com/Kaemo00/Sitegrow.git
cd Sitegrow
```
