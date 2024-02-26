#!/usr/bin/env python3

"""
Script to get desrired potion effects and outputs to 
a file in the output directory.

Relies on data already being processed

Outputted files are in JSON format for easy implementation
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import json

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#General Purpose Util~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def load_json(filename):
    with open(filename,'r') as f:
        data = json.load(f)
    return data

def save_json(filename, data):
    dname = os.path.dirname(filename)
    os.makedirs(dname, exist_ok = True)
    with open(filename, 'w') as f:
        f.write(json.dumps(data, indent = 4))
    return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Primary Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def parse_input(inp):
    if inp == "":
        return False
    return int(inp)

def get_merchants(ing, merchants):
    """
    Get merchants who sell an ingredient
    """
    mer_data = []
    for k,v in merchants.items():
        num = v['ingredients'].get(ing,0)
        if num > 0:
            mer_data.append({
                'name': k, 
                'location': v['location'],
                'quantity': num})
    return mer_data

def effect_loop(tree):
    if len(tree) == 0:
        print('\nNo remaining effects to choose from...')
        return False
    ks = sorted(list(tree.keys()))
    for i, v in enumerate(ks):
        print(f"{i+1}:\t {v}")
    inp = input("Select Effect (or [ENTER] to end): ")
    parsed = parse_input(inp)
    if parsed:
        tk = ks[parsed-1]
        rem = effect_loop(tree[tk])
        if type(rem) is bool:
            rem = []
        out = tuple(sorted([tk, *rem]))
        return out
    return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    kwargs = dict(
        filename_tree   = 'data/potion_effect_tree.json',
        filename_pots   = 'data/potion_data.json',
        filename_merc   = 'data/merchants.json',
        output_dir      = "recipes"
    )
    full_tree = load_json(kwargs['filename_tree'])
    potions = load_json(kwargs['filename_pots'])
    merchants = load_json(kwargs['filename_merc'])
    output_dir = kwargs['output_dir']

    loop_v = effect_loop(full_tree)
    if not loop_v:
        print(f"\n\nNo effect targets, exiting...\n")
        return
    print(f"\n\nTagetted effects: {', '.join(loop_v)}\n")
    effname = '|'.join(sorted([b for a in loop_v for b in a.split('|')]))
    recipes = potions[effname]
    recipe_filename = os.path.join(output_dir, f"recipe_{effname}")
    print(f"Saving recipes to : {recipe_filename}")
    save_json(recipe_filename,recipes)

    uq_ings = list(set([b for a in recipes for b in a['recipe']]))
    mer_data = {}
    for ci in uq_ings:
        mer_data[ci] = get_merchants(ci, merchants)
    ingredient_filename = os.path.join(output_dir, f"ingredients_{effname}.txt")
    print(f"Saving ingredient information to : {ingredient_filename}")
    save_json(ingredient_filename, mer_data)

if __name__ == "__main__":
    main()
