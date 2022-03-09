from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship
from sqlalchemy import sql


class Lootboxes(db.Model, ModelMixin):
    __tablename__ = 'lootboxes'
    
    name = db.Column(db.String(20), nullable = False)
    active = db.Column(db.Boolean, nullable = False, default = False)
    # color = x

    def __repr__(self):
        return '{} lootbox. Active:{}.'.format(self.name, self.active)