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
import argparse

from bottle.ext import beaker
from bottle import request
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.backend.constants import (
    STATIC_JS_FILE_PATH, STATIC_CSS_FILE_PATH, STATIC_VIEW_FILE_PATH, STATIC_IMAGE_FILE_PATH,
    STATIC_FONT_FILE_PATH
)

from core.backend.config import update_client_config, view_client_config
from core.scheduler.web import (
    save_scheduler_config, search_scheduled_job,
    deactivate_scheduled_job, update_scheduled_job,
    check_enabled_valves, get_sms_config, update_sms_config, fetch_scheduler_search_type
)
from core.backend.utils.butils import decode_form_data
from core.backend.utils.core_utils import common_route, AutoSession

from core.backend.api.user import (
    authenticate_user, create_user, get_user_details,
    update_user_details, forgot_password_validation, update_password
)

from core.backend.api.dashboard import dashboard, delete_failed_sms

from core.utils.environ import get_user_session_details
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]

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
@common_route()
def on_login(session, *args, **kwargs):

    form_data = decode_form_data(request.forms)

    if form_data:
        kwargs['form_data'] = form_data

    return authenticate_user(session, *args, **kwargs)

@app_route('/createUser', method='POST')
def on_create_user(*args, **kwargs):

    with AutoSession() as auto_session:
        form_data = decode_form_data(request.forms)

        if form_data:
            kwargs['form_data'] = form_data

        return create_user(auto_session, *args, **kwargs)

@app_route('/forgotpasswordvalidation', method='POST')
def on_forgot_password_validation(*args, **kwargs):

    with AutoSession() as auto_session:
        form_data = decode_form_data(request.forms)

        if form_data:
            kwargs['form_data'] = form_data

        return forgot_password_validation(auto_session, form_data)

@app_route('/updatepassword', method='POST')
def on_update_password(*args, **kwargs):

    with AutoSession() as auto_session:
        form_data = decode_form_data(request.forms)

        if form_data:
            kwargs['form_data'] = form_data

        return update_password(auto_session, form_data)

@app_route('/viewclientconfig')
@common_route()
def show_client_config():
    return view_client_config()

@app_route('/checkenabledvalves', method='POST')
@common_route(use_transaction=True)
def on_check_enabled_valves(session, *args, **kwargs):
    selected_node = decode_form_data(request.forms)
    return check_enabled_valves(session, selected_node)

@app_route('/getsmsconfig', method='GET')
@common_route(use_transaction=True)
def on_get_sms_config(session, *args, **kwargs):
    return get_sms_config(session)

@app_route('/updatesmsconfig', method='POST')
@common_route(use_transaction=True)
def on_update_sms_config(session, *args, **kwargs):
    sms_data = decode_form_data(request.forms)
    return update_sms_config(session, sms_data)

@app_route('/getuserdetails')
@common_route(use_transaction=True)
def on_get_user_details(session, *args, **kwargs):
    user_id = request['beaker.session']['user_id'] or ''
    return get_user_details(session, user_id)

@app_route('/updateuserdetails', method='POST')
@common_route(use_transaction=True)
def on_update_user_details(session, *args, **kwargs):
    form_data = decode_form_data(request.forms)
    return update_user_details(session, form_data)

@app_route('/modifyclientconfig', method='POST')
@common_route()
def modify_client_config():
    form_data = decode_form_data(request.forms)
    return update_client_config(form_data)

@app_route('/logoutuser')
@common_route()
def logout_user():
    return True

@app_route('/saveschedulerconfig', method='POST')
@common_route(use_transaction=True)
def on_scheduler_config(session, *args, **kwargs):
    form_data = decode_form_data(request.forms)
    return save_scheduler_config(session, form_data)

@app_route('/dashboard', method='GET')
@common_route(use_transaction=True)
def on_dashboard(session, *args, **kwargs):
    return dashboard(session)

@app_route('/deletefailedsms', method='POST')
@common_route(use_transaction=True)
def on_delete_failed_sms(session, *args, **kwargs):
    form_data = decode_form_data(request.forms)
    return delete_failed_sms(session, form_data)

@app_route('/searchscheduledjob', method='POST')
@common_route(use_transaction=True)
def on_search_job(session, *args, **kwargs):
    form_data = decode_form_data(request.forms)
    return search_scheduled_job(session, form_data)

@app_route('/fetchschedulersearchtype', method='POST')
@common_route(use_transaction=True)
def on_fetch_scheduler_search_type(session, *args, **kwargs):
    form_data = decode_form_data(request.forms)
    return fetch_scheduler_search_type(session, form_data)

@app_route('/deactivatescheduledjob', method='POST')
@common_route(use_transaction=True)
def on_deactivate_job(session, *args, **kwargs):
    form_data = decode_form_data(request.forms)
    return deactivate_scheduled_job(session, form_data)

@app_route('/updateschedulerconfig', method='POST')
@common_route(use_transaction=True)
def on_update_job(session, *args, **kwargs):
    form_data = decode_form_data(request.forms)
    return update_scheduled_job(session, form_data)

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

@app_route('/<filename:re:.*\.(eot|svg|ttf|woff|woff2)>')
def fonts(filename):
    filename = filename.split('/')[-1]
    return bottle.static_file(filename, root=STATIC_FONT_FILE_PATH)


def main():

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '--port', '-p',
        required=True,
        help='Instance port number to be served'
    )

    cmd_args = parser.parse_args()

    port = cmd_args.port

    if isinstance(port, str):
        if port.isdigit():
            port = int(port)
        else:
            raise Exception("Invalid port name supplied !")

    elif isinstance(port, int):
        pass

    else:
        raise Exception("Invalid port name supplied !")

    #
    # App instance
    session_opts = {
        'session.type': 'file',
        'session.cookie_expires': get_user_session_details()['timeout'],
        'session.data_dir': './.data',
        'session.auto': True
    }

    app = bottle.app()

    bottle.run(
        app=beaker.middleware.SessionMiddleware(app, session_opts),
        host='0.0.0.0',
        port=port
    )
