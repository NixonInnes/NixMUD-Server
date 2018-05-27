from passlib.hash import pbkdf2_sha256
from sqlalchemy import Column, Integer, String, Boolean, PickleType, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from Server import config

engine = create_engine(config.DATABASE)
Base = declarative_base()

USER_FLAGS = {
    'admin': False,
    'banned': False,
    'muted': False,
    'frozen': False
}


def generate_password_hash(password):
    return pbkdf2_sha256.encrypt(password, rounds=150000, salt_size=15)


def check_password_hash(password, password_hash):
    return pbkdf2_sha256.verify(password, password_hash)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    _password = Column(String)

    aliases = Column(MutableDict.as_mutable(PickleType), default={})
    flags = Column(MutableDict.as_mutable(PickleType), default=USER_FLAGS)
    listening = Column(String)

    _tile = Column(Integer, ForeignKey('tiles.id'))
    tile = relationship('Tile')

    _race = Column(Integer, ForeignKey('races.id'))
    race = relationship('Race')

    _class_ = Column(Integer, ForeignKey('classes.id'))
    class_ = relationship('Class')

    str = Column(Integer)
    dex = Column(Integer)
    con = Column(Integer)
    int = Column(Integer)
    wis = Column(Integer)
    cha = Column(Integer)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(password, self._password)

    def __repr__(self):
        return f'<Database.User(id={self.id}, name="{self.name}")>'


class Race(Base):
    __tablename__ = 'races'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)

    str_mod = Column(Integer, default=0)
    dex_mod = Column(Integer, default=0)
    con_mod = Column(Integer, default=0)
    int_mod = Column(Integer, default=0)
    wis_mod = Column(Integer, default=0)
    cha_mod = Column(Integer, default=0)

    def __repr__(self):
        return f'<Database.Race(id={self.id}, name="{self.name}")>'


class Class(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)

    def __repr__(self):
        return f'<Database.Class(id={self.id}, name="{self.name}")>'


class NPC(Base):
    __tablename__ = 'npcs'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    flags = Column(MutableDict.as_mutable(PickleType), default={})

    def __repr__(self):
        return f'<Database.NPC(id={self.id}, name="{self.name}")>'


class Plane(Base):
    __tablename__ = 'planes'
    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True, index=True)
    tiles = relationship('Tile', back_populates='plane')

    def __repr__(self):
        return f'<Database.Plane(id={self.id}, name="{self.name}")>'


class Tile(Base):
    __tablename__ = 'tiles'
    id = Column(Integer, primary_key=True)

    _plane = Column(Integer, ForeignKey('planes.id'))
    plane = relationship('Plane', back_populates='tiles')

    x = Column(Integer, index=True)
    y = Column(Integer, index=True)
    z = Column(Integer, index=True, default=0)

    name = Column(String)
    description = Column(String)
    properties = Column(MutableDict.as_mutable(PickleType), default={})

    _n = Column(Integer, ForeignKey('tiles.id'))
    n = relationship('Tile', foreign_keys=[_n], uselist=False, backref=backref('s', uselist=False, remote_side=[id]))

    _ne = Column(Integer, ForeignKey('tiles.id'))
    ne = relationship('Tile', foreign_keys=[_ne], uselist=False, backref=backref('sw', uselist=False, remote_side=[id]))

    _e = Column(Integer, ForeignKey('tiles.id'))
    e = relationship('Tile', foreign_keys=[_e], uselist=False, backref=backref('w', uselist=False, remote_side=[id]))

    _se = Column(Integer, ForeignKey('tiles.id'))
    se = relationship('Tile', foreign_keys=[_se], uselist=False, backref=backref('nw', uselist=False, remote_side=[id]))

    _u = Column(Integer, ForeignKey('tiles.id'))
    u = relationship('Tile', foreign_keys=[_u], uselist=False, backref=backref('d', uselist=False, remote_side=[id]))

    def __repr__(self):
        return f'<Database.Tile(id={self.id}, coord=({(self.x, self.y, self.z)}), name="{self.name}">'


class Channel(Base):
    __tablename__ = 'channels'

    key = Column(String(1), primary_key=True)
    name = Column(String, unique=True)
    token = Column(String(2))
    # Channel.types:
    # 0 - server
    # 1 - room
    # 2 - group
    # 3 - user (whisper)
    type = Column(Integer)
    default = Column(Boolean, default=False)

    def __repr__(self):
        return f'<Database.Channel(id={self.id}, name="{self.name}">'


class Emote(Base):
    __tablename__ = 'emotes'

    id = Column(Integer, primary_key=True)
    name = Column(String(16), unique=True)

    user_no_vict = Column(String(128))
    others_no_vict = Column(String(128))
    user_vict = Column(String(128))
    others_vict = Column(String(128))
    vict_vict = Column(String(128))
    user_vict_self = Column(String(128))
    others_vict_self = Column(String(128))

    def __repr__(self):
        return f'<Database.Emote(id={self.id}, name="{self.name}">'


Base.metadata.create_all(engine)
