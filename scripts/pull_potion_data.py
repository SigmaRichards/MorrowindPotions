#!/usr/bin/env python3

"""
Script to pull raw data from UESP website.
This was prototyped in a jupyter notebook.

Script not strictly necessary if you aleady have the data
but I enjoy cleaning it up to be self-contained.
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import bs4
import json
import requests
from itertools import combinations

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Consts~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ING_URL = "https://en.uesp.net/wiki/Morrowind:Ingredients"
MER_URL = "https://en.uesp.net/wiki/Morrowind:Restocking_Alchemy_Merchants"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#General Utils~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def pull_bs4_url(url):
    """
    Get BeautifulSoup from URL
    """
    soup = requests.get(url).text
    return bs4.BeautifulSoup(soup, features="lxml")

def save_dict_as_json(filename, d_in, clean_keys = False):
    """
    Parses dictionary as json and saves to 'filename'.

    Additionally, ensures path exists

    If clean_keys is set, keys are treated as tuples 
    of strings, and joined by delimiting '|'.
    """
    if clean_keys:
        d_cl = dict()
        for kt,v in d_in.items():
            k = '|'.join(kt)
            d_cl[k] = v
    else:
        d_cl = d_in
    tdir = os.path.dirname(filename)
    os.makedirs(tdir, exist_ok = True)

    d_dump = json.dumps(d_cl, indent = 4)
    with open(filename, 'w') as f:
        f.write(d_dump)
    return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Data-getters~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
Each URL only needs to be processed once,
and has a unique process - hence unique functions.
"""

#Getter for ingredients and effect-pos/neg
def pull_ing_data():
    """
    Pull ingredient data from URL and
    extract following specific rules
    """
    #Define outputs
    ing_data = dict()
    eff_data = dict()
    
    #Get data for processing
    raw = pull_bs4_url(ING_URL)
    ing_tab_rows = raw.find('table').find_all('tr')[1:]

    #Process
    for crow in ing_tab_rows:
        c_id = crow.get('id')
        c_id = c_id.replace(".27","'")
        #Get effects
        ing_data[c_id] = {'effects':[]}
        effs = crow.find_all('td')[2]
        for ceff in effs.find_all('li'):
            eff_name = ceff.find('a').text
            if eff_name not in eff_data:
                eff_data[eff_name] = ceff['class'][-1]
            ing_data[c_id]['effects'].append(eff_name)
        #Get value
        ing_data[c_id]['value'] = int(crow.find_all('td')[3].text)
        #Get weight
        ing_data[c_id]['weight'] = float(crow.find_all('td')[4].text)
    return ing_data, eff_data

#Getter for merchant info
def pull_mer_data():
    """
    Pull ingredient data from URL and
    extract following specific rules
    """
    #Define outputs - assume unique on name
    mer_data = dict()

    #Get data for processing
    raw = pull_bs4_url(MER_URL)
    mer_tab_rows = raw.find('table').find_all('tr')[1:]

    #Process
    for crow in mer_tab_rows:
        c_data = {}
        row_mer, row_ing, _ = crow.find_all('td')
        #Get merchant info
        mer_name, mer_loc, mer_gol = row_mer.find_all('p')
        c_data['location'] = mer_loc.text
        c_data['gold'] = mer_gol.text
        c_data['ingredients'] = dict()
        #Get ingredient info
        for c_ing in row_ing.find_all('li'):
            av = c_ing.find('a')
            c_id = av['href'].split(':')[-1]
            c_id = c_id.replace("%27","'")
            av.extract()
            num = int(c_ing.text[2:-1])
            c_data['ingredients'][c_id] = num
        mer_data[mer_name.text] = c_data
    return mer_data

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Unique-Potion Computation~~~~~~~~~~~~~~~~~~~~~~~

def potion_from_ings(ref_ings, *ings):
    """
    Gets the potion effects given a list of ingredients.
    Returns as sorted tuple
    """
    joined_effs = []
    known_effs = []
    for ci in ings:
        for ce in ref_ings[ci]['effects']:
            if ce in known_effs:
                if ce not in joined_effs:
                    joined_effs.append(ce)
            else:
                known_effs.append(ce)
    joined_effs = sorted(joined_effs)
    return tuple(joined_effs)

def is_potion_non_trivial(ref_ings, *ings):
    """
    Potion is considered 'trivial' if the exact same
    effects can be achieved with fewer ingredients
    """
    ce = potion_from_ings(ref_ings, *ings)
    if len(ings) <= 2:
        return ((len(ce)>0), ce)
    num_c = len(ings) - 1
    for cr in combinations(ings, num_c):
        ne = potion_from_ings(ref_ings, *cr)
        if ne == ce:
            return (False, ce)
    return (True, ce)

def _get_ni_potions(ings, ni):
    """
    Gets all valid, non-trivial potions 
      from 'ni' ingredients from list of 
      all ingredients
    """
    out = dict()
    for cr in combinations(ings, ni):
        is_nt, ce = is_potion_non_trivial(ings, *cr)
        if is_nt:
            if ce not in out:
                out[ce] = []
            out[ce].append(sorted(cr))
    return out

def get_all_potions(ings):
    out = dict()
    for ni in range(2, 4 + 1):
        for k,v in _get_ni_potions(ings, ni).items():
            if k not in out:
                out[k] = []
            out[k].extend(v)
    return out

def is_potion_minimal_neg(c_eff, all_eff, eff_status):
    """
    Checks whether a potion has
    minimal negative stats. A potion
    is non-minimal if there exists 
    a potion with all positive effects,
    and fewer negative effects.
    """
    eff_pos = [a for a in c_eff if eff_status[a] == "EffectPos"]
    eff_neg = [a for a in c_eff if eff_status[a] == "EffectNeg"]
    if len(eff_pos) == 0:
        return False
    if len(eff_neg) == 0:
        return True
    for num_neg in range(len(eff_neg)):
        for c_negs in combinations(eff_neg, num_neg):
            ne = tuple(sorted([*eff_pos, *c_negs]))
            if ne in all_eff:
                return False
    return True

def evaluate_recipe(recipe, ing_data, mer_data):
    """
    Evaluate a recipe by computing to total 
    value, i.e. the sum of values from each
    ingredient; as well as the 
    'minimal-availability', i.e. the minimum
    restocked amount for all ingredients,
    across all merchants
    """
    out = dict(
        recipe = recipe,
        val = 0,
        min_avail = float('inf')
    )
    for ci in recipe:
        avail = max([
            c_merchant['ingredients'].get(ci,0) \
            for c_merchant in mer_data.values()
        ])
        out['min_avail'] = min(out['min_avail'], avail)
        out['val'] += ing_data[ci]['value']
    return out

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    kwargs = dict(
        save_dir =          'data',
        file_ingredients =  'restocked_ingredients.json',
        file_effects =      'effects_pos_neg.json',
        file_merchants =    'merchants.json',
        file_potions =      'potion_data.json',
    )

    #Get data
    print('Pulling data from UESP...')
    ing_data, eff_data = pull_ing_data()
    mer_data = pull_mer_data()

    #Filter ingredients to restocked only
    print('Filtering ingredients...')
    restocking_ids = list(set([b for a in mer_data.values() for b in a['ingredients']]))
    res_ings = {k:v for k,v in ing_data.items() if k in restocking_ids}

    #Compute all potion combinations and filter
    print('Computing potion combinations...')
    pots = get_all_potions(res_ings)
    print('Filtering negative potions...')
    pot_neg_filter = lambda eff: is_potion_minimal_neg(eff,pots,eff_data)
    pos_potions = {k:pots[k] for k in filter(pot_neg_filter, pots)}

    #Evaluate all potions
    print('Evaluating potions...')
    potion_data = {
        k: [evaluate_recipe(cr, ing_data, mer_data) for cr in vs] \
        for k,vs in pos_potions.items()
    }

    #Saving data
    print(f'Saving data to directory `{kwargs["save_dir"]}\'...')
    save_dict_as_json(
            os.path.join(kwargs['save_dir'], kwargs['file_ingredients']),
            res_ings, clean_keys = False)
    save_dict_as_json(
            os.path.join(kwargs['save_dir'], kwargs['file_effects']),
            eff_data, clean_keys = False)
    save_dict_as_json(
            os.path.join(kwargs['save_dir'], kwargs['file_merchants']),
            mer_data, clean_keys = False)
    save_dict_as_json(
            os.path.join(kwargs['save_dir'], kwargs['file_potions']),
            potion_data, clean_keys = True)
    return

if __name__ == "__main__":
    main()
