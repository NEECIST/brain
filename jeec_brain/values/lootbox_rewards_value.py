from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.values.rewards_value import RewardsValue

class LootboxRewardsValue(ValueComposite):
	def __init__(self, lootbox_rewards):
		super(LootboxRewardsValue, self).initialize({})

		lootbox_rewards_array = []
		for lootbox_reward in lootbox_rewards:
			lootbox_reward_value = {
				"reward": RewardsValue(lootbox_reward.reward).to_dict()
			}
			lootbox_rewards_array.append(lootbox_reward_value)

		self.serialize_with(data=lootbox_rewards_array)