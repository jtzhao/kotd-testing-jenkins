#!/usr/bin/env python
import commands
import logging

logger = logging.getLogger(__name__)

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
