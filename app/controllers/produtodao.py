from app.models.produtos import Produtos

class ProdutosDAO():

  def __init__(self, db):
    self.db = db

  
  def cadastrar(self, produtos: Produtos):
    sql = """
    insert into produtos
    (nome, preco, situacao, categoria, data_pub, nome_imagem, usuario_id)
    values
    (?, ?, ?, ?, ? , ?, ?);
    """
  
    cursor = self.db.cursor()
    cursor.execute(sql, (
      produtos.nome,
      produtos.preco,
      produtos.situacao,
      produtos.categoria,
      produtos.data_pub,
      produtos.nome_imagem,
      produtos.usuario_id)
    )

    self.db.commit()

    return cursor.lastrowid

  def obter(self, id):
    sql = """
    select * from produtos
    where usuario_id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (id,))

    return cursor.fetchall()

  def obter_especifico(self, id):
    sql = """
    select * from produtos
    where id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (id,))

    return cursor.fetchone()

  def listar(self):
    sql = """
    select * from produtos;
    """

    cursor = self.db.cursor()
    cursor.execute(sql)

    return cursor.fetchall()
  
  def atualizar(self, nome, preco, situacao, categoria, produto_id, usuario_id):
    sql = """
    update produtos
    set nome = ?, preco = ?, situacao = ?, categoria = ?
    where id = ? and usuario_id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (
      nome,
      preco,
      situacao,
      categoria,
      produto_id,
      usuario_id)
    )

    self.db.commit()

    return cursor.rowcount
  
  def deletar(self, id, usuario_id):
    sql = """
    delete from produtos
    where id = ? and usuario_id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (
      id,
      usuario_id)
    )

    self.db.commit()

    return cursor.rowcount 
  
  def obterUltimos(self):
    sql = """
    select nome_imagem, nome
    from produtos 
    order by data_pub desc 
    limit 6;
    """

    cursor = self.db.cursor()
    cursor.execute(sql)

    return cursor.fetchall()

  def obterPorNome(self, nome):
    sql = """
    select * from produtos
    where nome like ?;
    """
    
    cursor = self.db.cursor()
    cursor.execute(sql, (nome,))

    return cursor.fetchall()

  def obterVendidos(self, usuario_id):
    sql = """
    select produtos
    """