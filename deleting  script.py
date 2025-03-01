from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm  import declarative_base,sessionmaker
from models import CommunityMarket

engine = create_engine('sqlite:///UserInfo.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

session.query(CommunityMarket).delete()
session.commit()

