from urllib.parse import urlparse

import validators
import re
import furl
import config


debug = int(config.BaseConfig.DEBUG)

vid_pattern = re.compile("^[a-zA-Z0-9\_\-]{11}$")
http_valid_methods = re.compile("^(GET|HEAD|POST|OPTIONS|PUT|DELETE|CONNECT|TRACE|PATCH)$", re.IGNORECASE)


def is_string(obj):
    return isinstance(obj, str)


def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_valid_hostname(hostname):
    try:
        return validators.domain(hostname) or is_valid_ip_address(hostname)
    except ValueError:
        return False


def is_valid_ip_address(hostname):
    try:
        return validators.ipv4(hostname) or validators.ipv6(hostname)
    except ValueError:
        return False


def is_method(method):
    if not is_string(method):
        return False

    res = http_valid_methods.match(method.upper())
    if res is not None:
        return True

    return False


def valid_rate(s):
    try:
        val = int(s)
        if val < -128 or val > 128:
            return False, val
        return True, val
    except ValueError:
        return False, -1


def is_valid_port(s):
    try:
        val = int(s)
        if val < 1 or val > 65536:
            return False, val
        return True, val
    except ValueError:
        return False, -1


def is_valid_score(s):
    try:
        val = int(s)
        if val < -16384 or val > 16384:
            return False, val
        return True, val
    except ValueError:
        return False, -1

def is_valid_title(s):
    return is_string(s) and len(s) > 1


def is_valid_vid(s):
    return vid_pattern.match(s)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# https://pythex.org/
# https://github.com/kvesteri/validators/blob/master/validators/email.py
# https://regexr.com/3anm9
# https://regexr.com/3dj5t
# https://regex101.com/r/rN1qR5/2

def prefix_match(s, prefix_list):
    if is_string(s) is False:
        return False
    for prefix in prefix_list:
        if s.startswith(prefix):
            return True
    return False


def suffix_match(s, suffix_list):
    if is_string(s) is False:
        return False
    for suffix in suffix_list:
        if s.endswith(suffix):
            return True
    return False


def regex_list_match(s, regex_list):
    if is_string(s) is False:
        return False
    for s_regex in regex_list:
        res = re.search(s_regex, s)
        if res is not None:
            return res

    return None


def sort_url_query(request_url):
    testurl = furl.furl(request_url.url)
    keysOrderDict = sorted(testurl.query.params.keys())
    newquerystr = ""
    for i in keysOrderDict:
        if len(newquerystr) > 0:
            newquerystr = newquerystr + "&" + i + "=" + testurl.query.params[i]
        else:
            newquerystr = + i + "=" + testurl.query.params[i]
    return newquerystr
