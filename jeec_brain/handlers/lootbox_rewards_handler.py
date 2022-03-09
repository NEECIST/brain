from flask import current_app
# SERVICES
from jeec_brain.services.rewards.create_lootbox_reward_service import CreateLootboxRewardService
from jeec_brain.services.rewards.update_lootbox_reward_service import UpdateLootboxRewardService
from jeec_brain.services.rewards.delete_lootbox_reward_service import DeleteLootboxRewardService
from jeec_brain.services.files.upload_image_service import UploadImageService
from jeec_brain.services.files.delete_image_service import DeleteImageService
from jeec_brain.services.files.find_image_service import FindImageService
from datetime import datetime, timedelta

class LootboxRewardsHandler():

    @classmethod
    def create_lootbox_reward(cls, **kwargs):
        return CreateLootboxRewardService(kwargs=kwargs).call()

    @classmethod
    def update_lootbox_reward(cls, lootbox, **kwargs):
        return UpdateLootboxRewardService(lootbox_reward=lootbox, kwargs=kwargs).call()

    @classmethod
    def delete_lootbox_reward(cls, lootbox_reward):
        return DeleteLootboxRewardService(lootbox_reward).call()
