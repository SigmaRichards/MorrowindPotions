# Morrowind Potion Finder/Builder

You found my scripts for finding/building morrowind potions. These are simple scripts designed to help you find which potions are craftable by what ingredients. The ingredients the script considers is only those which are RESTOCKABLE by merchants. So ingredients obtainable by collecting in the wild are ignored (unless also sold by vendors).

I'm uploading this code for posterity. This information is bound to exist elsewhere, and be clearer, more informative or more easily accessible. This was a personal project that I found fun.

Included is the source for two applications. The first is the command-line scripts using python. The second is a web-app designed in react by someone who has a total of 4 hours experience in JS and has a few missing lobes in his brain.

## Data

Regardless of how you want to use this, you will need the data. In the first upload of this, I've included the data files, but whether I need to remove them for whatever reason later we'll see.

If you want (or need) to pull the data, you can use the scripts. I have included a utility bash-script `get_data.sh` - which effectively just runs the python scripts in the `scripts` folder. This will create a `data` folder with all the necessary data.

All the data is stored in JSON so feel free to use it for whatever you want.

## Using the CLI

With the repo cloned, and the data available, just run: 

```
./potions_cli.sh
```

It will give you a list of effects you want to include in the potion. These are numbered so just select the first effect you want in your potion and press enter. The program will update and give you the same prompt again, except the effects now are only those which can be combined with your previously selected effects. This will continue until either there are no more possible effects you can include, or if you press enter early to end.

Once you've selected all the effects you want, it will either automatically give you the recipes, or just press "enter" without entering any numbers. The recipes will be saved in the output directotry `recipes` with 2 files. The first will be `recipes_{selected effects}.txt` and will contain the actual recipes along with other information. The "val" is the total cost/value of each ingredient, so is proportional to what you will be paying to craft each potion. The "min_avail" stat is the minimum stocked amount for all ingredients across all vendors who stock those ingredients. The second file `ingredients_{selected effects}.txt` will contain a list of all ingredients in the recipes file and which vendors stock that ingredient.

### Effects split by '|'

Some effects you can only include by include other effects. "Fortify Speed" is a good example, as the only possible way you can make this potion with restockable ingredients is by also having "Drain Fatigue". The program will show you this by splitting the effects with "|" character.

## Setting up the web-app

I have almost no experience with JS, node, or react so whether this is sufficient or too much information for setup I have no idea.

The versions I'm using:

```
node: -v21.6.2
npm:  -v10.2.4
```

In order to setup, follow the steps below:

```
cd web-app
npm install .
npm run build
cp -r ../data build/.
```

And then the static directory should be available in `web-app/build/`. You can host this however you like. If you want to host locally, you can use:

```
#(inside the web-app directory)
npm install -g serve
serve -s build/
```

### Ingredient pages not working

This web-app uses reacts-dom routing so needs to be hosted in some weird specific way which I don't actually understand. However, running into this myself, I made simple (but somewhat awful) solution.

In one terminal, in the `web-app` directory, run:

```
npm start
```

And wait for the setup to finish. Connect to the testing webpage and ensure it is all working as intended. Next, in a new terminal, cd into the root directory for this repo, and run the script:

```
./fix_ingredients.sh
```
