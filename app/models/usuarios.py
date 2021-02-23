class Usuarios():

  def __init__(self, nome, login, senha):
    self.id = 0
    self.nome = nome
    self.login = login
    self.senha = senha

  def getId(self):
    return self._id
  
  def setId(self, id):
    self._id = id

  id = property(fget=getId, fset=setId)
