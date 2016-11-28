import webapp2
import os
import jinja2
import hashlib
import hmac
#
# template_dir = os.path.join(os.path.dirname(__file__), 'templates')
# jinja_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir), autoescape=True)

SPLIT_CHARACTER = '|'
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


SECRET = 'imsosecret'
def hash_str(str):
    return hmac.new(SECRET, str).hexdigest()

def make_secure_val(data):
    return data + SPLIT_CHARACTER + hash_str(data)

def check_secure_val(data):
    print "In check secure val", SPLIT_CHARACTER in data
    if SPLIT_CHARACTER in data:
        x = int(data.split(SPLIT_CHARACTER)[0])
        actual_value = data.split(SPLIT_CHARACTER)[1]
        expected_value = hash_str(str(x))
        if(actual_value == expected_value):
            return x
        else:
            return None

class CookieHandler(Handler):
    def get(self):
        self.response.headers["Content-Type"] = "text/plain"
        visit_cookie = self.request.cookies.get("visits")

        if visit_cookie != None :
            visit_count = check_secure_val(visit_cookie)
            if visit_count == None :
                visit_count = 0
        else:
            visit_count = 0

        visit_count += 1
        cookie_str = make_secure_val(str(visit_count))

        self.response.headers.add_header("Set-Cookie", "visits=%s" % cookie_str)
        if visit_count >= 10 :
            self.write("Hurrayy! You are special visitor!!! ")
        else:
            self.write("You have visited %s times and hash is: " % visit_count)


app = webapp2.WSGIApplication([
    ('/', CookieHandler)],
    debug=True)
