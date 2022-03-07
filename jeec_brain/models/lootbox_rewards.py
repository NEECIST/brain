from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship
from sqlalchemy import sql


class LootboxRewards(db.Model, ModelMixin):
    __tablename__ = 'lootbox_rewards'
    
    reward = relationship('Rewards')
    reward_id = db.Column(db.Integer, db.ForeignKey('rewards.id', ondelete='SET NULL'))
    
    name = db.Column(db.String(20), nullable = False)
    # reward_type = db.Column(db.String(10), nullable = False)
    
    active = db.Column(db.Boolean, nullable = False, default = False)
    probability = db.Column(db.Float)
    repeatable = db.Column(db.Boolean, nullable = False, default = False)

    def __repr__(self):
        return '{} lootbox. Reward:{}. Active:{}. Repeatable:{}. Probability:{}'.format(self.name, self.reward_id, self.active, self.repeatable, self.probability)