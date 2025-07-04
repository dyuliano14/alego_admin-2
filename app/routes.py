from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Disciplina
from .forms import LoginForm, RegisterForm, RequestResetForm, ResetPasswordForm, NovaDisciplinaForm
from flask_mail import Message, Mail
from .utils import gerar_token, verificar_token
from . import db
from datetime import datetime
import os
import csv
import json

main = Blueprint('main', __name__)
mail = Mail()



# routes.py

@main.route('/login', methods=['GET', 'POST'])
def login_view():
    form = LoginForm()  # 👈 Isso é bom!

    if form.validate_on_submit(): # Código para POST
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard_view'))

        flash('Usuário ou senha inválidos', 'danger')
        # ❗️ Faltava um retorno aqui para o caso de falha no POST e re-renderização do form
        return render_template('login.html', form=form) # Adicione este retorno

    # Código para GET (primeira vez que acessa a página)
    return render_template('login.html', form=form)

# routes.py
@main.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard_view'))
    return redirect(url_for('main.login_view'))

@main.route('/logout')
@login_required
def logout_view():
    logout_user()
    return redirect(url_for('main.login_view'))



@main.context_processor
def inject_current_year():
    """
    Injects the current year into the template context.
    This makes {{ current_year }} available in all templates
    rendered by routes in this blueprint.
    """
    return {'current_year': datetime.utcnow().year}

@main.route('/dashboard')
@login_required
def dashboard_view():
    return render_template('admin/dashboard.html')

@main.route('/nova_disciplina', methods=['GET', 'POST'])
@login_required
def nova_disciplina_view():
    form = NovaDisciplinaForm()
    
    if form.validate_on_submit():
        nova = Disciplina(
            titulo=form.nome_disciplina.data,
            categoria="",
            tipo="",
            ordem=0,
            descricao="",
            link="",
            aulas="",
            planejamento="",
            flashcards="",
            resumos="",
            apresentacao=""
        )
        db.session.add(nova)
        db.session.commit()
        flash("Disciplina criada com sucesso!")
        return redirect(url_for('main.listar_disciplinas_view'))

    # 🔥 Importante: precisa ter esse retorno para método GET
    return render_template('admin/nova_disciplina.html', form=form)



@main.route('/disciplinas/<nome>/upload_flashcards', methods=['POST'])
@login_required
def upload_flashcards(nome):
    file = request.files.get('file')
    if not file or not file.filename.endswith('.csv'):
        flash("Envie um arquivo .CSV válido.")
        return redirect(url_for('main.dashboard_view'))

    path = os.path.join(current_app.config['UPLOAD_FOLDER'], nome)
    os.makedirs(path, exist_ok=True)

    reader = csv.DictReader(file.stream.read().decode('utf-8').splitlines())
    data = list(reader)

    json_path = os.path.join(path, 'flashcards.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    flash("Flashcards enviados com sucesso!")
    return redirect(url_for('main.dashboard_view'))

@main.route('/disciplinas')
@login_required
def listar_disciplinas_view():
    disciplinas = Disciplina.query.order_by(Disciplina.ordem).all()
    return render_template('admin/listar_disciplinas.html', disciplinas=disciplinas)

@main.route('/editar_disciplina/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_disciplina_view(id):
    disciplina = Disciplina.query.get_or_404(id)
    form = NovaDisciplinaForm(obj=disciplina)

    if form.validate_on_submit():
        disciplina.titulo = form.nome_disciplina.data.strip()
        db.session.commit()
        flash('Disciplina atualizada com sucesso!', 'success')
        return redirect(url_for('main.listar_disciplinas_view'))  # ✅ Corrigido: precisa retornar aqui

    return render_template('admin/editar_disciplina.html', form=form, disciplina=disciplina)  # ✅ retorno em qualquer caso



@main.route('/excluir_disciplina/<int:id>', methods=['POST'])
@login_required
def excluir_disciplina_view(id):
    d = Disciplina.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    flash(f'Disciplina "{d.titulo}" excluída com sucesso!')
    return redirect(url_for('main.listar_disciplinas_view'))



# routes.py
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Este nome de usuário já existe. Por favor, escolha outro.', 'danger')
            return render_template('admin/register.html', form=form) # Re-renderiza com o erro

        # Se o email for um campo obrigatório e único:
        # existing_email = User.query.filter_by(email=form.email.data).first()
        # if existing_email:
        #     flash('Este email já está registrado. Por favor, use outro.', 'danger')
        #     return render_template('admin/register.html', form=form)

        new_user = User(
            username=form.username.data,
            # email=form.email.data, # Se você tiver o campo email no RegisterForm e no modelo User
            password=generate_password_hash(form.password.data)
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário registrado com sucesso! Faça o login.', 'success')
        return redirect(url_for('main.login_view'))

    return render_template('admin/register.html', form=form) # Passe o form para o template

@main.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = gerar_token(user.email)
            link = url_for('main.redefinir', token=token, _external=True)
            msg = Message('Recuperação de Senha ALEGO',
                          sender='seuemail@gmail.com',
                          recipients=[user.email])
            msg.body = f'Acesse este link para redefinir sua senha: {link}'
            mail.send(msg)

        flash('Se o e-mail estiver registrado, enviaremos um link.', 'info')
        return redirect(url_for('main.login_view'))

    return render_template('admin/recuperar.html', form=form)

@main.route('/redefinir/<token>', methods=['GET', 'POST'])
def redefinir(token):
    email = verificar_token(token)
    if not email:
        flash('Token inválido ou expirado', 'danger')
        return redirect(url_for('main.recuperar'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        user.password = form.password.data
        db.session.commit()
        flash('Senha redefinida com sucesso!', 'success')
        return redirect(url_for('main.login_view'))

    return render_template('admin/redefinir.html', form=form)
