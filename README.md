# projeto-site-flask

Projeto: Painel Administrativo ALEGO Admin
Descrição: Interface web para criar e alimentar disciplinas para o site estático "AlegoMain".
Tecnologias: Flask, HTML, CSS, Contentful API

Execução local:
1. python -m venv venv
2. source venv/bin/activate (ou venv\Scripts\activate no Windows)
3. pip install -r requirements.txt
4. python run.py


acesse:
https://dyuliano14.github.io/alego_admin/

~~~arduino
alego_admin/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── forms.py
│   ├── models.py
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       └── dashboard.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── config.py
├── run.py
├── requirements.txt
└── README.md
~~~
