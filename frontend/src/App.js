import React from 'react';
import AppRouter from './AppRouter';
import { ThemeProvider } from './ThemeProvider';
import './App.css';

function App() {
  return (
    <ThemeProvider>
      <AppRouter />
    </ThemeProvider>
  );
}

export default App;
//create a fitness plan for 1 day weight is 76kg height is 5.8 begineer muscle strength for male age is 27