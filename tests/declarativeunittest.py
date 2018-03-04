import pytest
xfail = pytest.mark.xfail
skip = pytest.mark.skip
skipif = pytest.mark.skipif

import os, math, random, collections, itertools, io, hashlib, binascii

from construct import *
from construct.lib import *

ontravis = "TRAVIS" in os.environ
ident = lambda x: x
devzero = open("/dev/zero", "rb")


cached_cache = {}
def cached(key, factory):
    if key not in cached_cache:
        cached_cache[key] = factory()
    return cached_cache[key]


def raises(func, *args, **kw):
    try:
        return func(*args, **kw)
    except Exception as e:
        return e.__class__


def common(format, datasample, objsample, sizesample=SizeofError, **kw):
    obj = format.parse(datasample, **kw)
    assert obj == objsample
    data = format.build(objsample, **kw)
    assert data == datasample
    # following are implied by above (re-parse and re-build)
    # assert format.parse(format.build(obj)) == obj
    # assert format.build(format.parse(data)) == data
    if isinstance(sizesample, int):
        size = format.sizeof(**kw)
        assert size == sizesample
    else:
        size = raises(format.sizeof, **kw)
        assert size == sizesample


def commonhex(format, hexdata):
    commonbytes(format, binascii.unhexlify(hexdata))


def commondump(format, filename):
    filename = "examples/formats/" + filename
    if not ontravis:
        filename = "tests/" + filename
    with open(filename,'rb') as f:
        data = f.read()
    commonbytes(format, data)


def commonbytes(format, data):
    obj = format.parse(data)
    data2 = format.build(obj)
