class Enderecos():

  def __init__(self, cidade, rua, bairro, numero_casa):
    self.id = 0
    self.cidade = cidade
    self.rua = rua
    self.bairro = bairro
    self.numero_casa = numero_casa

  def getId(self):
    return self._id
  
  def setId(self, id):
    self._id = id
  
  id = property(fget=getId, fset=setId)