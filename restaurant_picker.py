from random import randint

restaurants = ['Blackthorn',
               'Kings Pizza',
               'Tropicana',
               'Instant Karma',
               'Hackett Hot Wings',
               'The Mill',
               'Old Chicago',
               "Sam's Cellar",
               ]

print(restaurants[randint(0, len(restaurants) - 1)])
