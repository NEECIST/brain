from flask import request, render_template, redirect, url_for, session
from jeec_brain.apps.companies_api import bp
from flask_login import current_user
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.apps.auth.handlers.auth_handler import AuthHandler
from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.finders.auctions_finder import AuctionsFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.handlers.companies_handler import CompaniesHandler
from jeec_brain.handlers.users_handler import UsersHandler

#Schemas
from jeec_brain.schemas.companies_api.schemas import Company_Login_Form,Company_Login_Body

from datetime import datetime


@bp.get('/')
def get_company_login_form():
    """
        Description: Accepts company user into dashboard if user is authenticated, otherwise user goes to login page
        Possible response codes: 200 , 302
    """
    if current_user.is_authenticated and current_user.role == 'company':
        return redirect(url_for('companies_api.dashboard'))

    return render_template('companies/companies_login.html')


@bp.post('/')
def company_login(form: Company_Login_Form, body: Company_Login_Body):    

    """
        Description:  Accepts company user into dashboard if username and password are correct otherwise user goes to login page
        Possible response codes: 200 , 302
    """
    username = form.username
    password = form.password
   

    # if credentials are sent in json (for stress testing purposes)
    if not username and not password:
        username = body.username
        password = body.password

    if AuthHandler.login_company(username, password) is False:
        return render_template('companies/companies_login.html', error = "Invalid credentials!")

    return redirect(url_for('companies_api.dashboard'))


@bp.get('/company-logout')
def company_logout():
    """
        Description: Redirects the company user to login page after logging out
        Possible response codes: 302
    """
    try:
        AuthHandler.logout_user()
    except:
        pass
    return redirect(url_for('companies_api.get_company_login_form'))


@bp.get('/dashboard')
@require_company_login
def dashboard(company_user):
    """
        Description: If company hasn't accepted terms and conditions, loads them;If company has accepted terms and conditions loads dashboard     
        Possible response codes: 200     
    """
    if not company_user.user.accepted_terms:
        return render_template('companies/terms_conditions.html', user=company_user.user)

    if company_user.company.cvs_access:
        event = EventsFinder.get_default_event()
        today = datetime.now()
        cvs_access_start = datetime.strptime(event.cvs_access_start, '%d %b %Y, %a')
        cvs_access_end = datetime.strptime(event.cvs_access_end, '%d %b %Y, %a')
        if today < cvs_access_start or today > cvs_access_end:
            cvs_enabled = False
        else:
            cvs_enabled = True
    else:
        cvs_enabled = False

    company_auctions = CompaniesFinder.get_company_auctions(company_user.company)
    auctions = []
    now = datetime.utcnow()
    for company_auction in company_auctions:
        end = datetime.strptime(company_auction.closing_date + " " + company_auction.closing_time,'%d %b %Y, %a %H:%M')
        auction = company_auction._asdict()
        auction["is_open"] = True if now < end else False
        auctions.append(auction)

    company_logo = CompaniesHandler.find_image(company_user.company.name)

    job_fair = False
    activity_types = []
    activities = ActivitiesFinder.get_current_company_activities(company_user.company)
    for activity in activities:
        if (activity.activity_type not in activity_types) and (activity.activity_type.name not in ['Job Fair','Job Fair Booth']):
            activity_types.append(activity.activity_type)

        if (activity.activity_type.name in ['Job Fair','Job Fair Booth']):
            job_fair = True

    activity_job_fair = True
    if not activities : 
        activity_job_fair = False

    today = now.strftime('%d %b %Y, %a')
    activity_job_fair_today = False
    for activity in activities:
        if activity.activity_type.name == 'Job Fair Booth' and activity.day == today:
            activity_job_fair_today = True
            break


    return render_template('companies/dashboard.html', auctions=auctions, job_fair=job_fair, company_logo=company_logo, activity_types=activity_types, user=company_user, cvs_enabled=cvs_enabled, activity_job_fair = activity_job_fair, activity_job_fair_today = activity_job_fair_today)


@bp.post('/dashboard')
@require_company_login
def accept_terms(company_user):
    """
        Description: Function to accept terms and conditions, then redirects to dashboard 
        Possible response codes: 302   
    """
    UsersHandler.update_user(user=company_user.user, accepted_terms=True)

    return redirect(url_for('companies_api.dashboard'))
