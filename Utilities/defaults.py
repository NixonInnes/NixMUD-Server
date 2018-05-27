import json
import Database as db

DEFAULT_CHANNELS = [
    {
        'name':    'chat',
        'key':     '.',
        'token':   '&G',
        'type':    1,
        'default': True
    },
    {
        'name':    'say',
        'key':     '\'',
        'token':   '&C',
        'type':    2,
        'default': True
    },
    {
        'name':    'whisper',
        'key':     '>',
        'token':   '&M',
        'type':    4,
        'default': True
    },
]

DEFAULT_PLANE = {
    'name': 'The Aether'
}

DEFAULT_TILE = {
    'name': 'The Void',
    'description': 'You are suspended weightlessly in a void, bathing in infinite darkness.',
    'x': 0,
    'y': 0,
    'z': 0,
    'properties': {},
}

DEFAULT_RACE = {
    'name': 'Human',
    'str_mod': 0,
    'dex_mod': 0,
    'con_mod': 0,
    'int_mod': 0,
    'wis_mod': 0,
    'cha_mod': 0
}


DEFAULT_CLASS = {
    'name': 'Fighter'
}

DEFAULT_NPC = {
    'name': 'small rabbit',
    'description': 'A small fluffy rabbit'
}


def create_default_channels():
    for channel in DEFAULT_CHANNELS:
        db.session.add(
            db.models.Channel(**channel)
        )
    db.session.commit()


def create_default_plane():
    db.session.add(db.models.Plane(**DEFAULT_PLANE))
    db.session.commit


def create_default_tile():
    tile = db.models.Tile(**DEFAULT_TILE)
    tile.plane = db.session.query(db.models.Plane).filter_by(name=DEFAULT_PLANE['name']).first()
    db.session.add(tile)
    db.session.commit()


def create_default_race():
    db.session.add(db.models.Race(**DEFAULT_RACE))
    db.session.commit


def create_default_class():
    db.session.add(db.models.Class(**DEFAULT_CLASS))
    db.session.commit


def create_default_npc():
    db.session.add(db.models.NPC(**DEFAULT_NPC))
    db.session.commit()


def create_default_emotes(overwrite=False):
    with open('Utilities/emotes.json') as emotes_json:
        emotes = json.load(emotes_json)
    for emote in emotes.values():
        existing_emote = db.session.query(db.models.Emote).filter_by(name=emote['name']).first()
        if existing_emote is not None:
            if overwrite:
                print("Existing emote {} found. Deleting.")
                db.session.remove(existing_emote)
            else:
                print("Emote {} found. Skipping")
                continue
        print("Adding emote: {}".format(emote['name']))
        dbEmote = db.models.Emote(
            name=emote['name'],
            user_no_vict=emote['user_no_vict'],
            others_no_vict=emote['others_no_vict'] if 'others_no_vict' in emote else None,
            user_vict=emote['user_vict'] if 'user_vict' in emote else None,
            others_vict=emote['others_vict'] if 'others_vict' in emote else None,
            vict_vict=emote['vict_vict'] if 'vict_vict' in emote else None,
            user_vict_self=emote['user_vict_self'] if 'user_vict_self' in emote else None,
            others_vict_self=emote['others_vict_self'] if 'others_vict_self' in emote else None
        )
        db.session.add(dbEmote)
    db.session.commit()
