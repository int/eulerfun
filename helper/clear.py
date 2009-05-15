# clear datastore

import hashlib

from google.appengine.ext import db

class Problem(db.Model):
    pid = db.IntegerProperty()
    ans = db.StringProperty()

class Code(db.Model):
    name = db.StringProperty()
    text = db.TextProperty()
    problem = db.ReferenceProperty(Problem, collection_name='code')

db.delete(db.Query(Problem))
db.delete(db.Query(Code))
