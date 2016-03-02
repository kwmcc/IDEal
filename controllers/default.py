# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    redirect(URL('project_init'))
    return dict()

@auth.requires_login()
def project_init():
    files = db().select(db.files.ALL, orderby=db.files.filename)
    form = FORM('Filename: ', INPUT(_name='name'), INPUT(_type='submit'))
    if form.accepts(request,session):
        name = form.vars.name
        redirect(URL('ideal_editor', vars=dict(name=name, load=False)))
    return dict(form=form, files=files)

def ideal_editor():
    """
    This creates the ideal/default/ideal_editor page.

    If this file is being loaded from a file on the server, then
    the file is read and stored in the data variable. Otherwise,
    data is the empty string.
    """
    db.files.insert(auth_user_id = auth.user.id, filename = request.vars.get('name'))
    if request.vars.get('load') == 'True':
        f = open('applications/ideal/uploads/' + request.vars.get('name'))
        data = f.read()
        f.close()
    else:
        data = ""
    filename = request.vars.get('name')
    load = request.vars.get('load')
    return dict(filename=filename, load=load, data=data)

def save_to_server():
   db.files.insert(filename=request.vars.filename)
   f = open('applications/ideal/uploads/' + request.vars.filename, 'w')
   f.write(request.vars.code)
   f.close
   return dict()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
