from flask import Flask, render_template, redirect, url_for, request, flash, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Configurações básicas
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Modelo de usuário
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Formulário de registro
class RegisterForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Registrar')

# Formulário de login
class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

# Carregamento de usuário
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rota inicial
@app.route('/')
@login_required
def index():
    return f"Olá, {current_user.username}! <a href='/logout'>Sair</a> | <a href='/usuarios'>Ver usuários</a>"

# Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Usuário já existe!', 'danger')
            return redirect(url_for('register'))
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Usuário registrado! Faça login.', 'success')
        return redirect(url_for('login'))
    return render_template_string('''
        <h2>Registrar</h2>
        <form method="post">
            {{ form.hidden_tag() }}
            {{ form.username.label }} {{ form.username() }}<br>
            {{ form.password.label }} {{ form.password() }}<br>
            {{ form.submit() }}
        </form>
        <a href="/login">Login</a>
    ''', form=form)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Credenciais inválidas', 'danger')
    return render_template_string('''
        <h2>Login</h2>
        <form method="post">
            {{ form.hidden_tag() }}
            {{ form.username.label }} {{ form.username() }}<br>
            {{ form.password.label }} {{ form.password() }}<br>
            {{ form.submit() }}
        </form>
        <a href="/register">Registrar</a>
    ''', form=form)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu com sucesso.', 'success')
    return redirect(url_for('login'))

# ✅ Rota para listar todos os usuários
@app.route('/usuarios')
@login_required
def listar_usuarios():
    usuarios = User.query.all()
    return render_template_string('''
        <h2>Usuários cadastrados</h2>
        <table border="1">
            <tr><th>ID</th><th>Usuário</th><th>Senha (hash)</th></tr>
            {% for u in usuarios %}
            <tr><td>{{ u.id }}</td><td>{{ u.username }}</td><td>{{ u.password }}</td></tr>
            {% endfor %}
        </table>
        <a href="/">Voltar</a>
    ''', usuarios=usuarios)

# Execução
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
