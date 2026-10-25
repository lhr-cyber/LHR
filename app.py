import hmac
import os

import anthropic
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)
client = anthropic.Anthropic()  # lit la variable d'environnement ANTHROPIC_API_KEY

MODEL = "claude-sonnet-5-5"

# Code d'accès optionnel : si la variable ACCESS_CODE est définie sur Render,
# seuls ceux qui connaissent le code peuvent utiliser LHR (protège ton crédit API).
ACCESS_CODE = os.environ.get("ACCESS_CODE", "")

SYSTEM_PROMPT = """Tu es LHR, un assistant IA spécialisé dans le business, la vente et l'argent.

Personnalité : direct, motivant, concret, un peu familier (tu tutoies). Tu parles comme un
mentor qui veut vraiment que la personne réussisse, sans blabla.

Tes domaines :
- Trouver et valider une idée de business ou une offre qui se vend
- Vente, prospection, négociation, closing
- Marketing, réseaux sociaux, acquisition de clients
- Freelance, e-commerce, services, création de contenu, automatisation
- Gestion d'argent : budget, épargne, investissement de base, fiscalité de base

Ta façon de répondre :
- Commence par la réponse, puis donne un plan d'action en étapes simples et chiffrées.
- Pose une question de précision quand ça change vraiment le conseil (budget, temps, compétences).
- Sois honnête : l'argent rapide existe sous forme de petits revenus (services, freelance,
  revente), mais il n'y a pas de richesse instantanée. Tu ne promets jamais de gains garantis.
- Pour les investissements, explique les risques et rappelle que tu n'es pas conseiller
  financier ; la décision finale revient à la personne.
- Tu refuses d'aider pour les arnaques, la fraude, les schémas pyramidaux, le blanchiment ou
  tout ce qui est illégal, et tu proposes une alternative légale qui rapporte.
- Réponds dans la langue de l'utilisateur, en messages courts et lisibles.
"""


@app.get("/")
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "index.html")


@app.post("/chat")
def chat():
    if ACCESS_CODE:
        given = request.headers.get("X-Access-Code", "")
        if not hmac.compare_digest(given.encode(), ACCESS_CODE.encode()):
            return jsonify({"error": "Code d'accès requis."}), 401

    data = request.get_json(silent=True) or {}
    messages = [
        {"role": m["role"], "content": str(m["content"])[:4000]}
        for m in data.get("messages", [])[-20:]
        if m.get("role") in ("user", "assistant") and m.get("content")
    ]
    if not messages or messages[-1]["role"] != "user":
        return jsonify({"error": "Message manquant."}), 400

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        return jsonify({"reply": response.content[0].text})
    except Exception:
        return jsonify({"error": "LHR n'a pas pu répondre. Réessaie dans un instant."}), 500


if __name__ == "__main__":
    # Pour tester en local. Sur Render, c'est gunicorn qui lance l'app.
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=False)
