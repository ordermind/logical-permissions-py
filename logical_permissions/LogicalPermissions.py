from logical_permissions.exceptions import *
import copy

class LogicalPermissions(object):

  def __init__(self):
    self.__types = {}
    self.__bypass_callback = None

  def addType(self, name, callback):
    """Adds a permission type.

    Args:
      name: A string with the name of the permission type
      callback: The callback that evaluates the permission type. Upon calling checkAccess() the registered callback will be passed two parameters: a permission string (such as a role) and the context dictionary passed to checkAccess(). The permission will always be a single string even if for example multiple roles are accepted. In that case the callback will be called once for each role that is to be evaluated. The callback should return a boolean which determines whether access should be granted.

    """
    if not isinstance(name, str):
      raise InvalidArgumentTypeException('The name parameter must be a string.')
    if not name:
      raise InvalidArgumentValueException('The name parameter cannot be empty.')
    if name in self.__getCorePermissionKeys():
      raise InvalidArgumentValueException('The name parameter has the illegal value "{0}". It cannot be one of the following values: {1}'.format(name, ','.join(self.__getCorePermissionKeys())))
    if self.typeExists(name = name):
      raise PermissionTypeAlreadyExistsException('The type "{0}" already exists! If you want to change the callback for an existing type, please use LogicalPermissions:setTypeCallback().'.format(name))
    if not hasattr(callback, '__call__'):
      raise InvalidArgumentTypeException('The callback parameter must be a callable data type.')

    types = self.getTypes()
    types[name] = callback
    self.setTypes(types = types)

  def removeType(self, name):
    """Removes a permission type.

    Args:
      name: A string with the name of the permission type

    """
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
    """Checks whether a permission type is registered.

    Args:
      name: A string with the name of the permission type

    Returns:
      True if the type is found or False if the type isn't found.

    """
    if not isinstance(name, str):
      raise InvalidArgumentTypeException('The name parameter must be a string.')
    if not name:
      raise InvalidArgumentValueException('The name parameter cannot be empty.')

    types = self.getTypes()
    return name in types

  def getTypeCallback(self, name):
    """Gets the callback for a permission type.

    Args:
      name: A string with the name of the permission type

    Returns:
      Callback for the permission type.

    """
    if not isinstance(name, str):
      raise InvalidArgumentTypeException('The name parameter must be a string.')
    if not name:
      raise InvalidArgumentValueException('The name parameter cannot be empty.')
    if not self.typeExists(name = name):
      raise PermissionTypeNotRegisteredException('The permission type "{0}" has not been registered. Please use LogicalPermissions::addType() or LogicalPermissions::setTypes() to register permission types.'.format(name))

    types = self.getTypes()
    return types[name]

  def setTypeCallback(self, name, callback):
    """Changes the callback for an existing permission type.

    Args:
      name: A string with the name of the permission type
      callback: The callback that evaluates the permission type. Upon calling checkAccess() the registered callback will be passed two parameters: a permission string (such as a role) and the context dictionary passed to checkAccess(). The permission will always be a single string even if for example multiple roles are accepted. In that case the callback will be called once for each role that is to be evaluated. The callback should return a boolean which determines whether access should be granted.

    """
    if not isinstance(name, str):
      raise InvalidArgumentTypeException('The name parameter must be a string.')
    if not name:
      raise InvalidArgumentValueException('The name parameter cannot be empty.')
    if not self.typeExists(name = name):
      raise PermissionTypeNotRegisteredException('The permission type "{0}" has not been registered. Please use LogicalPermissions::addType() or LogicalPermissions::setTypes() to register permission types.'.format(name))
    if not hasattr(callback, '__call__'):
      raise InvalidArgumentTypeException('The callback parameter must be a callable data type.')

    types = self.getTypes()
    types[name] = callback
    self.setTypes(types = types)

  def getTypes(self):
    """Gets all defined permission types.

    Returns:
      A dictionary of permission types with the structure {name: callback, name2: callback2, ...}. This dictionary is shallow copied.

    """
    return copy.copy(self.__types)

  def setTypes(self, types):
    """Overwrites all defined permission types.

    Args:
      types: A dictionary of permission types with the structure {name: callback, name2: callback2, ...}. This dictionary is shallow copied.

    """
    if not isinstance(types, dict):
      raise InvalidArgumentTypeException('The types parameter must be a dictionary.')
    for name in types:
      if not isinstance(name, str):
        raise InvalidArgumentValueException('The types keys must be strings.')
      if not name:
        raise InvalidArgumentValueException('The name for a type cannot be empty.')
      if name in self.__getCorePermissionKeys():
        raise InvalidArgumentValueException('The name for a type has the illegal value "{0}". It cannot be one of the following values: {1}'.format(name, ','.join(self.__getCorePermissionKeys())))
      if not hasattr(types[name], '__call__'):
        raise InvalidArgumentValueException('The types callbacks must be callables.')

    self.__types = copy.copy(types)

  def getBypassCallback(self):
    """Gets the current bypass access callback.

    Returns:
      Callback for checking access bypass.

    """
    return self.__bypass_callback

  def setBypassCallback(self, callback):
    """Sets the bypass access callback.

    Args:
      callback: The callback that evaluates access bypassing. Upon calling checkAccess() the registered bypass callback will be passed one parameter, which is the context dictionary passed to checkAccess(). It should return a boolean which determines whether bypass access should be granted.

    """
    if not hasattr(callback, '__call__'):
      raise InvalidArgumentTypeException('The callback parameter must be a callable data type.')

    self.__bypass_callback = callback

  def getValidPermissionKeys(self):
    """Gets all keys that can be part of a permission tree.

    Returns:
      List of valid permission keys

    """
    return self.__getCorePermissionKeys() + list(self.getTypes())

  def checkAccess(self, permissions, context = {}, allow_bypass = True):
    """Checks access for a permission tree.

    Args:
      permissions: A dictionary, list, string or boolean of the permission tree to be evaluated
      context (optional): A context dictionary that could for example contain the evaluated user and document. Default value is an empty dictionary.
      allow_bypass (optional): Determines whether bypassing access should be allowed. Default value is True.

    Returns:
      True if access is granted or False if access is denied.

    """
    if not isinstance(permissions, (dict, list, str, bool)):
      raise InvalidArgumentTypeException('The permissions parameter must be a dictionary or a list, or in certain cases a string or boolean.')
    if not isinstance(context, dict):
      raise InvalidArgumentTypeException('The context parameter must be an dictionary.')
    if not isinstance(allow_bypass, bool):
      raise InvalidArgumentTypeException('The allow_bypass parameter must be a boolean.')

    permissions_copy = copy.deepcopy(permissions)
    if isinstance(permissions_copy, dict) and 'no_bypass' in permissions_copy:
      if allow_bypass:
        if isinstance(permissions_copy['no_bypass'], bool):
          allow_bypass = not permissions_copy['no_bypass']
        elif isinstance(permissions_copy['no_bypass'], dict):
          allow_bypass = not self.__processOR(permissions = permissions_copy['no_bypass'], context = context)
        else:
          raise InvalidArgumentValueException('The no_bypass value must be a boolean or a dictionary. Current value: {0}'.format(permissions_copy['no_bypass']))
      permissions_copy.pop('no_bypass', None)

    if allow_bypass and self.__checkBypassAccess(context = context):
      return True

    if isinstance(permissions_copy, (str, bool)):
      return self.__dispatch(permissions_copy)
    if isinstance(permissions_copy, (dict, list)) and permissions_copy:
      return self.__processOR(permissions = permissions_copy, context = context)

    return False

  def __getCorePermissionKeys(self):
    return ['no_bypass', 'AND', 'NAND', 'OR', 'NOR', 'XOR', 'NOT', 'TRUE', 'FALSE']

  def __checkBypassAccess(self, context):
    bypass_callback = self.getBypassCallback()
    if not hasattr(bypass_callback, '__call__'):
      return False

    bypass_access = bypass_callback(context)
    if not isinstance(bypass_access, bool):
      raise InvalidCallbackReturnTypeException('The bypass access callback must return a boolean.')
    return bypass_access

  def __dispatch(self, permissions, context = {}, type = None):
    if isinstance(permissions, bool):
      if permissions == True:
        if type is not None:
          raise InvalidArgumentValueException('You cannot put a boolean permission as a descendant to a permission type. Existing type: {0}. Evaluated permissions: {1}'.format(type, permissions))
        return True
      if permissions == False:
        if type is not None:
          raise InvalidArgumentValueException('You cannot put a boolean permission as a descendant to a permission type. Existing type: {0}. Evaluated permissions: {1}'.format(type, permissions))
        return False
    if isinstance(permissions, str):
      if permissions == 'TRUE':
        if type is not None:
          raise InvalidArgumentValueException('You cannot put a boolean permission as a descendant to a permission type. Existing type: {0}. Evaluated permissions: {1}'.format(type, permissions))
        return True
      if permissions == 'FALSE':
        if type is not None:
          raise InvalidArgumentValueException('You cannot put a boolean permission as a descendant to a permission type. Existing type: {0}. Evaluated permissions: {1}'.format(type, permissions))
        return False
      return self.__externalAccessCheck(permission = permissions, context = context, type = type)
    if isinstance(permissions, list) and len(permissions) > 0:
      return self.__processOR(permissions = permissions, context = context, type = type)
    if isinstance(permissions, dict):
      if len(permissions) == 1:
        key = list(permissions.keys())[0]
        value = permissions[key]
        if key is 'no_bypass':
          raise InvalidArgumentValueException('The no_bypass key must be placed highest in the permission hierarchy. Evaluated permissions: {}'.format(permissions))
        if key is 'AND':
          return self.__processAND(permissions = value, context = context, type = type)
        if key is 'NAND':
          return self.__processNAND(permissions = value, context = context, type = type)
        if key is 'OR':
          return self.__processOR(permissions = value, context = context, type = type)
        if key is 'NOR':
          return self.__processNOR(permissions = value, context = context, type = type)
        if key is 'XOR':
          return self.__processXOR(permissions = value, context = context, type = type)
        if key is 'NOT':
          return self.__processNOT(permissions = value, context = context, type = type)
        if key is 'TRUE' or key is 'FALSE':
          raise InvalidArgumentValueException('A boolean permission cannot have children. Evaluated permissions: {}'.format(permissions))

        if 'long' not in globals(): # Python 3 compability
          long = int
        if not isinstance(key, (int, long, float)):
          if type is not None:
            raise InvalidArgumentValueException('You cannot put a permission type as a descendant to another permission type. Existing type: {0}. Evaluated permissions: {1}'.format(type, permissions))
          type = key

        if isinstance(value, (dict, list)):
          return self.__processOR(permissions = value, context = context, type = type)
        return self.__dispatch(permissions = value, context = context, type = type)
      if len(permissions) > 1:
        return self.__processOR(permissions = permissions, context = context, type = type)
    raise InvalidArgumentTypeException('Permissions must either be a boolean, a string, a dictionary or a list. Evaluated permissions: {0}'.format(permissions))

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

    return not self.__processAND(permissions = permissions, context = context, type = type)

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

    return not self.__processOR(permissions = permissions, context = context, type = type)

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

    return not self.__dispatch(permissions = permissions, context = context, type = type)

  def __externalAccessCheck(self, permission, context, type):
    if not self.typeExists(type):
      raise PermissionTypeNotRegisteredException('The permission type "{0}" has not been registered. Please use LogicalPermissions::addType() or LogicalPermissions::setTypes() to register permission types.'.format(type))
    access = False
    callback = self.getTypeCallback(type)
    if hasattr(callback, '__call__'):
      access = callback(permission, context)
      if not isinstance(access, bool):
        raise InvalidCallbackReturnTypeException('The registered callback for the permission type "{0}" must return a boolean.'.format(type))
    return access
