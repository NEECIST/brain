from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship
from sqlalchemy import sql


class LootboxRewards(db.Model, ModelMixin):
    __tablename__ = 'lootbox_rewards'
    
    reward = relationship('Rewards')
    reward_id = db.Column(db.Integer, db.ForeignKey('rewards.id', ondelete='SET NULL'))
    
    lootbox_id = db.Column(db.Integer, db.ForeignKey('lootboxes.id', ondelete='SET NULL'))
    lootbox = relationship('Lootboxes')
    
    # active = db.Column(db.Boolean, nullable = False, default = False)
    probability = db.Column(db.Float)
    # repeatable = db.Column(db.Boolean, nullable = False, default = False)

    def __repr__(self):
        return '{} lootbox. Reward:{}. Probability:{}'.format(self.lootbox_id, self.reward_id, self.probability)