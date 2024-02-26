"use client";

import * as React from 'react';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';

let tree_data = require("./data/potion_effect_tree.json");
let recipes = require("./data/potion_data.json");

function getKeys(data){
  return Object.keys(data).sort();
}

function sortByKey(list, key) {
  return list.sort((a, b) => {
    if (a[key] < b[key]) {
      return -1;
    }
    if (a[key] > b[key]) {
      return 1;
    }
    return 0;
  });
}

function recurseKeys(data, lKeys){
  if (lKeys.length === 0){
    return data;
  } else {
    return recurseKeys(data[lKeys[0]], lKeys.slice(1));
  }
}

function createRecipeKey(keys){
  const fKeys = keys.filter(key => key !== null);
  if (fKeys.length === 0){
    return null;
  }
  return fKeys.flatMap((key) => key.split('|')).sort().join('|');
}

function displayRecipe(recipe, index){
  return (
    <div>
      <b>Recipe {index + 1}</b>
      <p>Cost: {recipe['val']}</p>
      <p>Availability (min): {recipe['min_avail']}</p>
      <ul>
      {recipe['recipe'].map((ing) => (<li><a href={"/ingredients/" + ing}>{ing}</a></li>))}
      </ul><br/>
    </div>
  );
}

function displayRecipeKey(recipeKey){
  if (!recipeKey){
    return ;
  } else{
    return (
      <div>
        {sortByKey(recipes[recipeKey],'val').map((rec, index)=> (
	  displayRecipe(rec, index)
	))}
      </div>
    );
  }
}

function MultiEffectHandler(){
  const [keys, setKeys] = React.useState([null]);
  const recipeKey = createRecipeKey(keys);

  const handleKeyChange = (index, value) => {
    const updatedKeys = [...keys.slice(0, index), value, null];
    setKeys(updatedKeys);
  };

  const handleSelectChange = (index) => (event) => {
    handleKeyChange(index, event.target.value);
  };

  const renderSelect = (path, index) => {
    const data = recurseKeys(tree_data, path);
    if (getKeys(data).length === 0){
      return ;
    }else {
      return (
        <Select
          key={index}
          value={keys[index] || ''}
          onChange={handleSelectChange(index)}
        >
          <MenuItem value="">Select</MenuItem>
          {getKeys(data).map((key) => (
            <MenuItem key={key} value={key}>
              {key}
            </MenuItem>
          ))}
        </Select>
      );
    }
  };

  return (
    <div>
      {renderSelect([], 0)}
      {keys.slice(1).map((_, index) => (
        renderSelect(keys.slice(0, index + 1), index + 1)
      ))}
      <p>Potion recipe key: {recipeKey}</p>
      {displayRecipeKey(recipeKey)}
    </div>
  );
}

function BuilderPage() {
  return (
    <body>
      <h1>Potion Creator</h1>
      <div>{MultiEffectHandler()}</div>
    </body>
  );
}

export default BuilderPage;

