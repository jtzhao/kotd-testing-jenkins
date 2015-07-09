#!/usr/bin/env python
import requests
import re
from kotd_config import config
from kotd_rpm import rpm_version_cmp


def kotd_get_file_list():
    url = config.get('kotd', 'base_url').format(release=config.get('kotd', 'release'),
                                                arch=config.get('kotd', 'arch'))
    res = requests.get(url)
    if res.status_code not in [200, 201]:
        return None
    file_list = re.findall(r'[\w\-_.]+.rpm', res.text)
    file_list = list(set(file_list))
    return file_list

def kotd_get_package_list(package_name, file_list=None):
    if file_list is None:
        file_list = kotd_get_file_list()
    # filter rpms
    def filter_rpm(file_name):
        if re.search(r'%s-[\d.]+-[\d.]+' % (package_name),
                    file_name):
            return True
        return False
    return filter(filter_rpm, file_list)

def kotd_get_latest_package(package_name, package_list=None):
    if package_list is None:
        package_list = kotd_get_package_list(package_name)
    sentinel = '%s-0-0.noarch.rpm'    # sentinel
    latest = sentinel
    for item in package_list:
        if rpm_version_cmp(item, latest) == 1:
            latest = item
    if latest == sentinel:
        return None
    return latest
