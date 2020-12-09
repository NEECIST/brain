from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy import Column, Integer, ForeignKey


class StudentsRewards(db.Model, ModelMixin):
    __tablename__ = 'students_rewards'

    student_id = Column(Integer, ForeignKey('students.id'), index=True)
    reward_id = Column(Integer, ForeignKey('solo_rewards.id'), index=True)