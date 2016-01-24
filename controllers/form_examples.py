# -*- coding: utf-8 -*-
# try something like
def index(): return dict(message="hello from form_examples.py")

def form1():
    form=FORM(TABLE(TR("Profile",TEXTAREA(_name="profile",value="write something here")),
                    TR("",INPUT(_type="submit",_value="SUBMIT"))))
    form.element('textarea[name=profile]')['_style'] = 'width200px;height:200px;'
    if form.accepts(request,session):
        response.flash="form accepted"
    elif form.errors:
        response.flash="form is invalid"
    else:
        response.flash="please fill the form"
    return dict(form=form,vars=form.vars)
