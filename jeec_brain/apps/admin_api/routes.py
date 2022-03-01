from flask import request, render_template, session, redirect, url_for
from . import bp

from flask_login import current_user
from jeec_brain.apps.auth.wrappers import allow_all_roles
from jeec_brain.apps.auth.handlers.auth_handler import AuthHandler
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.handlers.events_handler import EventsHandler
from jeec_brain.schemas.admin_api.schemas import AdminLoginBody, AdminLoginForm

import logging
logger = logging.getLogger(__name__)


@bp.get('/')
def get_admin_login_form():
    """
    Description: Accepts admin user into dashboard if user is authenticated, otherwise user goes to login page
    Possible response codes: 200, 302
    """
    if current_user.is_authenticated and current_user.role.name in ['admin', 'companies_admin', 'speakers_admin', 'teams_admin', 'activities_admin', 'viewer']:
        return redirect(url_for('admin_api.dashboard'))

    return render_template('admin/admin_login.html')


@bp.post('/')
def admin_login(form:AdminLoginForm, body:AdminLoginBody):
    """
    Description: Authenticates admin user and sends user to dashboard if username and password are correct. Otherwise user remains in login page
    Possible response codes: 200, 302 
    """    
    username = form.username
    password = form.password

    # if credentials are sent in json (for stress testing purposes)
    if not username and not password:
        username = body.username
        password = body.password

    if AuthHandler.login_admin_dashboard(username, password) is False:
        return render_template('admin/admin_login.html', error="Invalid credentials!")

    return redirect(url_for('admin_api.dashboard'))


# content routes
@bp.get('/admin-logout')
def admin_logout():
    """
    Description: Logs out admin user and sends user back to login page
    Possible response codes: 302
    """
    try:
        AuthHandler.logout_user()
    except:
        pass
    return redirect(url_for('admin_api.get_admin_login_form'))


# content routes
@bp.get('/dashboard')
@allow_all_roles
def dashboard():
    """
    Description: Loads dashboard with default event if it exists
    Possible response codes: 200
    """
    event = EventsFinder.get_default_event()
    if(event is None):
        return render_template('admin/dashboard.html', event=None, logo=None, user=current_user)

    logo = EventsHandler.find_image(image_name=str(event.external_id))
    return render_template('admin/dashboard.html', event=event, logo=logo, user=current_user)
