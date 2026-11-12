import os
from flask import Flask, jsonify, render_template, request
from openai import OpenAI, OpenAIError

app = Flask(__name__)
MAX_HISTORY = 12
SYSTEM_PROMPT = ("Tu es un assistant de démonstration pour une petite entreprise. "
                 "Réponds en français, clairement et brièvement. "
                 "N'invente pas les horaires, les tarifs ou les disponibilités : "
                 "demande des précisions si ces informations ne sont pas fournies.")


def normalize_history(value):
    if not isinstance(value, list):
        return []
    result = []
    for item in value[-MAX_HISTORY:]:
        if (isinstance(item, dict) and item.get('role') in ('user', 'assistant')
                and isinstance(item.get('content'), str)):
            content = item['content'].strip()[:2000]
            if content:
                result.append({'role': item['role'], 'content': content})
    return result


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/api/chat')
def chat():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error='Corps JSON invalide.'), 400
    message = payload.get('message')
    if not isinstance(message, str) or not message.strip():
        return jsonify(error='Le message ne peut pas être vide.'), 400
    message = message.strip()
    if len(message) > 2000:
        return jsonify(error='Message trop long (2000 caractères maximum).'), 400
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return jsonify(error='Clé API absente : configurez OPENAI_API_KEY dans .env.'), 503
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
    messages.extend(normalize_history(payload.get('history')))
    messages.append({'role': 'user', 'content': message})
    try:
        client = OpenAI(api_key=api_key, timeout=25.0, max_retries=1)
        completion = client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            messages=messages,
            max_tokens=400,
        )
        answer = completion.choices[0].message.content or 'Aucune réponse générée.'
        return jsonify(reply=answer)
    except OpenAIError:
        app.logger.exception('Erreur OpenAI')
        return jsonify(error="Le service IA est indisponible. Vérifiez la clé API et réessayez."), 502


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    app.run(host='127.0.0.1', port=5000, debug=False)
