#!/usr/bin/python
#
# generate code that can be run at App Engine
# (either via Admin Consonle interactively or directly from url)
#
# Usage:
# ./update [id] ...
#
# update all if no args specified:
# update corresponding problem(s) if there are id(s) specified
#
# Example:
# ./update              # update all
# ./update 123          # update problem '123'
# ./update 1 2 3        # update problem '1', '2', and '3'

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
    print 'problem = Problem.gql("WHERE pid = %s").get()' % p
    print 'if problem == None:'
    print '    problem = Problem(pid = %s)' % p
    print "problem.ans = hashlib.md5('%s').hexdigest()" % ans[p]
    print 'problem.put()' # put for later reference
    for f in os.listdir('.'):
        print 'code = Code.gql("WHERE problem = :1 AND name = \'%s\'", problem).get()' % f
        print 'if code == None:'
        print '    code = Code(problem = problem, name = "%s")' % f
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
