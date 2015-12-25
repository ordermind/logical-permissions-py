from logical_permissions.interfaces.LogicalPermissionsBase import LogicalPermissionsBase

class LogicalPermissions(LogicalPermissionsBase):

  def addType(self, name, callback):
    pass
  
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
  
  def __dispatch(self, permissions, type = None, context):
    pass
  
  def __processAND(self, permissions, type = None, context):
    pass
  
  def __processNAND(self, permissions, type = None, context):
    pass
  
  def __processOR(self, permissions, type = None, context):
    pass
  
  def __processNOR(self, permissions, type = None, context):
    pass
  
  def __processXOR(self, permissions, type = None, context):
    pass
  
  def __processNOT(self, permissions, type = None, context):
    pass
  
  def __externalAccessCheck(self, permission, type, context):
    pass
