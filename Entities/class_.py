import Database as db
from Entities.base import Entity


class Class(Entity):
    """
    Class entity - inherits from Entities.base.Entity
    No current need for any additional properties so just returns the Database.models.Class object
    """
    model = db.models.Class

    @staticmethod
    def preload(dbClass):
        return dbClass