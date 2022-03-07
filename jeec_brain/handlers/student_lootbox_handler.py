from flask import current_app
# SERVICES
from jeec_brain.services.rewards.create_student_lootbox_service import CreateStudentLootboxService
from jeec_brain.services.rewards.update_student_lootbox_service import UpdateStudentLootboxService
from jeec_brain.services.rewards.delete_student_lootbox_service import DeleteStudentLootboxService

class LootboxStudentHandler():

    @classmethod
    def create_lootbox_student(cls, **kwargs):
        return CreateStudentLootboxService(kwargs=kwargs).call()

    @classmethod
    def update_lootbox_student(cls, lootbox, **kwargs):
        return UpdateStudentLootboxService(lootbox=lootbox, kwargs=kwargs).call()

    @classmethod
    def delete_lootbox_student(cls, lootbox):

        if DeleteStudentLootboxService(lootbox=lootbox).call():
            return DeleteStudentLootboxService(lootbox)
        return False
