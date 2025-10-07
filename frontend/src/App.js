import React from 'react';
import { MantineProvider, createTheme } from '@mantine/core';
import AppRouter from './AppRouter';
import './App.css';

const theme = createTheme({
  colorScheme: 'dark',
  primaryColor: 'teal',
});

function App() {
  return (
    <MantineProvider theme={theme}>
      <AppRouter />
    </MantineProvider>
  );
}

export default App;