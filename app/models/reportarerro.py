class ReportarErro():

  def __init__(self, erro, usuario_id):
    self.id = 0
    self.erro = erro
    self.usuario_id = usuario_id

  def getId(self):
    return self._id
  
  def setId(self, id):
    self._id = id
  
  def getUsuarioId(self):
    return self._usuario_id
  
  def setUsuarioId(self, usuario_id):
    self._usuario_id = usuario_id
  
  id = property(
    fget=getId,
    fset=setId
  )

  usuario_id = property(
    fget=getUsuarioId,
    fset=setUsuarioId
  )