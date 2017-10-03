from random import randint
import json

def pick_restaurant():
    with open('./data/data.json') as json_file:
            json_data = json.load(json_file)

    restaurants = json_data['restaurants']

    return restaurants[randint(0, len(restaurants) - 1)]

if __name__ == "__main__":
    print(pick_restaurant())
