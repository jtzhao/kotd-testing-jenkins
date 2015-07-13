#!/usr/bin/env python
import argparse
import json
import paramiko
import os
import sys
LIB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib'))
CONF_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'conf'))
sys.path.append(LIB_DIR)
import kotd
import kotd_config
import kotd_logger

if __name__ == '__main__':
    logger = kotd_logger.get_logger(__file__)
    #latest = kotd.kotd_get_latest_package('kernel-default')
    parser = argparse.ArgumentParser(description='Monitor kotd updates')
    parser.add_argument('release', help='OS version the kotd kernels belong to')
    parser.add_argument('arch', type=str, nargs='+',
                        help='architectures to be tested')
    parser.add_argument('-f', '--file', dest='file', type=str,
                        default='/tmp/kotd.dat', help='Already tested kernel')
    parser.add_argument('-i', '--install', dest='install', type=str,
                        help='SLE version to be installed')
    # TBD
    #parser.add_argument('-d', '--daemon', action="store_true",
    #                    help='Run monitor as a daemon')
    args = parser.parse_args()
    print args

    # Check machine status
    machine_data_file = os.path.join(CONF_DIR, 'machines')
    try:
        f = file(machine_data_file, 'r')
        machine_data = json.load(f)
        f.close()
    except ValueError, e:
        logger.error("%s is not in json format" % (machine_data_file))
        exit(255)
    except IOError, e:
        logger.error("Unable to open %s" % (machine_data_file))
        exit(255)
    # Use ssh to check machine status
