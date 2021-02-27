from flask import render_template, request, url_for, redirect, session
from datetime import datetime
from PIL import Image
import os
from app import app

from app.models.connection import get_db

from app.models.usuarios import Usuarios
from app.models.telefones import Telefones
from app.models.emails import Emails
from app.models.produtos import Produtos

from app.controllers.usuariodao import UsuarioDAO
from app.controllers.telefonedao import TelefoneDAO
from app.controllers.emaildao import EmailDAO
from app.controllers.produtodao import ProdutosDAO

# User routes
@app.route('/')
@app.route('/index/')
def index():
  return render_template("index.html")
  
@app.route('/login/', methods=["GET", "POST"])
def login():
  if( request.method == "POST" ):
    email = request.form['email']
    senha = request.form['senha']

    usuario = UsuarioDAO(get_db())
    usuario = usuario.autenticar(
      email,
      senha
    )

    if( usuario is not None ):
      session['logado'] = usuario
      
      return redirect(url_for('produtos'))

  return render_template("login.html")

@app.route('/logout/')
def logout():
  session['logado'] = None
  session.clear()

  return redirect(url_for('login'))

@app.route('/sign-up/', methods=["GET", "POST"])
def cadastrarUsuarios():  
  if( request.method == "POST" ):
    controle = UsuarioDAO(get_db())

    usuario = Usuarios(
      request.form['nome'],
      request.form['email'],
      request.form['senha']
    )

    controle_telefone = TelefoneDAO(get_db())
    numero_telefone = request.form['telefone']

    controle_email = EmailDAO(get_db())

    usuario_id = None
    if( usuario.nome and usuario.login and usuario.senha ):
      if( numero_telefone != 0 and len(numero_telefone) == 9 ):
        usuario_id = controle.cadastrar(usuario)

        telefone = Telefones(
          numero_telefone,
          usuario_id
        )

        email = Emails(
          request.form['email'],
          usuario_id,
        )

        controle_telefone.cadastrar(telefone)
        controle_email.cadastrar(email)
      
    if( usuario_id is not None and usuario_id > 0 ):
      return redirect(url_for('login'))
    else:
      return 'Falha no cadastro!'

  return render_template("register.html")

@app.route('/produtos/')
@app.route('/produtos/<int:produto_id>/')
def produtos(produto_id = ""):
  if( 'logado' not in session or session['logado'] == None ):
    return redirect(url_for('login'))

  if(produto_id == ""):
    controle_produtos = ProdutosDAO(get_db())
    produtos = controle_produtos.listar()

    return render_template("mostrarTodos.html", produtos=produtos)
  else:
    return ('Produto, {}' .format(produto_id))

@app.route('/shopping/')
def listaPedidos():
  if( 'logado' not in session or session['logado'] == None ):
    return redirect(url_for('login'))

  return 'List Shopping'

#admin
@app.route('/meus-produtos/', methods=['GET', 'POST','PUT', 'DELETE',])
def meusItens():
  if( 'logado' not in session or session['logado'] == None ):
    return redirect(url_for('login'))

  controle_produtos = ProdutosDAO(get_db())
  produtos = controle_produtos.obter(
    session['logado'][0]
  )

  # Criar uma rota especifica para isso
  if request.method == 'POST':
    produto = Produtos(
      request.form['nome'],
      request.form['preco'],
      request.form['situacao'],
      request.form['categoria'],
      datetime.now(),
      'DATTE.png',
      session['logado'][0]
    )
    print(produto.nome)

    novo_produto = controle_produtos.atualizar(produto, 1)
    return redirect(request.url)

  return render_template('listarItens.html', produtos=produtos)

@app.route('/vendidos/')
def vendidos():
  if( 'logado' not in session or session['logado'] == None ):
    return redirect(url_for('login'))

  return render_template('vendidos.html')

@app.route('/cadastrar-produtos/', methods=["GET", "POST"])
def vender():
  if( 'logado' not in session or session['logado'] == None ):
    return redirect(url_for('login'))

  
  if( request.method == "POST" ):
    arquivo = request.files['arquivos']
    momento = datetime.now()
    nome_imagem = '{}{}'.format(momento, arquivo.filename)

    controle_produto = ProdutosDAO(get_db())
    produto = Produtos(
      request.form['nome'],
      request.form['preco'],
      request.form['situacao'],
      request.form['categoria'],
      datetime.now(),
      nome_imagem,
      session['logado'][0]
    )

    arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], '{}{}'.format(momento, arquivo.filename)))

    produto_id = None

    produto_id = controle_produto.cadastrar(produto)
    
    #if( produto_id is not None and produto_id > 0 ):

  return render_template('vender.html')

@app.route('/reportar-erro/')
def reportarErro():
  if( 'logado' not in session or session['logado'] == None ):
    return redirect(url_for('login'))

  return render_template('erro.html')

@app.route('/ajuda/')
def ajuda():
  return render_template('ajuda.html')