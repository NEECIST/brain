from jeec_brain.models.lootbox import Lootboxes


class DeleteLootboxService():

    def __init__(self, lootbox: Lootboxes):
        self.lootbox = lootbox

    def call(self) -> bool:
        result = self.lootbox.delete()
        return result