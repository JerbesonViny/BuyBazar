from app.models.reportarerro import ReportarErro

class ReportarErroDAO():

  def __init__(self, db):
    self.db = db
  
  def listar(self):
    sql = """
    select * from erros;
    """

    cursor = self.db.cursor()
    cursor.execute(sql)

    return cursor.fetchall()

  def cadastrar(self, erro: ReportarErro):
    sql = """
    insert into erros
    (erro, usuario_id)
    values
    (?, ?);
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (erro.erro, erro.usuario_id,))

    self.db.commit()

    return cursor.lastrowid
  