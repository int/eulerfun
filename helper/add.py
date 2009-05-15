#!/usr/bin/python
#
# Same as update.py except that, it's assumed to be the first add.
# (does not check if the entity is already put)
# Faster than update.py
#
# generate code that can be run at App Engine
# (either via Admin Consonle interactively or directly from url)
#
# Usage:
# ./add [id] ...
#
# 
# add all if no args specified:
# add corresponding problem(s) if there are id(s) specified
#
# Example:
# ./add              # add all
# ./add 123          # add problem '123'
# ./add 1 2 3        # add problem '1', '2', and '3'

import os
import sys

print r"""
import time
import hashlib

from google.appengine.ext import db

class Problem(db.Model):
    pid = db.IntegerProperty()
    ans = db.StringProperty()

class Code(db.Model):
    name = db.StringProperty()
    text = db.TextProperty()
    problem = db.ReferenceProperty(Problem, collection_name='code')
"""

ans = {}
file = '/home/alecs/acm/.euler'
for x in open(file).readlines():
    p, a = x.strip().split(': ')
    ans[p] = a

dir = '/home/alecs/acm/euler'
os.chdir(dir)
if len(sys.argv) == 1:
    probs = os.listdir('.')
else:
    probs = sys.argv[1:]
for p in probs:
    os.chdir(p)
    print 'problem = Problem(pid = %s)' % p
    print "problem.ans = hashlib.md5('%s').hexdigest()" % ans[p]
    print 'problem.put()' # put for later reference
    for f in os.listdir('.'):
        print 'code = Code(problem = problem, name = "%s")' % f
        # just a quick & dirty way to embed data to code
        # luckily, my euler python solutions dont contain """
        # use ''' instead
        print 't = ur"""'
        print open(f).read()
        print '"""'
        print 'code.text = db.Text(t)'
        print 'code.put()'
    #print 'time.sleep(10)' # cpu quota
    os.chdir('..')
