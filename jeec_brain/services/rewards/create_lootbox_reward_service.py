import logging
from jeec_brain.models.lootbox_rewards import LootboxRewards
from typing import Dict, Optional


logger = logging.getLogger(__name__)


class CreateLootboxRewardService():

    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[LootboxRewards]:
        
        lootbox_reward = LootboxRewards.create(**self.kwargs)

        if not lootbox_reward:
            return None

        return lootbox_reward

