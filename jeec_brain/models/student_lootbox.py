from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship
from sqlalchemy import sql


class StudentLootbox(db.Model, ModelMixin):
    __tablename__ = 'student_lootbox'
    
    lootbox_id = db.Column(db.Integer, db.ForeignKey('lootboxes.id', ondelete='SET NULL'))
    lootbox = relationship('Lootboxes')
    
    winner_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='SET NULL'), nullable = False)
    winner = relationship('Students')

    opened = db.Column(db.Boolean, nullable = False, default = False)

    def __repr__(self):
        return 'Lootbox:{}. Reward:{} Winner:{} Opened:{}'.format(self.lootbox_id, self.reward_id, self.winner_id, self.opened)