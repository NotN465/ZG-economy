import json
import random
import time
while True:
    with open("stocks.json") as f:
        data = json.load(f)
    k = len(data.keys())
    for x in range(k):
        i = random.randint(0,k-1)
        price = data[list(data.keys())[i]]
        diff = price/0.98-price
        #print(f"{list(data.keys())[i]}: {price}")
        random_chance = random.randint(0,100)
        if random_chance > 45:
            data[list(data.keys())[i]] += diff
        else:
            data[list(data.keys())[i]] -= diff
        with open("stocks.json", "w") as f:
            json.dump(data, f)

    time.sleep(2)