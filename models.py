from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey,create_engine,JSON,Date,Float
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///UserInfo.db')
Base = declarative_base()

class Server(Base):
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True)
    server_id = Column(Integer)
    stock_market_channel_id = Column(Integer)
    message_stock_market_id = Column(Integer)
    stocks = Column(JSON)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    posao = Column(String)
    lokacija = Column(String)
    xp = Column(Integer)
    chop_xp = Column(Integer)
    mine_xp = Column(Integer)
    fishing_xp = Column(Integer)
    last_chop_time = Column(String)
    last_mine_time = Column(String)
    last_fishing_time = Column(String)
    fight_style = Column(String)
    last_fight_style_selection = Column(String)
    last_fight_time = Column(String)

    bank = relationship('Bank', back_populates='user')
    inventory = relationship('Inventory', back_populates='user')
class Bank(Base):
    __tablename__ = 'bank'
    id = Column(Integer, primary_key=True)
    money = Column(Integer)
    savings = Column(Integer)
    last_work_time = Column(String)
    user_id = Column(Integer, ForeignKey('users.id',name="fk_user_id_bank"))
    user = relationship('User', back_populates='bank')
class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    items = Column(JSON)
    user_id = Column(Integer, ForeignKey('users.id',name="fk_user_id_inventory"))
    user = relationship('User', back_populates='inventory')
class Stocks(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    stocks = Column(JSON)
    user_id = Column(Integer, ForeignKey('users.id',name="fk_user_id_stocks"))
class CommunityMarket(Base):
    __tablename__ = 'community_market'
    id = Column(Integer, primary_key=True)
    items = Column(JSON)
    user_id = Column(Integer, ForeignKey('users.id',name="fk_user_id_community_market"))
class Combat(Base):
    __tablename__ = 'combat'
    id = Column(Integer, primary_key=True)
    health =  Column(Integer)
    remaining_health = Column(Integer)
    defence = Column(Integer)
    attack = Column(Integer)
    last_hunt_time = Column(String)
    equipment = Column(JSON)
    user_id = Column(Integer, ForeignKey('users.id', name="fk_user_id_combat"))
Base.metadata.create_all(engine)