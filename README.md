# LHR : coach business et argent

Site de chat avec l'IA LHR (Python + Flask), prêt pour Render.

## Fichiers à mettre sur GitHub
- `app.py` : le serveur (la personnalité de LHR est dans `SYSTEM_PROMPT`)
- `index.html` : la page de chat
- `requirements.txt` : les dépendances (flask, anthropic, gunicorn)
- `README.md` : ce fichier

## 1. Mettre les fichiers sur GitHub
1. Crée un compte sur github.com, puis un nouveau dépôt (par exemple `lhr`).
2. Dans le dépôt : "Add file" puis "Upload files", ajoute les 4 fichiers, puis "Commit changes".

## 2. Héberger sur Render
1. Crée un compte sur render.com et connecte ton GitHub.
2. "New" puis "Web Service", choisis le dépôt `lhr`.
3. Réglages :
   - Runtime : Python
   - Build Command : `pip install -r requirements.txt`
   - Start Command : `gunicorn app:app`
   - Instance Type : Free
4. Dans "Environment", ajoute deux variables :
   - `ANTHROPIC_API_KEY` : ta clé API (console.anthropic.com)
   - `ACCESS_CODE` : un mot de passe de ton choix, que tu donnes seulement aux personnes autorisées
5. Lance le déploiement. Render te donne une adresse en `.onrender.com`.

## Utilisation
Au premier message, LHR demande le code d'accès : écris celui que tu as mis dans `ACCESS_CODE`.
Sans `ACCESS_CODE`, n'importe qui avec le lien peut utiliser ta clé API et consommer ton crédit.

Sur l'offre gratuite, le site s'endort après 15 minutes sans visite et met environ une minute à se réveiller.

Ne mets jamais ta clé API dans un fichier GitHub : uniquement dans les variables d'environnement de Render.
