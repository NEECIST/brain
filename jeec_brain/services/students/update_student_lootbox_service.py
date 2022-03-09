from typing import Dict, Optional
from jeec_brain.models.student_lootbox import StudentLootbox


class UpdateStudentLootboxService():
    
    def __init__(self, student_lootbox: StudentLootbox, kwargs: Dict):
        self.student_lootbox = student_lootbox
        self.kwargs = kwargs

    def call(self) -> Optional[StudentLootbox]:
        try:
            update_result = self.student_lootbox.update(**self.kwargs)
        except:
            return None
            
        return update_result
