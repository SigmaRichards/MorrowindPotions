#!/usr/bin/env python3

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import json

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Constants~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

INPUT_FN  = "merchants.json"
OUTPUT_FN = "merchants_by_ingredient.json"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Util functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def load_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def save_data(filename, data):
    with open(filename, 'w') as f:
        f.write(json.dumps(data,indent = 4))
    return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    kwargs = dict(
        input_file  = "data/merchants.json",
        output_file = "data/merchants_by_ingredient.json",
    )
    print("Loading data...")
    data = load_data(kwargs['input_file'])
    all_ings = list(set([b for a in data.values() for b in a['ingredients']]))
    out = dict()
    print("Processing data...")
    for cing in all_ings:
        out[cing] = []
        for k,v in data.items():
            num = v['ingredients'].get(cing, False)
            if num:
                out[cing].append({k: {'num': num, 'location': v['location']}})
    print("Saving data...")
    save_data(kwargs['output_file'], out)
    return

if __name__ == "__main__":
    main()
