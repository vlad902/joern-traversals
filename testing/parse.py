#!/usr/bin/env python2
#
# Parse the YAML files, pull out positive and negative tests and write them to disk
#  indexed by their md5 hash. These are intended to be processed by joern, and then a
#  a second step (verify.py) will go through and verify that tests succeeded or failed
#  by correlating results to tests by their md5 hashes

import sys
import os.path
import hashlib

from yaml import load

try:
  from yaml import CLoader as Loader
except ImportError:
  from yaml import Loader

if len(sys.argv) < 3:
  print "Usage: parse.py <output directory> <file 1> <file 2> ..."
  exit(1)

sys.argv.pop(0)
output_dir = sys.argv.pop(0)

if not os.path.exists(output_dir):
  os.makedirs(output_dir)

for arg in sys.argv:
  yaml = load(file(arg, 'r'), Loader)

  for entry in yaml:
    tests = []
    if entry.has_key('POSITIVE_TESTS') and entry['POSITIVE_TESTS']:
      tests += entry['POSITIVE_TESTS']

    if entry.has_key('NEGATIVE_TESTS') and entry['NEGATIVE_TESTS']:
      tests += entry['NEGATIVE_TESTS']

    for t in tests:
      digest = hashlib.md5()
      digest.update(t)

      f = open(os.path.join(output_dir, digest.hexdigest() + '.c'), 'w')
      f.write(t)
      f.close()
