import sqlite3

# Conectando ao banco de dados
conn = sqlite3.connect("laliga.db")
cursor = conn.cursor()

# Consultando dados da tabela jogadores
cursor.execute("SELECT * FROM jogadores")
jogadores = cursor.fetchall()

# Mostrando os resultados
for jogador in jogadores:
    print(jogador)

# Fechando a conexão
conn.close()
