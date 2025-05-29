from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from .models import Disciplina, User
from . import db
from flask import Response
import csv
from io import StringIO

api = Blueprint('api', __name__)

@api.before_request
def skip_csrf_for_api():
    if request.path.startswith('/api/') and request.method in ['POST', 'PUT', 'DELETE']:
        setattr(request, '_dont_enforce_csrf', True)

@api.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'msg': 'Dados incompletos'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'msg': 'Credenciais inválidas'}), 401

    token = create_access_token(identity=user.id)
    return jsonify({'access_token': token}), 200

@api.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({'id': user.id, 'username': user.username}), 200

@api.route('/api/disciplinas', methods=['GET'])
def get_disciplinas():
    disciplinas = Disciplina.query.order_by(Disciplina.ordem).all()
    return jsonify([
        {
            'id': d.id,
            'titulo': d.titulo,
            'categoria': d.categoria,
            'tipo': d.tipo,
            'ordem': d.ordem,
            'descricao': d.descricao,
            'link': d.link
        } for d in disciplinas
    ])


@api.route('/api/disciplinas', methods=['POST'])
@jwt_required()
def criar_disciplina():
    data = request.get_json()
    nova = Disciplina(
        titulo=data.get('titulo'),
        categoria=data.get('categoria'),
        tipo=data.get('tipo'),
        ordem=data.get('ordem', 0),
        descricao=data.get('descricao'),
        link=data.get('link')
    )
    db.session.add(nova)
    db.session.commit()
    return jsonify({'message': 'Disciplina criada com sucesso!'}), 201

@api.route('/api/disciplinas/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_disciplina(id):
    d = Disciplina.query.get_or_404(id)
    data = request.get_json()
    d.titulo = data.get('titulo', d.titulo)
    d.categoria = data.get('categoria', d.categoria)
    d.tipo = data.get('tipo', d.tipo)
    d.ordem = data.get('ordem', d.ordem)
    d.descricao = data.get('descricao', d.descricao)
    d.link = data.get('link', d.link)
    db.session.commit()
    return jsonify({'message': 'Disciplina atualizada com sucesso!'})

@api.route('/api/disciplinas/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_disciplina(id):
    d = Disciplina.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    return jsonify({'message': 'Disciplina removida com sucesso!'})

@api.route('/api/disciplinas/exportar', methods=['GET'])
def exportar_disciplinas():
    disciplinas = Disciplina.query.all()
    data = []
    for d in disciplinas:
        data.append({
            "id": d.id,
            "nome": d.titulo,
            "conteudo": {
                "aulas": d.aulas,
                "planejamento": d.planejamento,
                "flashcards": d.flashcards,
                "resumos": d.resumos,
                "apresentacao": d.apresentacao
            }
        })
    return jsonify(data)

@api.route('/api/disciplinas/exportar/csv', methods=['GET'])
def exportar_disciplinas_csv():
    disciplinas = Disciplina.query.order_by(Disciplina.ordem).all()

    # Criar um buffer de string para armazenar o conteúdo CSV
    si = StringIO()
    writer = csv.writer(si)

    # Escrever o cabeçalho
    writer.writerow(['ID', 'Título', 'Categoria', 'Tipo', 'Ordem', 'Descrição', 'Link'])

    # Escrever os dados das disciplinas
    for d in disciplinas:
        writer.writerow([d.id, d.titulo, d.categoria, d.tipo, d.ordem, d.descricao, d.link])

    # Preparar a resposta com o conteúdo CSV
    output = si.getvalue()
    si.close()
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=disciplinas.csv'}
    )