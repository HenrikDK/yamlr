from datetime import date, datetime
from yamale import validators as val

# Unit test the dictionary of default validators.
def test_validator_defaults():
    assert 'str' in val.default
    assert 'any' in val.default

def test_integer():
    validator = val.default['int']
    func = validator['func']
    c_val = {'args': [], 'kw_args': {}}

    assert len(func({}, c_val, 1)) == 0
    assert len(func({}, c_val, "1")) == 1
    assert len(func({}, c_val, 1.34)) == 1

def test_string():
    validator = val.default['str']
    func = validator['func']
    c_val = {'args': [], 'kw_args': {}}

    assert len(func({}, c_val, "1")) == 0
    assert len(func({}, c_val, 1)) == 1

def test_regex():
    validator = val.default['regex']
    func = validator['func']
    c_val = {'args': [r"^(abc)\1?de$"], 'kw_args': { 'name': "test regex" }}

    assert len(func({}, c_val, "abcabcde")) == 0
    assert len(func({}, c_val, "abcabcabcde")) == 1
    assert len(func({}, c_val, "\12")) == 1

    result = func({}, c_val, "woopz")
    assert result[0] == "'woopz' is not a test regex."

def test_regex_ignore_case():
    validator = val.default['regex']
    func = validator['func']
    c_val = {'args': [r"[a-z0-9]{3,}s\s$"], 'kw_args': { 'ignore_case': True }}

    assert len(func({}, c_val, "b33S\v")) == 0
    assert len(func({}, c_val, "B33s\t")) == 0
    assert len(func({}, c_val, " b33s ")) == 1
    assert len(func({}, c_val, "b33s  ")) == 1

    result = func({}, c_val, "fdsa")
    assert result[0] == "'fdsa' is not a regex match."

def test_regex_multiline():
    validator = val.default['regex']
    func = validator['func']
    c_val = {'args': [r"A.+\d$"], 'kw_args': { 'ignore_case': False, 'multiline': True }}

    assert len(func({}, c_val, "A_-3\n\n")) == 0
    assert len(func({}, c_val, "a!!!!!5\n\n")) == 1

def test_regex_all_options():
    validator = val.default['regex']
    func = validator['func']
    c_val = {'args': [r".*^Ye.*s\."], 'kw_args': { 'ignore_case': True, 'multiline': True, 'dotall': True }}

    assert len(func({}, c_val, "YEeeEEEEeeeeS.")) == 0
    assert len(func({}, c_val, "What?\nYes!\nBEES.\nOK.")) == 0
    assert len(func({}, c_val, "YES-TA-TOES?")) == 1
    assert len(func({}, c_val, "\n\nYaes.")) == 1

def test_number():
    validator = val.default['num']
    func = validator['func']
    c_val = {'args': [], 'kw_args': {}}

    assert len(func({}, c_val, 1)) == 0
    assert len(func({}, c_val, 1.3425235)) == 0
    assert len(func({}, c_val, "str")) == 1

def test_boolean():
    validator = val.default['bool']
    func = validator['func']
    c_val = {'args': [], 'kw_args': {}}

    assert len(func({}, c_val, True)) == 0
    assert len(func({}, c_val, False)) == 0
    assert len(func({}, c_val, "")) == 1
    assert len(func({}, c_val, 0)) == 1

def test_date():
    validator = val.default['day']
    func = validator['func']
    c_val = {'args': [], 'kw_args': {}}

    assert len(func({}, c_val, date(2015, 1, 1))) == 0
    assert len(func({}, c_val, datetime(2015, 1, 1, 1))) == 0
    assert len(func({}, c_val, "")) == 1
    assert len(func({}, c_val, 0)) == 1

def test_datetime():
    validator = val.default['timestamp']
    func = validator['func']
    c_val = {'args': [], 'kw_args': {}}

    assert len(func({}, c_val, datetime(2015, 1, 1, 1))) == 0
    assert len(func({}, c_val, date(2015, 1, 1))) == 1
    assert len(func({}, c_val, "")) == 1
    assert len(func({}, c_val, 0)) == 1

def test_list():
    validator = val.default['list']
    func = validator['func']
    c_val = {'args': [], 'kw_args': {}}

    assert len(func({}, c_val, [])) == 0
    assert len(func({}, c_val, ())) == 0
    assert len(func({}, c_val, "")) == 1
    assert len(func({}, c_val, 0)) == 1

def test_null():
    validator = val.default['null']
    func = validator['func']
    c_val = {'args': [], 'kw_args': {}}

    assert len(func({}, c_val, None)) == 0
    assert len(func({}, c_val, "None")) == 1
    assert len(func({}, c_val, 0)) == 1
    assert len(func({}, c_val, float("nan"))) == 1
    assert len(func({}, c_val, {})) == 1

def test_ip_valid():
    validator = val.default['ip']
    func = validator['func']
    c_val = {'args': [], 'kw_args': {}}

    assert len(func({}, c_val, "192.168.1.1")) == 0
    assert len(func({}, c_val, "192.168.1.255")) == 0
    assert len(func({}, c_val, "192.168.3.1/24")) == 0

    assert len(func({}, c_val, "2001:db8::")) == 0
    assert len(func({}, c_val, "2001:db8::/64")) == 0

def test_ip_invalid():
    validator = val.default['ip']
    func = validator['func']
    c_val = {'args': [], 'kw_args': {}}

    assert len(func({}, c_val, "257.192.168.1")) == 1
    assert len(func({}, c_val, "192.168.1.256")) == 1

    assert len(func({}, c_val, "2001:db8::/129")) == 1
    assert len(func({}, c_val, "2001:dg8::/127")) == 1
    assert len(func({}, c_val, "asdf")) == 1

def test_mac_valid():
    validator = val.default['mac']
    func = validator['func']
    c_val = {'args': [], 'kw_args': {}}

    assert len(func({}, c_val, "12:34:56:78:90:ab")) == 0
    assert len(func({}, c_val, "1234:5678:90ab")) == 0
    assert len(func({}, c_val, "12-34-56-78-90-ab")) == 0
    assert len(func({}, c_val, "1234-5678-90ab")) == 0

    assert len(func({}, c_val, "12:34:56:78:90:AB")) == 0
    assert len(func({}, c_val, "1234:5678:90AB")) == 0
    assert len(func({}, c_val, "12-34-56-78-90-AB")) == 0
    assert len(func({}, c_val, "1234-5678-90AB")) == 0

    assert len(func({}, c_val, "ab:cd:ef:12:34:56")) == 0
    assert len(func({}, c_val, "abcd:ef12:3456")) == 0
    assert len(func({}, c_val, "ab-cd-ef-12-34-56")) == 0
    assert len(func({}, c_val, "abcd-ef12-3456")) == 0

    assert len(func({}, c_val, "AB:CD:EF:12:34:56")) == 0
    assert len(func({}, c_val, "ABCD:EF12:3456")) == 0
    assert len(func({}, c_val, "AB-CD-EF-12-34-56")) == 0
    assert len(func({}, c_val, "ABCD-EF12-3456")) == 0

def test_mac_invalid():
    validator = val.default['mac']
    func = validator['func']
    c_val = {'args': [], 'kw_args': {}}

    assert len(func({}, c_val, "qwertyuiop")) == 1
    assert len(func({}, c_val, "qw-er-ty-12-34-56")) == 1
    assert len(func({}, c_val, "ab:cd:ef:12:34:56:78")) == 1
    assert len(func({}, c_val, "abcdefghijkl")) == 1
    assert len(func({}, c_val, "1234567890ax")) == 1

# https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
# https://regex101.com/r/Ly7O1x/3/

def test_semver_valid():
    validator = val.default['semver']
    func = validator['func']
    c_val = {'args': [], 'kw_args': {}}

    assert len(func({}, c_val, "0.0.4")) == 0
    assert len(func({}, c_val, "1.2.3")) == 0
    assert len(func({}, c_val, "10.20.30")) == 0
    assert len(func({}, c_val, "1.1.2-prerelease+meta")) == 0
    assert len(func({}, c_val, "1.1.2+meta")) == 0
    assert len(func({}, c_val, "1.1.2+meta-valid")) == 0
    assert len(func({}, c_val, "1.0.0-alpha")) == 0
    assert len(func({}, c_val, "1.0.0-beta")) == 0
    assert len(func({}, c_val, "1.0.0-alpha.beta")) == 0
    assert len(func({}, c_val, "1.0.0-alpha.beta.1")) == 0
    assert len(func({}, c_val, "1.0.0-alpha.1")) == 0
    assert len(func({}, c_val, "1.0.0-alpha0.valid")) == 0
    assert len(func({}, c_val, "1.0.0-alpha.0valid")) == 0
    assert len(func({}, c_val, "1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay")) == 0
    assert len(func({}, c_val, "1.0.0-rc.1+build.1")) == 0
    assert len(func({}, c_val, "2.0.0-rc.1+build.123")) == 0
    assert len(func({}, c_val, "1.2.3-beta")) == 0
    assert len(func({}, c_val, "10.2.3-DEV-SNAPSHOT")) == 0
    assert len(func({}, c_val, "1.2.3-SNAPSHOT-123")) == 0
    assert len(func({}, c_val, "1.0.0")) == 0
    assert len(func({}, c_val, "2.0.0")) == 0
    assert len(func({}, c_val, "1.1.7")) == 0
    assert len(func({}, c_val, "2.0.0+build.1848")) == 0
    assert len(func({}, c_val, "2.0.1-alpha.1227")) == 0
    assert len(func({}, c_val, "1.0.0-alpha+beta")) == 0
    assert len(func({}, c_val, "1.2.3----RC-SNAPSHOT.12.9.1--.12+788")) == 0
    assert len(func({}, c_val, "1.2.3----R-S.12.9.1--.12+meta")) == 0
    assert len(func({}, c_val, "1.2.3----RC-SNAPSHOT.12.9.1--.12")) == 0
    assert len(func({}, c_val, "1.0.0+0.build.1-rc.10000aaa-kk-0.1")) == 0
    assert len(func({}, c_val, "99999999999999999999999.999999999999999999.99999999999999999")) == 0
    assert len(func({}, c_val, "1.0.0-0A.is.legal")) == 0

def test_semver_invalid():
    validator = val.default['semver']
    func = validator['func']
    c_val = {'args': [], 'kw_args': {}}

    assert len(func({}, c_val, "1")) == 1
    assert len(func({}, c_val, "1.2")) == 1
    assert len(func({}, c_val, "1.2.3-0123")) == 1
    assert len(func({}, c_val, "1.2.3-0123.0123")) == 1
    assert len(func({}, c_val, "1.1.2+.123")) == 1
    assert len(func({}, c_val, "+invalid")) == 1
    assert len(func({}, c_val, "-invalid")) == 1
    assert len(func({}, c_val, "-invalid+invalid")) == 1
    assert len(func({}, c_val, "-invalid.01")) == 1
    assert len(func({}, c_val, "alpha")) == 1
    assert len(func({}, c_val, "alpha.beta")) == 1
    assert len(func({}, c_val, "alpha.beta.1")) == 1
    assert len(func({}, c_val, "alpha.1")) == 1
    assert len(func({}, c_val, "alpha+beta")) == 1
    assert len(func({}, c_val, "alpha_beta")) == 1
    assert len(func({}, c_val, "alpha.")) == 1
    assert len(func({}, c_val, "alpha..")) == 1
    assert len(func({}, c_val, "beta")) == 1
    assert len(func({}, c_val, "1.0.0-alpha_beta")) == 1
    assert len(func({}, c_val, "-alpha.")) == 1
    assert len(func({}, c_val, "1.0.0-alpha..")) == 1
    assert len(func({}, c_val, "1.0.0-alpha..1")) == 1
    assert len(func({}, c_val, "1.0.0-alpha...1")) == 1
    assert len(func({}, c_val, "1.0.0-alpha....1")) == 1
    assert len(func({}, c_val, "1.0.0-alpha.....1")) == 1
    assert len(func({}, c_val, "1.0.0-alpha......1")) == 1
    assert len(func({}, c_val, "1.0.0-alpha.......1")) == 1
    assert len(func({}, c_val, "01.1.1")) == 1
    assert len(func({}, c_val, "1.01.1")) == 1
    assert len(func({}, c_val, "1.1.01")) == 1
    assert len(func({}, c_val, "1.2")) == 1
    assert len(func({}, c_val, "1.2.3.DEV")) == 1
    assert len(func({}, c_val, "1.2-SNAPSHOT")) == 1
    assert len(func({}, c_val, "1.2.31.2.3----RC-SNAPSHOT.12.09.1--..12+788")) == 1
    assert len(func({}, c_val, "1.2-RC-SNAPSHOT")) == 1
    assert len(func({}, c_val, "-1.0.3-gamma+b7718")) == 1
    assert len(func({}, c_val, "+justmeta")) == 1
    assert len(func({}, c_val, "9.8.7+meta+meta")) == 1
    assert len(func({}, c_val, "9.8.7-whatever+meta+meta")) == 1
