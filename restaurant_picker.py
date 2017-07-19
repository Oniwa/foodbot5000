from random import randint

def pick_restaurant():
    restaurants = ['Blackthorn',
                   'Kings Pizza',
                   'Tropicana',
                   'Instant Karma',
                   'Hackett Hot Wings',
                   'The Mill',
                   'Old Chicago',
                   "Sam's Cellar",
                   ]

    return restaurants[randint(0, len(restaurants) - 1)]

if __name__ == "__main__":
    print(pick_restaurant())
