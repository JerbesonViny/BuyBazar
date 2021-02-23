from app.models.pedidos import Pedidos

class pedidoDAO():

  def __init__(self, db):
    self.db = db

  
  def cadastrar(self, pedido: Pedidos):
    sql = """
    insert into pedidos
    (data_compra, usuario_id)
    values
    (? ,?);
    """
  
    cursor = self.db.cursor()
    cursor.execute(sql, (
      pedido.data_compra,
      pedido.usuario_id)
    )

    self.db.commit()

    return cursor.lastrowid

  def obter(self, id):
    sql = """
    select * from pedidos
    where id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (id))

    return cursor.fetchone()

  def listar(self):
    sql = """
    select * from pedidos;
    """

    cursor = self.db.cursor()
    cursor.execute(sql)

    return cursor.fetchall()
  
  def atualizar(self, pedido: Pedidos):
    sql = """
    update pedidos
    set data_compra = ?
    where id = ? and usuario_id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (
      pedido.data_compra,
      pedido.id,
      pedido.usuario_id)
    )

    self.db.commit()

    return cursor.rowcount
  
  def deletar(self, id):
    sql = """
    delete from pedidos
    where id = ?;
    """

    cursor = self.db.cursor()
    cursor.execute(sql, (id))

    self.db.commit()

    return cursor.rowcount 
  