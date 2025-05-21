import requests
import sqlite3

# Configuração da API
API_KEY = 'coloque sua api aqui'
BASE_URL = 'https://api.football-data.org/v4/competitions/BSA/scorers'

# Função para buscar os dados da API
def obter_dados():
    headers = {'X-Auth-Token': API_KEY}
    response = requests.get(BASE_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao acessar API: {response.status_code}")
        return None

# Banco de dados - Criar tabela
def criar_banco_dados():
    with sqlite3.connect('laliga.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS jogadores_Brasil (
                          nome TEXT, gols INTEGER, equipe TEXT, jogos INTEGER, posicao text, nationality text, assists INTERGER, penalties INTERGER)''')
        conexao.commit()

# Banco de dados - Limpar antes de salvar novos dados
def salvar_dados(dados):
    if "scorers" not in dados:  # Verifica se a chave 'scorers' está presente
        print("Erro: A chave 'scorers' não foi encontrada na resposta da API.")
        return
    
    with sqlite3.connect('laliga.db') as conexao:
        cursor = conexao.cursor()
        
        # Limpa a tabela antes de inserir novos dados
        cursor.execute('DELETE FROM jogadores_Brasil')
        conexao.commit()

        # Insere os novos dados
        for jogador in dados["scorers"][:20]:
            nome = jogador['player']['name']
            gols = jogador['goals']
            equipe = jogador['team']['name']
            jogos = jogador['playedMatches']
            posicao = jogador['player']['section']
            nationality = jogador['player']['nationality']
            assists = jogador['assists']
            penalties = jogador['penalties']

            cursor.execute('INSERT INTO jogadores_Brasil VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (nome, gols, equipe, jogos, posicao, nationality, assists, penalties))
        
        conexao.commit()
        print("Dados atualizados no banco com sucesso! 🚀")

# Execução
criar_banco_dados()
dados = obter_dados()

if dados:
    salvar_dados(dados)
