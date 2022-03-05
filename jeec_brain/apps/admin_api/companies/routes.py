from .. import bp
from flask import render_template, request, redirect, url_for, current_app
from flask_login import current_user
# handlers
from jeec_brain.handlers.companies_handler import CompaniesHandler
from jeec_brain.handlers.company_users_handler import CompanyUsersHandler
# finders
from jeec_brain.finders.companies_finder import CompaniesFinder
# values
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.apps.auth.wrappers import allowed_roles, allow_all_roles
# services
from jeec_brain.services.files.rename_image_service import RenameImageService
#schemas
from jeec_brain.schemas.admin_api.companies.schemas import *
from jeec_brain.schemas.admin_api.schemas import *



@bp.get('/companies')
@allow_all_roles
def companies_dashboard():
    """
    Description: Directs user to "companies dashboard" page
    Possible response codes: 200
    """
    companies_list = CompaniesFinder.get_all()

    if len(companies_list) == 0:
        error = 'No results found'
        return render_template('admin/companies/companies_dashboard.html', companies=None, error=error, search=None, role=current_user.role.name)

    return render_template('admin/companies/companies_dashboard.html', companies=companies_list, error=None, search=None, role=current_user.role.name)


@bp.post('/companies')
@allow_all_roles
def search_company(form: CompanySearchForm):
    """
    Description: Searches for company with name given by admin user in form
    Possible response codes: 200
    """
    #name = request.form.get('name')
    name= form.name
    companies_list = CompaniesFinder.search_by_name(name)

    if len(companies_list) == 0:
        error = 'No results found'
        return render_template('admin/companies/companies_dashboard.html', companies=None, error=error, search=name, role=current_user.role.name)

    return render_template('admin/companies/companies_dashboard.html', companies=companies_list, error=None, search=name, role=current_user.role.name)


@bp.get('/new-company')
@allowed_roles(['admin', 'companies_admin'])
def add_company_dashboard():
    """
    Description: Directs user to "add company" page
    Possible response codes: 200
    """
    return render_template('admin/companies/add_company.html', error=None)


@bp.post('/new-company')
@allowed_roles(['admin', 'companies_admin'])
def create_company(form: CompanyForm):
    """
    Description: Creates company with parameters given by admin user in form
    Possible response codes: 200, 302
    """
    # name = request.form.get('name')
    # link = request.form.get('link')
    # email = request.form.get('email')
    # business_area = request.form.get('business_area')
    # show_in_website = request.form.get('show_in_website')
    # partnership_tier = request.form.get('partnership_tier')
    # evf_username = request.form.get('evf_username')
    # evf_password = request.form.get('evf_password')
    # cvs_access = request.form.get('cvs_access')
    name = form.name
    link = form.link
    email = form.email
    business_area = form.business_area
    show_in_website = form.show_in_website
    partnership_tier = form.partnership_tier
    evf_username = form.evf_username
    evf_password = form.evf_password
    cvs_access = form.cvs_access

    if partnership_tier == "":
        partnership_tier = None

    if show_in_website == 'True':
        show_in_website = True
    else:
        show_in_website = False

    if cvs_access == 'True':
        cvs_access = True
    else:
        cvs_access = False

    company = CompaniesHandler.create_company(
        name=name,
        email=email,
        business_area=business_area,
        link=link,
        show_in_website=show_in_website,
        partnership_tier=partnership_tier,
        evf_username=evf_username,
        evf_password=evf_password,
        cvs_access=cvs_access
    )
    
    if company is None:
        return render_template('admin/companies/add_company.html', error="Failed to create company! Maybe it already exists :)")

    if 'file' in request.files:
        file = request.files['file']
        result, msg = CompaniesHandler.upload_image(file, name)

        if result == False:
            CompaniesHandler.delete_company(company)
            return render_template('admin/companies/add_company.html', error=msg)

    return redirect(url_for('admin_api.companies_dashboard'))


@bp.get('/company/<string:company_external_id>')
@allowed_roles(['admin', 'companies_admin'])
def get_company(path: CompanyPath):
    """
    Description: Directs admin user to "update company" page of the company labeled by id given in URL
    Possible response codes: 200 
    """
    company = CompaniesFinder.get_from_external_id(path.company_external_id)

    image_path = CompaniesHandler.find_image(company.name)

    return render_template('admin/companies/update_company.html', company=company, image=image_path, error=None)


@bp.post('/company/<string:company_external_id>', responses={'500': APIError})
@allowed_roles(['admin', 'companies_admin'])
def update_company(path: CompanyPath, form: CompanyForm):
    """
    Description: Updates company labeled by id given in URL with paramenters given by admin user in form
    Possible response codes: 200, 302, 500
    """

    company = CompaniesFinder.get_from_external_id(path.company_external_id)

    if company is None:
        return APIErrorValue('Couldnt find company').json(500)

    # name = request.form.get('name')
    # link = request.form.get('link')
    # email = request.form.get('email')
    # business_area = request.form.get('business_area')
    # show_in_website = request.form.get('show_in_website')
    # partnership_tier = request.form.get('partnership_tier')
    # evf_username = request.form.get('evf_username')
    # evf_password = request.form.get('evf_password')
    # cvs_access = request.form.get('cvs_access')

    name = form.name
    link = form.link
    email = form.email
    business_area = form.business_area
    show_in_website = form.show_in_website
    partnership_tier = form.partnership_tier
    evf_username = form.evf_username
    evf_password = form.evf_password
    cvs_access = form.cvs_access


    if partnership_tier == "":
        partnership_tier = None

    if show_in_website == 'True':
        show_in_website = True
    else:
        show_in_website = False

    if cvs_access == 'True':
        cvs_access = True
    else:
        cvs_access = False

    image_path = CompaniesHandler.find_image(name)
    old_company_name = company.name
    
    updated_company = CompaniesHandler.update_company(
        company=company,
        name=name,
        email=email,
        business_area=business_area,
        link=link,
        show_in_website=show_in_website,
        partnership_tier=partnership_tier,
        evf_username=evf_username,
        evf_password=evf_password,
        cvs_access=cvs_access
    )
    
    if updated_company is None:
        return render_template('admin/companies/update_company.html', company=company, image=image_path, error="Failed to update company!")

    if old_company_name != name:
        RenameImageService('static/companies', old_company_name, name).call()

    if 'file' in request.files:
        file = request.files['file']

        result, msg = CompaniesHandler.upload_image(file, name)

        if result == False:
            return render_template('admin/companies/update_company.html', company=updated_company, image=image_path, error=msg)

    return redirect(url_for('admin_api.companies_dashboard'))


@bp.get('/company/<string:company_external_id>/delete', responses={'500':APIError})
@allowed_roles(['admin', 'companies_admin'])
def delete_company(path: CompanyPath):
    """
    Description: Deletes company with id labeled in URL
    Possible response codes: 200, 302, 500
    """
    company = CompaniesFinder.get_from_external_id(path.company_external_id)

    if company is None:
        return APIErrorValue("Couldn't find company").json(500)
    
    name = company.name

    for company_user in company.users:
        CompanyUsersHandler.delete_company_user(company_user)
    
    if CompaniesHandler.delete_company(company):
        return redirect(url_for('admin_api.companies_dashboard'))

    else:
        image_path = CompaniesHandler.find_image(name)
        return render_template('admin/companies/update_company.html', company=company, image=image_path, error="Failed to delete company!")
