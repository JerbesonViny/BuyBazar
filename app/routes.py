from flask import render_template, request, url_for, redirect, session, flash
from sqlite3.dbapi2 import Error, complete_statement
from datetime import datetime
from app import app
import os, hashlib

from app.models.connection import get_db

from app.models.usuarios import Usuarios
from app.models.telefones import Telefones
from app.models.emails import Emails
from app.models.produtos import Produtos
from app.models.reportarerro import ReportarErro

from app.controllers.usuariodao import UsuarioDAO
from app.controllers.telefonedao import TelefonesDAO
from app.controllers.emaildao import EmailDAO
from app.controllers.produtodao import ProdutosDAO
from app.controllers.reportarerrodao import ReportarErroDAO

# User routes
@app.route('/')
@app.route('/index/')
def index():
  controle_produtos = ProdutosDAO(get_db())
  produtos = controle_produtos.obterUltimos()

  return render_template("index.html", produtos = produtos)
  
@app.route('/login/', methods=["GET", "POST"])
def login():
  if( request.method == "POST" ):
    hash = hashlib.sha512()
    senha = request.form['senha']

    hash.update(senha.encode('utf-8'))
    senha = hash.hexdigest()

    usuario = UsuarioDAO(get_db())
    usuario = usuario.autenticar(
      request.form['email'],
      senha
    )

    if( usuario is not None ):
      session['logado'] = usuario
      
      flash(f'Seja bem vindo(a), {usuario[1]}.', 'info')
      return redirect(url_for('produtos'))
    else:
      flash(f'E-mail e/ou senha incorretos!', 'danger')

  return render_template("login.html")

@app.route('/logout/')
def logout():
  session['logado'] = None
  session.clear()

  flash(f'Logout feito com sucesso!', 'success')
  return redirect(url_for('index'))

@app.route('/sign-up/', methods=["GET", "POST"])
def cadastrarUsuarios():  
  if( request.method == "POST" ):
    controle = UsuarioDAO(get_db())
    controle_telefone = TelefonesDAO(get_db())
    controle_email = EmailDAO(get_db())
    
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    numero_telefone = request.form['telefone']

    usuario_id = None
    if( nome and email and senha and numero_telefone ):
      if( len(numero_telefone) >= 9 ):
        hash = hashlib.sha512()
        hash.update(senha.encode('utf-8'))
        senha = hash.hexdigest()

        usuario = Usuarios(
          request.form['nome'],
          request.form['email'],
          senha
        )
        try:
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
        except:
          flash(f'Alguém já possui esse e-mail, tente novamente com outro!', 'danger')
          return redirect(request.url)
      else: 
        flash(f'Número inválido, certifique-se de ter preenchido corretamente!', 'danger')
        return redirect(request.url)
    else:
      flash(f'Preencha todos os campos!', 'danger')
      return redirect(request.url)

    if( usuario_id is not None and usuario_id > 0 ):
      flash(f'Usuário cadastrado com sucesso!', 'success')
      return redirect(url_for('login'))
    else:
      flash(f'Ocorreu um erro durante o cadastro, tente novamente!', 'danger')
      return redirect(request.url)

  return render_template("register.html")

@app.route('/atualizar-dados/', methods=['GET', 'POST',])
def atualizarDados():
  if( 'logado' not in session ):
    flash('Você não possui permissão!', 'danger')
    return redirect(url_for('login'))

  controle_usuarios = UsuarioDAO(get_db())
  controle_telefones = TelefonesDAO(get_db())
  nome_usuario, telefone_id, telefone = controle_usuarios.obterNomeTelefone(session['logado'][0])
  if( request.method == 'POST' ):
    nome = request.form['nome']
    n_telefone = request.form['telefone']

    if( nome and n_telefone ):
      novo_nome = controle_usuarios.atualizarNome(
        nome,
        session['logado'][0]
      )
      novo_telefone = controle_telefones.atualizar(
        n_telefone,
        telefone_id,
        session['logado'][0]
      )
    
    if( novo_nome > 0 or novo_telefone > 0 ):
      flash('Nome e/ou telefone alterado(s) com sucesso!', 'success')
      return redirect(url_for('produtos'))
    else:
      flash('Ocorreu um erro ao tentar atualizar!', 'danger')
      return redirect(url_for('produtos'))

  
  return render_template('atualizarDados.html', nome_usuario = nome_usuario, telefone = telefone)

@app.route('/atualizar-senha/', methods=['GET', 'POST',])
def atualizarSenha():
  if( 'logado' not in session ):
    flash('Você não possui permissão para isso!', 'danger')
    return redirect(url_for('index'))

  if( request.method == 'POST' ):
    email = request.form['email']
    senha_antiga = request.form['senha']
    nova_senha = request.form['nova_senha']

    hash = hashlib.sha512()
    hash.update(senha_antiga.encode('UTF-8'))
    senha_antiga = hash.hexdigest()

    usuario = None
    if( email and senha_antiga and nova_senha ):
      controle_usuarios = UsuarioDAO(get_db())
      usuario = controle_usuarios.autenticar(
        email,
        senha_antiga
      )
    else:
      flash('Preencha todos os campos!', 'danger')
      return redirect(request.url)

    if( usuario is not None ):
      hash = hashlib.sha512()
      hash.update(nova_senha.encode('UTF-8'))
      nova_senha = hash.hexdigest()

      conta = controle_usuarios.atualizarSenha(
        nova_senha,
        session['logado'][0]
      )
    else:
      flash('E-mail e/ou senha incorretos!', 'danger')
      return redirect(request.url)
    
    if( conta > 0 ):
      flash('Senha alterada!', 'success')
      return redirect(url_for('produtos'))
    else:
      flash('Não foi possível atualizar a senha, verifique os dados!')
      return redirect(request.url)


  return render_template('atualizarSenha.html')

@app.route('/excluir-conta/', methods=['GET', 'POST',])
def excluirConta():
  if( 'logado' not in session ):
    return redirect(url_for('index'))

  if( request.method == 'POST' ):
    controle_usuarios = UsuarioDAO(get_db())
    email = request.form['email']
    senha = request.form['senha']
    
    hash = hashlib.sha512()
    hash.update(senha.encode('UTF-8'))
    senha = hash.hexdigest()

    usuario = None
    if( email and senha ):
      usuario = controle_usuarios.autenticar(
        email,
        senha
      )
    else:
      flash('Preencha todos os campos!', 'danger')

    if( usuario is not None ):
      deleted = controle_usuarios.deletar(session['logado'][0])
      flash('Conta apagada com sucesso!', 'success')
      return redirect(url_for('index'))
    else:
      flash('E-mail e/ou senha incorretos!', 'danger')
      return redirect(request.url)

  return render_template('excluirConta.html')

@app.route('/tirar-vendido/<produto_id>/')
def tirarVendido(produto_id):
  controle_produtos = ProdutosDAO(get_db())
  try:
    produto = controle_produtos.obter_especifico(produto_id)

    if( produto[7] == session['logado'][0] ):
      produto_vendido = controle_produtos.tirarVendido(produto_id)

      if( produto_vendido is not None and produto_vendido > 0 ):
        flash(f'Produto retirado de vendidos com sucesso!', 'success')
        return redirect(url_for('meusItens'))
      else:
        flash(f'Ocorreu um erro durante a retirada de item vendido, tente novamente', 'danger')
        return redirect(url_for('meusItens'))
    else:
      flash(f'Esse produto não é seu!', 'danger')
      return redirect(url_for('meusItens'))
  except Error as err:
    print(err)
    flash(f'Ocorreu um erro, entre em contato com o suporte!', 'danger')
    return redirect(url_for('meusItens'))

@app.route('/declarar-vendido/<produto_id>/')
def declararVendido(produto_id):
  controle_produtos = ProdutosDAO(get_db())
  try:
    produto = controle_produtos.obter_especifico(produto_id)

    if( produto[7] == session['logado'][0] ):
      produto_vendido = controle_produtos.declararVendido(produto_id)

      if( produto_vendido is not None and produto_vendido > 0 ):
        flash(f'Produto declarado como vendido com sucesso!', 'success')
        return redirect(url_for('meusItens'))
      else:
        flash(f'Ocorreu um erro durante a declaração de item vendido, tente novamente', 'danger')
        return redirect(url_for('meusItens'))
    else:
      flash(f'Esse produto não é seu!', 'danger')
      return redirect(url_for('meusItens'))
  except Error as err:
    print(err)
    flash(f'Ocorreu um erro, entre em contato com o suporte!', 'danger')
    return redirect(url_for('meusItens'))

@app.route('/produtos/')
def produtos():
  if( 'logado' not in session or session['logado'] == None ):
    return redirect(url_for('login'))

  controle_produtos = ProdutosDAO(get_db())
  produtos = controle_produtos.listar()
  
  return render_template("mostrarTodos.html", produtos=produtos)

@app.route('/comprar-produto/<produto_id>/')
def comprarProduto(produto_id):
  if( 'logado' not in session or session['logado'] == None ):
    return redirect(url_for('login'))

  controle_telefones = TelefonesDAO(get_db())
  controle_produto = ProdutosDAO(get_db())
  
  produto = controle_produto.obter_especifico(
    produto_id
  )

  telefone = controle_telefones.obter_por_usuario(
    produto[7]
  )
  
  return redirect(f'https://api.whatsapp.com/send?phone={telefone[0]}&text=Desejo comprar este produto: {produto[1]}')

@app.route('/minhas-compras/')
def listaPedidos():
  if( 'logado' not in session or session['logado'] == None ):
    return redirect(url_for('login'))

  return 'List Shopping'

#admin
@app.route('/meus-produtos/')
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
      float(request.form['preco']),
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

@app.route('/atualizar-produto/<produto_id>/', methods=['GET', 'POST', 'PUT',])
def atualizarProduto(produto_id): 
  if( request.method == 'POST' ):
    controle_produto = ProdutosDAO(get_db())
    
    if( request.form['nome'] and request.form['preco'] and request.form['situacao'] and request.form['categoria'] ):
      produto = controle_produto.atualizar(
      request.form['nome'],
      request.form['preco'],
      request.form['situacao'],
      request.form['categoria'],
      produto_id,
      session['logado'][0]
    )

    flash(f'Atualização do produto {produto_id}, feita com sucesso!', 'success')
    return redirect(url_for('meusItens'))

  
  controle_produto = ProdutosDAO(get_db())
  produto = controle_produto.obter_especifico(  
    produto_id
  )

  return render_template('atualizar-produto.html', produto=produto)
  
@app.route('/deletar-produto/<produto_id>/', methods=['GET', 'POST', 'DELETE'])
def deletarProduto(produto_id):
  controle_produtos = ProdutosDAO(get_db())
  produto = controle_produtos.deletar(
    produto_id,
    session['logado'][0]
  )

  if( produto != 0 ):
    flash(f'Produto {produto_id} apagado com sucesso!', 'success')
    return redirect(url_for('meusItens'))

@app.route('/vendidos/')
def vendidos():
  if( 'logado' not in session or session['logado'] == None ):
    return redirect(url_for('login'))

  controle_produtos = ProdutosDAO(get_db())
  produtos = controle_produtos.obterVendidos(session['logado'][0])

  return render_template('vendidos.html', produtos = produtos)

@app.route('/cadastrar-produtos/', methods=["GET", "POST"])
def vender():
  if( 'logado' not in session or session['logado'] == None ):
    return redirect(url_for('login'))

  
  if( request.method == "POST" ):
    arquivo = request.files['arquivos']
    momento = datetime.now()
    nome_imagem = '{}{}'.format(momento, arquivo.filename)

    controle_produto = ProdutosDAO(get_db())

    produto_id = None
    if( request.form['nome'] and request.form['preco'] and request.form['situacao'] and request.form['categoria'] and momento and request.files['arquivos'] ):
      produto = Produtos(
        request.form['nome'],
        request.form['preco'],
        request.form['situacao'],
        request.form['categoria'],
        momento,
        nome_imagem,
        session['logado'][0]
      )

      arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], '{}{}'.format(momento, arquivo.filename)))
      produto_id = controle_produto.cadastrar(
        produto
      )
    
      if( produto_id is not None and produto_id > 0 ):
        flash(f'Produto cadastrado com sucesso!', 'success')
        
        return redirect(request.url)
      else:
        flash(f'Tente novamente mais tarde! Caso o erro volte a acontecer, entre em contato com o suporte!', 'danger')
    else:
      flash(f'Preencha todos os campos!', 'danger')
      return redirect(request.url)
    

  return render_template('vender.html')

@app.route('/reportar-erro/', methods=['GET', 'POST',])
def reportarErro():
  if( 'logado' not in session or session['logado'] == None ):
    return redirect(url_for('login'))

  if( request.method == 'POST' ):
    controle_erros = ReportarErroDAO(get_db())
    erro = request.form['erro']

    if( erro ):
      erros = ReportarErro(
        erro,
        session['logado'][0]
      )

      resultado = controle_erros.cadastrar(
        erros
      )

      if( resultado is not None and resultado > 0 ):
        flash(f'O problema foi mandado para a assistência técnica!\nObrigado pelo feedback!', 'success')
        return redirect(request.url)
      else:
        flash(f'Ocorreu um erro ao tentar reportar um erro!', 'danger')
        return redirect(request.url)
    else:
      flash(f'Preencha todos os campos!', 'danger')
      return redirect(request.url)

  return render_template('erro.html')

@app.route('/ajuda/')
def ajuda():
  return render_template('ajuda.html')

@app.route('/resultados/', methods=['GET', 'POST',])
def buscar_produtos():
  controle_produtos = ProdutosDAO(get_db())

  produtos = controle_produtos.obterPorNome(
    request.form['buscar']
  )

  return render_template('mostrarTodos.html', produtos = produtos)

@app.route('/resultado-vendidos/', methods=['GET', 'POST',])
def buscar_vendidos():
  controle_produtos = ProdutosDAO(get_db())

  """
  situação: {
    0 - Não vendido
    1 - Vendido
  }
  """
  produtos = controle_produtos.obterPorNomeUsuario(
    request.form['buscar'],
    session['logado'][0],
    1
  )

  return render_template('vendidos.html', produtos = produtos)

@app.route('/resultado-meus-itens/', methods=['GET', 'POST',])
def buscar_meus_itens():
  controle_produtos = ProdutosDAO(get_db())
  """
  situação: {
    0 - Não vendido
    1 - Vendido
  }
  """
  produtos = controle_produtos.obterPorNomeUsuario(
    request.form['buscar'],
    session['logado'][0],
    0
  )

  return render_template('listarItens.html', produtos = produtos)