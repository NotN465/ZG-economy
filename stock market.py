import json
import random
import time
import pandas as pd
import numpy as np


def simulate_crypto_prices(price, mu=0.0005, sigma=0.02):

        epsilon = np.random.normal(0, 1)
        price *=  np.exp((mu - 0.5 * sigma ** 2) + sigma * epsilon)
        return price
while True:
    with open("stocks.json") as f:
        data = json.load(f)
    k = len(data.keys())
    for x in range(random.randint(1,k)):
        i = random.randint(0,k-1)
        price = data[list(data.keys())[i]]

        diff = simulate_crypto_prices(price)
        data[list(data.keys())[i]] = diff
        with open("stocks.json", "w") as f:
            json.dump(data, f)

    time.sleep(5)