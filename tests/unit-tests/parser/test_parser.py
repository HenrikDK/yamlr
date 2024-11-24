import pytest

from yamale import parser as par

def test_basic_validators():
    assert par.parse("str()")['name'] == 'str'
    assert par.parse("num()")['name'] == 'num'
    assert par.parse("int()")['name'] == 'int'
    assert par.parse("day()")['name'] == 'day'
    assert par.parse("timestamp()")['name'] == 'timestamp'
    assert par.parse("regex()")['name'] == 'regex'
    assert par.parse("bool()")['name'] == 'bool'
    assert par.parse("ip()")['name'] == 'ip'
    assert par.parse("mac()")['name'] == 'mac'

def test_list_type_with_children():
    result = par.parse("list(str())")

    assert result['name'] == 'list'
    assert result['children'][0]['name'] == 'str'

def test_custom_validator():
    result = par.parse("custom()", {"custom": ''})
    assert result['name'] == 'custom'

def test_required():
    result = par.parse("str(required=True)")
    assert result['kw_args']['required'] == True

    result = par.parse("str(required=False)")
    assert result['kw_args']['required'] == False

def test_syntax_error():
    with pytest.raises(SyntaxError):
        par.parse("eval()")
