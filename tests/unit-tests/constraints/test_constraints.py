import datetime
from yamale.validators import constraints as con

def test_length_min():
    constraint = con.constraints['length_min']
    func = constraint['func']
    args = {'min':2}
    
    assert len(func("abcd", constraint, args)) == 0
    assert len(func("ab", constraint, args)) == 0
    assert len(func("a", constraint, args)) == 1

def test_length_max():
    constraint = con.constraints['length_max']
    func = constraint['func']
    args = {'max':3}

    assert len(func("abc", constraint, args)) == 0
    assert len(func("ab", constraint, args)) == 0
    assert len(func("abcd", constraint, args)) == 1

def test_number_max():
    constraint = con.constraints['max']
    func = constraint['func']
    args = {'max':10}

    assert len(func(4, constraint, args)) == 0
    assert len(func(10, constraint, args)) == 0
    assert len(func(11, constraint, args)) == 1

def test_number_min():
    constraint = con.constraints['min']
    func = constraint['func']
    args = {'min':0.5}

    assert len(func(4, constraint, args)) == 0
    assert len(func(0.5, constraint, args)) == 0
    assert len(func(0.1, constraint, args)) == 1

def test_timestamp_min():
    constraint = con.constraints['min']
    func = constraint['func']
    args = {'min':datetime.datetime(2010, 1, 1)}

    assert len(func(datetime.datetime(2010, 1, 1), constraint, args)) == 0
    assert len(func(datetime.datetime(2011, 2, 2), constraint, args)) == 0
    assert len(func(datetime.datetime(2009, 12, 31), constraint, args)) == 1

def test_timestamp_max():
    constraint = con.constraints['max']
    func = constraint['func']
    args = {'max':datetime.datetime(2010, 1, 1)}

    assert len(func(datetime.datetime(2010, 1, 1), constraint, args)) == 0
    assert len(func(datetime.datetime(2009, 2, 2), constraint, args)) == 0
    assert len(func(datetime.datetime(2010, 2, 2), constraint, args)) == 1

def test_day_min():
    constraint = con.constraints['min']
    func = constraint['func']
    args = {'min':datetime.date(2010, 1, 1)}

    assert len(func(datetime.date(2010, 1, 1), constraint, args)) == 0
    assert len(func(datetime.date(2011, 2, 2), constraint, args)) == 0
    assert len(func(datetime.date(2009, 12, 31), constraint, args)) == 1

def test_day_max():
    constraint = con.constraints['max']
    func = constraint['func']
    args = {'max':datetime.date(2010, 1, 1)}

    assert len(func(datetime.date(2010, 1, 1), constraint, args)) == 0
    assert len(func(datetime.date(2009, 2, 2), constraint, args)) == 0
    assert len(func(datetime.date(2010, 2, 2), constraint, args)) == 1

def test_str_equals():
    constraint = con.constraints['str_equals']
    func = constraint['func']
    args = {'equals':"abcd"}

    assert len(func("abcd", constraint, args)) == 0
    assert len(func("abcde", constraint, args)) == 1
    assert len(func("c", constraint, args)) == 1

def test_str_equals_ignore_case():
    constraint = con.constraints['str_equals']
    func = constraint['func']
    args = {'equals':"abcd", 'ignore_case': True}

    assert len(func("abCd", constraint, args)) == 0
    assert len(func("abcde", constraint, args)) == 1
    assert len(func("C", constraint, args)) == 1

def test_str_starts_with():
    constraint = con.constraints['str_starts_with']
    func = constraint['func']
    args = {'starts_with':"abc"}

    assert len(func("abcd", constraint, args)) == 0
    assert len(func("bcd", constraint, args)) == 1
    assert len(func("c", constraint, args)) == 1

def test_str_starts_with_ignore_case():
    constraint = con.constraints['str_starts_with']
    func = constraint['func']
    args = {'starts_with':"abC", 'ignore_case': True}

    assert len(func("abCde", constraint, args)) == 0
    assert len(func("abcde", constraint, args)) == 0
    assert len(func("bcd", constraint, args)) == 1
    assert len(func("C", constraint, args)) == 1

def test_str_ends_with():
    constraint = con.constraints['str_ends_with']
    func = constraint['func']
    args = {'ends_with':"abcd"}

    assert len(func("abcd", constraint, args)) == 0
    assert len(func("abcde", constraint, args)) == 1
    assert len(func("c", constraint, args)) == 1

def test_str_ends_with_ignore_case():
    v = val.String(ends_with="abC", ignore_case=True)
    assert v.is_valid("xyzabC")
    assert v.is_valid("xyzabc")
    assert not v.is_valid("cde")
    assert not v.is_valid("C")


tmp = '''



def test_str_matches():
    v = val.String(matches=r"^(abc)\1?de$")
    assert v.is_valid("abcabcde")
    assert not v.is_valid("abcabcabcde")
    assert not v.is_valid("\12")

    v = val.String(matches=r"[a-z0-9]{3,}s\s$", ignore_case=True)
    assert v.is_valid("b33S\v")
    assert v.is_valid("B33s\t")
    assert not v.is_valid(" b33s ")
    assert not v.is_valid("b33s  ")

    v = val.String(matches=r"A.+\d$", ignore_case=False, multiline=True)
    assert v.is_valid("A_-3\n\n")
    assert not v.is_valid("a!!!!!5\n\n")

    v = val.String(matches=r".*^Ye.*s\.", ignore_case=True, multiline=True, dotall=True)
    assert v.is_valid("YEeeEEEEeeeeS.")
    assert v.is_valid("What?\nYes!\nBEES.\nOK.")
    assert not v.is_valid("YES-TA-TOES?")
    assert not v.is_valid("\n\nYaes.")


def test_char_exclude():
    v = val.String(exclude="abcd")
    assert v.is_valid("efg")
    assert not v.is_valid("abc")
    assert not v.is_valid("c")


def test_char_exclude_igonre_case():
    v = val.String(exclude="abcd", ignore_case=True)
    assert v.is_valid("efg")
    assert v.is_valid("Efg")
    assert not v.is_valid("abc")
    assert not v.is_valid("Def")
    assert not v.is_valid("c")


def test_ip4():
    v = val.Ip(version=4)
    assert v.is_valid("192.168.1.1")
    assert v.is_valid("192.168.1.255")
    assert v.is_valid("192.168.3.1/24")
    assert not v.is_valid("2001:db8::")
    assert not v.is_valid("2001:db8::/64")


def test_ip6():
    v = val.Ip(version=6)
    assert not v.is_valid("192.168.1.1")
    assert not v.is_valid("192.168.1.255")
    assert not v.is_valid("192.168.3.1/24")
    assert v.is_valid("2001:db8::")
    assert v.is_valid("2001:db8::/64")
'''
