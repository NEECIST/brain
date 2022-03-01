from http.client import responses
from .. import bp
from flask import render_template, request, redirect, url_for
from jeec_brain.finders.teams_finder import TeamsFinder
from jeec_brain.finders.colaborators_finder import ColaboratorsFinder
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.handlers.teams_handler import TeamsHandler
from jeec_brain.apps.auth.wrappers import allowed_roles, allow_all_roles
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.schemas.admin_api.team.schemas import *
from flask_login import current_user
from jeec_brain.services.files.rename_image_service import RenameImageService

#Schemas
from jeec_brain.schemas.admin_api.schemas import *

# Team management
@bp.get('/teams')
@allow_all_roles
def teams_dashboard():
    """
        Description: Loads page with teams that are participating in the default event
        Possible response codes: 200
    """
    default_event = EventsFinder.get_default_event()
    events = EventsFinder.get_all()
    teams_list = TeamsFinder.get_from_parameters({'event_id':default_event.id})

    if len(teams_list) == 0:
        error = 'No results found'
        return render_template('admin/teams/teams_dashboard.html', teams=None, events=events, selected_event=default_event.id, error=error, search=None, role=current_user.role.name)

    return render_template('admin/teams/teams_dashboard.html', teams=teams_list, events=events, selected_event=default_event.id, error=None, search=None, role=current_user.role.name)


@bp.post('/teams')
@allow_all_roles
def search_team(form:TeamForm):
    """
        Description: Searches for a certain team that is partcipating in a specific event and loads a page with the results
        Possible response codes: 200
    """
    # name = request.form.get('name', None)
    # event_id = request.form.get('event', None)
    name = form.name
    event_id = form.event

    events = EventsFinder.get_all()
    search_parameters = {}

    if(name is not None):
        search_parameters['name'] = name
    if(event_id is not None):
        search_parameters['event_id'] = event_id
    
    teams_list = TeamsFinder.get_from_parameters(search_parameters)

    if len(teams_list) == 0:
        error = 'No results found'
        return render_template('admin/teams/teams_dashboard.html', teams=None, events=events, selected_event=event_id, error=error, search=name, role=current_user.role.name)

    return render_template('admin/teams/teams_dashboard.html', teams=teams_list, events=events, selected_event=event_id, error=None, search=name, role=current_user.role.name)


@bp.get('/new-team')
@allowed_roles(['admin', 'teams_admin'])
def add_team_dashboard():
    """
        Description: Directs user to "add_team" page
        Possible response codes: 200
    """
    events = EventsFinder.get_all()
    return render_template('admin/teams/add_team.html', events=events)


@bp.post('/new-team')
@allowed_roles(['admin', 'teams_admin'])
def create_team(form:TeamForm):
    """
        Description: Creates a team with some given parameters, such as name etc
        Possible response codes: 200 , 302
    """
    # name = request.form.get('name')
    # description = request.form.get('description')
    # website_priority = request.form.get('website_priority')
    # event_id = request.form.get('event')
    name = form.name
    description = form.description
    website_priority = form.website_priority
    event_id = form.event
   

    event = EventsFinder.get_from_id(event_id)
    if name in [team.name for team in event.teams]:
        return render_template('admin/teams/add_team.html', error="Failed to create team! Team name already exists")

    if not website_priority:
        website_priority = 0

    team = TeamsHandler.create_team(
        name=name,
        description=description,
        website_priority=website_priority,
        event_id=event_id
    )
    
    if team is None:
        return render_template('admin/teams/add_team.html', error="Failed to create team!")

    return redirect(url_for('admin_api.teams_dashboard'))


@bp.get('/team/<string:team_external_id>')
@allowed_roles(['admin', 'teams_admin'])
def get_team(path: TeamPath):
    """
        Description: Directs user to "update_team" page
        Possible response codes: 200
    """
    team = TeamsFinder.get_from_external_id(path.team_external_id)
    events = EventsFinder.get_all()

    return render_template('admin/teams/update_team.html', team=team, events=events)


@bp.post('/team/<string:team_external_id>', responses = {'500': APIError})
@allowed_roles(['admin', 'teams_admin'])
def update_team(path: TeamPath, form:TeamForm):
    """
        Description: Updates team with some parameters given in a form
        Possible response codes: 200 , 302 , 500
    """
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)

    # name = request.form.get('name')
    # description = request.form.get('description')
    # website_priority = request.form.get('website_priority')
    # event = request.form.get('event')
    name = form.name
    description = form.description
    website_priority = form.website_priority
    event_id = form.event

    event = EventsFinder.get_from_id(event_id)
    if name in [team.name for team in event.teams]:
        return render_template('admin/teams/add_team.html', error="Failed to update team! Team name already exists")


    updated_team = TeamsHandler.update_team(
        team=team,
        name=name,
        description=description,
        website_priority=website_priority,
        event_id=event_id
    )
    
    if updated_team is None:
        return render_template('admin/teams/update_team.html', team=team, error="Failed to update team!")

    return redirect(url_for('admin_api.teams_dashboard'))


@bp.get('/team/<string:team_external_id>/delete', responses = {'500': APIError})
@allowed_roles(['admin', 'teams_admin'])
def delete_team(path: TeamPath):
    """
        Description: Deletes team with id given in the URL if possible 
        Possible response codes: 200 , 302 , 500
    """
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)
        
    if TeamsHandler.delete_team(team):
        return redirect(url_for('admin_api.teams_dashboard'))

    else:
        return render_template('admin/teams/update_team.html', team=team, error="Failed to delete team!")


# Members management
@bp.get('/team/<string:team_external_id>/members', responses = {'500': APIError})
@allow_all_roles
def team_members_dashboard(path: TeamPath):
    """
        Description: Loads page with all the members that are part of the team given in the URL
        Possible response codes: 200 , 500
    """
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)

    if len(team.members.all()) == 0:
        error = 'No results found'
        return render_template('admin/teams/team_members_dashboard.html', team=team, members=None, error=error, search=None, role=current_user.role.name)

    return render_template('admin/teams/team_members_dashboard.html', team=team, members=team.members, error=None, search=None, role=current_user.role.name)


@bp.post('/team/<string:team_external_id>/members', responses = {'500': APIError})
@allow_all_roles
def search_team_members(path: TeamPath):
    """
        Description: Search for a member of a specific team, the team id is given in the URL
        Possible response codes: 200 , 500
    """
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)

    name = request.form.get('name')
    members_list = ColaboratorsFinder.search_by_name(name)

    if len(members_list) == 0:
        error = 'No results found'
        return render_template('admin/teams/team_members_dashboard.html', team=team, members=None, error=error, search=name, role=current_user.role.name)

    return render_template('admin/teams/team_members_dashboard.html', team=team, members=members_list, error=None, search=name, role=current_user.role.name)


@bp.get('/team/<string:team_external_id>/erase', responses = {'500': APIError})
@allowed_roles(['admin', 'teams_admin'])
def delete_all_team_members(path: TeamPath):
    """
        Description: Deletes all members in a team
        Possible response codes: 200 , 500
    """
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)

    members = ColaboratorsFinder.get_all_from_team(team)

    if not members:
        return APIErrorValue('Couldnt find team members').json(500)
    
    for member in members:
        TeamsHandler.delete_team_member(member)
    return redirect(url_for('admin_api.team_members_dashboard', team_external_id=path.team_external_id))


@bp.get('/team/<string:team_external_id>/new-member', responses = {'500': APIError})
@allowed_roles(['admin', 'teams_admin'])
def add_team_member_dashboard(path: TeamPath):
    """
        Description: Adds a member to a specific team, the team id is given in the URL
        Possible response codes: 200 , 500
    """
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)

    return render_template('admin/teams/add_team_member.html', team=team)


@bp.post('/team/<string:team_external_id>/new-member', responses = {'500': APIError})
@allowed_roles(['admin', 'teams_admin'])
def create_team_member(path: TeamPath,form:CreateMemberForm):
    """
        Description: Creates team member with parameters given in a form and a profile picture, the team id is given in the URL
        Possible response codes: 200 , 302 , 500
    """
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)

    # name = request.form.get('name')
    # ist_id = request.form.get('ist_id')
    # email = request.form.get('email')
    # linkedin_url = request.form.get('linkedin_url')
    name = form.name
    ist_id = form.ist_id
    email = form.email
    linkedin_url = form.linkedin_url

    if len(ColaboratorsFinder.get_from_event_and_name(team.event_id, name)) > 0:
        return render_template('admin/teams/add_team_member.html', team=team, error="Failed to create team member! Colaborator already exists")

    member = TeamsHandler.create_team_member(
        team=team,
        name=name,
        ist_id=ist_id,
        email=email,
        linkedin_url=linkedin_url
    )
    
    if member is None:
        return render_template('admin/teams/add_team_member.html', team=team, error="Failed to create team member!")

    if 'file' in request.files:
        file = request.files['file']
        result, msg = TeamsHandler.upload_member_image(file, name)

        if result == False:
            TeamsHandler.delete_team_member(member)
            return render_template('admin/teams/add_team_member.html', team=team, error=msg)

    return redirect(url_for('admin_api.team_members_dashboard', team_external_id=path.team_external_id))


@bp.get('/team/<string:team_external_id>/members/<string:member_external_id>', responses = {'500': APIError})
@allowed_roles(['admin', 'teams_admin'])
def get_team_member(path: TeamMemberPath):
    """
        Description: Searches for a team member with the id given in the URL that belongs to the team whose id is also in the URL
        Possible response codes: 200 , 500
    """
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)

    member = ColaboratorsFinder.get_from_external_id(path.member_external_id)

    if member is None:
        return APIErrorValue('Couldnt find team member').json(500)

    image_path = TeamsHandler.find_member_image(member.name)

    return render_template('admin/teams/update_team_member.html', member=member, image=image_path, error=None)


@bp.post('/team/<string:team_external_id>/members/<string:member_external_id>', responses = {'500': APIError})
@allowed_roles(['admin', 'teams_admin'])
def update_team_member(path: TeamMemberPath,form: CreateMemberForm):
    """
        Description: Updates the information about a team member with the id given in the URL that belongs to the team whose id is also in the URL
        Possible response codes: 200 , 302 , 500
    """
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)

    member = ColaboratorsFinder.get_from_external_id(path.member_external_id)

    if member is None:
        return APIErrorValue('Couldnt find team member').json(500)

    # name = request.form.get('name')
    # ist_id = request.form.get('ist_id')
    # email = request.form.get('email')
    # linkedin_url = request.form.get('linkedin_url')
    name = form.name
    ist_id = form.ist_id
    email = form.email
    linkedin_url = form.linkedin_url

    old_member_name = member.name

    if len(ColaboratorsFinder.get_from_event_and_name(team.event_id, name)) > 1:
        return render_template('admin/teams/add_team_member.html', team=team, error="Failed to create team member! Colaborator already exists")

    updated_member = TeamsHandler.update_team_member(
        member=member,
        name=name,
        ist_id=ist_id,
        email=email,
        linkedin_url=linkedin_url
    )

    image_path = TeamsHandler.find_member_image(name)
    
    if updated_member is None:
        return render_template('admin/teams/update_team_member.html', member=member, image=image_path, error="Failed to update team member!")

    if old_member_name != name:
        RenameImageService('static/members', old_member_name, name).call()

    if 'file' in request.files:
        file = request.files['file']
        result, msg = TeamsHandler.upload_member_image(file, name)

        if result == False:
            return render_template('admin/teams/update_team_member.html', member=updated_member, image=image_path, error=msg)

    return redirect(url_for('admin_api.team_members_dashboard', team_external_id=path.team_external_id))


@bp.get('/team/<string:team_external_id>/members/<string:member_external_id>/delete', responses = {'500': APIError})
@allowed_roles(['admin', 'teams_admin'])
def delete_team_member(path: TeamMemberPath):
    """
        Description: Deletes a team member with the id given in the URL that belongs to the team whose id is also in the URL
        Possible response codes: 200 , 302 , 500
    """
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)

    member = ColaboratorsFinder.get_from_external_id(path.member_external_id)

    if member is None:
        return APIErrorValue('Couldnt find team member').json(500)
    
    name = member.name

    if TeamsHandler.delete_team_member(member):
        return redirect(url_for('admin_api.team_members_dashboard', team_external_id=path.team_external_id))

    else:
        image_path = TeamsHandler.find_member_image(name)
        return render_template('admin/teams/update_team_member.html', member=member, image=image_path, error="Failed to delete team member!")
