import datetime
from yamale import validators as val


def test_str_length_min():
    kw_args = {'min': 2}
    c_val = {'name': 'str', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, "abcd")) == 0
    assert len(val.validate(c_sch, c_val, "ab")) == 0
    assert len(val.validate(c_sch, c_val, "a")) == 1

def test_str_length_max():
    kw_args = {'max': 3}
    c_val = {'name': 'str', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, "abc")) == 0
    assert len(val.validate(c_sch, c_val, "ab")) == 0
    assert len(val.validate(c_sch, c_val, "abcd")) == 1

def test_num_min():
    kw_args = {'min': 0.5}
    c_val = {'name': 'num', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, 4)) == 0
    assert len(val.validate(c_sch, c_val, 0.5)) == 0
    assert len(val.validate(c_sch, c_val, 0.1)) == 1

def test_num_max():
    kw_args = {'max': 10}
    c_val = {'name': 'num', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, 4)) == 0
    assert len(val.validate(c_sch, c_val, 10)) == 0
    assert len(val.validate(c_sch, c_val, 11)) == 1

def test_timestamp_min():
    kw_args = {'min': datetime.datetime(2010, 1, 1)}
    c_val = {'name': 'timestamp', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, datetime.datetime(2010, 1, 1))) == 0
    assert len(val.validate(c_sch, c_val, datetime.datetime(2010, 2, 2))) == 0
    assert len(val.validate(c_sch, c_val, datetime.datetime(2009, 12, 31))) == 1

def test_timestamp_max():
    kw_args = {'max': datetime.datetime(2010, 1, 1)}
    c_val = {'name': 'timestamp', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, datetime.datetime(2010, 1, 1))) == 0
    assert len(val.validate(c_sch, c_val, datetime.datetime(2009, 2, 2))) == 0
    assert len(val.validate(c_sch, c_val, datetime.datetime(2010, 2, 2))) == 1

def test_day_min():
    kw_args = {'min': datetime.date(2010, 1, 1)}
    c_val = {'name': 'day', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, datetime.date(2010, 1, 1))) == 0
    assert len(val.validate(c_sch, c_val, datetime.date(2011, 2, 2))) == 0
    assert len(val.validate(c_sch, c_val, datetime.date(2009, 12, 31))) == 1

def test_day_max():
    kw_args = {'max': datetime.date(2010, 1, 1)}
    c_val = {'name': 'day', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, datetime.date(2010, 1, 1))) == 0
    assert len(val.validate(c_sch, c_val, datetime.date(2009, 2, 2))) == 0
    assert len(val.validate(c_sch, c_val, datetime.date(2010, 2, 2))) == 1

def test_str_equals():
    kw_args = {'equals': 'abcd'}
    c_val = {'name': 'str', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, "abcd")) == 0
    assert len(val.validate(c_sch, c_val, "abcde")) == 1
    assert len(val.validate(c_sch, c_val, "c")) == 1

def test_str_equals_ignore_case():
    kw_args = {'equals': 'abcd', 'ignore_case': True}
    c_val = {'name': 'str', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, "abCd")) == 0
    assert len(val.validate(c_sch, c_val, "abcde")) == 1
    assert len(val.validate(c_sch, c_val, "C")) == 1

def test_str_starts_with():
    kw_args = {'starts_with': 'abc'}
    c_val = {'name': 'str', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, "abcd")) == 0
    assert len(val.validate(c_sch, c_val, "bcd")) == 1
    assert len(val.validate(c_sch, c_val, "c")) == 1

def test_str_starts_with_ignore_case():
    kw_args = {'starts_with': 'abC', 'ignore_case': True}
    c_val = {'name': 'str', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, "abCde")) == 0
    assert len(val.validate(c_sch, c_val, "abcde")) == 0
    assert len(val.validate(c_sch, c_val, "bcd")) == 1
    assert len(val.validate(c_sch, c_val, "C")) == 1

def test_str_ends_with():
    kw_args = {'ends_with': 'abcd'}
    c_val = {'name': 'str', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, "abcd")) == 0
    assert len(val.validate(c_sch, c_val, "abcde")) == 1
    assert len(val.validate(c_sch, c_val, "c")) == 1

def test_str_ends_with_ignore_case():
    kw_args = {'ends_with': 'abC', 'ignore_case': True}
    c_val = {'name': 'str', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, "xyzabC")) == 0
    assert len(val.validate(c_sch, c_val, "xyzabc")) == 0
    assert len(val.validate(c_sch, c_val, "cde")) == 1
    assert len(val.validate(c_sch, c_val, "C")) == 1

def test_str_matches():
    kw_args = {'matches': r"^(abc)\1?de$"}
    c_val = {'name': 'str', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, "abcabcde")) == 0
    assert len(val.validate(c_sch, c_val, "abcabcabcde")) == 1
    assert len(val.validate(c_sch, c_val, "\12")) == 1

def test_str_matches_ignore_case():
    kw_args = {'matches': r"[a-z0-9]{3,}s\s$", 'ignore_case': True}
    c_val = {'name': 'str', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, "b33S\v")) == 0
    assert len(val.validate(c_sch, c_val, "B33s\t")) == 0
    assert len(val.validate(c_sch, c_val, " b33s ")) == 1
    assert len(val.validate(c_sch, c_val, "b33s  ")) == 1

def test_str_matches_multiline():
    kw_args = {'matches': r"A.+\d$", 'ignore_case': False, 'multiline': True}
    c_val = {'name': 'str', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, "A_-3\n\n")) == 0
    assert len(val.validate(c_sch, c_val, "a!!!!!5\n\n")) == 1

def test_str_matches_all_options():
    kw_args = {'matches': r".*^Ye.*s\.", 'ignore_case': True, 'multiline': True, 'dotall': True}
    c_val = {'name': 'str', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, "YEeeEEEEeeeeS.")) == 0
    assert len(val.validate(c_sch, c_val, "What?\nYes!\nBEES.\nOK.")) == 0
    assert len(val.validate(c_sch, c_val, "YES-TA-TOES?")) == 1
    assert len(val.validate(c_sch, c_val, "\n\nYaes.")) == 1

def test_str_exclude():
    kw_args = {'exclude': 'abcd'}
    c_val = {'name': 'str', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, "efg")) == 0
    assert len(val.validate(c_sch, c_val, "abc")) == 1
    assert len(val.validate(c_sch, c_val, "c")) == 1

def test_char_exclude_igonre_case():
    kw_args = {'exclude': 'abcd', 'ignore_case': True}
    c_val = {'name': 'str', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, "efg")) == 0
    assert len(val.validate(c_sch, c_val, "Efg")) == 0
    assert len(val.validate(c_sch, c_val, "abc")) == 1
    assert len(val.validate(c_sch, c_val, "Def")) == 1
    assert len(val.validate(c_sch, c_val, "c")) == 1

def test_ip4():
    kw_args = {'version': 4}
    c_val = {'name': 'ip', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, "192.168.1.1")) == 0
    assert len(val.validate(c_sch, c_val, "192.168.1.255")) == 0
    assert len(val.validate(c_sch, c_val, "192.168.3.1/24")) == 0

    assert len(val.validate(c_sch, c_val, "2001:db8::")) == 1
    assert len(val.validate(c_sch, c_val, "2001:db8::/64")) == 1

def test_ip6():
    kw_args = {'version': 6}
    c_val = {'name': 'ip', 'kw_args': kw_args, 'args': []}
    c_sch = {'validators': val.default, 'data': {}}

    assert len(val.validate(c_sch, c_val, "192.168.1.1")) == 1
    assert len(val.validate(c_sch, c_val, "192.168.1.255")) == 1
    assert len(val.validate(c_sch, c_val, "192.168.3.1/24")) == 1
               
    assert len(val.validate(c_sch, c_val, "2001:db8::")) == 0
    assert len(val.validate(c_sch, c_val, "2001:db8::/64")) == 0
