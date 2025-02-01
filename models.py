from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey,create_engine,JSON,Date,Float
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///UserInfo.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    posao = Column(String)
    xp = Column(Integer)
    chop_xp = Column(Integer)
    mine_xp = Column(Integer)
    fishing_xp = Column(Integer)
    last_chop_time = Column(String)
    last_mine_time = Column(String)
    last_fishing_time = Column(String)

    bank = relationship('Bank', back_populates='user')
    inventory = relationship('Inventory', back_populates='user')
class Bank(Base):
    __tablename__ = 'bank'
    id = Column(Integer, primary_key=True)
    money = Column(Integer)
    savings = Column(Integer)
    last_work_time = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='bank')
class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    items = Column(JSON)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='inventory')
class Stocks(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    MEME = Column(Float)
    TROLL = Column(Float)
    FOMO = Column(Float)
    YOLO = Column(Float)
    LOL = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))
Base.metadata.create_all(engine)