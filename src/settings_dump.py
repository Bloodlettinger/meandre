# -*- coding: utf-8 -*-

import sys
import settings

for arg in sys.argv[1:]:
    value = getattr(settings, arg, 'UNKNOWN')
    print '%s=%s' % (arg[5:], value)
