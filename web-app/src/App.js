// App.js
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import BuilderPage from './builder'
import ingredientPage from './ingredient';

let merchants = require("./data/merchants_by_ingredient.json");

function App(){
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<BuilderPage />}/>
	{Object.keys(merchants).map((ing) => (
          <Route path={"/ingredients/"+ing} element={<html>{ingredientPage(ing)}</html>}/>
	))}
      </Routes>
    </BrowserRouter>
  );
};

export default App;
