from jeec_brain.handlers.lootbox_handler import LootboxHandler
from .. import bp
from flask import render_template, current_app, request, redirect, url_for, jsonify
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.finders.squads_finder import SquadsFinder
from jeec_brain.finders.levels_finder import LevelsFinder
from jeec_brain.finders.tags_finder import TagsFinder
from jeec_brain.finders.rewards_finder import RewardsFinder
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.finders.lootbox_finder import LootboxFinder
from jeec_brain.handlers.lootbox_rewards_handler import LootboxRewardsHandler
from jeec_brain.handlers.students_handler import StudentsHandler
from jeec_brain.handlers.squads_handler import SquadsHandler
from jeec_brain.handlers.levels_handler import LevelsHandler
from jeec_brain.handlers.users_handler import UsersHandler
from jeec_brain.handlers.tags_handler import TagsHandler
from jeec_brain.handlers.rewards_handler import RewardsHandler
from jeec_brain.handlers.events_handler import EventsHandler
from jeec_brain.apps.auth.wrappers import allowed_roles, allow_all_roles
from jeec_brain.schemas.admin_api.student_app.schemas import *
from flask_login import current_user
from datetime import datetime
from random import choice

# Student App routes
@bp.get('/students-app')
@allowed_roles(['admin'])
def students_app_dashboard():
    
    return render_template('admin/students_app/students_app_dashboard.html')

@bp.get('/students')
@allowed_roles(['admin'])
def students_dashboard():
    search = request.args.get('search')

    # handle search bar requests
    if search is not None:
        students_list = StudentsFinder.get_from_search(search)
    else:
        search = None
        students_list = StudentsFinder.get_all()
    
    if students_list is None or len(students_list) == 0:
        error = 'No students found'
        return render_template('admin/students_app/students/students_dashboard.html', students=None, error=error, search=search, current_user=current_user)
    
    return render_template('admin/students_app/students/students_dashboard.html', students=students_list, error=None, search=search, current_user=current_user)

@bp.post('/student/<string:student_external_id>/ban')
@allowed_roles(['admin'])
def ban_student(path: StudentPath):
    student = StudentsFinder.get_from_external_id(path.student_external_id)
    if student is None:
        return APIErrorValue('Couldnt find student').json(500)
    
    if student.squad:
        SquadsHandler.delete_squad(student.squad)
        
    banned_student = StudentsHandler.create_banned_student(student)
    if banned_student is None:
        return APIErrorValue('Error banning student').json(500)

    UsersHandler.delete_user(student.user)

    return redirect(url_for('admin_api.students_dashboard'))

@bp.get('/banned-students')
@allowed_roles(['admin'])
def banned_students_dashboard():
    banned_students = StudentsFinder.get_all_banned()

    if banned_students is None or len(banned_students) == 0:
        error = 'No banned students found'
        return render_template('admin/students_app/students/banned_students_dashboard.html', students=None, error=error, current_user=current_user)
    
    return render_template('admin/students_app/students/banned_students_dashboard.html', students=banned_students, error=None, current_user=current_user)

@bp.post('/student/<string:student_external_id>/unban')
@allowed_roles(['admin'])
def unban_student(path: StudentPath):
    banned_student = StudentsFinder.get_banned_student_from_external_id(path.student_external_id)
    if banned_student is None:
        return APIErrorValue('Couldnt find student').json(500)

    StudentsHandler.delete_banned_student(banned_student)

    return redirect(url_for('admin_api.banned_students_dashboard'))

@bp.get('/squads')
@allowed_roles(['admin'])
def squads_dashboard():
    search = request.args.get('search')

    # handle search bar requests
    if search is not None:
        squads = SquadsFinder.search_by_name(search)
    else:
        search = None
        squads = SquadsFinder.get_all()
    
    if squads is None or len(squads) == 0:
        error = 'No squads found'
        return render_template('admin/students_app/squads/squads_dashboard.html', squads=None, error=error, search=search, current_user=current_user)
    
    for squad in squads:
        squad.members_id = [member.user.username for member in squad.members]
        squad.members_id.remove(squad.captain_ist_id)
        squad.members_id = " ".join(squad.members_id)

    return render_template('admin/students_app/squads/squads_dashboard.html', squads=squads, error=None, search=search, current_user=current_user)

@bp.post('/squad/<string:squad_external_id>/ban')
@allowed_roles(['admin'])
def ban_squad(path: SquadPath):
    squad = SquadsFinder.get_from_external_id(path.squad_external_id)
    if squad is None:
        return APIErrorValue('Couldnt find squad').json(500)

    for member in squad.members:
        StudentsHandler.leave_squad(member)

        banned_student = StudentsHandler.create_banned_student(member)
        if banned_student is None:
            return APIErrorValue('Error banning student').json(500)

        UsersHandler.delete_user(member.user)

    return redirect(url_for('admin_api.squads_dashboard'))


@bp.get('/levels')
@allowed_roles(['admin'])
def levels_dashboard():
    levels = LevelsFinder.get_all_levels()
    rewards = RewardsFinder.get_all_rewards()
    if(levels is None):
        return render_template('admin/students_app/levels/levels_dashboard.html', levels=None, rewards=rewards, error='No levels found', current_user=current_user)    

    return render_template('admin/students_app/levels/levels_dashboard.html', levels=levels, rewards=rewards, error=None, current_user=current_user)

@bp.post('/create-level')
@allowed_roles(['admin'])
def create_level():
    value = request.form.get('value', None)
    points = request.form.get('points', None)
    reward_id = request.form.get('reward', None)
    if(reward_id == ""):
        reward_id = None

    if(value is None or points is None):
        return APIErrorValue('Invalid value or points').json(500)

    if(reward_id is not None):
        reward = RewardsFinder.get_reward_from_external_id(reward_id)
        if(reward is None):
            return APIErrorValue('Invalid reward Id')
        
        reward_id = reward.id

    levels = LevelsFinder.get_all_levels()

    if((len(levels) > 0 and int(levels[-1].value + 1) != int(value)) or (len(levels) == 0 and int(value) != 1)):
        return APIErrorValue('Invalid level value').json(500)

    level = LevelsHandler.create_level(value=value, points=points, reward_id=reward_id)
    if(level is None):
        return APIErrorValue('Error creating level').json(500)

    if(len(levels) == 0 and level.value == 1):
        students = StudentsFinder.get_from_parameters({'level_id': None})
        for student in students:
            StudentsHandler.update_student(student, level_id = level.id)

    levels = LevelsFinder.get_all_levels()
    rewards = RewardsFinder.get_all_rewards()
    if(levels is None):
        return render_template('admin/students_app/levels/levels_dashboard.html', levels=None, rewards=rewards, error='No levels found', current_user=current_user)    

    return render_template('admin/students_app/levels/levels_dashboard.html', levels=levels, rewards=rewards, error=None, current_user=current_user)

@bp.post('/level/<string:level_external_id>')
@allowed_roles(['admin'])
def update_level(path: LevelPath):
    level = LevelsFinder.get_level_from_external_id(path.level_external_id)
    if level is None:
        return APIErrorValue('Couldnt find level').json(500)

    reward_id = request.form.get('reward', None)
    if(reward_id == ""):
        reward_id = None
    if(reward_id is not None):
        reward = RewardsFinder.get_reward_from_external_id(reward_id)
        if(reward is None):
            return APIErrorValue('Invalid reward Id')
        
        reward_id = reward.id

    level = LevelsHandler.update_level(level, reward_id=reward_id)
    levels = LevelsFinder.get_all_levels()
    rewards = RewardsFinder.get_all_rewards()
    if(level is None):
        return render_template('admin/students_app/levels/levels_dashboard.html', levels=levels, rewards=rewards, error='Failed to update reward', current_user=current_user)

    return render_template('admin/students_app/levels/levels_dashboard.html', levels=levels, rewards=rewards, error=None, current_user=current_user)

@bp.post('/level/<string:level_external_id>/delete')
@allowed_roles(['admin'])
def delete_level(path: LevelPath):
    level = LevelsFinder.get_level_from_external_id(path.level_external_id)
    if level is None:
        return APIErrorValue('Couldnt find level').json(500)

    levels = LevelsFinder.get_all_levels()
    if(len(levels) == 0 or (len(levels) > 0 and levels[-1] == level)):
        students = StudentsFinder.get_from_level_or_higher(level)
        previous_level = LevelsFinder.get_level_by_value(level.value - 1)
        
        if(previous_level is None):
            for student in students:
                StudentsHandler.update_student(student, level_id = None, total_points=0)
        else:
            for student in students:
                StudentsHandler.update_student(student, level_id = previous_level.id, total_points=previous_level.points)

        LevelsHandler.delete_level(level)

    levels = LevelsFinder.get_all_levels()
    rewards = RewardsFinder.get_all_rewards()
    if(levels is None):
        return render_template('admin/students_app/levels/levels_dashboard.html', levels=None, rewards=rewards, error='No levels found', current_user=current_user)    

    return render_template('admin/students_app/levels/levels_dashboard.html', levels=levels, rewards=rewards, error=None, current_user=current_user)

@bp.get('/tags')
@allowed_roles(['admin'])
def tags_dashboard():
    tags = TagsFinder.get_all()
    if(tags is None):
        return render_template('admin/students_app/tags/tags_dashboard.html', tags=None, error='No tags found', current_user=current_user)

    return render_template('admin/students_app/tags/tags_dashboard.html', tags=tags, error=None, current_user=current_user)

@bp.post('/new-tag')
@allowed_roles(['admin'])
def create_tag():
    tags = TagsFinder.get_all()
    name = request.form.get('name',None)
    if(name is None):
        return render_template('admin/students_app/tags/tags_dashboard.html', tags=tags, error='Failed to create tag', current_user=current_user)

    tag = TagsHandler.create_tag(name=name)
    tags = TagsFinder.get_all()
    if(tag is None):
        return render_template('admin/students_app/tags/tags_dashboard.html', tags=tags, error='Failed to create tag', current_user=current_user)

    return render_template('admin/students_app/tags/tags_dashboard.html', tags=tags, error=None, current_user=current_user)

@bp.post('/tag/<string:tag_external_id>/delete')
@allowed_roles(['admin'])
def delete_tag(path: TagPath):
    tag = TagsFinder.get_from_external_id(path.tag_external_id)
    if tag is None:
        return APIErrorValue('Couldnt find tag').json(500)

    TagsHandler.delete_tag(tag)

    tags = TagsFinder.get_all()
    if(tags is None):
        return render_template('admin/students_app/tags/tags_dashboard.html', tags=tags, error='No tags found', current_user=current_user)    

    return render_template('admin/students_app/tags/tags_dashboard.html', tags=tags, error=None, current_user=current_user)

@bp.get('/rewards')
@allowed_roles(['admin'])
def rewards_dashboard():
    search = request.args.get('search', None)

    if search is not None:
        rewards = RewardsFinder.get_rewards_from_search(search)
    else:
        search = None
        rewards = RewardsFinder.get_all_rewards()
    
    if(rewards is None or len(rewards) == 0):
        return render_template('admin/students_app/rewards/rewards_dashboard.html', search=search, error = 'No rewards found', rewards=rewards, current_user=current_user)    

    return render_template('admin/students_app/rewards/rewards_dashboard.html', search=search, error=None, rewards=rewards, current_user=current_user)

@bp.get('/new-reward')
@allowed_roles(['admin'])
def add_reward_dashboard():

    return render_template('admin/students_app/rewards/add_reward.html')

@bp.post('/new-reward')
@allowed_roles(['admin'])
def create_reward():
    name = request.form.get('name', None)
    description = request.form.get('description', None)
    link = request.form.get('link', None)
    quantity = request.form.get('quantity', None)

    reward = RewardsHandler.create_reward(name=name, description=description, link=link, quantity=quantity)
    if(reward is None):
        return render_template('admin/students_app/rewards/add_reward.html', error='Failed to create reward')

    if request.files:
        image = request.files.get('image', None)
        if image:
            result, msg = RewardsHandler.upload_reward_image(image, str(reward.external_id))
            if result == False:
                RewardsHandler.delete_reward(reward)
                return render_template('admin/students_app/rewards/add_reward.html', error=msg)

    return render_template('admin/students_app/rewards/rewards_dashboard.html', search=None, error=None, rewards=RewardsFinder.get_all_rewards(), current_user=current_user)

@bp.get('/rewards/<string:reward_external_id>')
@allowed_roles(['admin'])
def update_reward_dashboard(path: RewardPath):
    reward = RewardsFinder.get_reward_from_external_id(path.reward_external_id)
    if(reward is None):
        redirect(url_for('admin_api.rewards_dashboard'))

    image = RewardsHandler.find_reward_image(str(reward.external_id))

    return render_template('admin/students_app/rewards/update_reward.html', error=None, reward=reward, current_user=current_user, image=image)

@bp.post('/rewards/<string:reward_external_id>')
@allowed_roles(['admin'])
def update_reward(path: RewardPath):
    reward = RewardsFinder.get_reward_from_external_id(path.reward_external_id)
    if(reward is None):
        redirect(url_for('admin_api.rewards_dashboard'))

    name = request.form.get('name', None)
    description = request.form.get('description', None)
    link = request.form.get('link', None)
    quantity = request.form.get('quantity', None)
    
    reward = RewardsHandler.update_reward(reward, name=name, description=description, link=link, quantity=quantity)
    image = RewardsHandler.find_reward_image(str(reward.external_id))
    if reward is None:
        return render_template('admin/students_app/rewards/update_reward.html', error='Failed to update reward', reward=reward, image=image)

    if request.files:
        image = request.files.get('image', None) 
        if image:
            result, msg = RewardsHandler.upload_reward_image(image, str(reward.external_id))
            if result == False:
                RewardsHandler.delete_reward(reward)
                return render_template('admin/students_app/rewards/update_reward.html', error=msg, reward=reward, image=image)
    
    return render_template('admin/students_app/rewards/rewards_dashboard.html', search=None, error=None, rewards=RewardsFinder.get_all_rewards(), current_user=current_user)

@bp.post('/reward/<string:reward_external_id>/delete')
@allowed_roles(['admin'])
def delete_reward(path: RewardPath):
    reward = RewardsFinder.get_reward_from_external_id(path.reward_external_id)
    image = RewardsHandler.find_reward_image(str(reward.external_id))

    if RewardsHandler.delete_reward(reward):
        return redirect(url_for('admin_api.rewards_dashboard'))

    else:
        return render_template('admin/students_app/rewards/update_reward.html', reward=reward, image=image, error="Failed to delete reward!")

@bp.get('/jeecpot-rewards')
@allowed_roles(['admin'])
def jeecpot_reward_dashboard():
    jeecpot_rewards = RewardsFinder.get_all_jeecpot_rewards()
    rewards = RewardsFinder.get_all_rewards()

    if(jeecpot_rewards is None or len(jeecpot_rewards) < 1):
        RewardsHandler.create_jeecpot_reward()
        jeecpot_rewards = RewardsFinder.get_all_jeecpot_rewards()

    return render_template('admin/students_app/rewards/jeecpot_rewards_dashboard.html', error=None, jeecpot_rewards=jeecpot_rewards[0], rewards=rewards, current_user=current_user)

@bp.post('/jeecpot-rewards/<string:jeecpot_rewards_external_id>')
@allowed_roles(['admin'])
def update_jeecpot_reward(path: JeecpotRewardsPath):
    jeecpot_rewards = RewardsFinder.get_jeecpot_reward_from_external_id(path.jeecpot_rewards_external_id)
    if(jeecpot_rewards is None):
        return APIErrorValue('JEECPOT Rewards not found').json(500)

    first_student_reward_id = request.form.get('first_student_reward', None)
    if(first_student_reward_id is not None):
        if(first_student_reward_id == ""):
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, first_student_reward_id = None)
        else:
            first_student_reward = RewardsFinder.get_reward_from_external_id(first_student_reward_id)
            if(first_student_reward is None):
                return APIErrorValue('Reward not found').json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, first_student_reward_id = first_student_reward.id)
        if(jeecpot_rewards is None):
            return APIErrorValue('Failed to update reward').json(500)

    second_student_reward_id = request.form.get('second_student_reward', None)
    if(second_student_reward_id is not None):
        if(second_student_reward_id == ""):
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, second_student_reward_id = None)
        else:
            second_student_reward = RewardsFinder.get_reward_from_external_id(second_student_reward_id)
            if(second_student_reward is None):
                return APIErrorValue('Reward not found').json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, second_student_reward_id = second_student_reward.id)
        if(jeecpot_rewards is None):
            return APIErrorValue('Failed to update reward').json(500)

    third_student_reward_id = request.form.get('third_student_reward', None)
    if(third_student_reward_id is not None):
        if(third_student_reward_id == ""):
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, third_student_reward_id = None)
        else:
            third_student_reward = RewardsFinder.get_reward_from_external_id(third_student_reward_id)
            if(third_student_reward is None):
                return APIErrorValue('Reward not found').json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, third_student_reward_id = third_student_reward.id)
        if(jeecpot_rewards is None):
            return APIErrorValue('Failed to update reward').json(500)
    
    first_squad_reward_id = request.form.get('first_squad_reward', None)
    if(first_squad_reward_id is not None):
        if(first_squad_reward_id == ""):
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, first_squad_reward_id = None)
        else:
            first_squad_reward = RewardsFinder.get_reward_from_external_id(first_squad_reward_id)
            if(first_squad_reward is None):
                return APIErrorValue('Reward not found').json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, first_squad_reward_id = first_squad_reward.id)
        if(jeecpot_rewards is None):
            return APIErrorValue('Failed to update reward').json(500)

    second_squad_reward_id = request.form.get('second_squad_reward', None)
    if(second_squad_reward_id is not None):
        if(second_squad_reward_id == ""):
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, second_squad_reward_id = None)
        else:
            second_squad_reward = RewardsFinder.get_reward_from_external_id(second_squad_reward_id)
            if(second_squad_reward is None):
                return APIErrorValue('Reward not found').json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, second_squad_reward_id = second_squad_reward.id)
        if(jeecpot_rewards is None):
            return APIErrorValue('Failed to update reward').json(500)

    third_squad_reward_id = request.form.get('third_squad_reward', None)
    if(third_squad_reward_id is not None):
        if(third_squad_reward_id == ""):
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, third_squad_reward_id = None)
        else:
            third_squad_reward = RewardsFinder.get_reward_from_external_id(third_squad_reward_id)
            if(third_squad_reward is None):
                return APIErrorValue('Reward not found').json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, third_squad_reward_id = third_squad_reward.id)
        if(jeecpot_rewards is None):
            return APIErrorValue('Failed to update reward').json(500)

    king_job_fair_reward_id = request.form.get('king_job_fair_reward', None)
    if(king_job_fair_reward_id is not None):
        if(king_job_fair_reward_id == ""):
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, king_job_fair_reward_id = None)
        else:
            king_job_fair_reward = RewardsFinder.get_reward_from_external_id(king_job_fair_reward_id)
            if(king_job_fair_reward is None):
                return APIErrorValue('Reward not found').json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, king_job_fair_reward_id = king_job_fair_reward.id)
        if(jeecpot_rewards is None):
            return APIErrorValue('Failed to update reward').json(500)

    king_knowledge_reward_id = request.form.get('king_knowledge_reward', None)
    if(king_knowledge_reward_id is not None):
        if(king_knowledge_reward_id == ""):
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, king_knowledge_reward_id = None)
        else:
            king_knowledge_reward = RewardsFinder.get_reward_from_external_id(king_knowledge_reward_id)
            if(king_knowledge_reward is None):
                return APIErrorValue('Reward not found').json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, king_knowledge_reward_id = king_knowledge_reward.id)
        if(jeecpot_rewards is None):
            return APIErrorValue('Failed to update reward').json(500)

    king_hacking_reward_id = request.form.get('king_hacking_reward', None)
    if(king_hacking_reward_id is not None):
        if(king_hacking_reward_id == ""):
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, king_hacking_reward_id = None)
        else:
            king_hacking_reward = RewardsFinder.get_reward_from_external_id(king_hacking_reward_id)
            if(king_hacking_reward is None):
                return APIErrorValue('Reward not found').json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, king_hacking_reward_id = king_hacking_reward.id)
        if(jeecpot_rewards is None):
            return APIErrorValue('Failed to update reward').json(500)

    king_networking_reward_id = request.form.get('king_networking_reward', None)
    if(king_networking_reward_id is not None):
        if(king_networking_reward_id == ""):
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, king_networking_reward_id = None)
        else:
            king_networking_reward = RewardsFinder.get_reward_from_external_id(king_networking_reward_id)
            if(king_networking_reward is None):
                return APIErrorValue('Reward not found').json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, king_networking_reward_id = king_networking_reward.id)
        if(jeecpot_rewards is None):
            return APIErrorValue('Failed to update reward').json(500)

    cv_platform_raffle_reward_id = request.form.get('cv_platform_raffle_reward', None)
    if(cv_platform_raffle_reward_id is not None):
        if(cv_platform_raffle_reward_id == ""):
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, cv_platform_raffle_reward_id = None)
        else:
            cv_platform_raffle_reward = RewardsFinder.get_reward_from_external_id(cv_platform_raffle_reward_id)
            if(cv_platform_raffle_reward is None):
                return APIErrorValue('Reward not found').json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, cv_platform_raffle_reward_id = cv_platform_raffle_reward.id)
        if(jeecpot_rewards is None):
            return APIErrorValue('Failed to update reward').json(500)

    return render_template('admin/students_app/rewards/jeecpot_rewards_dashboard.html', error=None, jeecpot_rewards=jeecpot_rewards, rewards=RewardsFinder.get_all_rewards(), current_user=current_user)


@bp.get('/lootboxes')
@allowed_roles(['admin'])
def lootboxes_dashboard():
    lootboxes = LootboxFinder.get_all_lootbox()
    lootbox_icons=[]
    lootbox_counts=[]
    lootbox_percentages=[]
    lootbox_delivered=[]
    lootbox_opened=[]
    for lootbox in lootboxes:
        lootbox_icons.append(LootboxHandler.find_image(str(lootbox.external_id)))
        rewards = LootboxFinder.get_rewards_from_lootbox(lootbox)
        count = len(rewards)
        lootbox_counts.append(count)
        lootbox_percentages.append(0)
        lootbox_delivered.append(0)
        lootbox_opened.append(0)
        if count != 0:
            for reward in rewards:
                lootbox_percentages[-1] += reward.probability
        
    return render_template('admin/students_app/rewards/lootboxes_dashboard.html', error=None, lootboxes=zip(lootboxes,lootbox_counts,lootbox_icons,lootbox_percentages,lootbox_delivered,lootbox_opened), current_user=current_user)


@bp.get('/new-lootbox')
@allowed_roles(['admin'])
def add_lootbox_dashboard():
    rewards = RewardsFinder.get_all_rewards()
    
    return render_template('admin/students_app/rewards/add_lootbox.html', error=None, rewards=rewards, current_user=current_user)


@bp.post('/new-lootbox')
@allowed_roles(['admin'])
def create_lootbox():
    name = request.form.get('name', None)
    active = request.form.get('active', None)
    
    rewards = RewardsFinder.get_all_rewards()
    
    if LootboxFinder.get_lootbox_from_parameters({"name":name}):
        return render_template('admin/students_app/rewards/add_lootbox.html', error='Lootbox already exists', rewards=rewards, current_user=current_user)
        
    
    if active == 'True':
        active = True
    else:
        active = False

    lootbox = LootboxHandler.create_lootbox(
        name=name,
        active=active,
        )
    
    if lootbox is None:
        return render_template('admin/students_app/rewards/add_lootbox.html', error='Failed to create lootbox', rewards=rewards, current_user=current_user)
    
    if request.files:
        image_file = request.files.get('lootbox_icon', None) 

        if image_file:
            result, msg = LootboxHandler.upload_image(image_file, str(lootbox.external_id))
            if result == False:
                LootboxHandler.delete_lootbox(lootbox)
                return render_template('admin/students_app/rewards/add_lootbox.html', error=msg, rewards=rewards, current_user=current_user)
            
        mobile_file = request.files.get('mobile_lootbox_icon', None) 

        if mobile_file:
            image_name = f'{lootbox.external_id}_mobile'
            result, msg = LootboxHandler.upload_image(mobile_file, image_name)
            if result == False:
                LootboxHandler.delete_lootbox(lootbox)
                return render_template('admin/students_app/rewards/add_lootbox.html', error=msg, rewards=rewards, current_user=current_user)
    
    return redirect(url_for('admin_api.lootboxes_dashboard'))


@bp.post('/lootbox/<string:lootbox_external_id>/reward')
@allowed_roles(['admin'])
def new_reward_lootbox(path:LootboxPath):
    lootbox_external_id = path.lootbox_external_id
    reward_external_id = request.form.get('new_reward', None)
    probability = request.form.get('new_reward_probability', None)

    lootbox = LootboxFinder.get_lootbox_from_external_id(lootbox_external_id)
    if lootbox is None:
        return redirect(url_for('admin_api.lootboxes_dashboard'))
    reward = RewardsFinder.get_reward_from_external_id(reward_external_id)
    
    new_lootbox_reward = LootboxRewardsHandler.create_lootbox_reward(
        lootbox_id=lootbox.id,
        reward_id=reward.id,
        probability=probability
    )
        
    return redirect(url_for('admin_api.update_lootbox_dashboard', lootbox_external_id = lootbox.external_id))
    
    
@bp.get('/lootbox/<string:lootbox_external_id>')
@allowed_roles(['admin'])
def update_lootbox_dashboard(path:LootboxPath):
    lootbox = LootboxFinder.get_lootbox_from_external_id(path.lootbox_external_id)
    if lootbox is None:
        return redirect(url_for('admin_api.lootboxes_dashboard'))
        
    lootbox_icon = LootboxHandler.find_image(str(lootbox.external_id))
    image_name = f'{lootbox.external_id}_mobile'
    lootbox_mobile_icon = LootboxHandler.find_image(image_name)
    rewards = RewardsFinder.get_all_rewards()
    lootbox_rewards = LootboxFinder.get_rewards_from_lootbox(lootbox)
    total_percentage = 0
    
    if not lootbox_rewards:
        lootbox_rewards = None
    else:
        for reward in lootbox_rewards:
            total_percentage += reward.probability
        
    return render_template('admin/students_app/rewards/update_lootbox.html', error=None, lootbox=lootbox, lootbox_rewards=lootbox_rewards, icon=lootbox_icon, mobile_icon=lootbox_mobile_icon, rewards=rewards, total_percentage=total_percentage)
    
    
@bp.post('/lootbox/<string:lootbox_external_id>') # <----
@allowed_roles(['admin'])
def update_lootbox(path:LootboxPath):
    lootbox = LootboxFinder.get_lootbox_from_external_id(path.lootbox_external_id)
    if lootbox is None:
        return redirect(url_for('admin_api.lootboxes_dashboard'))
        
    name = request.form.get('name', None)
    active = request.form.get('active', None)
    
    if active == 'True':
        active = True
    else:
        active = False

    lootbox_updated = LootboxHandler.update_lootbox(
        lootbox=lootbox,
        name=name,
        active=active,
        )
    
    if request.files:
        image_file = request.files.get('lootbox_icon', None) 

        if image_file:
            LootboxHandler.delete_image(str(lootbox_updated.external_id))
            result, msg = LootboxHandler.upload_image(image_file, str(lootbox_updated.external_id))
            if result == False:
                lootboxes = LootboxFinder.get_all_lootbox()
                lootbox_icons=[]
                lootbox_counts=[]
                lootbox_percentages=[]
                lootbox_delivered=[]
                lootbox_opened=[]
                for lootbox in lootboxes:
                    lootbox_icons.append(LootboxHandler.find_image(str(lootbox.external_id)))
                    rewards = LootboxFinder.get_rewards_from_lootbox(lootbox)
                    count = len(rewards)
                    lootbox_counts.append(count)
                    lootbox_percentages.append(0)
                    lootbox_delivered.append(0)
                    lootbox_opened.append(0)
                    if count != 0:
                        for reward in rewards:
                            lootbox_percentages[-1] += reward.probability
                    
                return render_template('admin/students_app/rewards/lootboxes_dashboard.html', error="Error uploading new Icon image!", lootboxes=zip(lootboxes,lootbox_counts,lootbox_icons,lootbox_percentages,lootbox_delivered,lootbox_opened), current_user=current_user)
            
        mobile_file = request.files.get('mobile_lootbox_icon', None) 

        if mobile_file:
            image_name = f'{lootbox_updated.external_id}_mobile'
            LootboxHandler.delete_image(image_name)
            result, msg = LootboxHandler.upload_image(mobile_file, image_name)
            if result == False:
                lootboxes = LootboxFinder.get_all_lootbox()
                lootbox_icons=[]
                lootbox_counts=[]
                lootbox_percentages=[]
                lootbox_delivered=[]
                lootbox_opened=[]
                for lootbox in lootboxes:
                    lootbox_icons.append(LootboxHandler.find_image(str(lootbox.external_id)))
                    rewards = LootboxFinder.get_rewards_from_lootbox(lootbox)
                    count = len(rewards)
                    lootbox_counts.append(count)
                    lootbox_percentages.append(0)
                    lootbox_delivered.append(0)
                    lootbox_opened.append(0)
                    if count != 0:
                        for reward in rewards:
                            lootbox_percentages[-1] += reward.probability
                    
                return render_template('admin/students_app/rewards/lootboxes_dashboard.html', error="Error uploading new mobile Icon image!", lootboxes=zip(lootboxes,lootbox_counts,lootbox_icons,lootbox_percentages,lootbox_delivered,lootbox_opened), current_user=current_user)

    return redirect(url_for('admin_api.lootboxes_dashboard'))


@bp.post('/lootbox/<string:lootbox_external_id>/delete')
@allowed_roles(['admin'])
def delete_lootbox(path:LootboxPath):

    lootbox = LootboxFinder.get_lootbox_from_external_id(path.lootbox_external_id)
    if lootbox is None:
        return redirect(url_for('admin_api.lootboxes_dashboard'))
    
    lootbox_rewards = LootboxFinder.get_rewards_from_lootbox(lootbox)
    for lootbox_reward in lootbox_rewards:
        LootboxRewardsHandler.delete_lootbox_reward(lootbox_reward)
        
    LootboxHandler.delete_lootbox(lootbox)
    
    return redirect(url_for('admin_api.lootboxes_dashboard'))


@bp.post('/lootbox/<string:lootbox_external_id>/delete/reward')
@allowed_roles(['admin'])
def delete_lootbox_reward(path:LootboxPath):
    
    lootbox_reward_external_id = request.form.get('reward_external_id', None)
    if lootbox_reward_external_id is None:
        return redirect(url_for('admin_api.lootboxes_dashboard'))
        

    lootbox_reward = LootboxFinder.get_lootbox_reward_from_external_id(lootbox_reward_external_id)
    if lootbox_reward is None:
        return redirect(url_for('admin_api.lootboxes_dashboard'))
    
    lootbox = LootboxFinder.get_lootbox_from_external_id(path.lootbox_external_id)
    if lootbox is None:
        return redirect(url_for('admin_api.lootboxes_dashboard'))
        
    LootboxRewardsHandler.delete_lootbox_reward(lootbox_reward)
    
    return redirect(url_for('admin_api.update_lootbox_dashboard', lootbox_external_id = lootbox.external_id))


@bp.get('/lootbox/<string:lootbox_external_id>/winners')
@allowed_roles(['admin'])
def winners_lootbox(path:LootboxPath):
    
    return jsonify({"msg":"agora é meter aqui a tabela coma info toda do lootbox_student"})


@bp.get('/squad-rewards')
@allowed_roles(['admin'])
def squad_rewards_dashboard():
    squad_rewards = RewardsFinder.get_all_squad_rewards()
    rewards = RewardsFinder.get_all_rewards()
    event = EventsFinder.get_default_event()
    if(event is None or event.start_date is None or event.end_date is None):
        return render_template('admin/students_app/rewards/rewards_dashboard.html', search=None, error='Please select a default event and its date', rewards=rewards, current_user=current_user)
    
    event_dates = EventsHandler.get_event_dates(event)

    for squad_reward in squad_rewards:
        if(squad_reward.date not in event_dates):
            RewardsHandler.delete_squad_reward(squad_reward)

    rewards_dates = [squad_reward.date for squad_reward in squad_rewards]

    for date in event_dates:
        if(not date in rewards_dates):
            RewardsHandler.create_squad_reward(reward_id=None, date=date)

    rewards = RewardsFinder.get_all_rewards()
    squad_rewards = RewardsFinder.get_all_squad_rewards()

    return render_template('admin/students_app/rewards/squad_rewards_dashboard.html', error=None, squad_rewards=squad_rewards, rewards=rewards, current_user=current_user)

@bp.post('/squad-rewards/<string:squad_reward_external_id>')
@allowed_roles(['admin'])
def update_squad_reward(path: SquadRewardPath):
    squad_reward = RewardsFinder.get_squad_reward_from_external_id(path.squad_reward_external_id)
    if squad_reward is None:
        return APIErrorValue('Squad Reward not found').json(404)

    reward_id = request.form.get('reward', None)
    if(reward_id != ""):
        reward = RewardsFinder.get_reward_from_external_id(reward_id)
        if reward is None:
            return APIErrorValue('Reward not found').json(404)

        squad_reward = RewardsHandler.update_squad_reward(squad_reward, reward_id=reward.id)
    else:
        squad_reward = RewardsHandler.update_squad_reward(squad_reward, reward_id=None)

    if squad_reward is None:
        return render_template('admin/students_app/rewards/squad_rewards_dashboard.html', error='Failed to update reward', squad_rewards=None, rewards=None, current_user=current_user)
    
    return render_template('admin/students_app/rewards/squad_rewards_dashboard.html', error=None, squad_rewards=RewardsFinder.get_all_squad_rewards(), rewards=RewardsFinder.get_all_rewards(), current_user=current_user)

@bp.post('/reset-daily-points')
@allowed_roles(['admin'])
def reset_daily_points():
    squads = SquadsFinder.get_all()
    for squad in squads:
        if not SquadsHandler.reset_daily_points(squad):
            return APIErrorValue("Reset failed").json(500)

    students = StudentsFinder.get_all()
    for student in students:
        if not StudentsHandler.reset_daily_points(student):
            return APIErrorValue("Reset failed").json(500)
    
    return jsonify("Success"), 200

@bp.post('/select-winners')
@allowed_roles(['admin'])
def select_winners():
    top_squads = SquadsFinder.get_first()
    if top_squads is None:
        return APIErrorValue("No squad found").json(404)

    winner = choice(top_squads)
    now = datetime.utcnow()
    date = now.strftime('%d %b %Y, %a')

    squad_reward = RewardsFinder.get_squad_reward_from_date(date)
    if squad_reward is None:
        return APIErrorValue("No reward found").json(404)

    squad_reward = RewardsHandler.update_squad_reward(squad_reward, winner_id=winner.id)
    if squad_reward is None:
        return APIErrorValue("Error selecting winner").json(500)

    return jsonify("Success"), 200