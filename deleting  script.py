from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm  import declarative_base,sessionmaker
from models import CommunityMarket,User,Bank,Inventory,Combat

engine = create_engine('sqlite:///UserInfo.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
def all_user_deletion():
    session.query(User).delete()
    session.query(Bank).delete()
    session.query(Inventory).delete()
    session.query(CommunityMarket).delete()
    session.query(Combat).delete()

all_user_deletion()

session.commit()

