from flask import Flask, render_template, redirect, url_for, request, flash
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import os
from werkzeug.security import generate_password_hash, check_password_hash




app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'users.db')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class RegisterForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Registrar')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

def get_standings():
    conn = sqlite3.connect("laliga.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, posicao, jogos_jogados, pontos FROM standings ORDER BY posicao")
    teams = cursor.fetchall()
    conn.close()
    return teams
def get_standings_br():
    conn = sqlite3.connect("laliga.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, posicao, jogos_jogados, pontos FROM standings_Brasil ORDER BY posicao")
    teams_br = cursor.fetchall()
    conn.close()
    return teams_br
def get_jogadores_br():
    conn = sqlite3.connect("laliga.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, gols, equipe, jogos, posicao, nationality, assists, penalties FROM jogadores_Brasil")
    jogadores_br = cursor.fetchall()
    conn.close()
    return jogadores_br

@app.route('/logout')
@login_required
def logout():
    logout_user()  # Faz logout do usuário
    flash('Você saiu da conta com sucesso!', 'success')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Usuário já existe!', 'danger')  # A mensagem será armazenada
            return redirect(url_for('register'))  # Redireciona para a página de registro


        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash('Registro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):  # Correção do hash de senha
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Credenciais inválidas! Tente novamente.', 'danger')
    
    return render_template('login.html', form=form)   


@app.route('/')
@login_required
def index():
    if not current_user.is_authenticated:  # Verifica se o usuário está logado
        return redirect(url_for('login'))  # Redireciona para a tela de login
    
    standings = get_standings()
    standings_br = get_standings_br()
    jogadores_br = get_jogadores_br()

    conn = sqlite3.connect("laliga.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jogadores")
    jogadores = cursor.fetchall()
    conn.close()
    
    return render_template("index.html", standings=standings, jogadores=jogadores, standings_br=standings_br, jogadores_br=jogadores_br)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()

    # Conectar ao banco de dados
    conn = sqlite3.connect("laliga.db")
    cursor = conn.cursor()

    # Buscar dados das tabelas de jogadores
    cursor.execute("SELECT nome, gols, equipe, jogos, posicao, nationality, assists, penalties FROM jogadores")
    jogadores_la_liga = cursor.fetchall()

    cursor.execute("SELECT nome, gols, equipe, jogos, posicao, nationality, assists, penalties FROM jogadores_Brasil")
    jogadores_brasileirao = cursor.fetchall()

    # Buscar dados das tabelas de classificação
    cursor.execute("SELECT nome, posicao, jogos_jogados, pontos FROM standings ORDER BY posicao")
    times_la_liga = cursor.fetchall()

    cursor.execute("SELECT nome, posicao, jogos_jogados, pontos FROM standings_Brasil ORDER BY posicao")
    times_brasileirao = cursor.fetchall()

    conn.close()

    # Filtrar jogadores e times que contenham o texto digitado pelo usuário
    def filtrar(lista):
        return [item for item in lista if any(query in str(valor).lower() for valor in item)]

    filtered_players_la_liga = filtrar(jogadores_la_liga)
    filtered_players_brasileirao = filtrar(jogadores_brasileirao)
    filtered_teams_la_liga = filtrar(times_la_liga)
    filtered_teams_brasileirao = filtrar(times_brasileirao)

    return render_template(
        'index.html',
        jogadores=filtered_players_la_liga,
        jogadores_br=filtered_players_brasileirao,
        standings=filtered_teams_la_liga,
        standings_br=filtered_teams_brasileirao
    )




if __name__ == '__main__':
        with app.app_context():
            db.create_all()
        app.run(debug=True)
        
