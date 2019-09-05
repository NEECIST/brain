from jeec_brain.models.speakers import Speakers


class SpeakersFinder():

    @classmethod
    def get_from_external_id(cls, external_id):
        return Speakers.query().filter_by(external_id=external_id).first()

    @classmethod
    def search_by_name(cls, name):
        search = "%{}%".format(name)
        return Speakers.query().filter(Speakers.name.ilike(search)).all()
    
    @classmethod
    def get_all(cls):
        return Speakers.query().order_by(Speakers.name).all()
    