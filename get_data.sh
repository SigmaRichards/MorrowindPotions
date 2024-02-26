#!/bin/bash

PY_WRAP="python3"
PULL_SCR="scripts/pull_potion_data.py"
TREE_SCR="scripts/potion_effect_tree.py"
MERC_SCR="scripts/create_merchant_by_ingredient.py"

echo -e \
"Running data-puller script for morrowind potions. V1.0.0

This will likely never be maintained, but it's simple enough, you could probably update it yourself.

This script assume the environment has the correct setup.

The python scripts only require 2 packages not in python by default:
	- beautifulsoup4
	- requests

This bash script runs 3 python scripts to achieve different tasks.

The first is designed to pull data from UESP. I didn't bother checking if there is an API, and it is more or less hard-coded to pull the data from that tables. If the site changes, this will likely break, but I'm going to supply the data as well so deal with the data supplied, or sort it out yourself.

The second script builds a tree-style hierarchy file from the sourced data. This is not strictly necessary, but it helps simplify the processing later.

The third script restructures the merchant data to be keyed by ingredient.
"
read -p "Press [ENTER] to continue"

echo -e "Running script 1:"
$PY_WRAP $PULL_SCR

echo ""
echo -e "Running script 2:"
$PY_WRAP $TREE_SCR

echo ""
echo -e "Running script 3:"
$PY_WRAP $MERC_SCR
