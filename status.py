import requests
import json

API_KEY = "coloque sua api aqui"
URL = "https://api.football-data.org/v4/competitions/BSA/scorers"

headers = {"X-Auth-Token": API_KEY}
response = requests.get(URL, headers=headers)

if response.status_code == 200:
    dados = response.json()
    print(json.dumps(dados, indent=4))  # Agora os dados são impressos corretamente
else:
    print("Erro ao acessar API:", response.status_code)

