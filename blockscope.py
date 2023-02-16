""" Utility for local block scoped variables """

__version__ = "0.1"

from itertools import zip_longest


# pylint: disable=multiple-statements

class Local(object):
    """ Allows for block local variables, as much as Python would allow anyways.
        Use a `with` statement::

            with Local(x=1, any_var=5, ...) as local:
                assert local.x == 1
                # new variables are fine too:
                local.z = 2

        When the `with` block exits all of the attributes of `local` are destroyed.

        ### Tuple (or any iterable) unpacking

        ```
            with Local('x, _, z', f_returning_tuple()) as local:
                # Given f_returning_tuple() returns a tuple (42, 137, 35)
                # local.x gets 1st element of tuple or 1
                # 2nd elmenet is ignored
                # local.z gets the third value of the tuple returned by f_returning_tuple()
                # the sceond value of the tuple is ignored, because we used _
        ```
    """

    def __init__(self, *args, **kwargs):
        """ Basic use::

                with Local(x=1, y=2, z=3) as local:
                    ...

            Tuple or any iterable unpacking into variables (technically, Local's attributes)::

                with Local('x, _,y,z', (1, 'ignore', 2, 3)) as local:
                    assert local.x == 1 and local.y == 2 and local.z == 3

            Optional argument unpacking with ? * ~ modifiers ::

                'x, _, z' - placeholder _ ? ~ can also be applied to it
                'x, y, z?' - z is optional if not present in tuple it won't be set as attribute of Local.
                'x,y,z~' - z is optional if not present in the following tuple will be set to None.
                'x,y,z,_*' - only first three elements of the tuple are used, the rest is ignored.
                'x,y,z,*'  - aslo allowed the same as above

            Also tries to unpack dicitonaries and lists if not set to keyword argument::

                Local(zip(('x','y','z'), (1, 2, 3)))
                Local([('x',1), ('y',2), ('z',3)])
                Local(d = [('x',1), ('y',2), ('z',3)]) # just assign the whole dict to d, no arg unpacking

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
        # Not neccessary but implementing this shuts pylint up
        raise AttributeError(f"'Local' object has no attribute '{name}'")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__dict__.clear()
        return False # True suppresses the exception
