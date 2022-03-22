from sqlalchemy import text
from jeec_brain.models.lootbox import Lootboxes
from jeec_brain.models.lootbox_rewards import LootboxRewards
from jeec_brain.models.rewards import Rewards
from jeec_brain.models.student_lootbox import StudentLootbox
from jeec_brain.models.students import Students
from jeec_brain.models.users import Users

class LootboxFinder():
        
    @classmethod
    def get_lootbox_from_external_id(cls, external_id):
        return Lootboxes.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def get_lootbox_reward_from_external_id(cls, external_id):
        return LootboxRewards.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def get_student_lootbox_from_external_id(cls, external_id):
        return StudentLootbox.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def get_all_lootbox(cls):
        return Lootboxes.query.order_by(Lootboxes.name).all()
    
    @classmethod
    def get_all_lootbox_rewards(cls):
        return LootboxRewards.query.order_by(LootboxRewards.lootbox_id).all()
    
    @classmethod
    def get_all_student_lootbox(cls):
        return StudentLootbox.query.order_by(StudentLootbox.lootbox_id).all()
    
    @classmethod
    def get_all_student_lootbox_with_names(cls):
        return StudentLootbox.query.join(Lootboxes, (Lootboxes.id == StudentLootbox.lootbox_id)) \
            .join(Students, (Students.id == StudentLootbox.winner_id)) \
            .join(Users, (Students.user_id == Users.id)) \
            .outerjoin(Rewards, (Rewards.id == StudentLootbox.reward_id)) \
            .order_by(Lootboxes.name) \
            .with_entities(Users.name.label("student"), StudentLootbox.opened.label("opened"),
                           Lootboxes.name.label("lootbox"), Rewards.name.label("reward")).all()
    
    @classmethod
    def get_all_student_lootbox_with_names_by_student_id_with_icon(cls, student_id):
        return StudentLootbox.query.join(Lootboxes, (Lootboxes.id == StudentLootbox.lootbox_id)) \
            .join(Students, (Students.id == StudentLootbox.winner_id)) \
            .join(Users, (Students.user_id == Users.id)) \
            .outerjoin(Rewards, (Rewards.id == StudentLootbox.reward_id)) \
            .order_by(StudentLootbox.opened, Lootboxes.name) \
            .filter(Students.id == student_id) \
            .with_entities(Users.name.label("student"), StudentLootbox.opened.label("opened"),
                           Lootboxes.name.label("lootbox"), Rewards.name.label("reward"),
                           Lootboxes.external_id.label("icon")).all()
            
    @classmethod
    def get_all_student_lootbox_with_names_from_parameters(cls, order, filters):
        return StudentLootbox.query.join(Lootboxes, (Lootboxes.id == StudentLootbox.lootbox_id)) \
            .join(Students, (Students.id == StudentLootbox.winner_id)) \
            .join(Users, (Students.user_id == Users.id)) \
            .outerjoin(Rewards, (Rewards.id == StudentLootbox.reward_id)) \
            .order_by(text(order)) \
            .filter(text(filters)) \
            .with_entities(Users.name.label("student"), StudentLootbox.opened.label("opened"),
                           Lootboxes.name.label("lootbox"), Rewards.name.label("reward")).all()
            
    @classmethod
    def get_rewards_from_lootbox(cls, lootbox):
        return LootboxRewards.query.filter_by(lootbox_id=lootbox.id).order_by(LootboxRewards.probability).all()
    
    @classmethod
    def get_student_lootboxes_from_lootbox(cls, lootbox):
        return StudentLootbox.query.filter_by(lootbox_id=lootbox.id).order_by(StudentLootbox.id).all()

    @classmethod
    def get_lootbox_from_parameters(cls, kwargs):
        try:
            return Lootboxes.query.filter_by(**kwargs).order_by(Lootboxes.id).all()
        except Exception:
            return None

    @classmethod
    def get_lootbox_rewards_from_parameters(cls, kwargs):
        try:
            return LootboxRewards.query.filter_by(**kwargs).order_by(LootboxRewards.lootbox_id).all()
        except Exception:
            return None

    @classmethod
    def get_student_lootbox_from_parameters(cls, kwargs):
        try:
            return StudentLootbox.query.filter_by(**kwargs).order_by(StudentLootbox.lootbox_id).all()
        except Exception:
            return None