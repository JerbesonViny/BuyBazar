class UsuariosPossuemEnderecos():

  def __init__(self, endereco_id, usuario_id):
    self.id = 0
    self.endereco_id = endereco_id
    self.usuario_id = usuario_id

  def getId(self):
    return self._id

  def setId(self, id):
    self._id = id
  
  def getEnderecoId(self):
    return self.endereco_id
   
  def setEnderecoId(self, endereco_id):
    self.endereco_id = endereco_id
  
  def getUsuarioId(self):
    return self.usuario_id
  
  def setUsuarioId(self, usuario_id):
    self.usuario_id = usuario_id
  
  id = property(fget=getId, fset=setId)
  endereco_id = property(fget=getEnderecoId, fset=setEnderecoId)
  usuario_id = property(fget=getUsuarioId, fset=setUsuarioId)