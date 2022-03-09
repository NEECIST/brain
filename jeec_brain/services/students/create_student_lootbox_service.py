import logging
from jeec_brain.models.student_lootbox import StudentLootbox
from typing import Dict, Optional


logger = logging.getLogger(__name__)


class CreateStudentLootboxService():

    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[StudentLootbox]:
        
        student_lootbox = StudentLootbox.create(**self.kwargs)

        if not student_lootbox:
            return None

        return student_lootbox

