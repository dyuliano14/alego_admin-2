from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50))
    tipo = db.Column(db.String(50))
    ordem = db.Column(db.Integer, default=0)
    descricao = db.Column(db.Text)
    link = db.Column(db.String(255))
    aulas = db.Column(db.PickleType, default=list)         # lista de strings
    planejamento = db.Column(db.Text)
    flashcards = db.Column(db.PickleType, default=list)    # lista de strings
    resumos = db.Column(db.Text)
    apresentacao = db.Column(db.Text)

