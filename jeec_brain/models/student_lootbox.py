from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship
from sqlalchemy import sql


class StudentLootbox(db.Model, ModelMixin):
    __tablename__ = 'student_lootbox'
    
    lootbox = relationship('LootboxRewards')
    lootbox_id = db.Column(db.Integer, db.ForeignKey('lootbox_rewards.id', ondelete='CASCADE'), nullable = False)
    reward_id = db.Column(db.Integer, db.ForeignKey('lootbox_rewards.reward_id', ondelete='SET NULL'))

    winner = relationship('Students')
    winner_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable = False)

    opened = db.Column(db.Boolean, nullable = False, default = False)

    def __repr__(self):
        return 'Lootbox:{}. Reward:{} Winner:{} Opened:{}'.format(self.lootbox_id, self.reward_id, self.winner_id, self.opened)