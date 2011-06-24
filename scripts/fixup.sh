#!/bin/bash

APPENGINE="${1:-/opt/google-appengine/lib/}"
shift
LIBS="${*:-fancy_urllib yaml/lib antlr3 webob ipaddr}"
for lib in $LIBS; do
  PYTHONPATH=$PYTHONPATH:$APPENGINE/$lib
done
echo "export PYTHONPATH=$PYTHONPATH"
