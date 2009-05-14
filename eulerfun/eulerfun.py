import cgi
import hashlib

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Problem(db.Model):
    pid = db.IntegerProperty()
    ans = db.StringProperty()
    code = db.ListProperty(db.Text)

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""
      <html>
        <body>
          <p>my <a href="http://projecteuler.net">Project Euler</a> solutions: </p>
          <form action="/show" method="post">
            <div> problem id: <input type="text" name="pid" size=4 maxlength=3></div>
            <div> answer: <input type="text" name="ans" size=20 maxlength=30></div>
            <div><input type="submit" value="I'm Feeling Lucky"></div>
          </form>
        </body>
      </html>""")


class Show(webapp.RequestHandler):
    def post(self):
        pid = int(cgi.escape(self.request.get('pid')))
        problem = Problem.gql("WHERE pid = :1", pid).get()
        self.response.headers['Content-Type'] = 'text/plain'
        if problem == None:
            self.response.out.write('Problem ')
            self.response.out.write(pid)
            self.response.out.write(' is not available.')
        else:
            ans = cgi.escape(self.request.get('ans'))
            if hashlib.md5(ans).hexdigest() == problem.ans:
                self.response.out.write('Congrats!\n\n')
                for x in problem.code:
                    self.response.out.write(x)
                    self.response.out.write('\n\n')

            else:
                self.response.out.write('Wrong Answer')

application = webapp.WSGIApplication(
        [('/', MainPage),
            ('/show', Show)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
