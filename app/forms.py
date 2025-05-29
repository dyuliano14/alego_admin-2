from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class DisciplinaForm(FlaskForm):
    nome_disciplina = StringField('Nome da Disciplina', validators=[DataRequired()])
    submit = SubmitField('Criar')

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirme a Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Enviar link de recuperação')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nova Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirme a Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Redefinir Senha')

class RecuperarSenhaForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar')

class RedefinirSenhaForm(FlaskForm):
    password = PasswordField('Nova Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Redefinir')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar link de redefinição')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nova senha', validators=[
        DataRequired(), Length(min=6)
    ])
    confirm_password = PasswordField('Confirmar senha', validators=[
        DataRequired(), EqualTo('password')
    ])
    submit = SubmitField('Redefinir senha')

class NovaDisciplinaForm(FlaskForm):
    nome_disciplina = StringField('Nome da Disciplina', validators=[DataRequired()])
    categoria = StringField('Categoria')
    tipo = StringField('Tipo')
    ordem = IntegerField('Ordem', default=0)
    descricao = TextAreaField('Descrição')
    link = StringField('Link')
    
    aulas = TextAreaField('Aulas (separadas por vírgula)')
    planejamento = TextAreaField('Planejamento')
    flashcards = TextAreaField('Flashcards (separados por vírgula)')
    resumos = TextAreaField('Resumos')
    apresentacao = TextAreaField('Apresentação')

    submit = SubmitField('Salvar')
