from flask import render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from app.model import Usuario
from app import app, db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')

    usuario = Usuario.query.filter_by(email_user=email).first()

    if usuario and check_password_hash(usuario.senha_user, senha):
       
        return render_template('home.html', nome_usuario=usuario.nome_user)
    else:
        
        return render_template('index.html', error_message='Login falhou. Verifique suas credenciais.')

    
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        hashed_senha = generate_password_hash(senha)

        novo_usuario = Usuario(nome_user=nome, email_user=email, senha_user=hashed_senha)

        db.session.add(novo_usuario)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('cadastro.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
