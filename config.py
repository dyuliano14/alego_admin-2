import os

class Config:
    SECRET_KEY = 'admin123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///alego_admin.db'  # ✅ Aqui!
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'admin@gmail.com'
    MAIL_PASSWORD = 'admin123'
 # 💡 Adicione essa linha:
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'disciplinas')