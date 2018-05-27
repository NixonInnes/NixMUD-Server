import Database as db
from Entities.base import Entity


class Race(Entity):
    """
        Race entity - inherits from Entities.base.Entity
        No current need for any additional properties so just returns the Database.models.Race object
        """
    model = db.models.Race

    @staticmethod
    def preload(dbRace):
        return dbRace