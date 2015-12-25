import abc

class LogicalPermissionsBase(metaclass=abc.ABCMeta):

  __metaclass__ = abc.ABCMeta
  
  @abc.abstractmethod
  def addType(self, name, callback):
    pass
  
  @abc.abstractmethod
  def removeType(self, name):
    pass 
    
  @abc.abstractmethod
  def typeExists(self, name):
    pass 

  @abc.abstractmethod
  def getTypeCallback(self, name):
    pass

  @abc.abstractmethod
  def getTypes(self):
    pass

  @abc.abstractmethod
  def setTypes(self, types):
    pass
  
  @abc.abstractmethod
  def getBypassCallback(self):
    pass 
    
  @abc.abstractmethod
  def setBypassCallback(self, callback):
    pass 

  @abc.abstractmethod
  def checkAccess(self, permissions, context):
    pass


