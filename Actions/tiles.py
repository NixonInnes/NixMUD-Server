from collections import namedtuple

from Entities.tile import Tile
from Utilities.defaults import DEFAULT_TILE


Point = namedtuple('Point', ['x', 'y', 'z'])


def do_dig(user, args):
    """
    Create a new tile adjacent to the users current tile, in the direction specified
    """
    COMPASS = {
        'n':  Point(0, 1, 0),
        'ne': Point(1, 1, 0),
        'e':  Point(1, 0, 0),
        'se': Point(1, -1, 0),
        's':  Point(0, -1, 0),
        'sw': Point(-1, -1, 0),
        'w':  Point(-1, 0, 0),
        'nw': Point(-1, 1, 0),

        'u':  Point(0, 0, 1),
        'd':  Point(0, 0, -1)
    }

    direction = args[0].lower()
    coord_mod = COMPASS.get(args[0])
    current_tile = user.tile

    if not coord_mod:
        user.p.send_text('You want to dig where?!')
        return
    if hasattr(current_tile, direction):
        user.p.send_text('There\'s already an exit in that direction!')
        return

    dbTile = Tile.create(
        name=DEFAULT_TILE['name'],
        description=DEFAULT_TILE['description'],
        x=current_tile.x + coord_mod.x,
        y=current_tile.y + coord_mod.y,
        z=current_tile.z + coord_mod.z,
        plane=current_tile.plane,
    )
    setattr(user.tile.db, direction, dbTile)
    user.tile.save()
    user.p.send_text('A fresh void opens forth!')