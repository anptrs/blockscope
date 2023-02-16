# Block Local Scope

This simple package allows for variables to be block scoped, which is a common feature of many languages but is missing in Python.

Here is an example of the most basic of uses:
```py
    from blockscope import Local

    with Local(x=1, y=2) as local:
        print( local.x, local.y )  # prints: 1 2
        local.z = 3                # declare new variable
        print( local.z )           # prints: 3

    # when `with` exits: local's x, y, and z
    # are cleaned up automatically
```
Tuple Unpacking
---------------
One of the more useful features is tuple (or any iterable) unpacking:
```py
    def foo():
        return 1, 2, 3

    with Local('x, _, z', foo()) as local:
        print( local.x, local.z )  # prints: 1 3
```
Note the *placeholder* `_` to ignore the second element of the tuple. This is in step with Python's regular syntax for tuple unpacking: `x, _, z = foo() `


You can use `*`, `?`, and `~` modifiers to fine tune the unpacking.
Here are some examples:
```py
    def bar():
        return 4, 5

    with Local('x, _?, y? , z~ ,_*', bar()) as local:
        # x   local.x is set to the first element of the tuple (4)
        # _?  second element of the tuple (5) will be ignored if present
        #     If _ was by itself and element not present an exception
        #     would be raised: AttributeError with a helpful message
        # y?  local.y is set to 3rd element of tuple if present,
        #     In this case there's no 3rd element and local.y will
        #     not exist.
        # z~  local.z would be set if present or set to None otherwise
        #     In this case local.z will be None
        # _*  ignore the rest of the tuple elements. Always used
        #     in the last position with a placeholder _ or by itself
        print( local.x, local.z) # prints: 4 None
```

You can chain multiple un-packings and declarations:
```py

    with Local('x,y,*', foo(), '_,z' = bar(), i=6, j=7) as local:
        print( local.x, local.y, local.z )  # prints: 1 2 5
        print(i, j) # prints: 6 7
```

Dictionary and List Unpacking
-----------------------------
Dictionaries `{str:any}` and lists of tuples `[(str, any)]` are unpacked automatically if not assigned to a keyword argument:
```py
    d = {'x':1, 'y':2, 'z':3}
    l = [('a': 4), ('b': 5), ('c': 6)]

    with Local(d, l) as local:
        print( local.x, local.y, local.z ) # prints: 1 2 3
        print( local.a, local.b, local.c ) # prints: 4 5 6
```

