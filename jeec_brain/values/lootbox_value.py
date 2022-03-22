from jeec_brain.finders.lootbox_finder import LootboxFinder
from jeec_brain.handlers.lootbox_handler import LootboxHandler
from jeec_brain.models.student_lootbox import StudentLootbox
from jeec_brain.values.lootbox_rewards_value import LootboxRewardsValue
from jeec_brain.values.value_composite import ValueComposite

class LootboxValue(ValueComposite):
	def __init__(self, lootboxes, student_lootboxes):
		super(LootboxValue, self).initialize({})

		lootbox_array = []
		for lootbox in lootboxes:
			lootbox_value = {
				"name":lootbox.name,
				"rewards": LootboxRewardsValue(LootboxFinder.get_lootbox_rewards_from_parameters({"lootbox_id":lootbox.id})).to_dict(),
				"icon":LootboxHandler.find_image(str(lootbox.external_id))
			}
			lootbox_array.append(lootbox_value)

		self.serialize_with(lootboxes=lootbox_array)
  
		student_lootbox_array = []
		for student_lootbox in student_lootboxes:
			student_lootbox_value = {
				"lootbox":student_lootbox.lootbox,
				"opened":student_lootbox.opened,
				"reward":student_lootbox.reward,
				"icon":LootboxHandler.find_image(str(student_lootbox.icon)),
			}
			student_lootbox_array.append(student_lootbox_value)
   
		self.serialize_with(student_lootboxes=student_lootbox_array)