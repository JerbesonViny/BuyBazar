class Produtos():

  def __init__(self, nome, preco, situacao, categoria, data_pub, nome_imagem, usuario_id):
    self.id = 0
    self.nome = nome
    self.categoria = categoria
    self.preco = preco
    self.situacao = situacao
    self.data_pub = data_pub
    self.nome_imagem = nome_imagem
    self.usuario_id = usuario_id

  def getId(self):
    return self._id 

  def setId(self, id):
    self._id = id

  def getUsuarioId(self):
    return self._usuario_id

  def setUsuarioId(self, usuario_id):
    self._usuario_id = usuario_id

  id = property(fget=getId, fset=setId)
  usuario_id = property(fget=getUsuarioId, fset=setUsuarioId)