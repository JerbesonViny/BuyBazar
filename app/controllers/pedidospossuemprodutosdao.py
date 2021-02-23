from app.models.pedidos_possuem_produtos import PedidosPossuemProdutos

class pedidoDAO():

  def __init__(self, db):
    self.db = db

  
  def cadastrar(self, pedido: PedidosPossuemProdutos):
    sql = """
    insert into pedidos_possuem_produtos
    (pedido_id, produto_id)
    values
    (? ,?);
    """
  
    cursor = self.db.cursor()
    cursor.execute(sql, (
      pedido.pedido_id,
      pedido.produto_id)
    )

    self.db.commit()

    return cursor.lastrowid

  def obter(self, id):
    sql = """
    select * from pedidos_possuem_produtos
    where id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (id))

    return cursor.fetchone()

  def listar(self):
    sql = """
    select * from pedidos_possuem_produtos;
    """

    cursor = self.db.cursor()
    cursor.execute(sql)

    return cursor.fetchall()
  
  def atualizar(self, pedido: PedidosPossuemProdutos):
    sql = """
    update pedidos_possuem_produtos
    set produto_id = ?
    where id = ? and pedido_id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (
      pedido.produto_id,
      pedido.id,
      pedido.pedido_id)
    )

    self.db.commit()

    return cursor.rowcount
  
  def deletar(self, id):
    sql = """
    delete from pedidos_possuem_produtos
    where id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (id))

    self.db.commit()

    return cursor.rowcount 
  