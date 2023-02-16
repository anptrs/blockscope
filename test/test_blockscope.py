""" Tests Local.py """

import pytest

from blockscope import Local

def test_scope():
    """ Tests Local class() """

    def tu3( ):
        return 1, 2, 3

    with Local(x=1, y=2, z=3) as lcl:
        assert lcl.x == 1
        assert lcl.y == 2
        assert lcl.z == 3
        lcl.a = 4
        assert lcl.a == 4
        lcl.x = 5
        assert lcl.x == 5

    assert hasattr(lcl, 'x') is False
    assert hasattr(lcl, 'y') is False
    assert hasattr(lcl, 'z') is False
    assert hasattr(lcl, 'a') is False

    with Local(zip(('x','y','z'), tu3())) as lcl:
        assert lcl.x == 1
        assert lcl.y == 2
        assert lcl.z == 3

    with Local([('x', 1), ('y', 2), ('z', 3)]) as lcl:
        assert lcl.x == 1
        assert lcl.y == 2
        assert lcl.z == 3

    with Local(dict(zip(('x','y','z'), tu3()))) as lcl:
        assert lcl.x == 1
        assert lcl.y == 2
        assert lcl.z == 3

    # Tuple unpacking:
    with Local('x, y, z', tu3()) as lcl:
        assert lcl.x == 1
        assert lcl.y == 2
        assert lcl.z == 3

    with Local('_, y, z', tu3()) as lcl:
        assert hasattr(lcl, '_') is False
        assert lcl.y == 2
        assert lcl.z == 3

    with Local('x, _ ,z', tu3()) as lcl:
        assert lcl.x == 1
        assert hasattr(lcl, '_') is False
        assert lcl.z == 3

    with Local(' x ,y,_', tu3()) as lcl:
        assert lcl.x == 1
        assert lcl.y == 2
        assert hasattr(lcl, '_') is False

    with Local('x, y, z?', tu3()) as lcl:
        assert lcl.x == 1
        assert lcl.y == 2
        assert lcl.z == 3

    with Local('x, y, z~', tu3()) as lcl:
        assert lcl.x == 1
        assert lcl.y == 2
        assert lcl.z == 3

    with Local('x, y, z,*', tu3()) as lcl:
        assert lcl.x == 1
        assert lcl.y == 2
        assert lcl.z == 3

    with Local('x, y, z?,*', tu3()) as lcl:
        assert lcl.x == 1
        assert lcl.y == 2
        assert lcl.z == 3

    with Local('x, y, z~,*', tu3()) as lcl:
        assert lcl.x == 1
        assert lcl.y == 2
        assert lcl.z == 3

    with Local('x, y, z, n~', tu3()) as lcl:
        assert lcl.x == 1
        assert lcl.y == 2
        assert lcl.z == 3
        assert lcl.n is None

    with Local('x, y, z, n?', tu3()) as lcl:
        assert lcl.x == 1
        assert lcl.y == 2
        assert lcl.z == 3
        assert hasattr(lcl, 'n') is False

    with Local('x?, y?, z~, n?', tu3()) as lcl:
        assert lcl.x == 1
        assert lcl.y == 2
        assert lcl.z == 3
        assert hasattr(lcl, 'n') is False

    with Local(' x ? , y ?  , z ~ , n ? ', tu3()) as lcl:
        assert lcl.x == 1
        assert lcl.y == 2
        assert lcl.z == 3
        assert hasattr(lcl, 'n') is False

    with Local('x, y, *', tu3()) as lcl:
        assert lcl.x == 1
        assert lcl.y == 2
        assert hasattr(lcl, '*') is False

    with Local('x, y, _*', tu3()) as lcl:
        assert lcl.x == 1
        assert lcl.y == 2
        assert hasattr(lcl, '_*') is False
        assert hasattr(lcl, '_') is False
        assert hasattr(lcl, '*') is False

    with Local(x=42) as lcl:
        assert lcl.x == 42

    with Local('x,*', 42) as lcl:
        assert lcl.x == 42

    with Local('x, _, y, *', "hello") as lcl:
        assert lcl.x == 'h'
        assert lcl.y == 'l'

    with Local('x, _, y, *', "hello", 'a,b,_', tu3()) as lcl:
        assert lcl.x == 'h'
        assert lcl.y == 'l'
        assert lcl.a == 1
        assert lcl.b == 2


    # Exceptions:
    with pytest.raises(AttributeError) as excinfo:
        with Local('x,y', tu3()) as _sc:
            pass
    assert "'Local': no attribute name supplied for '3' in (1, 2, 3)" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local('x,y, z, n', tu3()) as _sc:
            pass
    assert "'Local': no value present for 'n' in (1, 2, 3)" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local('x,,n', tu3()) as _sc:
            pass
    assert "'Local': empty attribute name" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local('x,n,', tu3()) as _sc:
            pass
    assert "'Local': empty attribute name" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local('x,n, ', tu3()) as _sc:
            pass
    assert "'Local': empty attribute name" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local('x,n , ', tu3()) as _sc:
            pass
    assert "'Local': empty attribute name" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local('  ', tu3()) as _sc:
            pass
    assert "'Local': empty attribute name" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local('', tu3()) as _sc:
            pass
    assert "'Local': empty attribute name" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local(',', tu3()) as _sc:
            pass
    assert "'Local': empty attribute name" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local('?,x', tu3()) as _sc:
            pass
    assert "'Local': empty attribute name before '?'" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local(' ~,x', tu3()) as _sc:
            pass
    assert "'Local': empty attribute name before '~'" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local('x,?', tu3()) as _sc:
            pass
    assert "'Local': empty attribute name before '?'" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local('x, ?', tu3()) as _sc:
            pass
    assert "'Local': empty attribute name before '?'" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local('x,~ ', tu3()) as _sc:
            pass
    assert "'Local': empty attribute name before '~'" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local('x, ~ ', tu3()) as _sc:
            pass
    assert "'Local': empty attribute name before '~'" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local('x, ~, ', tu3()) as _sc:
            pass
    assert "'Local': empty attribute name before '~'" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local('x,~, ', tu3()) as _sc:
            pass
    assert "'Local': empty attribute name before '~'" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local('x,_~', tu3()) as _sc:
            pass
    assert "'Local': modifier '~' can't be applied to placeholder '_'" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local('x,y*', tu3()) as _sc:
            pass
    assert "'Local': '*' wildcard must appear on its own after a comma or after"\
           " the last placeholder '_'. Instead got 'y*'" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        with Local('23,y,*', tu3()) as _sc:
            pass
    assert "'Local': attribute name '23' is not a valid identifier." in str(excinfo.value)
