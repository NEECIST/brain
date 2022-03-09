from sqlalchemy import and_, func
from jeec_brain.models.lootbox import Lootboxes
from jeec_brain.models.lootbox_rewards import LootboxRewards
from jeec_brain.models.student_lootbox import StudentLootbox

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
    def get_rewards_from_lootbox(cls, lootbox):
        return LootboxRewards.query.filter_by(lootbox_id=lootbox.id).order_by(LootboxRewards.probability).all()

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