#!/usr/bin/env python
import os
import ConfigParser


CONF_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'conf'))
CONF_FILE = os.path.join(CONF_DIR, 'kotd.conf')

def get(section, option):
    return config.get(section, option)

def set(section, option, value):
    return config.set(section, option, value)

def read(path):
    return config.read(path)

def save(path):
    return config.write(path)


config = ConfigParser.ConfigParser()
read(CONF_FILE)
