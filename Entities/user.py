from sqlalchemy import literal

import Database as db
from Entities.base import Entity
from Entities.tile import Tile
from Presenters import presenters
from Mud import mud


class User(Entity):
    """
    User entity - inherits from Entities.base.Entity
    Loads the user from the database and stores additional runtime properties
    """
    model = db.models.User

    def __init__(self, dbUser):
        self.authed = True
        self.name = dbUser.name
        self.flags = dbUser.flags
        self.aliases = dbUser.aliases
        self.listening = dbUser.listening
        self.race = dbUser.race
        self.class_ = dbUser.class_
        self.db = dbUser
        mud.add_user(self)
        self.tile = None
        try:
            self.move(dbUser.tile)
        except AssertionError:
            print(f'Couldn\'t load room for {self.name}')
            self.move(db.session.query(db.models.Tile).get(1))
        self.presenter = None
        self.disconnect = None
        self.ticks = []

    def hook_client(self, client):
        """
        Sets up the presenter with TCPServer.TCPHandler.send() so it can send the formatted data.
        Also wraps User.disconnect() to the TCPServer.TCPHandler.disconnect() for convenience.
        """
        self.presenter = presenters['default'](client.send)
        self.disconnect = client.disconnect

    @staticmethod
    def preload(dbUser):
        """
        Before the Database.models.User is loaded, mud.users is checked to make sure there isn't already an Entities.User
        loaded with that Database.models.User. If so, it is disconnected and that Entities.User instance is returned
        instead of creating another.
        """
        if dbUser.name in mud.users:
            other = mud.get_user(dbUser.name)
            if other:
                other.p.send_text('You have signed in from another location!')
                other.disconnect()
                return other
            else:
                mud.rem_user(dbUser.name)

    def save(self):
        """
        Writes any changes made on the Entities.User back to the Database.models.User
        """
        self.db.name = self.name
        self.db.flags = self.flags
        self.db.aliases = self.aliases
        self.db.listening = self.listening
        self.db.race = self.race
        self.db.class_ = self.class_
        self.db.tile = self.tile.db
        db.session.commit()

    def stop_ticks(self):
        """
        Kills any threads attached
        """
        for tick in self.ticks:
            tick.cancel()

    def move(self, destination):
        """
        Moves the Entities.User to the destination Tile
        """
        assert type(destination) is db.models.Tile, \
            f'{self.__class__}.move() expects a Database.models.Tile, got a {type(destination)}.'
        if self.tile:
            self.tile.occupants.remove(self)
        self.tile = Tile.load(destination)
        self.tile.occupants.append(self)

    @property
    def p(self):
        return self.presenter

    @property
    def str(self):
        return self.db.str + self.race.str_mod

    @property
    def dex(self):
        return self.db.dex + self.race.dex_mod

    @property
    def con(self):
        return self.db.con + self.race.con_mod

    @property
    def int(self):
        return self.db.int + self.race.int_mod

    @property
    def wis(self):
        return self.db.wis + self.race.wis_mod

    @property
    def cha(self):
        return self.db.cha + self.race.cha_mod

    def __repr__(self):
        return f'<Entities.User(id={self.id}, username="{self.name}")>'
