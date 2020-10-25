from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from jeec_brain.models.users import Users
from jeec_brain.models.company_activities import CompanyActivities
from jeec_brain.models.activities import Activities
from jeec_brain.models.company_meals import CompanyMeals
from jeec_brain.models.meals import Meals
from jeec_brain.models.company_dishes import CompanyDishes
from jeec_brain.models.dishes import Dishes
from jeec_brain.models.tags import Tags
from jeec_brain.models.companies_tags import CompaniesTags
from sqlalchemy.orm import relationship
from sqlalchemy import sql


class Companies(db.Model, ModelMixin):
    __tablename__ = 'companies'
    
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100))
    link = db.Column(db.String(100))
    business_area = db.Column(db.String(100))

    partnership_tier = db.Column(db.String(20))

    show_in_website = db.Column(db.Boolean, default=True)

    activities = relationship("Activities",
        secondary="company_activities",
        secondaryjoin=sql.and_(CompanyActivities.activity_id == Activities.id))

    dishes = relationship("Dishes",
        secondary="company_dishes",
        secondaryjoin=sql.and_(CompanyDishes.dish_id == Dishes.id))

    meals = relationship("Meals",
        secondary="company_meals",
        secondaryjoin=sql.and_(CompanyMeals.meal_id == Meals.id))

    tags = relationship("Tags",
        secondary="companies_tags",
        secondaryjoin=sql.and_(CompaniesTags.tag_id == Tags.id))

    users = relationship("Users", back_populates='company', lazy='dynamic', cascade="all,delete")

    def __repr__(self):
        return 'Name: {}'.format(self.name)
