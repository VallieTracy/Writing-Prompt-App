"""Linking back to data/prompts.py
Unsure what to actually write here..."""

from model import db, User, Nugget, Word, connect_to_db
import random
import data.prompts as dp

def test():

    prompts_list = dp.prompts_dicts
    directions = []
    for dictionary in prompts_list:
        directions.append(dictionary['directions'])
    return directions

def test2():
    prompts = ['p-1', 'p-2', 'p-3']
    return prompts

def get_random_dictionary():
    """randomly picks a dictionary from data/prompts.py and returns the associated directions in list form"""
    
    prompts_list = dp.prompts_dicts
    random_dict = random.choice(prompts_list)
    return random_dict['directions']

# Do I need this code? What is it doing?
if __name__ == '__main__':
    from server import app
    connect_to_db(app)