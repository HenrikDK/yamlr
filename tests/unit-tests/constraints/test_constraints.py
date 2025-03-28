import datetime
from yamlr import constraints as con

def test_length_min():
    constraint = con.default['length_min']
    func = constraint['func']
    c_val = {'kw_args': {'min':2}}
    
    assert len(func({}, c_val, "abcd")) == 0
    assert len(func({}, c_val, "ab")) == 0
    assert len(func({}, c_val, "a")) == 1

def test_length_max():
    constraint = con.default['length_max']
    func = constraint['func']
    c_val = {'kw_args': {'max':3}}

    assert len(func({}, c_val, "abc")) == 0
    assert len(func({}, c_val, "ab")) == 0
    assert len(func({}, c_val, "abcd")) == 1

def test_number_max():
    constraint = con.default['max']
    func = constraint['func']
    c_val = {'kw_args': {'max':10}}

    assert len(func({}, c_val, 4)) == 0
    assert len(func({}, c_val, 10)) == 0
    assert len(func({}, c_val, 11)) == 1

def test_number_min():
    constraint = con.default['min']
    func = constraint['func']
    c_val = {'kw_args': {'min':0.5}}

    assert len(func({}, c_val, 4)) == 0
    assert len(func({}, c_val, 0.5)) == 0
    assert len(func({}, c_val, 0.1)) == 1

def test_timestamp_min():
    constraint = con.default['min']
    func = constraint['func']
    c_val = {'kw_args': {'min':datetime.datetime(2010, 1, 1)}}

    assert len(func({}, c_val, datetime.datetime(2010, 1, 1))) == 0
    assert len(func({}, c_val, datetime.datetime(2011, 2, 2))) == 0
    assert len(func({}, c_val, datetime.datetime(2009, 12, 31))) == 1

def test_timestamp_max():
    constraint = con.default['max']
    func = constraint['func']
    c_val = {'kw_args': {'max':datetime.datetime(2010, 1, 1)}}

    assert len(func({}, c_val, datetime.datetime(2010, 1, 1))) == 0
    assert len(func({}, c_val, datetime.datetime(2009, 2, 2))) == 0
    assert len(func({}, c_val, datetime.datetime(2010, 2, 2))) == 1

def test_day_min():
    constraint = con.default['min']
    func = constraint['func']
    c_val = {'kw_args': {'min':datetime.date(2010, 1, 1)}}

    assert len(func({}, c_val, datetime.date(2010, 1, 1))) == 0
    assert len(func({}, c_val, datetime.date(2011, 2, 2))) == 0
    assert len(func({}, c_val, datetime.date(2009, 12, 31))) == 1

def test_day_max():
    constraint = con.default['max']
    func = constraint['func']
    c_val = {'kw_args': {'max':datetime.date(2010, 1, 1)}}

    assert len(func({}, c_val, datetime.date(2010, 1, 1))) == 0
    assert len(func({}, c_val, datetime.date(2009, 2, 2))) == 0
    assert len(func({}, c_val, datetime.date(2010, 2, 2))) == 1

def test_str_equals():
    constraint = con.default['str_equals']
    func = constraint['func']
    c_val = {'kw_args': {'equals':"abcd"}}

    assert len(func({}, c_val, "abcd")) == 0
    assert len(func({}, c_val, "abcde")) == 1
    assert len(func({}, c_val, "c")) == 1

def test_str_equals_ignore_case():
    constraint = con.default['str_equals']
    func = constraint['func']
    c_val = {'kw_args': {'equals':"abcd", 'ignore_case': True}}

    assert len(func({}, c_val, "abCd")) == 0
    assert len(func({}, c_val, "abcde")) == 1
    assert len(func({}, c_val, "C")) == 1

def test_str_starts_with():
    constraint = con.default['str_starts_with']
    func = constraint['func']
    c_val = {'kw_args': {'starts_with':"abc"}}

    assert len(func({}, c_val, "abcd")) == 0
    assert len(func({}, c_val, "bcd")) == 1
    assert len(func({}, c_val, "c")) == 1

def test_str_starts_with_ignore_case():
    constraint = con.default['str_starts_with']
    func = constraint['func']
    c_val = {'kw_args': {'starts_with':"abC", 'ignore_case': True}}

    assert len(func({}, c_val, "abCde")) == 0
    assert len(func({}, c_val, "abcde")) == 0
    assert len(func({}, c_val, "bcd")) == 1
    assert len(func({}, c_val, "C")) == 1

def test_str_ends_with():
    constraint = con.default['str_ends_with']
    func = constraint['func']
    c_val = {'kw_args': {'ends_with':"abcd"}}

    assert len(func({}, c_val, "abcd")) == 0
    assert len(func({}, c_val, "abcde")) == 1
    assert len(func({}, c_val, "c")) == 1

def test_str_ends_with_ignore_case():
    constraint = con.default['str_ends_with']
    func = constraint['func']
    c_val = {'kw_args': {'ends_with':"abC", 'ignore_case': True}}

    assert len(func({}, c_val, "xyzabC")) == 0
    assert len(func({}, c_val, "xyzabc")) == 0
    assert len(func({}, c_val, "cde")) == 1
    assert len(func({}, c_val, "C")) == 1

def test_str_matches():
    constraint = con.default['str_matches']
    func = constraint['func']
    c_val = {'kw_args': {'matches':r"^(abc)\1?de$"}}

    assert len(func({}, c_val, "abcabcde")) == 0
    assert len(func({}, c_val, "abcabcabcde")) == 1
    assert len(func({}, c_val, "\12")) == 1

def test_str_matches_ignore_case():
    constraint = con.default['str_matches']
    func = constraint['func']
    c_val = {'kw_args': {'matches':r"[a-z0-9]{3,}s\s$", 'ignore_case': True}}

    assert len(func({}, c_val, "b33S\v")) == 0
    assert len(func({}, c_val, "B33s\t")) == 0
    assert len(func({}, c_val, " b33s ")) == 1
    assert len(func({}, c_val, "b33s  ")) == 1

def test_str_matches_multi():
    constraint = con.default['str_matches']
    func = constraint['func']
    c_val = {'kw_args': {'matches':r"A.+\d$", 'multiline': True}}

    assert len(func({}, c_val, "A_-3\n\n")) == 0
    assert len(func({}, c_val, "a!!!!!5\n\n")) == 1

def test_str_matches_ignore_case_multi_dotall():
    constraint = con.default['str_matches']
    func = constraint['func']
    c_val = {'kw_args': {'matches':r".*^Ye.*s\.", 'ignore_case': True, 'multiline': True, 'dotall': True}}

    assert len(func({}, c_val, "YEeeEEEEeeeeS.")) == 0
    assert len(func({}, c_val, "What?\nYes!\nBEES.\nOK.")) == 0
    assert len(func({}, c_val, "YES-TA-TOES?")) == 1
    assert len(func({}, c_val, "\n\nYaes.")) == 1

def test_char_exclude():
    constraint = con.default['str_exclude']
    func = constraint['func']
    c_val = {'kw_args': {'exclude': "abcd"}}

    assert len(func({}, c_val, "efg")) == 0
    assert len(func({}, c_val, "abc")) == 1
    assert len(func({}, c_val, "c")) == 1

def test_char_exclude_igonre_case():
    constraint = con.default['str_exclude']
    func = constraint['func']
    c_val = {'kw_args': {'exclude': "abcd", 'ignore_case': True}}

    assert len(func({}, c_val, "efg")) == 0
    assert len(func({}, c_val, "Efg")) == 0
    assert len(func({}, c_val, "abc")) == 1
    assert len(func({}, c_val, "Def")) == 1
    assert len(func({}, c_val, "c")) == 1

def test_ip4():
    constraint = con.default['ip_version']
    func = constraint['func']
    c_val = {'kw_args': {'version': 4}}

    assert len(func({}, c_val, "192.168.1.1")) == 0
    assert len(func({}, c_val, "192.168.1.255")) == 0
    assert len(func({}, c_val, "192.168.3.1/24")) == 0
    assert len(func({}, c_val, "2001:db8::")) == 1
    assert len(func({}, c_val, "2001:db8::/64")) == 1

def test_ip6():
    constraint = con.default['ip_version']
    func = constraint['func']
    c_val = {'kw_args': {'version': 6}}

    assert len(func({}, c_val, "192.168.1.1")) == 1
    assert len(func({}, c_val, "192.168.1.255")) == 1
    assert len(func({}, c_val, "192.168.3.1/24")) == 1
    assert len(func({}, c_val, "2001:db8::")) == 0
    assert len(func({}, c_val, "2001:db8::/64")) == 0
