from .. import bp
from flask import render_template, current_app, request, redirect, url_for
from jeec_brain.finders.users_finder import UsersFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.handlers.users_handler import UsersHandler
from jeec_brain.handlers.company_users_handler import CompanyUsersHandler
from jeec_brain.handlers.activities_handler import ActivitiesHandler
from jeec_brain.services.users.get_roles_service import GetRolesService
from jeec_brain.services.users.generate_credentials_service import GenerateCredentialsService
from jeec_brain.apps.auth.wrappers import allowed_roles
from jeec_brain.models.enums.roles_enum import RolesEnum
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.schemas.admin_api.users.schemas import *
from flask_login import current_user

#Schemas
from jeec_brain.schemas.admin_api.schemas import *

# Users routes
@bp.get('/users')
@allowed_roles(['admin'])
def users_dashboard(query:AdminQuery):
    """
        Description: Loads a page with a list of specific users according to URL parameters
        Possible response codes: 200
    """
    # search_parameters = request.args
    # username = request.args.get('username')
    search_parameters = request.args
    username = query.username
    
    # handle search bar requests
    if username is not None:
        search = username
        users_list = UsersFinder.get_admin_users_by_username(username)
        company_users_list = UsersFinder.get_company_users_from_username(username)
    
    # handle parameter requests
    elif len(search_parameters) != 0:
        search_parameters = request.args
        search = 'search name'

        users_list = UsersFinder.get_admin_users_from_parameters(search_parameters)
        company_users_list = None

    # request endpoint with no parameters should return all users
    else:
        search = None
        users_list = UsersFinder.get_all_admin_users()
        company_users_list = UsersFinder.get_all_company_users()
    
    if (users_list is None or len(users_list) == 0) and (company_users_list is None or len(company_users_list) == 0):
        error = 'No results found'
        return render_template('admin/users/users_dashboard.html', users=None, company_users=None, error=error, search=search, current_user=current_user)

    return render_template('admin/users/users_dashboard.html', users=users_list, company_users=company_users_list, error=None, search=search, current_user=current_user)


@bp.get('/new-user')
@allowed_roles(['admin'])
def add_user_dashboard():
    """
        Description: Removes the roles of company and student of a certain user
        Possible response codes: 200
    """
    roles = GetRolesService.call()

    if 'company' and 'student' in roles: 
        roles.remove('company')
        roles.remove('student')

    return render_template('admin/users/add_user.html', \
        user = current_user, \
        roles = roles, \
        error=None)


@bp.get('/new-organization-user')
@allowed_roles(['admin'])
def add_company_user_dashboard():
    """
        Description: Loads page to add company user
        Possible response codes: 200
    """
    companies = CompaniesFinder.get_all()

    return render_template('admin/users/add_company_user.html', \
        user = current_user, \
        companies=companies, \
        error=None)


@bp.post('/new-user', responses = {'404': APIError})
@allowed_roles(['admin'])
def create_user(form:UserForm):
    """
        Description: Creates user or company user using form data 
        Possible response codes: 200 , 302 , 404
    """
    # extract form parameters
    #name = request.form.get('name')
    #username = request.form.get('username')
    #email = request.form.get('email', None)
    #role = request.form.get('role', None)
    #post = request.form.get('post', None)
    #evf_username = request.form.get('evf_username', None)
    #evf_password = request.form.get('evf_password', None)
    name = form.name
    username = form.username
    email = form.email
    role = form.role
    post = form.post
    evf_username = form.evf_username
    evf_password = form.evf_password
    
    # check if is creating company user
    #company_external_id = request.form.get('company_external_id')
    company_external_id = form.company_external_id
    if company_external_id is not None:
        company = CompaniesFinder.get_from_external_id(company_external_id)
        company_id = company.id

        if company is None:
            return 'No company found', 404

    # extract food_manager from parameters
    #food_manager = request.form.get('food_manager', None)
    food_manager = form.food_manager

    if food_manager == 'True':
        food_manager = True
    elif food_manager == 'False':
        food_manager = False
    else:
        food_manager = None

    # create new company user
    if company_external_id:
        company_user = CompanyUsersHandler.create_company_user(name, username, email, company_id, post, food_manager, evf_username, evf_password)
        if not company_user:
            return render_template('admin/users/add_company_user.html', \
                    user=current_user, \
                    companies=CompaniesFinder.get_all(), \
                    roles=GetRolesService.call(), \
                    error="Failed to create user!")

        # if not UsersHandler.join_channel(company_user.user, company.chat_id, company.chat_code):
        #     CompanyUsersHandler.delete_company_user(company_user)
        #     return render_template('admin/users/add_company_user.html', \
        #             user=current_user, \
        #             companies=CompaniesFinder.get_all(), \
        #             roles=GetRolesService.call(), \
        #             error="Failed to create user!")

        # for activity in company_user.company.activities:
        #     if activity.chat_id:
        #         if not ActivitiesHandler.join_channel(company_user.user, activity):
        #             CompanyUsersHandler.delete_company_user(company_user)
        #             return render_template('admin/users/add_company_user.html', \
        #                 user=current_user, \
        #                 companies=CompaniesFinder.get_all(), \
        #                 roles=GetRolesService.call(), \
        #                 error="Failed to create user!")

    else:
        if role not in GetRolesService.call():
            return 'Wrong role type provided', 404
        else:
            role = RolesEnum[role]

        user = UsersHandler.create_user(
            name=name,
            username=username,
            email=email,
            role=role,
            password=GenerateCredentialsService().call()
        )

        if user is None:
            return render_template('admin/users/add_user.html', \
                roles=GetRolesService.call(), \
                error="Failed to create user!")

    return redirect(url_for('admin_api.users_dashboard'))


@bp.get('/user/<string:user_external_id>/delete', responses = {'500': APIError})
@allowed_roles(['admin'])
def delete_user(path: UserPath):
    """
        Description: Deletes user or company user if it exists
        Possible response codes: 302 , 500
    """
    user = UsersFinder.get_from_external_id(path.user_external_id)

    if user is None:
        return APIErrorValue('Couldnt find user').json(500)

    if user.role.name == 'company':
        company_user = UsersFinder.get_company_user_from_user(user)
        if not company_user:
            return APIErrorValue('Couldnt find user').json(500)
            
        CompanyUsersHandler.delete_company_user(company_user)

    else:
        UsersHandler.delete_user(user)
    
    return redirect(url_for('admin_api.users_dashboard'))


@bp.get('/user/<string:user_external_id>/credentials', responses = {'500': APIError})
@allowed_roles(['admin'])
def generate_user_credentials(path: UserPath):
    """
        Description: Generates new credentials for a specific user given in URL
        Possible response codes: 302 , 500
    """
    user = UsersFinder.get_from_external_id(path.user_external_id)

    if user is None:
        return APIErrorValue('Couldnt find user').json(500)
            
    UsersHandler.generate_new_user_credentials(user=user)
    return redirect(url_for('admin_api.companies_dashboard'))
