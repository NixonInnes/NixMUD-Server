import Database as db
from Mud.ticker import RTimer
from Utilities import defaults


class Mud(object):
    """
    Overarching mud object
    Sets up the database and manages loaded entities
    """
    def __init__(self):
        self.users = {}
        self.tiles = {}
        self.channels = {}
        self.ticker = RTimer(interval=900, function=self.tick)
        self.start()

    def start(self):
        print('Checking the planes database...')
        if db.session.query(db.models.Plane).count() < 1:
            print('No planes found, creating defaults...')
            defaults.create_default_plane()

        print('Checking tile database...')
        if db.session.query(db.models.Tile).count() < 1:
            print('No tiles found, creating defaults...')
            defaults.create_default_tile()

        print('Checking race database...')
        if db.session.query(db.models.Race).count() < 1:
            print('No races found, creating defaults...')
            defaults.create_default_race()

        print('Checking class database...')
        if db.session.query(db.models.Class).count() < 1:
            print('No classes found, creating defaults...')
            defaults.create_default_class()

        print('Checking NPC database...')
        if db.session.query(db.models.NPC).count() < 1:
            print('No NPCs found, creating defaults...')
            defaults.create_default_npc()

        print('Checking channels database...')
        if db.session.query(db.models.Channel).count() < 1:
            print('No channels found, creating defaults...')
            defaults.create_default_channels()
        self.load_channels()

        print('Checking emotes database...')
        if db.session.query(db.models.Emote).count() < 1:
            print('No emotes found, creating defaults...')
            defaults.create_default_emotes()

        print('Starting ticker...')
        self.ticker.start()

    def load_channels(self):
        print('Loading channels...')
        if self.channels:
            self.channels.clear()
        for channel in db.session.query(db.models.Channel).all():
            self.channels.update({channel.key: channel})
        print('Channels loaded')

    def tick(self):

        users_to_unload = []
        for username, user in self.users.items():
            user.p.send_text('You feel a strange sense... dejavu?')
            if user is None:
                users_to_unload.append(username)
        for user in users_to_unload:
            del self.users[user]

        tiles_to_unload = []
        for id, tile in self.tiles.items():
            if not tile.occupants:
                tiles_to_unload.append(id)
        for tile in tiles_to_unload:
            del self.tiles[tile]

    def add_user(self, user):
        self.users[user.name] = user

    def rem_user(self, username):
        del self.users[username]

    def get_user(self, username):
        return self.users[username]

    def get_users(self):
        return self.users.values()