""" Utility for local block scoped variables """

__version__ = "0.1"

from itertools import zip_longest

# pylint: disable=multiple-statements

class Local(object):
    """ Allows for block local variables. To be used with a `with` statement::

            with Local(x=1, any_var=5, ...) as local:
                assert local.x == 1
                # new variables are fine too:
                local.z = local.any_var + 2

        When the `with` block exits all of the attributes of `local` are destroyed.

        ### Tuple (or any iterable) unpacking

        ```
            with Local('x, _, z', foo()) as local:
                # Given foo() returns a tuple (42, 137, 35)
                # local.x gets 1st element of tuple or 42
                # 2nd element, 137, is ignored, because _
                # local.z gets the third value, 35, of the tuple
        ```
    """

    def __init__(self, *args, **kwargs):
        """ Basic use, keyword arguments define the attributes of `local`::

                with Local(x=1, y=2) as local:
                    # introduce new 'variable' z:
                    local.z = local.x + local.y
                    print( local.z ) # --> 3
                # when 'with' exits all three, x, y, and z are destroyed

            Tuple or any iterable unpacking into variables (technically, `local`'s attributes)::

                with Local('x, _, y, z', (1, 'ignored', 2, 3)) as local:
                    assert local.x == 1 and local.y == 2 and local.z == 3

            Control optional unpacking with `?` `*` `~` modifiers:
                - `'x, _?, z?'`   : `?` optional, if not present in the next tuple don't set z as an attribute of Local.
                - `'x, y, z~'`    : `~` None-optional, if not present in the next tuple z will be set to None.
                - `'x, y, z, _*'` : `*` must be the last element, ignores the rest of tuple elements.
                - `'x, y, z, *'`  : the same as above, `*` by itself

            Also will unpack dictionaries and lists if not set to keyword argument::

                Local(zip(('x','y','z'), (1, 2, 3)))
                Local([('x',1), ('y',2), ('z',3)])
                # just assign the whole dict to my_d, with no unpacking:
                Local(my_d = [('x',1), ('y',2), ('z',3)])

        """

        class _NotPresent:
            pass

        def parse_name_(s: str):
            s = s.strip()
            if len(s) == 0:
                raise AttributeError("'Local': got empty attribute name")
            mfr = s[-1]
            if mfr == '?' or mfr == '~':
                s = s[:-1].rstrip()
                if len(s) == 0:
                    raise AttributeError(f"'Local': got empty attribute name before '{mfr}'")
                if mfr == '~' and s == '_':
                    raise AttributeError("'Local': got placeholder '_' attribute name and '~'")
            elif mfr == '*':
                rem = s[:-1].rstrip()
                if (len(rem) != 0) and (rem != '_'):
                    raise AttributeError("'Local': '*' wildcard must appear on its own after a "\
                                         f"comma or after last placeholder '_'. Instead got '{s}'")
                return (None, '*')
            else:
                mfr = None
            if not s.isidentifier():
                raise AttributeError(f"'Local': attribute name '{s}' is not a valid identifier.")
            return (s, mfr)

        var_names = None
        for i in args:
            if var_names is None:
                if isinstance(i, str):
                    var_names = map(parse_name_, i.split(','))
                    continue

            if var_names:
                if isinstance(i, dict):
                    values = i.items()
                else:
                    values = i

                try:
                    zipped = zip_longest(var_names, values, fillvalue=_NotPresent())
                except TypeError:
                    zipped = zip_longest(var_names, [values], fillvalue=_NotPresent())

                for name, val in zipped:
                    if isinstance(name, _NotPresent):
                        raise AttributeError(f"'Local': no attribute name supplied for '{val}' in {i}")
                    if isinstance(val, _NotPresent):
                        if name[1] == '*': break
                        if name[1] == '?': continue
                        if name[1] == '~':
                            val = None
                        else:
                            raise AttributeError(f"'Local' object can't map value for '{name[0]}' in {i}")
                    if name[1] == '*': break
                    if name[0] == '_': continue
                    self.__setattr__(name[0], val)

                var_names = None
            else:
                if isinstance(i, dict):
                    for j in i.items():
                        self.__setattr__(j[0], j[1])
                else:
                    for j in i:
                        self.__setattr__(j[0], j[1])

        for i in kwargs.items():
            self.__setattr__(i[0], i[1])

    def __getattr__(self, name):
        # Not necessary but implementing this shuts pylint up
        raise AttributeError(f"'Local' object has no attribute '{name}'")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__dict__.clear()
        return False # True suppresses the exception
