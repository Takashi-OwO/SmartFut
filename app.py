import requests
import sqlite3

# Sua chave da API do Football Data
API_KEY = 'coloque sua api aqui'

# URL base da API
BASE_URL = 'https://api.football-data.org/v4/competitions/PD/scorers'

# Função para buscar dados da API
def obter_dados():
    headers = {'X-Auth-Token': API_KEY}
    response = requests.get(BASE_URL, headers=headers)
    if response.status_code == 200:
        return response.json() 
    else:
        print(f"Erro: {response.status_code}")
        return None
dados = obter_dados()
print(dados) 


# Banco de dados
def criar_banco_dados():
    conexao = sqlite3.connect('laliga.db')
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS jogadores (
                       nome TEXT, gols INTEGER, equipe TEXT, jogos INTERGER, posicao text, nationality text, assists INTERGER, penalties INTERGER)''')
    conexao.commit()
    cursor.execute('DELETE FROM jogadores')
    conexao.commit()
    conexao.close()

def salvar_dados(dados):
    conexao = sqlite3.connect('laliga.db')
    cursor = conexao.cursor()
    for jogador in dados['scorers']:
        nome = jogador['player']['name']
        gols = jogador['goals']
        equipe = jogador['team']['name']
        jogos = jogador['playedMatches']
        posicao = jogador['player']['section']
        nationality = jogador['player']['nationality']
        assists = jogador['assists']
        penalties = jogador['penalties']

        cursor.execute('INSERT INTO jogadores VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (nome, gols, equipe, jogos, posicao, nationality, assists, penalties))
    conexao.commit()
    conexao.close()

# Execução
criar_banco_dados()
dados = obter_dados()
if dados:
    salvar_dados(dados)
    print("Dados salvos no banco de dados com sucesso!")
