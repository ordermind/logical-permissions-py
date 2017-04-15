import unittest
from logical_permissions.LogicalPermissions import LogicalPermissions
from logical_permissions.exceptions import *

class LogicalPermissionsTest(unittest.TestCase):

  def testCreation(self):
    lp = LogicalPermissions()
    self.assertTrue(type(lp) is LogicalPermissions)

  # -----------LogicalPermissions::addType()-------------

  def testAddTypeParamNameWrongType(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentTypeException):
      lp.addType(name = 0, callback = lambda: true)

  def testAddTypeParamNameEmpty(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentValueException):
      lp.addType(name = '', callback = lambda: true)

  def testAddTypeParamNameIsCoreKey(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentValueException):
      lp.addType(name = 'AND', callback = lambda: true)

  def testAddTypeParamNameExists(self):
    lp = LogicalPermissions()
    with self.assertRaises(PermissionTypeAlreadyExistsException):
      lp.addType(name = 'test', callback = lambda: true)
      lp.addType(name = 'test', callback = lambda: true)

  def testAddTypeParamCallbackWrongType(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentTypeException):
      lp.addType(name = 'test', callback = 0)

  def testAddType(self):
    lp = LogicalPermissions()
    lp.addType(name = 'test', callback = lambda: true)
    self.assertTrue(lp.typeExists(name = 'test'))

  # -------------LogicalPermissions::removeType()--------------

  def testRemoveTypeParamNameWrongType(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentTypeException):
      lp.removeType(name = 0)

  def testRemoveTypeParamNameEmpty(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentValueException):
      lp.removeType(name = '')

  def testRemoveTypeUnregisteredType(self):
    lp = LogicalPermissions()
    with self.assertRaises(PermissionTypeNotRegisteredException):
      lp.removeType(name = 'test')

  def testRemoveType(self):
    lp = LogicalPermissions()
    lp.addType(name = 'test', callback = lambda: true)
    lp.removeType(name = 'test')
    self.assertFalse(lp.typeExists(name = 'test'))

  # ------------LogicalPermissions::typeExists()---------------

  def testTypeExistsParamNameWrongType(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentTypeException):
      lp.typeExists(name = 0)

  def testTypeExistsParamNameEmpty(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentValueException):
      lp.typeExists(name = '')

  def testTypeExists(self):
    lp = LogicalPermissions()
    self.assertFalse(lp.typeExists('test'))
    lp.addType(name = 'test', callback = lambda: true)
    self.assertTrue(lp.typeExists(name = 'test'))

  # ------------LogicalPermissions::getTypeCallback()---------------

  def testGetTypeCallbackParamNameWrongType(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentTypeException):
      lp.getTypeCallback(name = 0)

  def testGetTypeCallbackParamNameEmpty(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentValueException):
      lp.getTypeCallback(name = '')

  def testGetTypeCallbackUnregisteredType(self):
    lp = LogicalPermissions()
    with self.assertRaises(PermissionTypeNotRegisteredException):
      lp.getTypeCallback(name = 'test')

  def testGetTypeCallback(self):
    lp = LogicalPermissions()
    callback = lambda: true
    lp.addType(name = 'test', callback = callback)
    self.assertIs(lp.getTypeCallback(name = 'test'), callback)

  # ------------LogicalPermissions::setTypeCallback()---------------

  def testSetTypeCallbackParamNameWrongType(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentTypeException):
      lp.setTypeCallback(name = 0, callback = 0)

  def testSetTypeCallbackParamNameEmpty(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentValueException):
      lp.setTypeCallback(name = '', callback = 0)

  def testSetTypeCallbackUnregisteredType(self):
    lp = LogicalPermissions()
    with self.assertRaises(PermissionTypeNotRegisteredException):
      lp.setTypeCallback(name = 'test', callback = 0)

  def testSetTypeCallbackParamCallbackWrongType(self):
    lp = LogicalPermissions()
    lp.addType(name = 'test', callback = lambda: true)
    with self.assertRaises(InvalidArgumentTypeException):
      lp.setTypeCallback(name = 'test', callback = 0)

  def testSetTypeCallback(self):
    lp = LogicalPermissions()
    lp.addType(name = 'test', callback = lambda: true)
    callback = lambda: true
    self.assertIsNot(lp.getTypeCallback(name = 'test'), callback)
    lp.setTypeCallback(name = 'test', callback = callback)
    self.assertIs(lp.getTypeCallback(name = 'test'), callback)

  # ------------LogicalPermissions::getTypes()---------------

  def testGetTypes(self):
    lp = LogicalPermissions()
    self.assertEqual(lp.getTypes(), {})
    callback = lambda: true
    lp.addType(name = 'test', callback = callback)
    types = lp.getTypes()
    self.assertEqual(types, {'test': callback})
    self.assertIs(types['test'], callback)
    types['test2'] = lambda: true
    self.assertFalse('test2' in lp.getTypes())

  # ------------LogicalPermissions::setTypes()---------------

  def testSetTypesParamTypesWrongType(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentTypeException):
      lp.setTypes(types = 55)

  def testSetTypesParamTypesNameWrongType(self):
    lp = LogicalPermissions()
    callback = lambda: true
    with self.assertRaises(InvalidArgumentValueException):
      lp.setTypes(types = {0: callback})

  def testSetTypesParamTypesNameEmpty(self):
    lp = LogicalPermissions()
    callback = lambda: true
    with self.assertRaises(InvalidArgumentValueException):
      lp.setTypes(types = {'': callback})

  def testSetTypesParamTypesNameIsCoreKey(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentValueException):
      callback = lambda: true
      lp.setTypes(types = {'AND': callback})

  def testSetTypesParamTypesCallbackWrongType(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentValueException):
      lp.setTypes(types = {'test': 'hej'})

  def testSetTypes(self):
    lp = LogicalPermissions()
    callback = lambda: true
    types = {'test': callback}
    lp.setTypes(types = types)
    existing_types = lp.getTypes()
    self.assertEqual(existing_types, {'test': callback})
    self.assertIs(existing_types['test'], callback)
    types['test2'] = lambda: true
    self.assertFalse('test2' in lp.getTypes())

  # ------------LogicalPermissions::getBypassCallback()---------------

  def testGetBypassCallback(self):
    lp = LogicalPermissions()
    self.assertIsNone(lp.getBypassCallback())

  # ------------LogicalPermissions::setBypassCallback()---------------

  def testSetBypassCallbackParamCallbackWrongType(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentTypeException):
      lp.setBypassCallback(callback = 'hej')

  def testSetBypassCallback(self):
    lp = LogicalPermissions()
    callback = lambda: true
    lp.setBypassCallback(callback = callback)
    self.assertIs(lp.getBypassCallback(), callback)

  # ------------LogicalPermissions:getValidPermissionKeys()------------

  def testGetValidPermissionKeys(self):
    lp = LogicalPermissions()
    self.assertEqual(sorted(lp.getValidPermissionKeys()), sorted(['no_bypass', 'AND', 'NAND', 'OR', 'NOR', 'XOR', 'NOT', 'TRUE', 'FALSE']))
    def flag_callback(flag, context):
      access = False
      if flag is 'testflag':
        if 'testflag' in context.get('user', {}):
          access = context['user']['testflag']
      return access
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    def misc_callback(item, context):
      access = False
      if item in context.get('user', {}):
        access = context['user'][item]
      return access
    types = {
      'flag': flag_callback,
      'role': role_callback,
      'misc': misc_callback,
    }
    lp.setTypes(types)
    self.assertEqual(sorted(lp.getValidPermissionKeys()), sorted(['no_bypass', 'AND', 'NAND', 'OR', 'NOR', 'XOR', 'NOT', 'TRUE', 'FALSE', 'flag', 'role', 'misc']))

  # ------------LogicalPermissions::checkAccess()---------------

  def testCheckAccessParamPermissionsWrongType(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentTypeException):
      lp.checkAccess(permissions = 50)

  def testCheckAccessParamPermissionsWrongPermissionType(self):
    lp = LogicalPermissions()
    permissions = {
      'flag': 50,
    }
    with self.assertRaises(InvalidArgumentTypeException):
      lp.checkAccess(permissions = permissions)

  def testCheckAccessParamPermissionsNestedTypes(self):
    lp = LogicalPermissions()
    # Directly nested
    permissions = {
      'flag': {
        'flag': 'testflag',
      },
    }
    with self.assertRaises(InvalidArgumentValueException):
      lp.checkAccess(permissions = permissions)

    # Indirectly nested
    permissions = {
      'flag': {
        'OR': {
          'flag': 'testflag',
        },
      },
    }
    with self.assertRaises(InvalidArgumentValueException):
      lp.checkAccess(permissions = permissions)

  def testCheckAccessParamPermissionsUnregisteredType(self):
    lp = LogicalPermissions()
    permissions = {
      'flag': 'testflag',
    }
    with self.assertRaises(PermissionTypeNotRegisteredException):
      lp.checkAccess(permissions = permissions)

  def testCheckAccessParamContextWrongType(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentTypeException):
      lp.checkAccess(permissions = False, context = [])

  def testCheckAccessParamAllowBypassWrongType(self):
    lp = LogicalPermissions()
    with self.assertRaises(InvalidArgumentTypeException):
      lp.checkAccess(permissions = False, context = {}, allow_bypass = 'test')

  def testCheckAccessEmptyDictAllow(self):
    lp = LogicalPermissions()
    self.assertTrue(lp.checkAccess(permissions = {}))

  def testCheckAccessBypassAccessCheckContextPassing(self):
    lp = LogicalPermissions()
    user = {'id': 1}
    def bypass_callback(context):
      self.assertTrue('user' in context)
      self.assertEqual(context['user'], user)
      return True
    lp.setBypassCallback(bypass_callback)
    lp.checkAccess(permissions = False, context = {'user': user})

  def testCheckAccessBypassAccessWrongReturnType(self):
    lp = LogicalPermissions()
    def bypass_callback(context):
      return 1
    lp.setBypassCallback(bypass_callback)
    with self.assertRaises(InvalidCallbackReturnTypeException):
      lp.checkAccess(permissions = False)

  def testCheckAccessBypassAccessIllegalDescendant(self):
    lp = LogicalPermissions()
    permissions = {
      'OR': {
        'no_bypass': True
      }
    }
    with self.assertRaises(InvalidArgumentValueException):
      lp.checkAccess(permissions = permissions)

  def testCheckAccessBypassAccessAllow(self):
    lp = LogicalPermissions()
    def bypass_callback(context):
      return True
    lp.setBypassCallback(bypass_callback)
    self.assertTrue(lp.checkAccess(permissions = False))

  def testCheckAccessBypassAccessDeny(self):
    lp = LogicalPermissions()
    def bypass_callback(context):
      return False
    lp.setBypassCallback(bypass_callback)
    self.assertFalse(lp.checkAccess(permissions = False))

  def testCheckAccessBypassAccessDeny2(self):
    lp = LogicalPermissions()
    def bypass_callback(context):
      return True
    lp.setBypassCallback(bypass_callback)
    self.assertFalse(lp.checkAccess(permissions = False, context = {}, allow_bypass = False))

  def testCheckAccessNoBypassWrongType(self):
    lp = LogicalPermissions()
    def bypass_callback(context):
      return True
    lp.setBypassCallback(bypass_callback)
    with self.assertRaises(InvalidArgumentValueException):
      lp.checkAccess(permissions = {'no_bypass': 'test'})

  def testCheckAccessNoBypassEmptyPermissionsAllow(self):
    lp = LogicalPermissions()
    self.assertTrue(lp.checkAccess(permissions = {'no_bypass': True}))

  def testCheckAccessNoBypassAccessBooleanAllow(self):
    lp = LogicalPermissions()
    def bypass_callback(context):
      return True
    lp.setBypassCallback(bypass_callback)
    permissions = {'no_bypass': False}
    self.assertTrue(lp.checkAccess(permissions = permissions))
    # Test that permission dict is not changed
    self.assertTrue('no_bypass' in permissions)

  def testCheckAccessNoBypassAccessBooleanDeny(self):
    lp = LogicalPermissions()
    def bypass_callback(context):
      return True
    lp.setBypassCallback(bypass_callback)
    self.assertFalse(lp.checkAccess(permissions = {'no_bypass': True, 0 : False}))

  def testCheckAccessNoBypassAccessStringAllow(self):
    lp = LogicalPermissions()
    def bypass_callback(context):
      return True
    lp.setBypassCallback(bypass_callback)
    permissions = {'no_bypass': 'false'}
    self.assertTrue(lp.checkAccess(permissions = permissions))
    # Test that permission dict is not changed
    self.assertTrue('no_bypass' in permissions)

  def testCheckAccessNoBypassAccessStringDeny(self):
    lp = LogicalPermissions()
    def bypass_callback(context):
      return True
    lp.setBypassCallback(bypass_callback)
    permissions = {'no_bypass': 'true', 0: False}
    self.assertFalse(lp.checkAccess(permissions = permissions))

  def testCheckAccessNoBypassAccessDictAllow(self):
    lp = LogicalPermissions()
    def flag_callback(flag, context):
      access = False
      if flag is 'never_bypass':
        if 'never_bypass' in context.get('user', {}):
          access = context['user']['never_bypass']
      return access
    types = {
      'flag': flag_callback,
    }
    lp.setTypes(types)
    def bypass_callback(context):
      return True
    lp.setBypassCallback(bypass_callback)
    permissions = {
      'no_bypass': {
        'flag': 'never_bypass',
      },
    }
    user = {
      'id': 1,
      'never_bypass': False,
    }
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))

  def testCheckAccessNoBypassAccessDictDeny(self):
    lp = LogicalPermissions()
    def flag_callback(flag, context):
      access = False
      if flag is 'never_bypass':
        if 'never_bypass' in context.get('user', {}):
          access = context['user']['never_bypass']
      return access
    types = {
      'flag': flag_callback,
    }
    lp.setTypes(types)
    def bypass_callback(context):
      return True
    lp.setBypassCallback(bypass_callback)
    permissions = {
      'no_bypass': {
        'flag': 'never_bypass',
      },
      0: False,
    }
    user = {
      'id': 1,
      'never_bypass': True,
    }
    self.assertFalse(lp.checkAccess(permissions, {'user': user}))

  def testCheckAccessWrongPermissionCallbackReturnType(self):
    lp = LogicalPermissions()
    def flag_callback(flag, context):
      access = False
      if flag is 'testflag':
        if 'testflag' in context.get('user', {}):
          access = context['user']['testflag']
      return 0
    types = {
      'flag': flag_callback,
    }
    lp.setTypes(types)
    permissions = {
      'no_bypass': {
        'flag': 'never_bypass',
      },
      'flag': 'testflag',
    }
    user = {
      'id': 1,
      'testflag': True
    }
    with self.assertRaises(InvalidCallbackReturnTypeException):
      lp.checkAccess(permissions, {'user': user})

  def testCheckAccessSingleItemAllow(self):
    lp = LogicalPermissions()
    def flag_callback(flag, context):
      access = False
      if flag is 'testflag':
        if 'testflag' in context.get('user', {}):
          access = context['user']['testflag']
      return access
    types = {
      'flag': flag_callback,
    }
    lp.setTypes(types)
    permissions = {
      'no_bypass': {
        'flag': 'never_bypass',
      },
      'flag': 'testflag',
    }
    user = {
      'id': 1,
      'testflag': True
    }
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))

  def testCheckAccessSingleItemDeny(self):
    lp = LogicalPermissions()
    def flag_callback(flag, context):
      access = False
      if flag is 'testflag':
        if 'testflag' in context.get('user', {}):
          access = context['user']['testflag']
      return access
    types = {
      'flag': flag_callback,
    }
    lp.setTypes(types)
    permissions = {
      'no_bypass': {
        'flag': 'never_bypass',
      },
      'flag': 'testflag',
    }
    user = {
      'id': 1,
    }
    self.assertFalse(lp.checkAccess(permissions, {'user': user}))
    self.assertFalse(lp.checkAccess(permissions, {}))

  def testCheckAccessMultipleTypesShorthandOR(self):
    lp = LogicalPermissions()
    def flag_callback(flag, context):
      access = False
      if flag is 'testflag':
        if 'testflag' in context.get('user', {}):
          access = context['user']['testflag']
      return access
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    def misc_callback(item, context):
      access = False
      if item in context.get('user', {}):
        access = context['user'][item]
      return access
    types = {
      'flag': flag_callback,
      'role': role_callback,
      'misc': misc_callback,
    }
    lp.setTypes(types)
    permissions = {
      'no_bypass': {
        'flag': 'never_bypass',
      },
      'flag': 'testflag',
      'role': 'admin',
      'misc': 'test',
    }
    user = {
      'id': 1,
    }

    # OR truth table
    # 0 0 0
    self.assertFalse(lp.checkAccess(permissions, {'user': user}))
    # 0 0 1
    user['test'] = True
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))
    # 0 1 0
    user['test'] = False
    user['roles'] = ['admin']
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))
    # 0 1 1
    user['test'] = True
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))
    # 1 0 0
    user = {
      'id': 1,
      'testflag': True,
    }
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))
    # 1 0 1
    user['test'] = True
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))
    # 1 1 0
    user['test'] = False
    user['roles'] = ['admin']
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))
    # 1 1 1
    user['test'] = True
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))

  def testCheckAccessMultipleItemsShorthandOR(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)
    permissions = {'role': ['admin', 'editor']}
    user = {'id': 1}

    # OR truth table
    # 0 0
    self.assertFalse(lp.checkAccess(permissions, {'user': user}))
    user['roles'] = []
    self.assertFalse(lp.checkAccess(permissions, {'user': user}))
    # 0 1
    user['roles'] = ['editor']
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))
    # 1 0
    user['roles'] = ['admin']
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))
    # 1 1
    user['roles'] = ['editor', 'admin']
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))

  def testCheckAccessANDWrongValueType(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)
    permissions = {
      'role': {
        'AND': 'admin',
      },
    }
    user = {
      'id': 1,
      'roles': ['admin'],
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {'user': user})

  def testCheckAccessANDTooFewElements(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)
    user = {
      'id': 1,
      'roles': ['admin'],
    }

    permissions = {
      'role': {
        'AND': [],
      },
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {'user': user})

    permissions = {
      'role': {
        'AND': {},
      },
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {'user': user})

  def testCheckAccessMultipleItemsAND(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)
    def run_truth_table(permissions):
      user = {'id': 1}
      # AND truth table
      # 0 0 0
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))
      user['roles'] = []
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))
      # 0 0 1
      user['roles'] = ['writer']
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))
      # 0 1 0
      user['roles'] = ['editor']
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))
      # 0 1 1
      user['roles'] = ['editor', 'writer']
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))
      # 1 0 0
      user['roles'] = ['admin']
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))
      # 1 0 1
      user['roles'] = ['admin', 'writer']
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))
      # 1 1 0
      user['roles'] = ['admin', 'editor']
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))
      # 1 1 1
      user['roles'] = ['admin', 'editor', 'writer']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))

    # Test list values
    permissions = {
      'role': {
        'AND': [
          'admin',
          'editor',
          'writer'
        ]
      }
    }
    run_truth_table(permissions)

    # Test dict values
    permissions = {
      'role': {
        'AND': {
          0: 'admin',
          1: 'editor',
          2: 'writer'
        }
      }
    }
    run_truth_table(permissions)

    # Test list/dict mixes
    permissions = {
      'role': {
        'AND': [
          ['admin'],
          {0: 'editor'},
          'writer'
        ]
      }
    }
    run_truth_table(permissions)
    permissions = {
      'role': {
        'AND': {
          0: ['admin'],
          1: {0: 'editor'},
          2: 'writer'
        }
      }
    }
    run_truth_table(permissions)

  def testCheckAccessNANDWrongValueType(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)
    permissions = {
      'role': {
        'NAND': 'admin',
      },
    }
    user = {
      'id': 1,
      'roles': ['admin'],
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {'user': user})

  def testCheckAccessNANDTooFewElements(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)
    user = {
      'id': 1,
      'roles': ['admin'],
    }

    permissions = {
      'role': {
        'NAND': [],
      },
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {'user': user})

    permissions = {
      'role': {
        'NAND': {},
      },
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {'user': user})

  def testCheckAccessMultipleItemsNAND(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)
    def run_truth_table(permissions):
      user = {'id': 1}
      # NAND truth table
      # 0 0 0
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      user['roles'] = []
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 0 0 1
      user['roles'] = ['writer']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 0 1 0
      user['roles'] = ['editor']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 0 1 1
      user['roles'] = ['editor', 'writer']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 1 0 0
      user['roles'] = ['admin']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 1 0 1
      user['roles'] = ['admin', 'writer']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 1 1 0
      user['roles'] = ['admin', 'editor']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 1 1 1
      user['roles'] = ['admin', 'editor', 'writer']
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))

    # Test list values
    permissions = {
      'role': {
        'NAND': [
          'admin',
          'editor',
          'writer'
        ]
      }
    }
    run_truth_table(permissions)

    # Test dict values
    permissions = {
      'role': {
        'NAND': {
          0: 'admin',
          1: 'editor',
          2: 'writer'
        }
      }
    }
    run_truth_table(permissions)

    # Test list/dict mixes
    permissions = {
      'role': {
        'NAND': [
          ['admin'],
          {0: 'editor'},
          'writer'
        ]
      }
    }
    run_truth_table(permissions)
    permissions = {
      'role': {
        'NAND': {
          0: ['admin'],
          1: {0: 'editor'},
          2: 'writer'
        }
      }
    }
    run_truth_table(permissions)

  def testCheckAccessORWrongValueType(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)
    permissions = {
      'role': {
        'OR': 'admin',
      },
    }
    user = {
      'id': 1,
      'roles': ['admin'],
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {'user': user})

  def testCheckAccessORTooFewElements(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)
    user = {
      'id': 1,
      'roles': ['admin'],
    }

    permissions = {
      'role': {
        'OR': [],
      },
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {'user': user})

    permissions = {
      'role': {
        'OR': {},
      },
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {'user': user})

  def testCheckAccessMultipleItemsOR(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)
    def run_truth_table(permissions):
      user = {'id': 1}
      # OR truth table
      # 0 0 0
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))
      user['roles'] = []
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))
      # 0 0 1
      user['roles'] = ['writer']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 0 1 0
      user['roles'] = ['editor']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 0 1 1
      user['roles'] = ['editor', 'writer']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 1 0 0
      user['roles'] = ['admin']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 1 0 1
      user['roles'] = ['admin', 'writer']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 1 1 0
      user['roles'] = ['admin', 'editor']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 1 1 1
      user['roles'] = ['admin', 'editor', 'writer']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))

    # Test list values
    permissions = {
      'role': {
        'OR': [
          'admin',
          'editor',
          'writer'
        ]
      }
    }
    run_truth_table(permissions)

    # Test dict values
    permissions = {
      'role': {
        'OR': {
          0: 'admin',
          1: 'editor',
          2: 'writer'
        }
      }
    }
    run_truth_table(permissions)

    # Test list/dict mixes
    permissions = {
      'role': {
        'OR': [
          ['admin'],
          {0: 'editor'},
          'writer'
        ]
      }
    }
    run_truth_table(permissions)
    permissions = {
      'role': {
        'OR': {
          0: ['admin'],
          1: {0: 'editor'},
          2: 'writer'
        }
      }
    }
    run_truth_table(permissions)

  def testCheckAccessNORWrongValueType(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)
    permissions = {
      'role': {
        'NOR': 'admin',
      },
    }
    user = {
      'id': 1,
      'roles': ['admin'],
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {'user': user})

  def testCheckAccessNORTooFewElements(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)
    user = {
      'id': 1,
      'roles': ['admin'],
    }

    permissions = {
      'role': {
        'NOR': [],
      },
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {'user': user})

    permissions = {
      'role': {
        'NOR': {},
      },
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {'user': user})

  def testCheckAccessMultipleItemsNOR(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)
    def run_truth_table(permissions):
      user = {'id': 1}
      # NOR truth table
      # 0 0 0
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      user['roles'] = []
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 0 0 1
      user['roles'] = ['writer']
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))
      # 0 1 0
      user['roles'] = ['editor']
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))
      # 0 1 1
      user['roles'] = ['editor', 'writer']
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))
      # 1 0 0
      user['roles'] = ['admin']
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))
      # 1 0 1
      user['roles'] = ['admin', 'writer']
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))
      # 1 1 0
      user['roles'] = ['admin', 'editor']
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))
      # 1 1 1
      user['roles'] = ['admin', 'editor', 'writer']
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))

    # Test list values
    permissions = {
      'role': {
        'NOR': [
          'admin',
          'editor',
          'writer'
        ]
      }
    }
    run_truth_table(permissions)

    # Test dict values
    permissions = {
      'role': {
        'NOR': {
          0: 'admin',
          1: 'editor',
          2: 'writer'
        }
      }
    }
    run_truth_table(permissions)

    # Test list/dict mixes
    permissions = {
      'role': {
        'NOR': [
          ['admin'],
          {0: 'editor'},
          'writer'
        ]
      }
    }
    run_truth_table(permissions)
    permissions = {
      'role': {
        'NOR': {
          0: ['admin'],
          1: {0: 'editor'},
          2: 'writer'
        }
      }
    }
    run_truth_table(permissions)

  def testCheckAccessXORWrongValueType(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)
    permissions = {
      'role': {
        'XOR': 'admin',
      },
    }
    user = {
      'id': 1,
      'roles': ['admin'],
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {'user': user})

  def testCheckAccessXORTooFewElements(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)
    user = {
      'id': 1,
      'roles': ['admin'],
    }

    permissions = {
      'role': {
        'XOR': ['admin'],
      },
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {'user': user})

    permissions = {
      'role': {
        'XOR': {0: 'admin'},
      },
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {'user': user})

  def testCheckAccessMultipleItemsXOR(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)
    def run_truth_table(permissions):
      user = {'id': 1}
      # XOR truth table
      # 0 0 0
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))
      user['roles'] = []
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))
      # 0 0 1
      user['roles'] = ['writer']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 0 1 0
      user['roles'] = ['editor']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 0 1 1
      user['roles'] = ['editor', 'writer']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 1 0 0
      user['roles'] = ['admin']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 1 0 1
      user['roles'] = ['admin', 'writer']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 1 1 0
      user['roles'] = ['admin', 'editor']
      self.assertTrue(lp.checkAccess(permissions, {'user': user}))
      # 1 1 1
      user['roles'] = ['admin', 'editor', 'writer']
      self.assertFalse(lp.checkAccess(permissions, {'user': user}))

    # Test list values
    permissions = {
      'role': {
        'XOR': [
          'admin',
          'editor',
          'writer'
        ]
      }
    }
    run_truth_table(permissions)

    # Test dict values
    permissions = {
      'role': {
        'XOR': {
          0: 'admin',
          1: 'editor',
          2: 'writer'
        }
      }
    }
    run_truth_table(permissions)

    # Test list/dict mixes
    permissions = {
      'role': {
        'XOR': [
          ['admin'],
          {0: 'editor'},
          'writer'
        ]
      }
    }
    run_truth_table(permissions)
    permissions = {
      'role': {
        'XOR': {
          0: ['admin'],
          1: {0: 'editor'},
          2: 'writer'
        }
      }
    }
    run_truth_table(permissions)

  def testCheckAccessNOTWrongValueType(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)
    permissions = {
      'role': {
        'NOT': True,
      },
    }
    user = {
      'id': 1,
      'roles': ['admin'],
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {'user': user})

  def testCheckAccessNOTTooFewElements(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)
    user = {
      'id': 1,
      'roles': ['admin'],
    }

    permissions = {
      'role': {
        'NOT': '',
      },
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {'user': user})

    permissions = {
      'role': {
        'NOT': {},
      },
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {'user': user})

  def testCheckAccessMultipleItemsNOT(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)

    permissions = {
      'role': {
        'NOT': {
          0: 'admin',
          1: 'editor',
          2: 'writer',
        },
      },
    }
    with self.assertRaises(InvalidValueForLogicGateException):
      lp.checkAccess(permissions, {})

  def testCheckAccessSingleItemNOTString(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)

    permissions = {
      'role': {
        'NOT': 'admin',
      },
    }
    user = {
      'id': 1,
      'roles': ['admin', 'editor'],
    }
    self.assertFalse(lp.checkAccess(permissions, {'user': user}))
    user.pop('roles')
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))
    user['roles'] = ['editor']
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))

  def testCheckAccessSingleItemNOTDict(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)

    permissions = {
      'role': {
        'NOT': {5: 'admin'},
      },
    }
    user = {
      'id': 1,
      'roles': ['admin', 'editor'],
    }
    self.assertFalse(lp.checkAccess(permissions, {'user': user}))
    user.pop('roles')
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))
    user['roles'] = ['editor']
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))

  def testCheckAccessBoolTRUEIllegalDescendant(self):
    lp = LogicalPermissions()
    permissions = {
      'role': [True]
    }
    with self.assertRaises(InvalidArgumentValueException):
      lp.checkAccess(permissions)

  def testCheckAccessBoolTRUE(self):
    lp = LogicalPermissions()
    permissions = True
    self.assertTrue(lp.checkAccess(permissions))

  def testCheckAccessBoolTRUEList(self):
    lp = LogicalPermissions()
    permissions = [
      True
    ]
    self.assertTrue(lp.checkAccess(permissions))

  def testCheckAccessBoolFALSEIllegalDescendant(self):
    lp = LogicalPermissions()
    permissions = {
      'role': [False]
    }
    with self.assertRaises(InvalidArgumentValueException):
      lp.checkAccess(permissions)

  def testCheckAccessBoolFALSE(self):
    lp = LogicalPermissions()
    permissions = False
    self.assertFalse(lp.checkAccess(permissions))

  def testCheckAccessBoolFALSEList(self):
    lp = LogicalPermissions()
    permissions = [False]
    self.assertFalse(lp.checkAccess(permissions))

  def testCheckAccessBoolFALSEBypass(self):
    lp = LogicalPermissions()
    def bypass_callback(context):
      return True
    lp.setBypassCallback(bypass_callback)
    permissions = [False]
    self.assertTrue(lp.checkAccess(permissions))

  def testCheckAccessBoolFALSENoBypass(self):
    lp = LogicalPermissions()
    def bypass_callback(context):
      return True
    lp.setBypassCallback(bypass_callback)
    permissions = {
      0: False,
      'no_bypass': True
    }
    self.assertFalse(lp.checkAccess(permissions))

  def testCheckAccessStringTRUEIllegalChildren(self):
    lp = LogicalPermissions()
    permissions = {
      'TRUE': False
    }
    with self.assertRaises(InvalidArgumentValueException):
      lp.checkAccess(permissions)
    permissions = {
      'TRUE': []
    }
    with self.assertRaises(InvalidArgumentValueException):
      lp.checkAccess(permissions)
    permissions = {
      'TRUE': {}
    }
    with self.assertRaises(InvalidArgumentValueException):
      lp.checkAccess(permissions)

  def testCheckAccessStringTRUEIllegalDescendant(self):
    lp = LogicalPermissions()
    permissions = {
      'role': ['TRUE']
    }
    with self.assertRaises(InvalidArgumentValueException):
      lp.checkAccess(permissions)

  def testCheckAccessStringTRUE(self):
    lp = LogicalPermissions()
    permissions = 'TRUE'
    self.assertTrue(lp.checkAccess(permissions))

  def testCheckAccessStringTRUEList(self):
    lp = LogicalPermissions()
    permissions = ['TRUE']
    self.assertTrue(lp.checkAccess(permissions))

  def testCheckAccessStringFALSEIllegalChildren(self):
    lp = LogicalPermissions()
    permissions = {
      'FALSE': False
    }
    with self.assertRaises(InvalidArgumentValueException):
      lp.checkAccess(permissions)
    permissions = {
      'FALSE': []
    }
    with self.assertRaises(InvalidArgumentValueException):
      lp.checkAccess(permissions)
    permissions = {
      'FALSE': {}
    }
    with self.assertRaises(InvalidArgumentValueException):
      lp.checkAccess(permissions)

  def testCheckAccessStringFALSEIllegalDescendant(self):
    lp = LogicalPermissions()
    permissions = {
      'role': ['FALSE']
    }
    with self.assertRaises(InvalidArgumentValueException):
      lp.checkAccess(permissions)

  def testCheckAccessStringFALSE(self):
    lp = LogicalPermissions()
    permissions = 'FALSE'
    self.assertFalse(lp.checkAccess(permissions))

  def testCheckAccessStringFALSEList(self):
    lp = LogicalPermissions()
    permissions = ['FALSE']
    self.assertFalse(lp.checkAccess(permissions))

  def testCheckAccessStringFALSEBypass(self):
    lp = LogicalPermissions()
    def bypass_callback(context):
      return True
    lp.setBypassCallback(bypass_callback)
    permissions = [
      'FALSE'
    ]
    self.assertTrue(lp.checkAccess(permissions))

  def testCheckAccessStringFALSENoBypass(self):
    lp = LogicalPermissions()
    def bypass_callback(context):
      return True
    lp.setBypassCallback(bypass_callback)
    permissions = {
      0: 'FALSE',
      'no_bypass': True
    }
    self.assertFalse(lp.checkAccess(permissions))

  def testCheckAccessNestedLogic(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)

    permissions = {
      'role': {
        'OR': {
          'NOT': {
            'AND': [
              'admin',
              'editor',
            ]
          }
        }
      },
      0: False,
      1: 'FALSE'
    }
    user = {
      'id': 1,
      'roles': ['admin', 'editor'],
    }
    self.assertFalse(lp.checkAccess(permissions, {'user': user}))
    user.pop('roles')
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))
    user['roles'] = ['editor']
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))

  def testCheckAccessLogicGateFirst(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)

    permissions = {
      'AND': {
        'role': {
          'OR': {
            'NOT': {
              'AND': [
                'admin',
                'editor',
              ]
            }
          }
        },
        0: True,
        1: 'TRUE'
      }
    }
    user = {
      'id': 1,
      'roles': ['admin', 'editor'],
    }
    self.assertFalse(lp.checkAccess(permissions, {'user': user}))
    user.pop('roles')
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))
    user['roles'] = ['editor']
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))

  def testCheckAccessShorthandORMixedDictsLists(self):
    lp = LogicalPermissions()
    def role_callback(role, context):
      access = False
      if 'roles' in context.get('user', {}):
        access = role in context['user']['roles']
      return access
    types = {
      'role': role_callback,
    }
    lp.setTypes(types)

    permissions = {
      'role': [
        'admin',
        {
          'AND': [
            'editor',
            'writer',
            {
              'OR': [
                'role1',
                'role2'
              ]
            }
          ]
        }
      ]
    }
    user = {
      'id': 1,
      'roles': ['admin', 'editor'],
    }
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))
    user.pop('roles')
    self.assertFalse(lp.checkAccess(permissions, {'user': user}))
    user['roles'] = ['editor']
    self.assertFalse(lp.checkAccess(permissions, {'user': user}))
    user['roles'] = ['editor', 'writer']
    self.assertFalse(lp.checkAccess(permissions, {'user': user}))
    user['roles'] = ['editor', 'writer', 'role1']
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))
    user['roles'] = ['editor', 'writer', 'role2']
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))
    user['roles'] = ['admin', 'writer']
    self.assertTrue(lp.checkAccess(permissions, {'user': user}))

if __name__ == '__main__':
  unittest.main()