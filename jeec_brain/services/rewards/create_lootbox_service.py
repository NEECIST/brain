import logging
from jeec_brain.models.lootbox import Lootboxes
from typing import Dict, Optional


logger = logging.getLogger(__name__)


class CreateLootboxService():

    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[Lootboxes]:
        
        lootbox = Lootboxes.create(**self.kwargs)

        if not lootbox:
            return None

        return lootbox

