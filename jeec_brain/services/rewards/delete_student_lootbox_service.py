from jeec_brain.models.student_lootbox import StudentLootbox


class DeleteStudentLootboxService():

    def __init__(self, student_lootbox: StudentLootbox):
        self.student_lootbox = student_lootbox

    def call(self) -> bool:
        result = self.student_lootbox.delete()
        return result