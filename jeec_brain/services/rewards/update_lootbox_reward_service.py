from typing import Dict, Optional
from jeec_brain.models.lootbox_rewards import LootboxRewards


class UpdateLootboxRewardService():
    
    def __init__(self, lootbox_reward: LootboxRewards, kwargs: Dict):
        self.lootbox_reward = lootbox_reward
        self.kwargs = kwargs

    def call(self) -> Optional[LootboxRewards]:
        try:
            update_result = self.lootbox_reward.update(**self.kwargs)
        except:
            return None
            
        return update_result
