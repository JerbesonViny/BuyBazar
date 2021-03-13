from app.models.telefones import Telefones

class TelefonesDAO():

  def __init__(self, db):
    self.db = db

  
  def cadastrar(self, telefone: Telefones):
    sql = """
    insert into telefones
    (numero, usuario_id)
    values
    (?, ?);
    """
  
    cursor = self.db.cursor()
    cursor.execute(sql, (
      telefone.numero,
      telefone.usuario_id)
    )

    self.db.commit()

    return cursor.lastrowid

  def obter(self, id):
    sql = """
    select * from telefones
    where id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (id,))

    return cursor.fetchone()

  def obter_por_usuario(self, usuario_id):
    sql = """
    select numero from telefones
    where usuario_id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (usuario_id,))

    return cursor.fetchone()

  def listar(self):
    sql = """
    select * from telefones;
    """

    cursor = self.db.cursor()
    cursor.execute(sql)

    return cursor.fetchall()
  
  def atualizar(self, telefone, telefone_id, usuario_id):
    sql = """
    update telefones 
    set numero = ?
    where id = ? and usuario_id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (
      telefone, 
      telefone_id, 
      usuario_id,
    ))

    self.db.commit()

    return cursor.rowcount
  
  def deletar(self, id):
    sql = """
    delete from telefones
    where id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (id))

    self.db.commit()

    return cursor.rowcount 
  