import cgi
import hashlib

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Problem(db.Model):
    pid = db.IntegerProperty()
    ans = db.StringProperty()

class Code(db.Model):
    name = db.StringProperty()
    text = db.TextProperty()
    problem = db.ReferenceProperty(Problem, collection_name='code')

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""
      <html>
        <body>
          <p>my <a href="http://projecteuler.net">Project Euler</a> solutions: </p>
          <form method="post">
            <div> problem id: <input type="text" name="pid" size=4 maxlength=3></div>
            <div> answer: <input type="text" name="ans" size=20 maxlength=30></div>
            <div><input type="submit" value="I'm Feeling Lucky"></div>
          </form>
        </body>
      </html>""")

    def post(self):
        self.redirect('/show/' + cgi.escape(self.request.get('pid')) + '/' + hashlib.md5(cgi.escape(self.request.get('ans'))).hexdigest())

class Show(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        pid, ans = self.request.path.split('/')[2:]
        pid = int(pid)
        problem = Problem.gql("WHERE pid = :1", pid).get()
        if problem == None:
            self.response.out.write('Problem ')
            self.response.out.write(pid)
            self.response.out.write(' is not available.')
        else:
            if ans == problem.ans:
                self.response.out.write('Congrats!\n\n')
                for x in problem.code:
                    self.response.out.write('--------------%s--------------'%x.name)
                    self.response.out.write(x.text)
                    self.response.out.write('--------------%s--------------'%x.name)
                    self.response.out.write('\n\n\n\n\n')

            else:
                self.response.out.write('Wrong Answer')


application = webapp.WSGIApplication(
        [('/', MainPage),
            ('/show/.*', Show)],
        debug=False)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
