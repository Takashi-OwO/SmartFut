import requests
import sqlite3

# Configuração da API
url = "https://api.football-data.org/v4/competitions/BSA/standings"
headers = {"X-Auth-Token": "coloque sua api aqui"}

# Criar conexão com o banco SQLite
conn = sqlite3.connect("laliga.db")
cursor = conn.cursor()



# Criar tabela para armazenar os dados
cursor.execute("""
CREATE TABLE IF NOT EXISTS standings_Brasil (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    posicao INTEGER,
    jogos_jogados INTEGER,
    pontos INTEGER
)
""")

cursor.execute('DELETE FROM standings_Brasil')
conn.commit()


response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    standings = data["standings"][0]["table"]

    

    for team in standings:
        nome = team["team"]["name"]
        posicao = team["position"]
        jogos_jogados = team["playedGames"]
        pontos = team["points"]

       
        print(f"Nome: {nome}, Posição: {posicao}, Jogos Jogados: {jogos_jogados}, Pontos: {pontos}")

       
        cursor.execute("""
        INSERT INTO standings_Brasil (nome, posicao, jogos_jogados, pontos)
        VALUES (?, ?, ?, ?)
        """, (nome, posicao, jogos_jogados, pontos))

    conn.commit()
    print("times salvos no banco com sucesso! 🚀")

else:
    print(f"Erro ao acessar API: {response.status_code}")


conn.close()