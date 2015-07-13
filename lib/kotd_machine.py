#!/usr/bin/env python
import paramiko
import re
import requests
import kotd_logger
import kotd_config
import kotd_utils

logger = kotd_logger.get_logger(__name__)

def get_installation_url(release, arch):
    url = kotd_config.get('install', 'repo')
    url = kotd_utils.url_join(url, release, arch, '/')
    links = kotd_utils.get_links(url)
    print links
    for item in links:
        if item.endswith('DVD1/') or item.endswith('dvd1/'):
            return item
    raise StandardError("Couldn't find proper installation link in %s" % (url))


def run_shell(ip, cmd_or_file, port=22, username=None, password=None, timeout=None):
    def _filter(item):
        if item.strip().startswith('#'):
            return False
        return True

    if isinstance(cmd_or_file, file):
        lines = cmd_or_file.readlines()
        cmd_or_file = '\n'.join(filter(_filter, lines))
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=username, password=password)
    chan = client.get_transport().open_session()
    logger.debug("%s> %s" % (ip, cmd_or_file))
    ret = chan.recv_exit_status()
    return ret

def reboot(ip, port=22, username=None, password=None, timeout=None):
    return run_shell(ip, 'reboot', port=port, username=username, password=password, timeout=timeout)

def reinstall(ip, port=22, username=None, password=None, timeout=None):
    repo = kotd_config.get('install', 'repo')
    return run_shell(ip, "/usr/share/qa/tools/install.pl '%s' -f ext3" % (repo))
