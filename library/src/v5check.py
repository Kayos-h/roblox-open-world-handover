"""Headless numbers check for v5 modules (own Blender process, never touches the live Blender).
  blender -b --factory-startup --python v5check.py -- <module> <batch,batch|-> <id,id|->
"""
import sys
import os
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
import v5live


def lst(i):
    v = argv[i] if len(argv) > i else '-'
    return [x for x in v.split(',') if x and x != '-'] or None


v5live.check(argv[0], batches=lst(1), only=lst(2))
