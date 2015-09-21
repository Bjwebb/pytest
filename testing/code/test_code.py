import py
import pytest
import sys

def test_ne():
    code1 = pytest.code.Code(compile('foo = "bar"', '', 'exec'))
    assert code1 == code1
    code2 = pytest.code.Code(compile('foo = "baz"', '', 'exec'))
    assert code2 != code1

def test_code_gives_back_name_for_not_existing_file():
    name = 'abc-123'
    co_code = compile("pass\n", name, 'exec')
    assert co_code.co_filename == name
    code = pytest.code.Code(co_code)
    assert str(code.path) == name
    assert code.fullsource is None

def test_code_with_class():
    class A:
        pass
    pytest.raises(TypeError, "pytest.code.Code(A)")

if True:
    def x():
        pass

def test_code_fullsource():
    code = pytest.code.Code(x)
    full = code.fullsource
    assert 'test_code_fullsource()' in str(full)

def test_code_source():
    code = pytest.code.Code(x)
    src = code.source()
    expected = """def x():
    pass"""
    assert str(src) == expected

def test_frame_getsourcelineno_myself():
    def func():
        return sys._getframe(0)
    f = func()
    f = pytest.code.Frame(f)
    source, lineno = f.code.fullsource, f.lineno
    assert source[lineno].startswith("        return sys._getframe(0)")

def test_getstatement_empty_fullsource():
    def func():
        return sys._getframe(0)
    f = func()
    f = pytest.code.Frame(f)
    prop = f.code.__class__.fullsource
    try:
        f.code.__class__.fullsource = None
        assert f.statement == pytest.code.Source("")
    finally:
        f.code.__class__.fullsource = prop

def test_code_from_func():
    co = pytest.code.Code(test_frame_getsourcelineno_myself)
    assert co.firstlineno
    assert co.path



def test_builtin_patch_unpatch(monkeypatch):
    cpy_builtin = py.builtin.builtins
    comp = cpy_builtin.compile
    def mycompile(*args, **kwargs):
        return comp(*args, **kwargs)
    class Sub(AssertionError):
        pass
    monkeypatch.setattr(cpy_builtin, 'AssertionError', Sub)
    monkeypatch.setattr(cpy_builtin, 'compile', mycompile)
    pytest.code.patch_builtins()
    assert cpy_builtin.AssertionError != Sub
    assert cpy_builtin.compile != mycompile
    pytest.code.unpatch_builtins()
    assert cpy_builtin.AssertionError is Sub
    assert cpy_builtin.compile == mycompile


def test_unicode_handling():
    value = py.builtin._totext('\xc4\x85\xc4\x87\n', 'utf-8').encode('utf8')
    def f():
        raise Exception(value)
    excinfo = pytest.raises(Exception, f)
    s = str(excinfo)
    if sys.version_info[0] < 3:
        u = unicode(excinfo)

def test_code_getargs():
    def f1(x):
        pass
    c1 = pytest.code.Code(f1)
    assert c1.getargs(var=True) == ('x',)

    def f2(x, *y):
        pass
    c2 = pytest.code.Code(f2)
    assert c2.getargs(var=True) == ('x', 'y')

    def f3(x, **z):
        pass
    c3 = pytest.code.Code(f3)
    assert c3.getargs(var=True) == ('x', 'z')

    def f4(x, *y, **z):
        pass
    c4 = pytest.code.Code(f4)
    assert c4.getargs(var=True) == ('x', 'y', 'z')


def test_frame_getargs():
    def f1(x):
        return sys._getframe(0)
    fr1 = pytest.code.Frame(f1('a'))
    assert fr1.getargs(var=True) == [('x', 'a')]

    def f2(x, *y):
        return sys._getframe(0)
    fr2 = pytest.code.Frame(f2('a', 'b', 'c'))
    assert fr2.getargs(var=True) == [('x', 'a'), ('y', ('b', 'c'))]

    def f3(x, **z):
        return sys._getframe(0)
    fr3 = pytest.code.Frame(f3('a', b='c'))
    assert fr3.getargs(var=True) == [('x', 'a'), ('z', {'b': 'c'})]

    def f4(x, *y, **z):
        return sys._getframe(0)
    fr4 = pytest.code.Frame(f4('a', 'b', c='d'))
    assert fr4.getargs(var=True) == [('x', 'a'), ('y', ('b',)),
                                     ('z', {'c': 'd'})]


class TestExceptionInfo:

    def test_bad_getsource(self):
        try:
            if False: pass
            else: assert False
        except AssertionError:
            exci = pytest.code.ExceptionInfo()
        assert exci.getrepr()


class TestTracebackEntry:

    def test_getsource(self):
        try:
            if False: pass
            else: assert False
        except AssertionError:
            exci = pytest.code.ExceptionInfo()
        entry = exci.traceback[0]
        source = entry.getsource()
        assert len(source) == 4
        assert 'else: assert False' in source[3]
