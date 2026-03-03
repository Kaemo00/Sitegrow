import os
import sys
import requests
import markdown
from dotenv import load_dotenv

def main():
    # Charger les variables d'environnement
    load_dotenv()
    
    # Vérifier les credentials
    wp_url = os.getenv('WP_URL', '').rstrip('/')
    wp_user = os.getenv('WP_USER')
    wp_password = os.getenv('WP_APP_PASSWORD')
    
    if not all([wp_url, wp_user, wp_password]):
        print("❌ Erreur : Variables manquantes dans .env")
        print("Requis : WP_URL, WP_USER, WP_APP_PASSWORD")
        sys.exit(1)
    
    # Lire le fichier markdown
    try:
        with open('article.md', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ Erreur : article.md introuvable")
        sys.exit(1)
    
    # Extraire titre et contenu
    lines = content.split('\n')
    title = None
    body_start = 0
    
    for i, line in enumerate(lines):
        if line.strip().startswith('# '):
            title = line.strip()[2:].strip()
            body_start = i + 1
            break
    
    if not title:
        print("❌ Erreur : Aucun titre (ligne '# ...') trouvé")
        sys.exit(1)
    
    # Convertir le contenu en HTML
    body_md = '\n'.join(lines[body_start:]).strip()
    body_html = markdown.markdown(body_md, extensions=['extra', 'codehilite'])
    
    # Préparer la requête
    endpoint = f"{wp_url}/wp-json/wp/v2/posts"
    data = {
        'title': title,
        'content': body_html,
        'status': 'publish'
    }
    
    print(f"📝 Publication : {title}")
    print(f"🌐 Serveur : {wp_url}")
    
    # Publier
    try:
        response = requests.post(
            endpoint,
            json=data,
            auth=(wp_user, wp_password),
            timeout=30
        )
        
        # Gestion des codes HTTP
        if response.status_code == 201:
            post = response.json()
            print(f"\n✅ Article publié avec succès !")
            print(f"📌 ID : {post['id']}")
            print(f"🔗 Lien : {post['link']}")
            
        elif response.status_code == 401:
            print("\n❌ Erreur 401 : Authentification échouée")
            print("Vérifiez WP_USER et WP_APP_PASSWORD")
            sys.exit(1)
            
        elif response.status_code == 403:
            print("\n❌ Erreur 403 : Accès refusé")
            print("Vérifiez les permissions de l'utilisateur")
            sys.exit(1)
            
        elif response.status_code == 404:
            print("\n❌ Erreur 404 : Endpoint introuvable")
            print("Vérifiez que l'API REST est activée sur WordPress")
            sys.exit(1)
            
        else:
            print(f"\n❌ Erreur HTTP {response.status_code}")
            try:
                error = response.json()
                if 'message' in error:
                    print(f"Message : {error['message']}")
            except:
                print(f"Réponse : {response.text[:200]}")
            sys.exit(1)
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Erreur : Impossible de se connecter au serveur")
        print(f"Vérifiez l'URL : {wp_url}")
        sys.exit(1)
        
    except requests.exceptions.Timeout:
        print("\n❌ Erreur : Timeout - Le serveur ne répond pas")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
