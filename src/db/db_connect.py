from sqlalchemy import create_engine, Column, Integer, ForeignKey, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import SQLITE3_CONNECT
from gasprice.gasPrice import GP_type


engine = create_engine(SQLITE3_CONNECT, connect_args={'check_same_thread': False})
Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
session.close()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    notices = relationship("Notice")

    def __init__(self, tg_id):
        self.tg_id = tg_id

    def __repr__(self):
        return '<User(id-%s, tg_id-%s)>' % (self.id, self.tg_id)


class Notice(Base):
    __tablename__ = 'notice'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'))
    gp = Column(Float)
    type = Column(Enum(GP_type), default=GP_type.standard)
    user = relationship(User, primaryjoin=user_id == User.id)

    def __init__(self, user_id, gp, type):
        self.user_id = user_id
        self.gp = gp
        self.type = type

    def __repr__(self):
        return '<Notice(id-%s user-%s gp-%s type-%s)>' % (self.id, self.user_id, self.gp, self.type)
