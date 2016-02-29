# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

auth_table = db.define_table(auth.settings.table_user_name,
                             Field('first_name', length=128, default=""),
                             Field('last_name', length=128, default=""),
                             Field('username', length=128, default="", unique=True),
                             Field('password', 'password', length=256,
                                   readable=False, label='Password'))

auth_table.username.requires = IS_NOT_IN_DB(db, auth_table.username)

db.define_table('owners',
    Field('ownername', notnull=True, unique=True))

db.define_table('files',
    Field('owners_id', 'reference owners', readable = False, writable = False),
    Field('filename'))



db.files.filename.requires = IS_NOT_EMPTY()
auth.define_tables()

## create all tables needed by auth if not custom tables
## auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

# processes Google auth tokens

from gluon.contrib.login_methods.oauth20_account import OAuthAccount
from gluon.storage import Storage
import urllib2
import os

try:
    import json
except ImportError:
    from gluon.contrib import simplejson as json

class GoogleAccount(OAuthAccount):
    "OAuth 2.0 for Google"

    def __init__(self):
        with open(os.path.join(request.folder, 'private/google_auth.json'), 'rb') as f:
            gai = Storage(json.load(f)['web'])

        OAuthAccount.__init__(self, None,
                              gai.client_id,
                              gai.client_secret,
                              gai.auth_uri,
                              gai.token_uri,
                              scope='https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
                              approval_prompt='force',
                              state="auth_provider=google")

    def get_user(self):

        token = self.accessToken()
        if not token:
            return None

        uinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo?access_token=%s' % urllib2.quote(token, safe='')

        uinfo = None

        try:
            uinfo_stream = urllib2.urlopen(uinfo_url)
        except:
            session.token = None
            return
        data = uinfo_stream.read()
        uinfo = json.loads(data)

        username = uinfo['id']

        return dict(first_name = uinfo['given_name'],
                    last_name = uinfo['family_name'],
                    username = username,
                    email = uinfo['email'])

auth.settings.actions_disabled=['register','change_password','request_reset_password','profile']

auth.settings.login_form = GoogleAccount()
