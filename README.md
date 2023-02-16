# Block Local Scope

This simple package allows for variables to be block scoped, which is a common feature of many languages but is missing in Python.

Installation & Basics
---------------------
```console
  $ pip install blockscope
```
The package exposes a single class `Local`. An instance of this class is meant to be used with the `with` block.

For the most basic use cases, the keyword arguments to the `Local` constructor declare and initialize "variables" that become attributes of the `Local` instance:
```py
    from blockscope import Local

    with Local(x=1, y=2) as local:
        print( local.x, local.y )  # prints: 1 2
        local.z = 3                # declare new variable
        print( local.z )           # prints: 3

    # when `with` exits: local's x, y, and z
    # are cleaned up automatically
```
Note that you can add as many new variables as you'd like inside the `with` block, such as the `local.z` variable shown above.

When the `with` block exits, all attributes of `Local` instance are released.

Tuple Unpacking
---------------
One of the more useful features is tuple (or any iterable) unpacking, which allows you to quickly and easily assign multiple values at once to separate variables. For example:
```py
    def foo():
        return 1, 2, 3

    with Local('x, _, z', foo()) as local:
        print( local.x, local.z )  # prints: 1 3
```
Note the *placeholder* `_` to ignore the second element of the tuple. This is in line with Python's regular syntax for tuple unpacking, such as `x, _, z = foo() `

You can use `*`, `?`, and `~` modifiers to fine-tune the unpacking process.
Consider this example:
```py
    def bar():
        return 4, 5

    with Local('x, _?, y? , z~ ,_*', bar()) as local:
        # x   Sets local.x to the first element of the tuple (4).
        # _?  ignores the second element of the tuple (5) if present.
        #     If _ is by itself (no ?) and the element is not present
        #     an AttributeError with a helpful message is raised.
        # y?  Sets local.y to the 3rd element of the tuple if present,
        #     In this case, there's no 3rd element and local.y will
        #     not exist.
        # z~  local.z would be set if present or set to None otherwise
        #     In this case, local.z will be None.
        # _*  Ignores the rest of the tuple elements, and is always used
        #     in the last position with a placeholder _ or by itself.
        print( local.x, local.z) # prints: 4 None
```

You can chain multiple unpackings and declarations together, allowing you to extract and assign values from multiple tuples or iterables in a single line of code.
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

