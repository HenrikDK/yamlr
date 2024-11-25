from datetime import date, datetime
from yamale import validators as val

# Unit test the dictionary of default validators.
def test_validator_defaults():
    assert 'str' in val.default
    assert 'any' in val.default

def test_integer():
    validator = val.default['int']
    func = validator['func']

    assert len(func({}, 1, [], {})) == 0
    assert len(func({}, "1", [], {})) == 1
    assert len(func({}, 1.34, [], {})) == 1

def test_string():
    validator = val.default['str']
    func = validator['func']

    assert len(func({}, "1", [], {})) == 0
    assert len(func({}, 1, [], {})) == 1

def test_regex():
    validator = val.default['regex']
    func = validator['func']
    args = [r"^(abc)\1?de$"]
    kw_args = { 'name': "test regex" }

    assert len(func({}, "abcabcde", args, kw_args)) == 0
    assert len(func({}, "abcabcabcde", args, kw_args)) == 1
    assert len(func({}, "\12", args, kw_args)) == 1

    result = func({}, "woopz", args, kw_args)
    assert result[0] == "'woopz' is not a test regex."

def test_regex_ignore_case():
    validator = val.default['regex']
    func = validator['func']
    args = [r"[a-z0-9]{3,}s\s$"]
    kw_args = { 'ignore_case': True }

    assert len(func({}, "b33S\v", args, kw_args)) == 0
    assert len(func({}, "B33s\t", args, kw_args)) == 0
    assert len(func({}, " b33s ", args, kw_args)) == 1
    assert len(func({}, "b33s  ", args, kw_args)) == 1

    result = func({}, "fdsa", args, kw_args)
    assert result[0] == "'fdsa' is not a regex match."

def test_regex_multiline():
    validator = val.default['regex']
    func = validator['func']
    args = [r"A.+\d$"]
    kw_args = { 'ignore_case': False, 'multiline': True }

    assert len(func({}, "A_-3\n\n", args, kw_args)) == 0
    assert len(func({}, "a!!!!!5\n\n", args, kw_args)) == 1

def test_regex_all_options():
    validator = val.default['regex']
    func = validator['func']
    args = [r".*^Ye.*s\."]
    kw_args = { 'ignore_case': True, 'multiline': True, 'dotall': True }

    assert len(func({}, "YEeeEEEEeeeeS.", args, kw_args)) == 0
    assert len(func({}, "What?\nYes!\nBEES.\nOK.", args, kw_args)) == 0
    assert len(func({}, "YES-TA-TOES?", args, kw_args)) == 1
    assert len(func({}, "\n\nYaes.", args, kw_args)) == 1

def test_number():
    validator = val.default['num']
    func = validator['func']

    assert len(func({}, 1, [], {})) == 0
    assert len(func({}, 1.3425235, [], {})) == 0
    assert len(func({}, "str", [], {})) == 1

def test_boolean():
    validator = val.default['bool']
    func = validator['func']

    assert len(func({}, True, [], {})) == 0
    assert len(func({}, False, [], {})) == 0
    assert len(func({}, "", [], {})) == 1
    assert len(func({}, 0, [], {})) == 1

def test_date():
    validator = val.default['day']
    func = validator['func']

    assert len(func({}, date(2015, 1, 1), [], {})) == 0
    assert len(func({}, datetime(2015, 1, 1, 1), [], {})) == 0
    assert len(func({}, "", [], {})) == 1
    assert len(func({}, 0, [], {})) == 1

def test_datetime():
    validator = val.default['timestamp']
    func = validator['func']

    assert len(func({}, datetime(2015, 1, 1, 1), [], {})) == 0
    assert len(func({}, date(2015, 1, 1), [], {})) == 1
    assert len(func({}, "", [], {})) == 1
    assert len(func({}, 0, [], {})) == 1

def test_list():
    validator = val.default['list']
    func = validator['func']

    assert len(func({}, [], [], {})) == 0
    assert len(func({}, (), [], {})) == 0
    assert len(func({}, "", [], {})) == 1
    assert len(func({}, 0, [], {})) == 1

def test_null():
    validator = val.default['null']
    func = validator['func']

    assert len(func({}, None, [], {})) == 0
    assert len(func({}, "None", [], {})) == 1
    assert len(func({}, 0, [], {})) == 1
    assert len(func({}, float("nan"), [], {})) == 1
    assert len(func({}, {}, [], {})) == 1

def test_ip_valid():
    validator = val.default['ip']
    func = validator['func']

    assert len(func({}, "192.168.1.1", [], {})) == 0
    assert len(func({}, "192.168.1.255", [], {})) == 0
    assert len(func({}, "192.168.3.1/24", [], {})) == 0

    assert len(func({}, "2001:db8::", [], {})) == 0
    assert len(func({}, "2001:db8::/64", [], {})) == 0

def test_ip_invalid():
    validator = val.default['ip']
    func = validator['func']

    assert len(func({}, "257.192.168.1", [], {})) == 1
    assert len(func({}, "192.168.1.256", [], {})) == 1

    assert len(func({}, "2001:db8::/129", [], {})) == 1
    assert len(func({}, "2001:dg8::/127", [], {})) == 1
    assert len(func({}, "asdf", [], {})) == 1

def test_mac_valid():
    validator = val.default['mac']
    func = validator['func']

    assert len(func({}, "12:34:56:78:90:ab", [], {})) == 0
    assert len(func({}, "1234:5678:90ab", [], {})) == 0
    assert len(func({}, "12-34-56-78-90-ab", [], {})) == 0
    assert len(func({}, "1234-5678-90ab", [], {})) == 0

    assert len(func({}, "12:34:56:78:90:AB", [], {})) == 0
    assert len(func({}, "1234:5678:90AB", [], {})) == 0
    assert len(func({}, "12-34-56-78-90-AB", [], {})) == 0
    assert len(func({}, "1234-5678-90AB", [], {})) == 0

    assert len(func({}, "ab:cd:ef:12:34:56", [], {})) == 0
    assert len(func({}, "abcd:ef12:3456", [], {})) == 0
    assert len(func({}, "ab-cd-ef-12-34-56", [], {})) == 0
    assert len(func({}, "abcd-ef12-3456", [], {})) == 0

    assert len(func({}, "AB:CD:EF:12:34:56", [], {})) == 0
    assert len(func({}, "ABCD:EF12:3456", [], {})) == 0
    assert len(func({}, "AB-CD-EF-12-34-56", [], {})) == 0
    assert len(func({}, "ABCD-EF12-3456", [], {})) == 0

def test_mac_invalid():
    validator = val.default['mac']
    func = validator['func']

    assert len(func({}, "qwertyuiop", [], {})) == 1
    assert len(func({}, "qw-er-ty-12-34-56", [], {})) == 1
    assert len(func({}, "ab:cd:ef:12:34:56:78", [], {})) == 1
    assert len(func({}, "abcdefghijkl", [], {})) == 1
    assert len(func({}, "1234567890ax", [], {})) == 1

# https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
# https://regex101.com/r/Ly7O1x/3/

def test_semver_valid():
    validator = val.default['semver']
    func = validator['func']

    assert len(func({}, "0.0.4", [], {})) == 0
    assert len(func({}, "1.2.3", [], {})) == 0
    assert len(func({}, "10.20.30", [], {})) == 0
    assert len(func({}, "1.1.2-prerelease+meta", [], {})) == 0
    assert len(func({}, "1.1.2+meta", [], {})) == 0
    assert len(func({}, "1.1.2+meta-valid", [], {})) == 0
    assert len(func({}, "1.0.0-alpha", [], {})) == 0
    assert len(func({}, "1.0.0-beta", [], {})) == 0
    assert len(func({}, "1.0.0-alpha.beta", [], {})) == 0
    assert len(func({}, "1.0.0-alpha.beta.1", [], {})) == 0
    assert len(func({}, "1.0.0-alpha.1", [], {})) == 0
    assert len(func({}, "1.0.0-alpha0.valid", [], {})) == 0
    assert len(func({}, "1.0.0-alpha.0valid", [], {})) == 0
    assert len(func({}, "1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay", [], {})) == 0
    assert len(func({}, "1.0.0-rc.1+build.1", [], {})) == 0
    assert len(func({}, "2.0.0-rc.1+build.123", [], {})) == 0
    assert len(func({}, "1.2.3-beta", [], {})) == 0
    assert len(func({}, "10.2.3-DEV-SNAPSHOT", [], {})) == 0
    assert len(func({}, "1.2.3-SNAPSHOT-123", [], {})) == 0
    assert len(func({}, "1.0.0", [], {})) == 0
    assert len(func({}, "2.0.0", [], {})) == 0
    assert len(func({}, "1.1.7", [], {})) == 0
    assert len(func({}, "2.0.0+build.1848", [], {})) == 0
    assert len(func({}, "2.0.1-alpha.1227", [], {})) == 0
    assert len(func({}, "1.0.0-alpha+beta", [], {})) == 0
    assert len(func({}, "1.2.3----RC-SNAPSHOT.12.9.1--.12+788", [], {})) == 0
    assert len(func({}, "1.2.3----R-S.12.9.1--.12+meta", [], {})) == 0
    assert len(func({}, "1.2.3----RC-SNAPSHOT.12.9.1--.12", [], {})) == 0
    assert len(func({}, "1.0.0+0.build.1-rc.10000aaa-kk-0.1", [], {})) == 0
    assert len(func({}, "99999999999999999999999.999999999999999999.99999999999999999", [], {})) == 0
    assert len(func({}, "1.0.0-0A.is.legal", [], {})) == 0

def test_semver_invalid():
    validator = val.default['semver']
    func = validator['func']

    assert len(func({}, "1", [], {})) == 1
    assert len(func({}, "1.2", [], {})) == 1
    assert len(func({}, "1.2.3-0123", [], {})) == 1
    assert len(func({}, "1.2.3-0123.0123", [], {})) == 1
    assert len(func({}, "1.1.2+.123", [], {})) == 1
    assert len(func({}, "+invalid", [], {})) == 1
    assert len(func({}, "-invalid", [], {})) == 1
    assert len(func({}, "-invalid+invalid", [], {})) == 1
    assert len(func({}, "-invalid.01", [], {})) == 1
    assert len(func({}, "alpha", [], {})) == 1
    assert len(func({}, "alpha.beta", [], {})) == 1
    assert len(func({}, "alpha.beta.1", [], {})) == 1
    assert len(func({}, "alpha.1", [], {})) == 1
    assert len(func({}, "alpha+beta", [], {})) == 1
    assert len(func({}, "alpha_beta", [], {})) == 1
    assert len(func({}, "alpha.", [], {})) == 1
    assert len(func({}, "alpha..", [], {})) == 1
    assert len(func({}, "beta", [], {})) == 1
    assert len(func({}, "1.0.0-alpha_beta", [], {})) == 1
    assert len(func({}, "-alpha.", [], {})) == 1
    assert len(func({}, "1.0.0-alpha..", [], {})) == 1
    assert len(func({}, "1.0.0-alpha..1", [], {})) == 1
    assert len(func({}, "1.0.0-alpha...1", [], {})) == 1
    assert len(func({}, "1.0.0-alpha....1", [], {})) == 1
    assert len(func({}, "1.0.0-alpha.....1", [], {})) == 1
    assert len(func({}, "1.0.0-alpha......1", [], {})) == 1
    assert len(func({}, "1.0.0-alpha.......1", [], {})) == 1
    assert len(func({}, "01.1.1", [], {})) == 1
    assert len(func({}, "1.01.1", [], {})) == 1
    assert len(func({}, "1.1.01", [], {})) == 1
    assert len(func({}, "1.2", [], {})) == 1
    assert len(func({}, "1.2.3.DEV", [], {})) == 1
    assert len(func({}, "1.2-SNAPSHOT", [], {})) == 1
    assert len(func({}, "1.2.31.2.3----RC-SNAPSHOT.12.09.1--..12+788", [], {})) == 1
    assert len(func({}, "1.2-RC-SNAPSHOT", [], {})) == 1
    assert len(func({}, "-1.0.3-gamma+b7718", [], {})) == 1
    assert len(func({}, "+justmeta", [], {})) == 1
    assert len(func({}, "9.8.7+meta+meta", [], {})) == 1
    assert len(func({}, "9.8.7-whatever+meta+meta", [], {})) == 1
