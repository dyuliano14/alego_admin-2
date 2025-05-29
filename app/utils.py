from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def gerar_token(email):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(email, salt='recuperacao-senha')

def verificar_token(token, expira_em=3600):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='recuperacao-senha', max_age=expira_em)
    except Exception:
        return None
    return email
