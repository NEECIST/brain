from flask import current_app
# SERVICES
from jeec_brain.services.rewards.create_lootbox_service import CreateLootboxService
from jeec_brain.services.rewards.update_lootbox_service import UpdateLootboxService
from jeec_brain.services.rewards.delete_lootbox_service import DeleteLootboxService
from jeec_brain.services.files.upload_image_service import UploadImageService
from jeec_brain.services.files.delete_image_service import DeleteImageService
from jeec_brain.services.files.find_image_service import FindImageService
from datetime import datetime, timedelta

class LootboxHandler():

    @classmethod
    def create_lootbox(cls, **kwargs):
        return CreateLootboxService(kwargs=kwargs).call()

    @classmethod
    def update_lootbox(cls, lootbox, **kwargs):
        return UpdateLootboxService(lootbox=lootbox, kwargs=kwargs).call()

    @classmethod
    def delete_lootbox(cls, lootbox):
        lootbox_external_id = lootbox.external_id

        if DeleteLootboxService(lootbox=lootbox).call():
            for extension in current_app.config['ALLOWED_IMAGES']:

                filename = f'{lootbox_external_id}.{extension}'
                DeleteImageService(filename, 'static/lootboxes').call()

                filename = f'{lootbox_external_id}_mobile.{extension}'
                DeleteImageService(filename, 'static/lootboxes').call()
            
            return DeleteLootboxService(lootbox)
        return False

    @classmethod
    def delete_image(cls, image_name):
        return DeleteImageService(image_name, 'static/lootboxes').call()

    @classmethod
    def upload_image(cls, file, image_name):
        return UploadImageService(file, image_name, 'static/lootboxes').call()

    @classmethod
    def find_image(cls, image_name):
        return FindImageService(image_name, 'static/lootboxes').call()
