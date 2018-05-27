import Database as db
from Entities.base import Entity


class Race(Entity):
    """
        Race entity - inherits from Entities.base.Entity

        """
    model = db.models.Race

    def __init__(self, dbRace):
        self.model_id = dbRace.id
        self.name = dbRace.name
        self.str_mod = dbRace.str_mod
        self.dex_mod = dbRace.dex_mod
        self.con_mod = dbRace.con_mod
        self.int_mod = dbRace.int_mod
        self.wis_mod = dbRace.wis_mod
        self.cha_mod = dbRace.cha_mod

    def save(self):
        self.db.name = self.name
        self.db.str_mod = self.str_mod
        self.db.dex_mod = self.dex_mod
        self.db.con_mod = self.con_mod
        self.db.int_mod = self.int_mod
        self.db.wis_mod = self.wis_mod
        self.db.cha_mod = self.cha_mod
        db.session.commit()