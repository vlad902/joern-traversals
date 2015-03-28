#!/usr/bin/env python2
#
# Run query unit tests.

import sys
import re
import os.path
import hashlib

from yaml import load
from joern.all import JoernSteps

try:
  from yaml import CLoader as Loader
except ImportError:
  from yaml import Loader

if len(sys.argv) < 2:
  print "Usage: verify.py <file 1> <file 2> ..."
  exit(1)

j = JoernSteps()
j.setGraphDbURL('http://localhost:7474/db/data')
j.connectToDatabase()

sys.argv.pop(0)
print "Running tests:"

# tests hashes are encoded in the intermediate path names, this extracts them
def extract_paths(paths):
  paths = map(lambda p: str.split(str(p), "/")[-1], paths)
  return map(lambda p: str.split(str(p), ".c")[0], paths)
  
all_tests = extract_paths(j.runGremlinQuery("getNodesWithType('File').filepath"))

for arg in sys.argv:
  yaml = load(file(arg, 'r'), Loader)

  for idx, entry in enumerate(yaml):
    query = entry['QUERY']
    query = re.sub("^ +", "", query, flags=re.MULTILINE)
    query = re.sub(" +$", "", query, flags=re.MULTILINE)
    query = str.split(query, "\n")
    query = filter(lambda l: not re.match('//', l), query)
    query = str.join("", query)

    query = """%s
      .transform { g.v(it.functionId).functionToFile().filepath }.scatter()
    """ % (query)

    try:
      result = j.runGremlinQuery(query)

      if not isinstance(result, list):
        raise Exception("aaa")

      # Get the test names by parsing the paths
      result = map(lambda path: str.split(str(path), "/")[-1], result)
      result = map(lambda path: str.split(str(path), ".c")[0], result)

      if entry.has_key('POSITIVE_TESTS') and entry['POSITIVE_TESTS']:
        test_names = [hashlib.md5(test).hexdigest() for test in entry['POSITIVE_TESTS']]
        missing = set(test_names) - set(all_tests)
        if len(missing) > 0:
          raise Exception("Unit test for hashes %s are not present in your database, re-create intermediates" % (missing))

        failures = set(test_names) - set(result)
        if len(failures) > 0:
          raise Exception("Positive test failure %s" % (failures))
        else:
          sys.stdout.write('.')

      if entry.has_key('NEGATIVE_TESTS') and entry['NEGATIVE_TESTS']:
        test_names = [hashlib.md5(test).hexdigest() for test in entry['NEGATIVE_TESTS']]
        missing = set(test_names) - set(all_tests)
        if len(missing) > 0:
          raise Exception("Unit test for hashes %s are not present in your database, re-create intermediates" % (missing))

        failures = set(result) & set(test_names)
        if len(failures) > 0:
          raise Exception("Negative test failure %s" % (failures))
        else:
          sys.stdout.write('.')

    except:
      print "Error (%s:entry %i): %s" % (arg, idx + 1, sys.exc_info()[1])
      pass

print
