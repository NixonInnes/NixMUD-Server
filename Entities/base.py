from sqlalchemy import literal

import Database as db


class Entity(object):
    """
    Base Entity object, all other Entity objects inherit from this.
    Entity.model should be overwritten with the corresponding Database.models class
    Provides an easy interface to the database model with class methods (create/exists/search/all)
    Entity.load() should be used to create instances, as it will call preload which should be overwritten by each
    subclass that wants to perform any setup and/or return an alternative instance.
    """
    model = None

    @classmethod
    def create(cls, **kwargs):
        """
        Creates a new database object
        """
        dbModel = cls.model(**kwargs)
        db.session.add(dbModel)
        db.session.commit()
        return dbModel

    @classmethod
    def exists(cls, **kwargs):
        q = db.session.query(cls.model).filter_by(**kwargs)
        return db.session.query(literal(True)).filter(q.exists()).scalar()

    @classmethod
    def search(cls, **kwargs):
        return db.session.query(cls.model).filter_by(**kwargs).first()

    @classmethod
    def all(cls):
        return db.session.query(cls.model).order_by(cls.model.id).all()

    @classmethod
    def load(cls, dbModel):
        preload = cls.preload(dbModel)
        if preload:
            return preload
        else:
            return cls(dbModel)

    @staticmethod
    def preload(dbModel):
        return None
