import os
import urllib

from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):

    def get(self):
        # guestbook_name = self.request.get('guestbook_name',
        #                                   DEFAULT_GUESTBOOK_NAME)
        # greetings_query = Greeting.query(
        #     ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        # greetings = greetings_query.fetch(10)

        # if users.get_current_user():
        #     url = users.create_logout_url(self.request.uri)
        #     url_linktext = 'Logout'
        # else:
        #     url = users.create_login_url(self.request.uri)
        #     url_linktext = 'Login'

        # collect 100M tweets
        

        template_values = {
        }
        words = {'hello' : 40, 'world' : 20, 'this'  : 10, 'is' : 10, 'my' : 10, 'time' : 40}
        print 'words["my"]:', words['my']
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(words = words))

# class Guestbook(webapp2.RequestHandler):

#     def post(self):
#         # We set the same parent key on the 'Greeting' to ensure each Greeting
#         # is in the same entity group. Queries across the single entity group
#         # will be consistent. However, the write rate to a single entity group
#         # should be limited to ~1/second.
#         guestbook_name = self.request.get('guestbook_name',
#                                           DEFAULT_GUESTBOOK_NAME)
#         greeting = Greeting(parent=guestbook_key(guestbook_name))

#         if users.get_current_user():
#             greeting.author = users.get_current_user()

#         greeting.content = self.request.get('content')
#         greeting.put()

#         query_params = {'guestbook_name': guestbook_name}
#         self.redirect('/?' + urllib.urlencode(query_params))


application = webapp2.WSGIApplication([
    ('/', MainPage)
    # ('/query', QueryMode),
], debug=True)