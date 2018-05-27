import Database as db
from Entities.base import Entity


class Class(Entity):
    """
    Class entity - inherits from Entities.base.Entity
    No current need for any additional properties so just returns the Database.models.Class object
    """
    model = db.models.Class

    def __init__(self, dbClass):
        self.model_id = dbClass.id
        self.name = dbClass.name

    def save(self):
        self.db.name = self.name
        db.session.commit()
