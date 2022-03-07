from jeec_brain.models.lootbox_rewards import LootboxRewards


class DeleteLootboxRewardService():

    def __init__(self, lootbox_reward: LootboxRewards):
        self.lootbox_reward = lootbox_reward

    def call(self) -> bool:
        result = self.lootbox_reward.delete()
        return result