# Importar
from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Chave secreta para uso de session
app.secret_key = 'my_top_secret_123'

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portifolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o banco
db = SQLAlchemy(app)
class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Card {self.id}>'
with app.app_context():
    db.create_all()

  


@app.route('/opinion', methods=['POST'])
def save_opinion():
    print("1. A rota /opinion foi chamada!")

    user_email = request.form.get('email', '').strip()
    text = request.form.get('text', '').strip()

    print("2. E-mail recebido:", user_email)
    print("3. Comentário recebido:", text)

    if not user_email or not text:
        return 'Preencha o e-mail e a opinião.', 400

    opinion = Opinion(user_email=user_email, text=text)

    try:
        db.session.add(opinion)
        db.session.commit()
        print("4. OPINIÃO SALVA NO BANCO!")
    except Exception as erro:
        db.session.rollback()
        print("ERRO AO SALVAR:", repr(erro))
        raise

    return redirect('/')

# Conteúdo da página
@app.route('/')
def index():
    return render_template('index.html')


# Habilidades Dinâmicas
@app.route('/', methods=['POST'])
def process_form():
    button_python = request.form.get('button_python')
    button_html = request.form.get('button_html')
    button_discord = request.form.get('button_discord')
    button_db = request.form.get('button_db')
    return render_template('index.html', button_python=button_python, button_html=button_html, button_discord=button_discord, button_db=button_db)


if __name__ == "__main__":
    app.run(debug=True)
