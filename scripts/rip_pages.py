#!/use/bin/env python3

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import json
import requests

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Util functions~~~~~~~~~~~~~~~~~~~~~~~~~~

def load_data(filename):
    with open(filename,'r') as f:
        data = json.load(f)
    return data

def save_html(tdir, html, filename='index.html'):
    os.makedirs(tdir, exist_ok = True)
    with open(os.path.join(tdir, filename),'w') as f:
        f.write(html)
    return

def get_source(url):
    return requests.get(url).text

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    kwargs = dict(
        webhost     = "http://localhost:3000/ingredients",
        data_src    = "data/merchants_by_ingredient.json",
        out_dir     = "ingredients"
    )
    print('Loading data...')
    data = load_data(kwargs['data_src'])
    print('Ripping and saving data from webpage...')
    for k in data:
        html = get_source(f"{kwargs['webhost']}/{k}")
        cdir = os.path.join(kwargs['out_dir'],k)
        save_html(cdir, html)
    print('Done')
    return

if __name__ == "__main__":
    main()
