#!/usr/bin/env python
"""rescaleImages.py

usage: rescaleImages scale_factor

Rescales all images in the current folder by scale_factor.
"""
import os
from PIL import Image
import sys
import types

try:
    factor = types.FloatType(sys.argv[1])
except:
    raise Exception('No valid scale specified.')
    sys.exit()

for infileName in os.listdir('.'):
    try:
        im = Image.open(infileName)
    except IOError as e:
        continue
    newSize = tuple(int(factor * dim) for dim in im.size)
    im.resize(newSize)
    fn = list(os.path.splitext(infileName))
    fn[0] += '_small'
    im.save(''.join(fn))

    