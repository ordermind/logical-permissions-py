from logical_permissions.interfaces.LogicalPermissionsBase import LogicalPermissionsBase
from logical_permissions.exceptions import *
import copy

class LogicalPermissions(LogicalPermissionsBase):
  
  def __init__(self):
    self.__types = {}
    self.__bypass_callback = None

  def addType(self, name, callback):
    if not isinstance(name, str):
      raise InvalidArgumentTypeException('The name parameter must be a string.')
    if not name:
      raise InvalidArgumentValueException('The name parameter cannot be empty.')
    if not hasattr(callback, '__call__'):
      raise InvalidArgumentTypeException('The callback parameter must be a callable data type.')

    types = self.getTypes()
    types[name] = callback
    self.setTypes(types = types)
  
  def removeType(self, name):
    if not isinstance(name, str):
      raise InvalidArgumentTypeException('The name parameter must be a string.')
    if not name:
      raise InvalidArgumentValueException('The name parameter cannot be empty.')
    if not self.typeExists(name = name):
      raise PermissionTypeNotRegisteredException('The permission type "{0}" has not been registered. Please use LogicalPermissions::addType() or LogicalPermissions::setTypes() to register permission types.'.format(name))
    
    types = self.getTypes()
    types.pop(name, None)
    self.setTypes(types = types)
    
  def typeExists(self, name):
    if not isinstance(name, str):
      raise InvalidArgumentTypeException('The name parameter must be a string.')
    if not name:
      raise InvalidArgumentValueException('The name parameter cannot be empty.')

    types = self.getTypes()
    return name in types

  def getTypeCallback(self, name):
    if not isinstance(name, str):
      raise InvalidArgumentTypeException('The name parameter must be a string.')
    if not name:
      raise InvalidArgumentValueException('The name parameter cannot be empty.')
    if not self.typeExists(name = name):
      raise PermissionTypeNotRegisteredException('The permission type "{0}" has not been registered. Please use LogicalPermissions::addType() or LogicalPermissions::setTypes() to register permission types.'.format(name))
    
    types = self.getTypes()
    return types[name]

  def getTypes(self):
    return copy.copy(self.__types)

  def setTypes(self, types):
    if not isinstance(types, dict):
      raise InvalidArgumentTypeException('The types parameter must be a dictionary.')
    for name in types:
      if not isinstance(name, str):
        raise InvalidArgumentValueException('The types keys must be strings.')
      if not name:
        raise InvalidArgumentValueException('The name parameter cannot be empty.')
      if not hasattr(types[name], '__call__'):
        raise InvalidArgumentValueException('The types callbacks must be callables.')

    self.__types = copy.copy(types)
  
  def getBypassCallback(self):
    return self.__bypass_callback
    
  def setBypassCallback(self, callback):
    if not hasattr(callback, '__call__'):
      raise InvalidArgumentTypeException('The callback parameter must be a callable data type.')
    
    self.__bypass_callback = callback

  def checkAccess(self, permissions, context):
    if not isinstance(permissions, dict):
      raise InvalidArgumentTypeException('The permissions parameter must be a dictionary.')
    if not isinstance(context, dict):
      raise InvalidArgumentTypeException('The context parameter must be an dictionary.')
    
    access = False
    allow_bypass = True
    permissions_copy = copy.deepcopy(permissions)
    if 'no_bypass' in permissions_copy:
      if isinstance(permissions_copy['no_bypass'], bool):
        allow_bypass = not permissions_copy['no_bypass']
      elif isinstance(permissions_copy['no_bypass'], dict):
        allow_bypass = not self.__dispatch(permissions = permissions_copy['no_bypass'], context = context)
      else:
        raise InvalidArgumentValueException('The no_bypass value must be a boolean or a dictionary. Current value: {0}'.format(permissions_copy['no_bypass']))
      permissions_copy.pop('no_bypass', None)
    if allow_bypass and self.__checkBypassAccess(context = context):
      access = True
    else:
      if permissions_copy:
        access = self.__processOR(permissions = permissions_copy, context = context)
    return access
  
  def __checkBypassAccess(self, context):
    bypass_access = False
    bypass_callback = self.getBypassCallback()
    if hasattr(bypass_callback, '__call__'):
      bypass_access = bypass_callback(context)
    return bypass_access
  
  def __dispatch(self, permissions, context, type = None):
    access = False
    if permissions:
      if isinstance(permissions, str):
        access = self.__externalAccessCheck(permission = permissions, context = context, type = type)
      elif isinstance(permissions, list):
        if len(permissions) > 0:
          access = self.__processOR(permissions = permissions, context = context, type = type)
      elif isinstance(permissions, dict):
        if len(permissions) == 1:
          key = list(permissions.keys())[0]
          value = permissions[key]
          if key is 'AND':
            access = self.__processAND(permissions = value, context = context, type = type)
          elif key is 'NAND':
            access = self.__processNAND(permissions = value, context = context, type = type)
          elif key is 'OR':
            access = self.__processOR(permissions = value, context = context, type = type)
          elif key is 'NOR':
            access = self.__processNOR(permissions = value, context = context, type = type)
          elif key is 'XOR':
            access = self.__processXOR(permissions = value, context = context, type = type)
          elif key is 'NOT':
            access = self.__processNOT(permissions = value, context = context, type = type)
          else:
            if 'long' not in globals(): # Python 3 compability
              long = int
            if not isinstance(key, (int, long, float)):
              if type is None:
                type = key
              else:
                raise InvalidArgumentValueException('You cannot put a permission type as a descendant to another permission type. Existing type: {0}. Evaluated permissions: {1}'.format(type, permissions))
            if isinstance(value, (dict, list)):
              access = self.__processOR(permissions = value, context = context, type = type)
            else:
              access = self.__dispatch(permissions = value, context = context, type = type)
        elif len(permissions) > 1:
          access = self.__processOR(permissions = permissions, context = context, type = type)
      else:
        raise InvalidArgumentTypeException('Permissions must either be a string, a dictionary or a list. Evaluated permissions: {0}'.format(permissions))
    return access
  
  def __processAND(self, permissions, context, type = None):
    access = False
    if isinstance(permissions, list):
      if len(permissions) < 1:
        raise InvalidValueForLogicGateException('The value list of an AND gate must contain a minimum of one element. Current value: {0}'.format(permissions))
      
      access = True
      for permission in permissions:
        access = access and self.__dispatch(permissions = permission, context = context, type = type)
        if not access:
          break
    elif isinstance(permissions, dict):
      if len(permissions) < 1:
        raise InvalidValueForLogicGateException('The value dict of an AND gate must contain a minimum of one element. Current value: {0}'.format(permissions))
      
      access = True
      for key in permissions:
        subpermissions = {key: permissions[key]}
        access = access and self.__dispatch(permissions = subpermissions, context = context, type = type)
        if not access:
          break
    else:
      raise InvalidValueForLogicGateException('The value of an AND gate must be a list or a dict. Current value: {0}'.format(permissions))
    return access
  
  def __processNAND(self, permissions, context, type = None):
    if isinstance(permissions, list):
      if len(permissions) < 1:
        raise InvalidValueForLogicGateException('The value list of a NAND gate must contain a minimum of one element. Current value: {0}'.format(permissions))
    elif isinstance(permissions, dict):
      if len(permissions) < 1:
        raise InvalidValueForLogicGateException('The value dict of a NAND gate must contain a minimum of one element. Current value: {0}'.format(permissions))
    else:
      raise InvalidValueForLogicGateException('The value of a NAND gate must be a list or a dict. Current value: {0}'.format(permissions))
    
    access = not self.__processAND(permissions = permissions, context = context, type = type)
    return access
  
  def __processOR(self, permissions, context, type = None):
    access = False
    if isinstance(permissions, list):
      if len(permissions) < 1:
        raise InvalidValueForLogicGateException('The value list of an OR gate must contain a minimum of one element. Current value: {0}'.format(permissions))

      for permission in permissions:
        access = access or self.__dispatch(permissions = permission, context = context, type = type)
        if access:
          break
    elif isinstance(permissions, dict):
      if len(permissions) < 1:
        raise InvalidValueForLogicGateException('The value dict of an OR gate must contain a minimum of one element. Current value: {0}'.format(permissions))

      for key in permissions:
        subpermissions = {key: permissions[key]}
        access = access or self.__dispatch(permissions = subpermissions, context = context, type = type)
        if access:
          break
    else:
      raise InvalidValueForLogicGateException('The value of an OR gate must be a list or a dict. Current value: {0}'.format(permissions))
    return access
  
  def __processNOR(self, permissions, context, type = None):
    if isinstance(permissions, list):
      if len(permissions) < 1:
        raise InvalidValueForLogicGateException('The value list of a NOR gate must contain a minimum of one element. Current value: {0}'.format(permissions))
    elif isinstance(permissions, dict):
      if len(permissions) < 1:
        raise InvalidValueForLogicGateException('The value dict of a NOR gate must contain a minimum of one element. Current value: {0}'.format(permissions))
    else:
      raise InvalidValueForLogicGateException('The value of a NOR gate must be a list or a dict. Current value: {0}'.format(permissions))
    
    access = not self.__processOR(permissions = permissions, context = context, type = type)
    return access
  
  def __processXOR(self, permissions, context, type = None):
    access = False
    count_true = 0
    count_false = 0
    if isinstance(permissions, list):
      if len(permissions) < 2:
        raise InvalidValueForLogicGateException('The value list of an XOR gate must contain a minimum of two elements. Current value: {0}'.format(permissions))
      
      for permission in permissions:
        this_access = self.__dispatch(permissions = permission, context = context, type = type)
        if this_access:
          count_true += 1
        else:
          count_false += 1
        if count_true > 0 and count_false > 0:
          access = True
          break
    elif isinstance(permissions, dict):
      if len(permissions) < 2:
        raise InvalidValueForLogicGateException('The value dict of an XOR gate must contain a minimum of two elements. Current value: {0}'.format(permissions))
      
      for key in permissions:
        subpermissions = {key: permissions[key]}
        this_access = self.__dispatch(permissions = subpermissions, context = context, type = type)
        if this_access:
          count_true += 1
        else:
          count_false += 1
        if count_true > 0 and count_false > 0:
          access = True
          break
    else:
      raise InvalidValueForLogicGateException('The value of an XOR gate must be a list or a dict. Current value: {0}'.format(permissions))
    return access
  
  def __processNOT(self, permissions, context, type = None):
    if isinstance(permissions, dict):
      if len(permissions) != 1:
        raise InvalidValueForLogicGateException('A NOT permission must have exactly one child in the value dict. Current value: {0}'.format(permissions))
    elif isinstance(permissions, str):
      if not permissions:
        raise InvalidValueForLogicGateException('A NOT permission cannot have an empty string as its value.')
    else:
      raise InvalidValueForLogicGateException('The value of a NOT gate must either be a dict or a string. Current value: {0}'.format(permissions))
    
    access = not self.__dispatch(permissions = permissions, context = context, type = type)
    return access
  
  def __externalAccessCheck(self, permission, context, type):
    if not self.typeExists(type):
      raise PermissionTypeNotRegisteredException('The permission type "{0}" has not been registered. Please use LogicalPermissions::addType() or LogicalPermissions::setTypes() to register permission types.'.format(type))
    access = False
    callback = self.getTypeCallback(type)
    if hasattr(callback, '__call__'):
      access = callback(permission, context)
    return access
