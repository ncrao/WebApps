#!/bin/bash

if [ $# -lt 1 ]; then
  echo "usage: $0 project"
  exit 1
fi

cat ~/application-specific-password | appcfg.py update -e nikhilcrao@gmail.com --passin $1
