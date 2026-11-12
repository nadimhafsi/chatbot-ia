# NovaChat — Chatbot IA (Flask + OpenAI)

Projet personnel de démonstration : interface conversationnelle responsive en HTML/CSS/Bootstrap/JavaScript, API REST Flask et réponses générées par l'API OpenAI.

## Fonctionnalités
- Chat web responsive
- Historique de conversation conservé en mémoire dans l'onglet courant (12 derniers messages)
- Backend REST `POST /api/chat`
- Validation des messages et messages d'erreur lisibles
- Clé API conservée côté serveur dans `.env`

## Installation (Python 3.10+)

```bash
python -m venv .venv
# Windows PowerShell :
.venv\Scripts\Activate.ps1
# macOS/Linux : source .venv/bin/activate
pip install -r requirements.txt
```

Copier `.env.example` vers `.env` et remplacer la valeur de `OPENAI_API_KEY` par votre clé API personnelle. **Ne jamais publier `.env` ni la clé.** L'utilisation de l'API OpenAI peut être facturée.

```bash
python app.py
```

Ouvrir http://127.0.0.1:5000

## API

`POST /api/chat` avec :

```json
{
  "message": "Bonjour !",
  "history": [{"role":"user","content":"Salut"},{"role":"assistant","content":"Bonjour !"}]
}
```

Réponse : `{"reply":"..."}` (ou `{"error":"..."}` en cas d'échec).

## Publication GitHub
Créer un dépôt `chatbot-ia`, puis téléverser le contenu du dossier (y compris `templates/`, `static/`, `README.md`, `requirements.txt`, `.gitignore` et `.env.example`). **Ne pas ajouter votre fichier `.env`.**

**Important :** GitHub Pages héberge des sites statiques et **ne peut pas exécuter Flask/Python**. Ce dépôt sert à montrer le code ; pour une démo interactive publique, il faut déployer le backend sur un hébergement Python adapté et configurer la sécurité (quotas, limitation des requêtes, protection de la clé).

## Limites
Prototype pédagogique : pas de comptes utilisateurs, pas de stockage persistant, pas de limitation serveur par utilisateur, pas de prise de rendez-vous et pas de tool calling. Ne pas exposer tel quel en production publique.
