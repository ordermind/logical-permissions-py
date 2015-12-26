from logical_permissions.interfaces.LogicalPermissionsBase import LogicalPermissionsBase

class LogicalPermissions(LogicalPermissionsBase):
  
  def __init__(self):
    self.__types = {}
    self.__bypass_callback = None

  def addType(self, name, callback):
    if(type(name) is not str):
      
  
  def removeType(self, name):
    pass 
    
  def typeExists(self, name):
    pass 

  def getTypeCallback(self, name):
    pass

  def getTypes(self):
    pass

  def setTypes(self, types):
    pass
  
  def getBypassCallback(self):
    pass 
    
  def setBypassCallback(self, callback):
    pass 

  def checkAccess(self, permissions, context):
    pass
  
  def __checkBypassAccess(self, context):
    pass
  
  def __dispatch(self, permissions, context, type = None):
    pass
  
  def __processAND(self, permissions, context, type = None):
    pass
  
  def __processNAND(self, permissions, context, type = None):
    pass
  
  def __processOR(self, permissions, context, type = None):
    pass
  
  def __processNOR(self, permissions, context, type = None):
    pass
  
  def __processXOR(self, permissions, context, type = None):
    pass
  
  def __processNOT(self, permissions, context, type = None):
    pass
  
  def __externalAccessCheck(self, permission, context, type):
    pass
