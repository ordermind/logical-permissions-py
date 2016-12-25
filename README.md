<a href="https://travis-ci.org/Ordermind/logical-permissions-py" target="_blank"><img src="https://travis-ci.org/Ordermind/logical-permissions-py.svg?branch=master" /></a>
# logical-permissions

This is a generic library that provides support for dictionary-based permissions with logic gates such as AND and OR. You can register any kind of permission types such as roles and flags. The idea with this library is to be an ultra-flexible foundation that can be used by any framework. It supports python 2 and 3.

## Getting started

### Installation

`pip install logical-permissions`

### Usage

```python
# Simple example for checking user roles

from logical_permissions.LogicalPermissions import LogicalPermissions

lp = LogicalPermissions()

def roleCallback(role, context):
  access = False
  if 'roles' in context.get('user', {}):
    access = role in context['user']['roles']
  return access
lp.addType('role', roleCallback)

permissions = {
  'role': ['editor', 'writer'],
}

user = {
  'id': 1,
  'roles': ['writer'],
}

access = lp.checkAccess(permissions, {'user': user})
print('Access granted: {0}'.format(access))
```

The main api method is [`LogicalPermissions::checkAccess()`](#checkaccess), which checks the access for a **permission tree**. A permission tree is a bundle of permissions that apply to a specific action. Let's say for example that you want to restrict access for updating a user. You'd like only users with the role "admin" to be able to update any user, but users should also be able to update their own user data (or at least some of it). With the structure this package provides, these conditions could be expressed elegantly in a permission tree as such:

```python
{
  'OR': {
    'role': 'admin',
    'flag': 'is_author',
  },
}
```

In this example `role` and `flag` are the evaluated permission types. For this example to work you will need to register the permission types 'role' and 'flag' so that the class knows which callbacks are responsible for evaluating the respective permission types. You can do that with [`LogicalPermissions::addType()`](#addtype).

### Bypassing permissions
This packages also supports rules for bypassing permissions completely for superusers. In order to use this functionality you need to register a callback with [`LogicalPermissions::setBypassCallback()`](#setbypasscallback). The registered callback will run on every permission check and if it returns `True`, access will automatically be granted. If you want to make exceptions you can do so by adding `'no_bypass': True` to the first level of a permission tree. You can even use permissions as conditions for `no_bypass`.

Examples:

```python
# Disallow access bypassing
{
  'no_bypass': True,
  'role': 'editor',
}
```

```python
# Disallow access bypassing only if the user is an admin
{
  'no_bypass': {
    'role': 'admin',
  },
  'role': 'editor',
}
```

## Logic gates

Currently supported logic gates are [AND](#and), [NAND](#nand), [OR](#or), [NOR](#nor), [XOR](#xor) and [NOT](#not). You can put logic gates anywhere in a permission tree and nest them to your heart's content. All logic gates support a dictionary or list as their value, except the NOT gate which has special rules. If a dictionary or list of values does not have a logic gate as its key, an OR gate will be assumed.

### AND

A logic AND gate returns True if all of its children return True. Otherwise it returns False.

Examples:

```python
# Allow access only if the user is both an editor and a sales person
{
  'role': {
    'AND': ['editor', 'sales'],
  },
}
```

```python
# Allow access if the user is both a sales person and the author of the document
{
  'AND': {
    'role': 'sales',
    'flag': 'is_author',
  },
}
```

### NAND

A logic NAND gate returns True if one or more of its children returns False. Otherwise it returns False.

Examples:

```python
# Allow access by anyone except if the user is both an editor and a sales person
{
  'role': {
    'NAND': ['editor', 'sales'],
  },
}
```

```python
# Allow access by anyone, but not if the user is both a sales person and the author of the document.
{
  'NAND': {
    'role': 'sales',
    'flag': 'is_author',
  },
}
```

### OR

A logic OR gate returns True if one or more of its children returns True. Otherwise it returns False.

Examples:

```python
# Allow access if the user is either an editor or a sales person, or both.
{
  'role': {
    'OR': ['editor', 'sales'],
  },
}
```

```python
# Allow access if the user is either a sales person or the author of the document, or both
{
  'OR': {
    'role': 'sales',
    'flag': 'is_author',
  },
}
```

### Shorthand OR

As previously mentioned, any dictionary or list of values that doesn't have a logic gate as its key is interpreted as belonging to an OR gate.

In other words, this permission tree:

```python
{
  'role': ['editor', 'sales'],
}
```
is interpreted exactly the same way as this permission tree:
```python
{
  'role': {
    'OR': ['editor', 'sales'],
  },
}
```

### NOR

A logic NOR gate returns True if all of its children returns False. Otherwise it returns False.

Examples:

```python
# Allow access if the user is neither an editor nor a sales person
{
  'role': {
    'NOR': ['editor', 'sales'],
  },
}
```

```python
# Allow neither sales people nor the author of the document to access it
{
  'NOR': {
    'role': 'sales',
    'flag': 'is_author',
  },
}
```


### XOR

A logic XOR gate returns True if one or more of its children returns True and one or more of its children returns False. Otherwise it returns False. An XOR gate requires a minimum of two elements in its value list or dictionary.

Examples:

```python
# Allow access if the user is either an editor or a sales person, but not both
{
  'role': {
    'XOR': ['editor', 'sales'],
  },
}
```

```python
# Allow either sales people or the author of the document to access it, but not if the user is both a sales person and the author
{
  'XOR': {
    'role': 'sales',
    'flag': 'is_author',
  },
}
```

### NOT

A logic NOT gate returns True if its child returns False, and vice versa. The NOT gate is special in that it supports either a string or a dictionary with a single element as its value.

Examples:

```python
# Allow access for anyone except editors
{
  'role': {
    'NOT': 'editor',
  },
}
```

```python
# Allow access for anyone except the author of the document
{
  'NOT': {
    'flag': 'is_author',
  },
}
```

## Boolean Permissions

Boolean permissions are a special kind of permission. They can be used for allowing or disallowing access for everyone (except those with bypass access). They are not allowed as descendants to a permission type and they may not contain children. Both true booleans and booleans represented as uppercase strings are supported. Of course a simpler way to allow access to everyone is to not define any permissions at all for that action, but it might be nice sometimes to explicitly allow access for everyone.

Examples:

```python
# Allow access for anyone
[
  True
]

# Using a boolean without a list is also permitted
True
```

```python
# Example with string representation
[
  'TRUE'
]

# Using a string representation without a list is also permitted
'TRUE'
```

```python
# Deny access for everyone except those with bypass access
[
  False
]

# Using a boolean without a list is also permitted
False
```

```python
# Example with string representation
[
  'FALSE'
]

# Using a string representation without a list is also permitted
'FALSE'
```

```python
# Deny access for everyone including those with bypass access
{
  0: False,
  'no_bypass': True
}
```

## API Documentation

## Table of Contents

* [LogicalPermissions](#logicalpermissions)
    * [addType](#addtype)
    * [removeType](#removetype)
    * [typeExists](#typeexists)
    * [getTypeCallback](#gettypecallback)
    * [setTypeCallback](#settypecallback)
    * [getTypes](#gettypes)
    * [setTypes](#settypes)
    * [getBypassCallback](#getbypasscallback)
    * [setBypassCallback](#setbypasscallback)
    * [getValidPermissionKeys](#getvalidpermissionkeys)
    * [checkAccess](#checkaccess)

## LogicalPermissions

### addType

Adds a permission type.

```python
LogicalPermissions::addType( name, callback )
```




**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | **string** | The name of the permission type. |
| `callback` | **callable** | The callback that evaluates the permission type. Upon calling checkAccess() the registered callback will be passed two parameters: a permission string (such as a role) and the context dictionary passed to checkAccess(). The permission will always be a single string even if for example multiple roles are accepted. In that case the callback will be called once for each role that is to be evaluated. The callback should return a boolean which determines whether access should be granted. |




---


### removeType

Removes a permission type.

```python
LogicalPermissions::removeType( name )
```




**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | **string** | The name of the permission type. |




---


### typeExists

Checks whether a permission type is registered.

```python
LogicalPermissions::typeExists( name )
```




**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | **string** | The name of the permission type. |


**Return Value:**

True if the type is found or False if the type isn't found.



---


### getTypeCallback

Gets the callback for a permission type.

```python
LogicalPermissions::getTypeCallback( name )
```




**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | **string** | The name of the permission type. |


**Return Value:**

Callback for the permission type.



---


### setTypeCallback

Changes the callback for an existing permission type.

```python
LogicalPermissions::setTypeCallback( name, callback )
```




**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | **string** | The name of the permission type. |
| `callback` | **callable** | The callback that evaluates the permission type. Upon calling checkAccess() the registered callback will be passed two parameters: a permission string (such as a role) and the context dictionary passed to checkAccess(). The permission will always be a single string even if for example multiple roles are accepted. In that case the callback will be called once for each role that is to be evaluated. The callback should return a boolean which determines whether access should be granted. |



---

### getTypes

Gets all defined permission types.

```python
LogicalPermissions::getTypes(  )
```





**Return Value:**

A dictionary of permission types with the structure {name: callback, name2: callback2, ...}. This dictionary is shallow copied.



---


### setTypes

Overwrites all defined permission types.

```python
LogicalPermissions::setTypes( types )
```




**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `types` | **dictionary** | A dictionary of permission types with the structure {name: callback, name2: callback2, ...}. This dictionary is shallow copied. |




---


### getBypassCallback

Gets the registered callback for access bypass evaluation.

```python
LogicalPermissions::getBypassCallback(  )
```





**Return Value:**

Bypass access callback.



---


### setBypassCallback

Sets the callback for access bypass evaluation.

```python
LogicalPermissions::setBypassCallback( callback )
```




**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `callback` | **callable** | The callback that evaluates access bypassing. Upon calling checkAccess() the registered bypass callback will be passed one parameter, which is the context dictionary passed to checkAccess(). It should return a boolean which determines whether bypass access should be granted. |




---


### getValidPermissionKeys

Gets all keys that can be part of a permission tree.

```python
LogicalPermissions::getValidPermissionKeys(  )
```





**Return Value:**

List of valid permission keys



---


### checkAccess

Checks access for a permission tree.

```python
LogicalPermissions::checkAccess( permissions, context = {}, allow_bypass = True )
```




**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `permissions` | **mixed** | The permission tree to be evaluated. |
| `context` | **dictionary** | (optional) A context dictionary that could for example contain the evaluated user and document. Default value is an empty dictionary. |
| `allow_bypass` | **boolean** | (optional) Determines whether bypassing access should be allowed. Default value is True. |


**Return Value:**

True if access is granted or False if access is denied.


---