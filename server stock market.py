import json
import random
import time
import pandas as pd
import numpy as np
from models import Server
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.attributes import flag_modified

engine = create_engine('sqlite:///UserInfo.db')
Session = sessionmaker(bind=engine)
session = Session()

def simulate_crypto_prices(price, mu=0.0005, sigma=0.02):

        epsilon = np.random.normal(0, 1)
        price *=  np.exp((mu - 0.5 * sigma ** 2) + sigma * epsilon)
        return price
while True:
    servers = session.query(Server).all()
    for server in servers:
        data = server.stocks
        k = len(data.keys())
        for x in range(random.randint(1,k)):
            i = random.randint(0,k-1)
            price = data[list(data.keys())[i]]

            diff = simulate_crypto_prices(price)
            data[list(data.keys())[i]] = diff
            server.stocks = data
            flag_modified(server, "stocks")
            session.commit()
        print(data)

    time.sleep(5)