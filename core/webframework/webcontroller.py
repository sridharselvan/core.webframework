# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry level.

"""

# ----------- START: Native Imports ---------- #
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
import bottle

from bottle.ext import beaker
from bottle import request
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.backend.constants import (
    STATIC_JS_FILE_PATH, STATIC_CSS_FILE_PATH, STATIC_VIEW_FILE_PATH, STATIC_IMAGE_FILE_PATH
)

from core.backend.config import update_client_config, view_client_config, save_scheduler_config
from core.backend.utils.butils import decode_form_data
from core.backend.utils.core_utils import common_route

from core.backend.api.user import authenticate_user, create_user
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]


#app = bottle.Bottle()

app_route = bottle.route


@app_route('/')
def index():
   """."""
   return views("index.html")


@app_route('/sorry_page/<page_name>', method=['GET'])
def sorry_page(page_name):
    """Serve sorry page"""
    return views("under_construction.html")

@app_route('/loginvalidation', method='POST')
@common_route
def on_login():
    return authenticate_user()

@app_route('/createUser', method='POST')
def on_create_user():
    return create_user()

@app_route('/viewclientconfig')
@common_route
def show_client_config():
    return view_client_config()


@app_route('/modifyclientconfig', method='POST')
@common_route
def modify_client_config():
    form_data = decode_form_data(request.forms)
    return update_client_config(form_data)

@app_route('/logoutuser')
@common_route
def logout_user():
    return True

@app_route('/saveschedulerconfig', method='POST')
@common_route
def on_scheduler_config():
    form_data = decode_form_data(request.forms)
    return save_scheduler_config(form_data)

@app_route('/<filename:re:.*\.(tpl|html)>')
def views(filename):
    return bottle.static_file(filename, root=STATIC_VIEW_FILE_PATH)

@app_route('/<filename:re:.*\.js>')
def javascripts(filename):
    return bottle.static_file(filename, root=STATIC_JS_FILE_PATH)

@app_route('/<filename:re:.*\.css>')
def stylesheets(filename):
    return bottle.static_file(filename, root=STATIC_CSS_FILE_PATH)

@app_route('/<filename:re:.*\.(jpg|jpeg|png|gif|ico)>')
def images(filename):
    return bottle.static_file(filename, root=STATIC_IMAGE_FILE_PATH)


def main():
    session_opts = {
        'session.type': 'file',
        'session.cookie_expires': 300,
        'session.data_dir': './data',
        'session.auto': True
    }

    bottle.run(
        app=beaker.middleware.SessionMiddleware(
            bottle.app(), session_opts
        ),
        host='0.0.0.0', port=8080
    )

