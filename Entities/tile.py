from collections import namedtuple

import Database as db
from Entities.base import Entity
from Mud import mud

Point = namedtuple('Point', ['x', 'y', 'z'])


class Tile(Entity):
    """
    Tile entity - inherits from Entities.base.Entity
    Loads the Tile from the database and stores additional runtime properties
    """
    model = db.models.Tile

    def __init__(self, dbTile):
        self.id = dbTile.id
        self.name = dbTile.name
        self.description = dbTile.description
        self.x = dbTile.x
        self.y = dbTile.y
        self.z = dbTile.z
        self.plane = dbTile.plane
        self.properties = dbTile.properties

        self.db = dbTile

        self.occupants = []
        self.contents = []

        mud.tiles[self.id] = self

    @staticmethod
    def preload(dbTile):
        if dbTile.id in mud.tiles:
            return mud.tiles[dbTile.id]

    def save(self):
        self.db.name = self.name
        self.db.description = self.description
        self.db.properties = self.properties
        db.session.commit()

    @property
    def exits(self):
        exits = {}
        for direction in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'u', 'd']:
            exit = getattr(self.db, direction, None)
            if exit:
                exits[direction] = exit
        return exits

    @property
    def coord(self):
        return Point(self.x, self.y, self.z)

    def __repr__(self):
        return f'<Entity.Tile(id={self.id}, coord=({(self.x, self.y, self.z)}), name="{self.name}">'
