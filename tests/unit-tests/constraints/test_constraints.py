import datetime
from yamale import constraints as con

def test_length_min():
    constraint = con.default['length_min']
    func = constraint['func']
    args = {'min':2}
    
    assert len(func("abcd", constraint, args)) == 0
    assert len(func("ab", constraint, args)) == 0
    assert len(func("a", constraint, args)) == 1

def test_length_max():
    constraint = con.default['length_max']
    func = constraint['func']
    args = {'max':3}

    assert len(func("abc", constraint, args)) == 0
    assert len(func("ab", constraint, args)) == 0
    assert len(func("abcd", constraint, args)) == 1

def test_number_max():
    constraint = con.default['max']
    func = constraint['func']
    args = {'max':10}

    assert len(func(4, constraint, args)) == 0
    assert len(func(10, constraint, args)) == 0
    assert len(func(11, constraint, args)) == 1

def test_number_min():
    constraint = con.default['min']
    func = constraint['func']
    args = {'min':0.5}

    assert len(func(4, constraint, args)) == 0
    assert len(func(0.5, constraint, args)) == 0
    assert len(func(0.1, constraint, args)) == 1

def test_timestamp_min():
    constraint = con.default['min']
    func = constraint['func']
    args = {'min':datetime.datetime(2010, 1, 1)}

    assert len(func(datetime.datetime(2010, 1, 1), constraint, args)) == 0
    assert len(func(datetime.datetime(2011, 2, 2), constraint, args)) == 0
    assert len(func(datetime.datetime(2009, 12, 31), constraint, args)) == 1

def test_timestamp_max():
    constraint = con.default['max']
    func = constraint['func']
    args = {'max':datetime.datetime(2010, 1, 1)}

    assert len(func(datetime.datetime(2010, 1, 1), constraint, args)) == 0
    assert len(func(datetime.datetime(2009, 2, 2), constraint, args)) == 0
    assert len(func(datetime.datetime(2010, 2, 2), constraint, args)) == 1

def test_day_min():
    constraint = con.default['min']
    func = constraint['func']
    args = {'min':datetime.date(2010, 1, 1)}

    assert len(func(datetime.date(2010, 1, 1), constraint, args)) == 0
    assert len(func(datetime.date(2011, 2, 2), constraint, args)) == 0
    assert len(func(datetime.date(2009, 12, 31), constraint, args)) == 1

def test_day_max():
    constraint = con.default['max']
    func = constraint['func']
    args = {'max':datetime.date(2010, 1, 1)}

    assert len(func(datetime.date(2010, 1, 1), constraint, args)) == 0
    assert len(func(datetime.date(2009, 2, 2), constraint, args)) == 0
    assert len(func(datetime.date(2010, 2, 2), constraint, args)) == 1

def test_str_equals():
    constraint = con.default['str_equals']
    func = constraint['func']
    args = {'equals':"abcd"}

    assert len(func("abcd", constraint, args)) == 0
    assert len(func("abcde", constraint, args)) == 1
    assert len(func("c", constraint, args)) == 1

def test_str_equals_ignore_case():
    constraint = con.default['str_equals']
    func = constraint['func']
    args = {'equals':"abcd", 'ignore_case': True}

    assert len(func("abCd", constraint, args)) == 0
    assert len(func("abcde", constraint, args)) == 1
    assert len(func("C", constraint, args)) == 1

def test_str_starts_with():
    constraint = con.default['str_starts_with']
    func = constraint['func']
    args = {'starts_with':"abc"}

    assert len(func("abcd", constraint, args)) == 0
    assert len(func("bcd", constraint, args)) == 1
    assert len(func("c", constraint, args)) == 1

def test_str_starts_with_ignore_case():
    constraint = con.default['str_starts_with']
    func = constraint['func']
    args = {'starts_with':"abC", 'ignore_case': True}

    assert len(func("abCde", constraint, args)) == 0
    assert len(func("abcde", constraint, args)) == 0
    assert len(func("bcd", constraint, args)) == 1
    assert len(func("C", constraint, args)) == 1

def test_str_ends_with():
    constraint = con.default['str_ends_with']
    func = constraint['func']
    args = {'ends_with':"abcd"}

    assert len(func("abcd", constraint, args)) == 0
    assert len(func("abcde", constraint, args)) == 1
    assert len(func("c", constraint, args)) == 1

def test_str_ends_with_ignore_case():
    constraint = con.default['str_ends_with']
    func = constraint['func']
    args = {'ends_with':"abC", 'ignore_case': True}

    assert len(func("xyzabC", constraint, args)) == 0
    assert len(func("xyzabc", constraint, args)) == 0
    assert len(func("cde", constraint, args)) == 1
    assert len(func("C", constraint, args)) == 1

def test_str_matches():
    constraint = con.default['str_matches']
    func = constraint['func']
    args = {'matches':r"^(abc)\1?de$"}

    assert len(func("abcabcde", constraint, args)) == 0
    assert len(func("abcabcabcde", constraint, args)) == 1
    assert len(func("\12", constraint, args)) == 1

def test_str_matches_ignore_case():
    constraint = con.default['str_matches']
    func = constraint['func']
    args = {'matches':r"[a-z0-9]{3,}s\s$", 'ignore_case': True}

    assert len(func("b33S\v", constraint, args)) == 0
    assert len(func("B33s\t", constraint, args)) == 0
    assert len(func(" b33s ", constraint, args)) == 1
    assert len(func("b33s  ", constraint, args)) == 1

def test_str_matches_multi():
    constraint = con.default['str_matches']
    func = constraint['func']
    args = {'matches':r"A.+\d$", 'multiline': True}

    assert len(func("A_-3\n\n", constraint, args)) == 0
    assert len(func("a!!!!!5\n\n", constraint, args)) == 1

def test_str_matches_ignore_case_multi_dotall():
    constraint = con.default['str_matches']
    func = constraint['func']
    args = {'matches':r".*^Ye.*s\.", 'ignore_case': True, 'multiline': True, 'dotall': True}

    assert len(func("YEeeEEEEeeeeS.", constraint, args)) == 0
    assert len(func("What?\nYes!\nBEES.\nOK.", constraint, args)) == 0
    assert len(func("YES-TA-TOES?", constraint, args)) == 1
    assert len(func("\n\nYaes.", constraint, args)) == 1

def test_char_exclude():
    constraint = con.default['str_exclude']
    func = constraint['func']
    args = {'exclude': "abcd"}

    assert len(func("efg", constraint, args)) == 0
    assert len(func("abc", constraint, args)) == 1
    assert len(func("c", constraint, args)) == 1

def test_char_exclude_igonre_case():
    constraint = con.default['str_exclude']
    func = constraint['func']
    args = {'exclude': "abcd", 'ignore_case': True}

    assert len(func("efg", constraint, args)) == 0
    assert len(func("Efg", constraint, args)) == 0
    assert len(func("abc", constraint, args)) == 1
    assert len(func("Def", constraint, args)) == 1
    assert len(func("c", constraint, args)) == 1

def test_ip4():
    constraint = con.default['ip_version']
    func = constraint['func']
    args = {'version': 4}

    assert len(func("192.168.1.1", constraint, args)) == 0
    assert len(func("192.168.1.255", constraint, args)) == 0
    assert len(func("192.168.3.1/24", constraint, args)) == 0
    assert len(func("2001:db8::", constraint, args)) == 1
    assert len(func("2001:db8::/64", constraint, args)) == 1

def test_ip6():
    constraint = con.default['ip_version']
    func = constraint['func']
    args = {'version': 6}

    assert len(func("192.168.1.1", constraint, args)) == 1
    assert len(func("192.168.1.255", constraint, args)) == 1
    assert len(func("192.168.3.1/24", constraint, args)) == 1
    assert len(func("2001:db8::", constraint, args)) == 0
    assert len(func("2001:db8::/64", constraint, args)) == 0
