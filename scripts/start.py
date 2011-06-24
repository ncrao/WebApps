#!/usr/bin/python

import sys
import os
import shutil

TESTAPP_DIR = "./scripts/testapp"

libs = [
  'django',
  'autoload',
  'dbindexer',
  'djangoappengine',
  'djangotoolbox',
]

def main(dir):
  print('Creating project in %s' % dir)
  shutil.copytree(TESTAPP_DIR, dir)
  for lib in libs:
    dest = os.path.join(dir, lib)
    src = os.path.join('lib', lib)
    shutil.copytree(src, dest)

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('usage: %s name' % sys.argv[0])
    sys.exit(1)

  if not os.path.exists(TESTAPP_DIR):
    print('run script from base directory')
    sys.exit(1)

  main(sys.argv[1])
