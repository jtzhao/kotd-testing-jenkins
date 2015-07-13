#!/usr/bin/env python
import commands
import logging
import re
import requests

logger = logging.getLogger(__name__)

def url_join(*args):
    assert len(args) > 0, "argument list can't be empty"
    if 1 == len(args):
        return args[0]
    lst = [args[0]]
    for i in range(1, len(args)):
        if not(args[i-1].endswith('/') or args[i].startswith('/')):
            lst.append('/')
        lst.append(args[i])
    return ''.join(lst)


def run_shell(cmd, logger):
    ret, output = commands.getstatusoutput(cmd)
    if logger:
        logger.debug(">$ %s" % cmd)
        logger.debug(output)
    return ret


def version_cmp(ver1, ver2):
    ver1_parts = ver1.split('.')
    ver2_parts = ver2.split('.')
    if len(ver1_parts) != len(ver2_parts):
        logger.warning("version %s and %s have different length" % (ver1, ver2))
    len1 = len(ver1_parts)
    len2 = len(ver1_parts)
    length = len1 if len1 > len2 else len2
    for i in range(0, length):
        # Convert version number to int if possible
        try:
            val1 = int(ver1_parts[i])
            val2 = int(ver2_parts[i])
        except ValueError:
            val1 = ver1_parts[i]
            val2 = ver2_parts[i]
        except IndexError, e:
            if len1 > len2:
                return 1
            elif len1 < len2:
                return -1
            else:
                raise e
        # Compare them
        if val1 > val2:
            return 1
        elif val1 < val2:
            return -1
        else:
            continue
    return 0


def get_links(url):
    res = requests.get(url, allow_redirects=True)
    if res.status_code in [200, 201, 202]:
        matches = re.findall(r'''href=(?:'|")([^'"]*)(?:'|")''',
                            res.text,
                            re.I)
        matches = list(set(matches))
        for i in range(0, len(matches)):
            if not(matches[i].startswith('http') or
                    matches[i].startswith('ftp')):
                matches[i] = url_join(url, matches[i])
        return matches
    return None
