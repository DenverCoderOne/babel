#!/usr/bin/env python
#
# Copyright (C) 2007-2011 Edgewall Software, 2013-2022 the Babel team
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution. The terms
# are also available at http://babel.edgewall.org/wiki/License.
#
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at http://babel.edgewall.org/log/.

import os
import sys
from pprint import pprint

import cPickle as pickle

import babel

dirname = os.path.join(os.path.dirname(babel.__file__))
filename = os.path.join(dirname, 'global.dat')
with open(filename, 'rb') as fileobj:
    data = pickle.load(fileobj)

if len(sys.argv) > 1:
    pprint(data.get(sys.argv[1]))
else:
    pprint(data)
