from jeec_brain.values.prizes_multiplayer_value import MultiplayerPrizesValue
from jeec_brain.values.prizes_singleplayer_value import SingleplayerPrizesValue
from jeec_brain.values.value_composite import ValueComposite
class PrizesValue(ValueComposite):
	def __init__(self, jeecpot_rewards, level_reward, activity_reward, daily_squad_reward):
		super(PrizesValue, self).initialize({})

		self.serialize_with(singleplayer=SingleplayerPrizesValue(jeecpot_rewards, level_reward, activity_reward).to_dict())
		self.serialize_with(multiplayer=MultiplayerPrizesValue(jeecpot_rewards, daily_squad_reward).to_dict())