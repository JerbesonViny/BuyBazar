class Demanda_Has_Produtos():
  def __init__(self, demandas_id, produtos_id):
    self.id = 0
    self.demandas_id = demandas_id
    self.produtos_id = produtos_id

  def getId(self):
    return self._id 

  def setId(self, id):
    self._id = id

  def getDemandasId(self):
    return self._demandas_id

  def setDemandasId(self, demandas_id):
    self._demandas_id = demandas_id

  def getProdutosId(self):
    return self._produtos_id

  def setProdutosId(self, produtos_id):
    self._produtos_id = produtos_id

  id = property(fget=getId, fset=setId)
  demandas_id = property(fget=getDemandasId, fset=setDemandasId)
  produtos_id = property(fget=getProdutosId, fset=setProdutosId)