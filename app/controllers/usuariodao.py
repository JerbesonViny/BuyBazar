from app.models.usuarios import Usuarios

class UsuarioDAO():

  def __init__(self, db):
    self.db = db

  
  def cadastrar(self, usuario: Usuarios):
    sql = """
    insert into usuarios
    (nome, log_in, senha)
    values
    (?, ?, ?);
    """
  
    cursor = self.db.cursor()
    cursor.execute(sql, (
      usuario.nome, 
      usuario.login, 
      usuario.senha)
    )

    self.db.commit()

    return cursor.lastrowid

  def obter(self, id):
    sql = """
    select * from usuarios
    where id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (id,))

    return cursor.fetchone()
  
  def autenticar(self, email, senha):
    sql = """
    select * from usuarios
    where log_in = ? and senha = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (email, senha,))

    return cursor.fetchone()

  def listar(self):
    sql = """
    select * from usuarios;
    """

    cursor = self.db.cursor()
    cursor.execute(sql)

    return cursor.fetchall()
  
  def atualizarNome(self, nome, usuario_id):
    sql = """
    update usuarios
    set nome = ?
    where id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (nome, usuario_id))

    self.db.commit()

    return cursor.rowcount
  
  def deletar(self, id):
    sql = """
    delete from usuarios
    where id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (id,))

    self.db.commit()

    return cursor.rowcount 
  
  def obterNomeTelefone(self, usuario_id):
    sql = """
    select usuarios.nome, telefones.id, telefones.numero
    from usuarios
    join telefones
    on telefones.usuario_id = usuarios.id
    where usuarios.id = ?;
    """
  
    cursor = self.db.cursor()
    cursor.execute(sql, (usuario_id,))

    return cursor.fetchone()

  def atualizarSenha(self, nova_senha, usuario_id):
    sql = """
    update usuarios
    set senha = ?
    where id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (
      nova_senha,
      usuario_id
    ))

    self.db.commit()

    return cursor.rowcount