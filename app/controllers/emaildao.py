from app.models.emails import Emails

class EmailDAO():

  def __init__(self, db):
    self.db = db

  
  def cadastrar(self, email: Emails):
    sql = """
    insert into emails
    (email, usuario_id)
    values
    (?, ?);
    """
  
    cursor = self.db.cursor()
    cursor.execute(sql, (
      email.email,
      email.usuario_id)
    )

    self.db.commit()

    return cursor.lastrowid

  def obter(self, id):
    sql = """
    select * from emails
    where id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (id))

    return cursor.fetchone()

  def listar(self):
    sql = """
    select * from emails;
    """

    cursor = self.db.cursor()
    cursor.execute(sql)

    return cursor.fetchall()
  
  def atualizar(self, email: Emails):
    sql = """
    update emails 
    set email = ?
    where id = ? and usuario_id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (
      email.email,
      email.id,
      email.usuario_id)
    )

    self.db.commit()

    return cursor.rowcount
  
  def deletar(self, id):
    sql = """
    delete from emails
    where id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (id))

    self.db.commit()

    return cursor.rowcount 
  