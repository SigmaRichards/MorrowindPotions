#!/usr/bin/env python3

"""
Script to look at tree of compounding effects.
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import json

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Utils~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def clean_tuple_keys(d_in, delim = '|'):
    out = dict()
    for k, v in d_in.items():
        new_k = k
        new_v = v
        if type(k) is tuple:
            new_k = delim.join(k)
        if type(v) is dict:
            new_v = clean_tuple_keys(v, delim = delim)
        out[new_k] = new_v
    return out

def load_json_as_dict(filename, delimit_keys = None):
    with open(filename,'r') as f:
        raw = json.load(f)
    if delimit_keys is None:
        return raw
    out = {tuple(k.split(delimit_keys)):v for k,v in raw.items()}
    return out

def save_dict_as_json(filename, d_in, delim = None):
    if delim is not None:
        d_cl = clean_tuple_keys(d_in, delim)
    else:
        d_cl = d_in
    with open(filename, 'w') as f:
        f.write(json.dumps(d_cl, indent = 4))
    return 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Tree functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def tree_insert(c_eff, tree):
    #This implies 'c_eff' is child of 'tree'
    out = dict()
    #Flags for error handling
    used_flag = False
    for k,v in tree.items():
        if set(c_eff) < set(k):
            #Is parent of node
            #Note: Can be parent of multiple nodes in tree
            if c_eff not in out:
                out[c_eff] = dict()
            out[c_eff][k] = v
            used_flag = True
        elif set(k) < set(c_eff):
            #Is child of node
            out[k] = tree_insert(c_eff, v)
            used_flag = True
        else:
            #Is sibling OR child of sibling
            out[k] = v
    if not used_flag:
        out[c_eff] = dict()
    return out

def build_tree(eff_tuples):
    tree = dict()
    for c_efft in eff_tuples:
        tree = tree_insert(c_efft, tree)
    return tree

def clean_tree(tree, cname = tuple()):
    out = dict()
    for k,v in tree.items():
        new_v = dict()
        if len(v) > 0:
            new_v = clean_tree(v, cname = k)
        new_k = tuple([a for a in k if a not in cname])
        out[new_k] = new_v
    return out

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    print("Loading data...")
    potion_data = load_json_as_dict('data/potion_data.json', delimit_keys = "|")
    print("Building tree...")
    eff_tree = build_tree(potion_data)
    print("Cleaning tree...")
    eff_tree = clean_tree(eff_tree)
    print("Saving data...")
    save_dict_as_json('data/potion_effect_tree.json', eff_tree, delim = "|")

if __name__ == "__main__":
    main()
