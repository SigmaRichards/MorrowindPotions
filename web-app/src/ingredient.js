import * as React from 'react';

let merchants = require("./data/merchants_by_ingredient.json");

function displayMerchantInfo(merchant){
  return (
    <div>
      <b>Name:</b> {Object.keys(merchant)[0]}<br/>
      <b>Count:</b> {merchant[Object.keys(merchant)[0]]['num']}<br/>
      <b>Location:</b> {merchant[Object.keys(merchant)[0]]['location']}<br/><br/>
    </div>
  );
}

function ingredientPage(ingredient){
  return (
    <body>
    <h1>{ingredient}</h1>
    <h2>Merchants who sell: </h2>
    {merchants[ingredient].map((merchant) => displayMerchantInfo(merchant))}
    <a href="/">Go back</a>
    </body>
  );
}

export default ingredientPage;
