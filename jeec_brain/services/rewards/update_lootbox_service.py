from typing import Dict, Optional
from jeec_brain.models.lootbox import Lootboxes


class UpdateLootboxService():
    
    def __init__(self, lootbox: Lootboxes, kwargs: Dict):
        self.lootbox = lootbox
        self.kwargs = kwargs

    def call(self) -> Optional[Lootboxes]:
        try:
            update_result = self.lootbox.update(**self.kwargs)
        except:
            return None
            
        return update_result
