from logical_permissions.interfaces.LogicalPermissionsBase import LogicalPermissionsBase

class LogicalPermissions(LogicalPermissionsBase):

  def addType(self, name, callback):
    return
  
  def removeType(self, name):
    return 
    
  def typeExists(self, name):
    return 

  def getTypeCallback(self, name):
    return

  def getTypes(self):
    return

  def setTypes(self, types):
    return
  
  def getBypassCallback(self):
    return 
    
  def setBypassCallback(self, callback):
    return 

  def checkAccess(self, permissions, context):
    return
