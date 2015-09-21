"""
py.test and pylib: rapid testing and development utils

this module uses apipkg.py for lazy-loading sub modules
and classes.  The initpkg-dictionary  below specifies
name->value mappings where value can be another namespace
dictionary or an import path.

(c) Holger Krekel and others, 2004-2014
"""
from py import _apipkg

_apipkg.initpkg(__name__, attr={'_apipkg': _apipkg}, exportdefs={
    '__doc__'           : '_pytest.code:__doc__',
    'compile'           : '_pytest.code.source:compile_',
    'Source'            : '_pytest.code.source:Source',
    'Code'              : '_pytest.code.code:Code',
    'Frame'             : '_pytest.code.code:Frame',
    'ExceptionInfo'     : '_pytest.code.code:ExceptionInfo',
    'Traceback'         : '_pytest.code.code:Traceback',
    'getfslineno'       : '_pytest.code.source:getfslineno',
    'getrawcode'        : '_pytest.code.code:getrawcode',
    'patch_builtins'    : '_pytest.code.code:patch_builtins',
    'unpatch_builtins'  : '_pytest.code.code:unpatch_builtins',
    '_AssertionError'   : '_pytest.code.assertion:AssertionError',
    '_reinterpret_old'  : '_pytest.code.assertion:reinterpret_old',
    '_reinterpret'      : '_pytest.code.assertion:reinterpret',
    '_reprcompare'      : '_pytest.code.assertion:_reprcompare',
    '_format_explanation' : '_pytest.code.assertion:_format_explanation',
})
