#!/usr/bin/env python
import re
import kotd_utils

def parse_rpm_name(rpm_file_name):
    rpm_file_name = rpm_file_name.strip()
    arch = rpm_file_name.split('.')[-2]
    match = re.search(r'^([^\d][\w\-_]+)-(\d+(?:\.\d+)*)-(.*)\.%s\.rpm' % arch,
                    rpm_file_name)
    if match is not None:
        return {'name': match.group(1),
                'arch': arch,
                'version': match.group(2),
                'release': match.group(3)}
    return None

def install_rpm(name_or_path, logger=None):
    cmd = "zypper install -y '%s'" % name_or_path
    return utils.run_shell(cmd, logger)

def rpm_version_cmp(rpm1, rpm2):
    rpm_info1 = parse_rpm_name(rpm1)
    rpm_info2 = parse_rpm_name(rpm2)
    if not (rpm_info1 and rpm_info2):
        return None
    ret = kotd_utils.version_cmp(rpm_info1['version'], rpm_info2['version'])
    if ret != 0:
        return ret
    ret = kotd_utils.version_cmp(rpm_info1['release'], rpm_info2['release'])
    return ret
