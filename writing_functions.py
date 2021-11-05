"""Linking back to data/prompts.py
Fuctions to handle my pdf and other data around the writing prompts"""

import random
import data.prompts as dp


def get_random_dictionary():
    """get random dictionary from data/prompts.py.  This will help in generating random writing prompts"""

    prompts_list = dp.prompts_dicts
    return random.choice(prompts_list)

# Right now not using this function
def get_random_directions():
    """returns the directions from a randomly selected dictionary"""

    random_dict = get_random_dictionary()
    return random_dict['directions']

def prompt_sentence():

    random_dict = get_random_dictionary()
    if random_dict['name'] == 'random combinations':
        return f'TWO words'
    else:
        return random_dict['prompt']



