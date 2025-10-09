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