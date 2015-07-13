import os
import requests
from kotd_config import config


def trigger(fullname, args={}, headers={}):
    names = fullname.split('/')
    jenkins_port = ":%s" % config.get('jenkins', 'port') if config.has_option('jenkins', 'port') else ''
    base_url = "http://%s%s" % (config.get('jenkins', 'host'), jenkins_port)
    url = "%s/%s" % (base_url,
                    ''.join(["job/%s/" % (item) for item in names]))
    res = requests.post(url, data=args, headers=headers)
    if res.status_code not in [200, 201, 202]:
        return False
    return True
