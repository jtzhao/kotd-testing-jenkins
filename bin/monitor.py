#!/usr/bin/env python
try:
    import kotd_config
except ImportError:
    import os
    import sys
    LIB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib'))
    sys.path.append(LIB_DIR)
    import kotd_config

import kotd
import kotd_logger

if __name__ == '__main__':
    latest = kotd.kotd_get_latest_package('kernel-default')
