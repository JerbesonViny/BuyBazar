class PedidosPossuemProdutos():

  def __init__(self, pedido_id, produto_id):
    self.id = 0
    self.pedido_id = pedido_id
    self.produto_id = produto_id

  def getId(self):
    return self._id 

  def setId(self, id):
    self._id = id

  def getPedidoId(self):
    return self._pedido_id

  def setPedidoId(self, pedido_id):
    self._pedido_id = pedido_id

  def getProdutoId(self):
    return self._produto_id

  def setProdutoId(self, produto_id):
    self._produto_id = produto_id

  id = property(fget=getId, fset=setId)
  pedido_id = property(fget=getPedidoId, fset=setPedidoId)
  produto_id = property(fget=getProdutoId, fset=setProdutoId)