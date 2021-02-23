from app.models.produtos import Produtos

class ProdutosDAO():

  def __init__(self, db):
    self.db = db

  
  def cadastrar(self, produtos: Produtos):
    sql = """
    insert into produtos
    (nome, preco, situacao, descricao, data_pub, usuario_id)
    values
    (?, ?, ?, ?, ? ,?);
    """
  
    cursor = self.db.cursor()
    cursor.execute(sql, (
      produtos.nome,
      produtos.preco,
      produtos.situacao,
      produtos.descricao,
      produtos.data_pub,
      produtos.usuario_id)
    )

    self.db.commit()

    return cursor.lastrowid

  def obter(self, id):
    sql = """
    select * from produtos
    where id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (id))

    return cursor.fetchone()

  def listar(self):
    sql = """
    select * from produtos;
    """

    cursor = self.db.cursor()
    cursor.execute(sql)

    return cursor.fetchall()
  
  def atualizar(self, produtos: Produtos):
    sql = """
    update produtos
    set nome = ?, preco = ?, situacao = ?, descricao = ?, data_pub = ?
    where id = ? and usuario_id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (
      produtos.nome,
      produtos.preco,
      produtos.situacao,
      produtos.descricao,
      produtos.data_pub,
      produtos.id,
      produtos.usuario_id)
    )

    self.db.commit()

    return cursor.rowcount
  
  def deletar(self, id):
    sql = """
    delete from produtos
    where id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (id))

    self.db.commit()

    return cursor.rowcount 
  