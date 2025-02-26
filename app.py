from flask import Flask, request, redirect
import requests
import os

app = Flask(__name__)

# Configurações
CLIENT_ID = os.getenv("CLIENT_ID")  # Obtenha do ambiente
CLIENT_SECRET = os.getenv("CLIENT_SECRET")  # Obtenha do ambiente
REDIRECT_URI = os.getenv("REDIRECT_URI")  # Obtenha do ambiente

# Rota inicial para redirecionar ao Mercado Livre
@app.route("/")
def index():
    auth_url = f"https://auth.mercadolivre.com.br/authorization?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    return redirect(auth_url)

# Rota de callback para receber o código de autorização
@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Erro: Código de autorização não encontrado.", 400

    # Trocar o código por um Access Token
    token_url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        return f"Access Token obtido: {access_token}"
    else:
        return f"Erro ao obter o token: {response.status_code}", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)