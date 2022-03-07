from sqlalchemy import func
from jeec_brain.models.lootbox_rewards import LootboxRewards

class LootboxFinder():
        
    @classmethod
    def get_lootbox_from_external_id(cls, external_id):
        return LootboxRewards.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def get_all_lootbox_rewards(cls):
        return LootboxRewards.query.order_by(LootboxRewards.name).all()
    
    @classmethod
    def get_all_lootbox_names(cls):
        return LootboxRewards.query.filter_by(reward_id = None) \
            .order_by(LootboxRewards.name) \
            .distinct(LootboxRewards.name) \
            .with_entities(LootboxRewards.name,
                           LootboxRewards.active,
                           LootboxRewards.repeatable,
                           LootboxRewards.external_id).all()
            
    @classmethod
    def get_all_lootbox_reward_count(cls):
        return LootboxRewards.query.order_by(LootboxRewards.name) \
            .group_by(LootboxRewards.name) \
            .with_entities(func.count(func.nullif(LootboxRewards.reward_id, 0)).label("reward_count")).all()

    @classmethod
    def get_lootbox_rewards_from_parameters(cls, kwargs):
        try:
            return LootboxRewards.query.filter_by(**kwargs).order_by(LootboxRewards.name).all()
        except Exception:
            return None