#!/usr/bin/env python
import logging
import kotd_config

def config(**kwargs):
    if isinstance(kwargs['level'], basestring):
        kwargs['level'] = getattr(logging, kwargs['level'])
    logging.basicConfig(**kwargs)

def get_logger(name, level=None):
    logger = logging.getLogger(name)
    if level is not None:
        level = getattr(logging, level)
    logger.setLevel(level)
    return logger

config(level=kotd_config.get('log', 'level'))
