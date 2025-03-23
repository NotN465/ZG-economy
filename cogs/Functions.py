import math
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User

engine = create_engine('sqlite:///UserInfo.db')
Session = sessionmaker(bind=engine)
session = Session()


def floor_decimal(number,decimal_places=2):
    return math.floor(number*10**2)/10**2
def level_xp(user_id):
    xp = session.query(User).filter_by(id=str(user_id)).first().xp
    xp_needed = 500
    level = 1
    while xp > xp_needed:
        level += 1
        xp -= xp_needed
        xp_needed = xp_needed +100
    remaining_xp = xp
    next_level_xp = xp_needed-remaining_xp
    #Prvo returna level onda koliko je ostalo xp za sledeci level i onda koliko jos treba xpa do sljedeceg levela
    return level, remaining_xp,next_level_xp