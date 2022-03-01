from jeec_brain.schemas.admin_api.activities.schemas import ActivityPath, ActivityTypePath, CodePath
from .. import bp
import uuid
from flask import render_template, current_app, request, redirect, url_for, jsonify
from flask_login import current_user
from datetime import datetime

from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.finders.activity_types_finder import ActivityTypesFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.speakers_finder import SpeakersFinder
from jeec_brain.finders.tags_finder import TagsFinder
from jeec_brain.finders.rewards_finder import RewardsFinder
from jeec_brain.handlers.tags_handler import TagsHandler
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.finders.activity_codes_finder import ActivityCodesFinder
from jeec_brain.handlers.activities_handler import ActivitiesHandler
from jeec_brain.handlers.activity_types_handler import ActivityTypesHandler
from jeec_brain.handlers.activity_codes_handler import ActivityCodesHandler
from jeec_brain.models.enums.activity_chat_enum import ActivityChatEnum
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.apps.auth.wrappers import allowed_roles, allow_all_roles
from jeec_brain.schemas.admin_api.activities import *
from jeec_brain.schemas.admin_api.schemas import *
# Activities routes
@bp.get('/activities')
@allow_all_roles
def activities_dashboard(query: ActivityQuery):
    """
    Description: Searches for the requested event and sends admin user to its dashboard if found
    Possible response codes: 200 
    """
    search_parameters = request.args
    #name = request.args.get('name')
    name = query.name

    # get event
    #event_id = request.args.get('event',None)
    event_id = query.event
    if(event_id is None):
        event = EventsFinder.get_default_event()
    else:
        event = EventsFinder.get_from_external_id(event_id)

    events = EventsFinder.get_all()

    if event is None:
        error = 'No default event found! Please set a default event in the menu "Events"'
        return render_template('admin/activities/activities_dashboard.html', event=None, events=events, activities=None, error=error, search=None, role=current_user.role.name)

    # handle search bar requests
    if name is not None:
        search = name
        activities_list = ActivitiesFinder.search_by_name_and_event(name, event)
    
    # handle parameter requests
    elif len(search_parameters) != 0:
        search_parameters = request.args
        search = 'search name'
        
        if 'type' in search_parameters:
            type_external_id = search_parameters['type']
            activity_type = ActivityTypesFinder.get_from_external_id(uuid.UUID(type_external_id))
            activities_list = ActivitiesFinder.get_all_from_type_and_event(activity_type)
        else:
            activities_list = event.activities

    # request endpoint with no parameters should return all activities
    else:
        search = None
        activities_list = event.activities
    
    if not activities_list:
        error = 'No results found'
        return render_template('admin/activities/activities_dashboard.html', event=event, events=events, activities=None, error=error, search=search, role=current_user.role.name)

    return render_template('admin/activities/activities_dashboard.html', event=event, events=events, activities=activities_list, error=None, search=search, role=current_user.role.name)


# Activities Types routes
@bp.get('/activities/types')
@allow_all_roles
def activity_types_dashboard(query: ActivityQuery):
    """
    Description: Searches event by id given in URL, if none is given seaches default event. Redirects to the event dashboard
    Possible response codes: 200
    """
    events = EventsFinder.get_all()

    #event_id = request.args.get('event',None)
    event_id = query.event
    if(event_id is None):
        event = EventsFinder.get_default_event()
    else:
        event = EventsFinder.get_from_external_id(event_id)

    if event is None:
        error = 'No default event found! Please set a default event in the menu "Events"'
        return render_template('admin/activities/activities_dashboard.html', event=None, events=events, error=error, role=current_user.role.name)
    
    return render_template('admin/activities/activity_types_dashboard.html', event=event, events=events, error=None, role=current_user.role.name)

@bp.post('/activities/types')
@allow_all_roles
def search_activity_types(query: ActivityQuery):
    """
    Description: Searches event by id given in form, if none is given searches default event. Redirects to the event dashboard
    Possible response codes: 200
    """
    events = EventsFinder.get_all()
    
    #event = request.form.get('event', None)
    event = query.event
    if(event is None):
        event = EventsFinder.get_default_event()
    else:
        event = EventsFinder.get_from_external_id(event)
        
    if event is None:
        error = 'No event found! Please set an event in the menu "Events"'
        return render_template('admin/activities/activities_dashboard.html', events=events, event=None, error=error, role=current_user.role.name)
    
    return render_template('admin/activities/activity_types_dashboard.html', events=events, event=event, error=None, role=current_user.role.name)


@bp.get('/new-activity-type',responses={'500':APIError})
@allowed_roles(['admin', 'activities_admin'])
def add_activity_type_dashboard(query:ActivityTypeQuery):
    """
    Description: Search event by id given in URL. Redirects to add activity type page of said event
    Possible response codes: 200, 500
    """
    #event_id = request.args.get('activity',None)
    event_id = query.event_id
    event = EventsFinder.get_from_external_id(event_id)
    if event is None:
        return APIErrorValue('No event found! Please set an event in the menu "Events"').json(500)

    return render_template('admin/activities/add_activity_type.html', event=event, error=None)


@bp.post('/new-activity-type',responses={'500':APIError})
@allowed_roles(['admin', 'activities_admin'])
def create_activity_type(form:ActivityTypeForm):
    """
    Description: Create activity type with parameters given in a form to an event with an id also given in form
    Possible response codes: 200, 302, 500
    """
    #name = request.form.get('name')
    #description = request.form.get('description')
   # price = request.form.get('price')
   # show_in_home = request.form.get('show_in_home')
   # show_in_schedule = request.form.get('show_in_schedule')
   # show_in_app = request.form.get('show_in_app')
    name = form.name
    description = form.description
    price = form.price
    show_in_home = form.show_in_home
    show_in_schedule = form.show_in_schedule
    show_in_app = form.show_in_app

    if show_in_home == 'True':
        show_in_home = True
    else:
        show_in_home = False

    if show_in_schedule == 'True':
        show_in_schedule = True
    else:
        show_in_schedule = False

    if show_in_app == 'True':
        show_in_app = True
    else:
        show_in_app = False

    event_id = form.event_id
    event = EventsFinder.get_from_external_id(event_id)
    if event is None:
        return APIErrorValue('No event found! Please set an event in the menu "Events"').json(500)

    activity_type = ActivityTypesHandler.create_activity_type(
            event=event,
            name=name,
            description=description,
            price=price,
            show_in_home=show_in_home,
            show_in_schedule=show_in_schedule,
            show_in_app=show_in_app
        )

    if activity_type is None:
        return render_template('admin/activities/add_activity_type.html',
            event=event,
            error="Failed to create activity type! Maybe it already exists :)")

    return redirect(url_for('admin_api.activity_types_dashboard'))


@bp.get('/activities/types/<string:activity_type_external_id>')
@allowed_roles(['admin', 'activities_admin'])
def get_activity_type(path: ActivityTypePath):
    """
    Description: Directs user to update activity type page
    Possible response codes: 200
    """
    activity_type = ActivityTypesFinder.get_from_external_id(path.activity_type_external_id)

    return render_template('admin/activities/update_activity_type.html', \
        activity_type=activity_type,
        error=None)


@bp.post('/activities/types/<string:activity_type_external_id>')
@allowed_roles(['admin', 'activities_admin'])
def update_activity_type(path: ActivityTypePath, form: ActivityTypeForm):
    """
    Description: Update activity type with parameters given in a form to an event with an id also given in form
    Possible response codes: 200, 302
    """
    #name = request.form.get('name')
    #description = request.form.get('description')
    #price = request.form.get('price')
    #show_in_home = request.form.get('show_in_home')
    #show_in_schedule = request.form.get('show_in_schedule')
    #show_in_app = request.form.get('show_in_app')
    name= form.name
    description= form.description
    price= form.price
    show_in_home= form.show_in_home
    show_in_schedule = form.show_in_schedule
    show_in_app = form.show_in_app

    if show_in_home == 'True':
        show_in_home = True
    else:
        show_in_home = False

    if show_in_schedule == 'True':
        show_in_schedule = True
    else:
        show_in_schedule = False

    if show_in_app == 'True':
        show_in_app = True
    else:
        show_in_app = False

    activity_type = ActivityTypesFinder.get_from_external_id(path.activity_type_external_id)

    updated_activity_type = ActivityTypesHandler.update_activity_type(
        activity_type=activity_type,
        name=name,
        description=description,
        price=price,
        show_in_home=show_in_home,
        show_in_schedule=show_in_schedule,
        show_in_app=show_in_app
    )

    if updated_activity_type is None:
        return render_template('admin/activities/update_activity_type.html',
            activity_type=activity_type,
            error="Failed to update activity type!")

    return redirect(url_for('admin_api.activity_types_dashboard'))

@bp.get('/activities/types/<string:activity_type_external_id>/delete',responses={'500':APIError})
@allowed_roles(['admin', 'activities_admin'])
def delete_activity_type(path: ActivityTypePath):
    """
    Description: Deletes activity type with id given by external id
    Possible response codes: 200, 302, 500
    """
    activity_type = ActivityTypesFinder.get_from_external_id(path.activity_type_external_id)

    if activity_type.activities:
        for activity in activity_type.activities:
            if activity is None:
                return APIErrorValue('Couldnt find activity').json(500)
            
            company_activities = ActivitiesFinder.get_company_activities_from_activity_id(activity.external_id)
            speaker_activities = ActivitiesFinder.get_speaker_activities_from_activity_id(activity.external_id)

            if company_activities:
                for company_activity in company_activities:
                    ActivitiesHandler.delete_company_activities(company_activity)

            if speaker_activities:
                for speaker_activity in speaker_activities:
                    ActivitiesHandler.delete_speaker_activities(speaker_activity)

            if not ActivitiesHandler.delete_activity(activity):
                return APIErrorValue('Couldnt delete activity').json(500)
                
    if ActivityTypesHandler.delete_activity_type(activity_type):
        return redirect(url_for('admin_api.activity_types_dashboard'))

    return render_template('admin/activities/update_activity_type.html',
            activity_type=activity_type,
            error="Failed to update activity type!")

@bp.get('/new-activity')
@allowed_roles(['admin', 'activities_admin'])
def add_activity_dashboard(query:ActivityQuery):
    """
    Description: Directs user to add activity page
    Possible response codes: 200
    """
    companies = CompaniesFinder.get_all()
    speakers = SpeakersFinder.get_all()
    tags = TagsFinder.get_all()
    rewards = RewardsFinder.get_all_rewards()

    #event_id = request.args.get('event',None)
    event_id = query.event_id
    if(event_id is None):
        event = EventsFinder.get_default_event()
    else:
        event = EventsFinder.get_from_external_id(event_id)
    
    if event is None:
        error = 'No default event found! Please set a default event in the menu "Events"'
        return render_template('admin/activities/activities_dashboard.html', event=None, error=error, role=current_user.role.name)
    
    try:
        minDate = datetime.strptime(event.start_date,'%d %b %Y, %a').strftime("%Y,%m,%d")
        maxDate = datetime.strptime(event.end_date,'%d %b %Y, %a').strftime("%Y,%m,%d")
    except:
        minDate = None
        maxDate = None

    return render_template('admin/activities/add_activity.html', \
        companies=companies, \
        speakers=speakers, \
        tags=tags, \
        minDate=minDate, \
        maxDate=maxDate, \
        event=event, \
        rewards=rewards, \
        error=None)


@bp.post('/new-activity',responses={'500':APIError})
@allowed_roles(['admin', 'activities_admin'])
def create_activity(form: ActivityForm):
    """
    Description: Creates activity with parameters given in form
    Possible response codes: 200, 500
    """
    # name = request.form.get('name')
    # description = request.form.get('description')
    # location = request.form.get('location')
    # day = request.form.get('day')
    # time = request.form.get('time')
    # end_time = request.form.get('end_time')
    # registration_link = request.form.get('registration_link')
    # registration_open = request.form.get('registration_open')
    # points = request.form.get('points') or None
    # quest = request.form.get('quest')
    # chat = request.form.get('chat')
    # zoom_link = request.form.get('zoom_url')
    # reward_id = request.form.get('reward') or None
    # moderator = request.form.get('moderator') or None

    name = form.name
    description = form.description
    location = form.location
    day = form.day
    time = form.time
    end_time = form.end_time
    registration_link = form.registration_link
    registration_open = form.registration_open
    points = form.points
    quest = form.quest
    chat = form.chat
    zoom_link = form.zoom_link
    reward_id = form.reward_id
    moderator = form.moderator

    if registration_open == 'True':
        registration_open = True
    else:
        registration_open = False

    if quest == 'True':
        quest = True
    else:
        quest = False

    chat_type = ActivityChatEnum[chat]

    #activity_type_external_id = request.form.get('type')
    activity_type_external_id = form.activity_type_external_id
    activity_type = ActivityTypesFinder.get_from_external_id(uuid.UUID(activity_type_external_id))
    event = activity_type.event

    if event is None:
        error = 'No default event found! Please set a default event in the menu "Events"'
        return render_template('admin/activities/activities_dashboard.html', event=None, error=error, role=current_user.role.name)

    if time > end_time:
        error = 'Activity starting time after ending time'
        return render_template('admin/activities/activities_dashboard.html', event=event, error=error, role=current_user.role.name)

    activity = ActivitiesHandler.create_activity(
            name=name,
            description=description,
            activity_type=activity_type,
            event=event,
            location=location,
            day=day,
            time=time,
            end_time=end_time,
            registration_link=registration_link,
            registration_open=registration_open,
            points=points,
            quest=quest,
            zoom_link=zoom_link,
            chat_type=chat_type,
            chat=(chat=='general'),
            reward_id=reward_id
        )

    if activity is None:
        companies = CompaniesFinder.get_all()
        speakers = SpeakersFinder.get_all()
        tags = TagsFinder.get_all()
        rewards = RewardsFinder.get_all_rewards()

        try:
            minDate = datetime.strptime(event.start_date,'%d %b %Y, %a').strftime("%Y,%m,%d")
            maxDate = datetime.strptime(event.end_date,'%d %b %Y, %a').strftime("%Y,%m,%d")
        except:
            minDate = None
            maxDate = None

        return render_template('admin/activities/add_activity.html', \
            companies=companies, \
            speakers=speakers, \
            tags=tags, \
            rewards=rewards, \
            minDate=minDate, \
            maxDate=maxDate, \
            event=event, \
            error="Failed to create activity! Maybe it already exists :)")

    # extract company names and speaker names from parameters
    # companies = request.form.getlist('company')
    # zoom_urls = request.form.getlist('url')
    # speakers = request.form.getlist('speaker')
    # tags = request.form.getlist('tag')
    companies = form.companies
    zoom_urls = form.zoom_urls
    speakers = form.speakers
    tags = form.tags
    job_fair_booth = ActivityTypesFinder.get_from_name('Job Fair Booth')

    # if company names where provided
    if companies:
        for index, name in enumerate(companies):
            company = CompaniesFinder.get_from_name(name)
            if company is None:
                return APIErrorValue('Couldnt find company').json(500)

            company_activity = ActivitiesHandler.add_company_activity(company, activity, zoom_urls[index])
            if company_activity is None:
                return APIErrorValue('Failed to create company activity').json(500)

            if activity_type.name == 'Job Fair':
                job_fair_booth_activity = ActivitiesHandler.create_activity(
                    name=company.name + " Booth",
                    description="Visit " + company.name + " booth to earn extra points",
                    activity_type=job_fair_booth,
                    event=event,
                    location="Job Fair",
                    day=day,
                    time='10:30',
                    end_time='16:30',
                    points=40,
                    quest=False
                )
                ActivitiesHandler.add_company_activity(company, job_fair_booth_activity)

    if speakers:
        for name in speakers:
            speaker = SpeakersFinder.get_from_name(name)
            if speaker is None:
                return APIErrorValue('Couldnt find speaker').json(500)

            speaker_activity = ActivitiesHandler.add_speaker_activity(speaker, activity)
            if speaker_activity is None:
                return APIErrorValue('Failed to create speaker activity').json(500)

        if(moderator and moderator in speakers):
            moderator = SpeakersFinder.get_from_name(moderator)
            if moderator is None:
                return APIErrorValue('Couldnt find moderator').json(500)

            ActivitiesHandler.update_activity(activity, activity_type, moderator_id = moderator.id)

    if tags:
        for name in tags:
            tag = TagsFinder.get_by_name(name)
            if tag is None:
                return APIErrorValue('Couldnt find tag').json(500)

            activity_tag = TagsHandler.add_activity_tag(activity, tag)
            if activity_tag is None:
                return APIErrorValue('Failed to create activity tag').json(500)        

    return redirect(url_for('admin_api.activities_dashboard'))


@bp.get('/activity/<string:activity_external_id>')
@allowed_roles(['admin', 'activities_admin'])
def get_activity(path: ActivityPath):
    """
    Description: Finds the activity labeled by the external id and directs admin user to the "update activity" page of said activity
    Possible response codes: 200 
    """
    activity = ActivitiesFinder.get_from_external_id(path.activity_external_id)
    companies = CompaniesFinder.get_all()
    speakers = SpeakersFinder.get_all()
    tags = TagsFinder.get_all()
    rewards = RewardsFinder.get_all_rewards()

    event = EventsFinder.get_from_parameters({"default": True})     
    if event is None or len(event) == 0:
        error = 'No default event found! Please set a default event in the menu "Events"'
        return render_template('admin/activities/activities_dashboard.html', event=None, error=error, role=current_user.role.name)
    
    activity_types = event[0].activity_types
    company_activities = ActivitiesFinder.get_company_activities_from_activity_id(path.activity_external_id)
    speaker_activities = ActivitiesFinder.get_speaker_activities_from_activity_id(path.activity_external_id)
    activity_tags = TagsFinder.get_activity_tags_from_activity_id(path.activity_external_id)

    try:
        minDate = datetime.strptime(event[0].start_date,'%d %b %Y, %a').strftime("%Y,%m,%d")
        maxDate = datetime.strptime(event[0].end_date,'%d %b %Y, %a').strftime("%Y,%m,%d")
    except:
        minDate = None
        maxDate = None

    companies_zoom_url = {}
    for company in company_activities:
        companies_zoom_url[company.company_id] = company.zoom_link

    return render_template('admin/activities/update_activity.html', \
        activity=activity, \
        activity_types=activity_types, \
        companies=companies, \
        speakers=speakers, \
        tags=tags, \
        rewards=rewards, \
        company_activities=[company.company_id for company in company_activities], \
        speaker_activities=[speaker.speaker_id for speaker in speaker_activities], \
        companies_zoom_url=companies_zoom_url, \
        activity_tags=[tag.tag_id for tag in activity_tags], \
        minDate=minDate, \
        maxDate=maxDate, \
        error=None)


@bp.post('/activity/<string:activity_external_id>',responses={'500':APIError})
@allowed_roles(['admin', 'activities_admin'])
def update_activity(path: ActivityPath, form:ActivityForm):
    """
    Description: Updates activity labeled by external id with parameters given in a form
    Possible response codes: 200, 302, 500
    """
    activity = ActivitiesFinder.get_from_external_id(path.activity_external_id)
    company_activities = ActivitiesFinder.get_company_activities_from_activity_id(path.activity_external_id)
    speaker_activities = ActivitiesFinder.get_speaker_activities_from_activity_id(path.activity_external_id)
    activity_tags = TagsFinder.get_activity_tags_from_activity_id(path.activity_external_id)

    if activity is None:
        return APIErrorValue('Couldnt find activity').json(500)

    # name = request.form.get('name')
    # description = request.form.get('description')
    # location = request.form.get('location')
    # day = request.form.get('day')
    # time = request.form.get('time')
    # end_time = request.form.get('end_time')
    # registration_link = request.form.get('registration_link')
    # registration_open = request.form.get('registration_open')
    # points = request.form.get('points') or None
    # quest = request.form.get('quest')
    # chat = request.form.get('chat')
    # zoom_link = request.form.get('zoom_url')
    # reward_id = request.form.get('reward') or None
    # moderator = request.form.get('moderator') or None
    name = form.name
    description = form.description
    location = form.location
    day = form.day
    time = form.time
    end_time = form.end_time
    registration_link = form.registration_link
    registration_open = form.registration_open
    points = form.points
    quest = form.quest
    chat = form.chat
    zoom_link = form.zoom_link
    reward_id = form.reward_id
    moderator = form.moderator

    if time > end_time is None:
        return APIErrorValue('Activity starting time after ending time').json(500)

    if registration_open == 'True':
        registration_open = True
    else:
        registration_open = False

    if quest == 'True':
        quest = True
    else:
        quest = False

    chat_type = ActivityChatEnum[chat] if chat else None

    #activity_type_external_id = request.form.get('type')
    activity_type_external_id = form.activity_type_external_id
    activity_type = ActivityTypesFinder.get_from_external_id(uuid.UUID(activity_type_external_id))

    updated_activity = ActivitiesHandler.update_activity(
        activity=activity,
        activity_type=activity_type,
        name=name,
        description=description,
        location=location,
        day=day,
        time=time,
        end_time=end_time,
        registration_link=registration_link,
        registration_open=registration_open,
        points=points,
        quest=quest,
        zoom_link=zoom_link,
        chat_type=chat_type,
        chat=(chat=='general'),
        reward_id=reward_id
    )

    if company_activities:
        for company_activity in company_activities:
            ActivitiesHandler.delete_company_activities(company_activity)

    if speaker_activities:
        for speaker_activity in speaker_activities:
            ActivitiesHandler.delete_speaker_activities(speaker_activity)

    if activity_tags:
        for activity_tag in activity_tags:
            TagsHandler.delete_activity_tag(activity_tag)

    # extract company names and speaker names from parameters
    # companies = request.form.getlist('company')
    # zoom_urls = request.form.getlist('url')
    # speakers = request.form.getlist('speaker')
    # tags = request.form.getlist('tag')

    companies = form.companies
    zoom_urls = form.zoom_urls
    speakers = form.speakers
    tags = form.tags


    # if company names where provided
    if companies:
        for index, name in enumerate(companies):
            company = CompaniesFinder.get_from_name(name)
            if company is None:
                return APIErrorValue('Couldnt find company').json(500)

            company_activity = ActivitiesHandler.add_company_activity(company, activity, zoom_urls[index])
            if company_activity is None:
                return APIErrorValue('Failed to create company activity').json(500)

            if activity_type.name == 'Job Fair':
                job_fair_booth = ActivityTypesFinder.get_from_name('Job Fair Booth')
                if not ActivitiesFinder.get_from_parameters({'name':company.name + " Booth",'day':day}):
                    job_fair_booth_activity = ActivitiesHandler.create_activity(
                        name=company.name + " Booth",
                        description="Visit " + company.name + " booth to earn extra points",
                        activity_type=job_fair_booth,
                        event=activity.event,
                        location="Job Fair",
                        day=day,
                        time='10:30',
                        end_time='16:30',
                        points=40,
                        quest=False
                    )
                    ActivitiesHandler.add_company_activity(company, job_fair_booth_activity)

    if speakers:
        for name in speakers:
            speaker = SpeakersFinder.get_from_name(name)
            if speaker is None:
                return APIErrorValue('Couldnt find speaker').json(500)

            speaker_activity = ActivitiesHandler.add_speaker_activity(speaker, activity)
            if speaker_activity is None:
                return APIErrorValue('Failed to create speaker activity').json(500)
        
        if(moderator and moderator in speakers):
            moderator = SpeakersFinder.get_from_name(moderator)
            if moderator is None:
                return APIErrorValue('Couldnt find moderator').json(500)

            ActivitiesHandler.update_activity(activity, activity_type, moderator_id = moderator.id)

        elif(not moderator):
            ActivitiesHandler.update_activity(activity, activity_type, moderator_id = None)


    if tags:
        for name in tags:
            tag = TagsFinder.get_by_name(name)
            if tag is None:
                return APIErrorValue('Couldnt find tag').json(500)

            activity_tag = TagsHandler.add_activity_tag(activity, tag)
            if activity_tag is None:
                return APIErrorValue('Failed to create activity tag').json(500)
                
    if updated_activity is None:
        event = EventsFinder.get_from_parameters({"default": True})
    
        if event is None or len(event) == 0:
            error = 'No default event found! Please set a default event in the menu "Events"'
            return render_template('admin/activities/activities_dashboard.html', event=None, error=error, role=current_user.role.name)
        
        activity_types = event[0].activity_types

        try:
            minDate = datetime.strptime(event[0].start_date,'%d %b %Y, %a').strftime("%Y,%m,%d")
            maxDate = datetime.strptime(event[0].end_date,'%d %b %Y, %a').strftime("%Y,%m,%d")
        except:
            minDate = None
            maxDate = None

        return render_template('admin/activities/update_activity.html', \
            activity=activity, \
            types=activity_types, \
            companies=CompaniesFinder.get_all(), \
            speakers=SpeakersFinder.get_all(), \
            tags=TagsFinder.get_all(), \
            rewards=RewardsFinder.get_all_rewards(), \
            minDate=minDate, \
            maxDate=maxDate, \
            error="Failed to update activity!")

    return redirect(url_for('admin_api.activities_dashboard'))


@bp.get('/activity/<string:activity_external_id>/delete', responses={'500':APIError})
@allowed_roles(['admin', 'activities_admin'])
def delete_activity(path: ActivityPath):
    """
    Description: Deletes activity labeled by external id
    Possible response codes: 200, 302, 500
    """
    activity = ActivitiesFinder.get_from_external_id(path.activity_external_id)
    company_activities = ActivitiesFinder.get_company_activities_from_activity_id(path.activity_external_id)
    speaker_activities = ActivitiesFinder.get_speaker_activities_from_activity_id(path.activity_external_id)
    activity_tags = TagsFinder.get_activity_tags_from_activity_id(path.activity_external_id)

    if activity is None:
        return APIErrorValue('Couldnt find activity').json(500)
        
    if company_activities:
        for company_activity in company_activities:
            ActivitiesHandler.delete_company_activities(company_activity)

    if speaker_activities:
        for speaker_activity in speaker_activities:
            ActivitiesHandler.delete_speaker_activities(speaker_activity)

    if activity_tags:
        for activity_tag in activity_tags:
            TagsHandler.delete_activity_tag(activity_tag)

    if ActivitiesHandler.delete_activity(activity):
        return redirect(url_for('admin_api.activities_dashboard'))

    else:
        return render_template('admin/activities/update_activity.html', activity=activity, error="Failed to delete activity!")

@bp.post('/activity/<string:activity_external_id>/code',responses={'201':ActivityCodes, '404':APIError})
@allowed_roles(['admin', 'activities_admin'])
def generate_codes(path: ActivityPath, form:ActivityCodesNumber):
    """
    Description: Creates codes (number of codes specified by admin user in a form) to activity labeled by external id
    Possible response codes: 201, 404
    """
    activity = ActivitiesFinder.get_from_external_id(path.activity_external_id)
    if activity is None:
        return APIErrorValue('Couldnt find activity').json(404)

    #number = request.form.get('number', 1)
    number = form.number
    activity_codes = []
    
    for _ in range(int(number)):
        activity_codes.append(ActivityCodesHandler.create_activity_code(activity_id=activity.id).code)

    return jsonify(activity_codes),201

@bp.post('/activity/<string:activity_external_id>/codes-delete',responses={'201':SuccessStr,'404':APIError, '500': APIError})
@allowed_roles(['admin', 'activities_admin'])
def delete_activity_code(path: ActivityPath):
    """
    Description: Deletes all codes with parametres given in URL of the activity labeled by external id
    Possible response codes: 201, 404, 500
    """
    activity = ActivitiesFinder.get_from_external_id(path.activity_external_id)
    if activity is None:
        return APIErrorValue('Couldnt find activity').json(404)

    codes = ActivityCodesFinder.get_from_parameters({'activity_id':activity.id})
    for code in codes:
        if not ActivityCodesHandler.delete_activity_code(code):
            return jsonify("Failed"), 500

    return jsonify("Success"),201

@bp.post('/code/<string:code>/delete', responses={'201':SuccessDict,'404':APIError})
@allowed_roles(['admin', 'activities_admin'])
def delete_code(path: CodePath):
    """
    Description: Deletes code given in URL
    Possible response codes: 201, 404
    """
    code = ActivityCodesFinder.get_from_code(path.code)
    if code is None:
        return APIErrorValue('Couldnt find code').json(404)

    return jsonify({'success':ActivityCodesHandler.delete_activity_code(code)}),201