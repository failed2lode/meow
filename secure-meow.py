#!/usr/bin/env python
#
# Wrapper to aid in the secure generation of stuff.
#
# Creates a tempfs where sensitive content can reside in memory-based file
# system. This script requires user to have sudo privileges. Elevated
# privileges are only necessary for mounting & unmounting the tempfs in 
# addition to wiping all file content generated.
#
# 
# $ sudo mount -t tmpfs tmpfs ./purrrse
# $ ./meow.py generate -w ./purrrse
# $ for f in $(find ./purrrse -type f); do \
#   sudo dd if=/dev/zero of=$f bs=1 count=$(wc -c $f | awk '{print $1}'); \
#   done
# # same thing as above using /dev/urandom
# $ sudo umount ./purrrse

import os
import subprocess

print('Mount tmpfs ./purrrse...')
if not os.path.isdir('./purrrse'):
    os.mkdir('./purrrse')
subprocess.call(['sudo', 'mount', '-t', 'tmpfs', 'tmpfs', './purrrse'])

print('Running meow...')
# TODO: Pass additional args onto this call to meow.py (e.g. --no-test-print)
subprocess.call(['./meow.py', 'generate', '-w', './purrse'])

print('Zero all generated file content...')
subprocess.call("for f in $(find ./purrrse -type f); " + \
        "do sudo dd if=/dev/zero of=$f bs=1 " + \
        "count=$(wc -c $f | awk '{print $1}'); done", shell=True)

print('Fill all generated files with garbage...')
subprocess.call("for f in $(find ./purrrse -type f); " + \
        "do sudo dd if=/dev/urandom of=$f bs=1 " + \
        "count=$(wc -c $f | awk '{print $1}'); done", shell=True)

print('Unmount tmpfs ./purrrse...')
subprocess.call(['sudo', 'umount', './purrrse'])
os.rmdir('./purrrse')
