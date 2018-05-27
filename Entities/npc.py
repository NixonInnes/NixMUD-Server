import random

from Entities.base import Entity
from Entities.tile import Tile
import Database as db
from Mud.ticker import make_tick


class NPC(Entity):
    """
    NPC entity - inherits from Entities.base.Entity
    Loads the NPC from the database and stores additional runtime properties
    """
    model = db.models.NPC

    def __init__(self, dbNPC):
        self.model_id = dbNPC.id
        self.name = dbNPC.name
        self.flags = dict(dbNPC.flags)
        self.tile = None
        make_tick(15, self.wander).start()

    def save(self):
        self.db.name = self.name
        self.db.flags = self.flags
        db.session.commit()

    def move(self, destination):
        assert type(destination) is db.models.Tile, \
            f'{self.__class__}.move() expects a Database.models.Tile, got a {type(destination)}.'
        if self.tile:
            self.tile.occupants.remove(self)
        self.tile = Tile.load(destination)
        self.tile.occupants.append(self)

    def wander(self):
        direction = random.choice(list(self.tile.exits.values()))
        self.move(direction)

