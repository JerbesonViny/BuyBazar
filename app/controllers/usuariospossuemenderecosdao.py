from app.models.usuarios_possuem_enderecos import UsuariosPossuemEnderecos

class requisicaoDAO():

  def __init__(self, db):
    self.db = db

  
  def cadastrar(self, requisicao: UsuariosPossuemEnderecos):
    sql = """
    insert into usuarios_possuem_enderecos
    (usuario_id, endereco_id)
    values
    (? ,?);
    """
  
    cursor = self.db.cursor()
    cursor.execute(sql, (
      requisicao.usuario_id,
      requisicao.endereco_id)
    )

    self.db.commit()

    return cursor.lastrowid

  def obter(self, id):
    sql = """
    select * from usuarios_possuem_enderecos
    where id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (id))

    return cursor.fetchone()

  def listar(self):
    sql = """
    select * from usuarios_possuem_enderecos;
    """

    cursor = self.db.cursor()
    cursor.execute(sql)

    return cursor.fetchall()
  
  def atualizar(self, requisicao: UsuariosPossuemEnderecos):
    sql = """
    update usuarios_possuem_enderecos
    set endereco_id = ?
    where id = ? and usuario_id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (
      requisicao.endereco_id,
      requisicao.id,
      requisicao.usuario_id)
    )

    self.db.commit()

    return cursor.rowcount
  
  def deletar(self, id):
    sql = """
    delete from usuarios_possuem_enderecos
    where id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (id))

    self.db.commit()

    return cursor.rowcount 
  