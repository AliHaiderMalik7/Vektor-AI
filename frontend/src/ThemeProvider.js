import React, { createContext, useContext, useState, useEffect } from 'react';
import { MantineProvider, createTheme } from '@mantine/core';

const ThemeContext = createContext();

export const useTheme = () => useContext(ThemeContext);

const lightTheme = createTheme({
  colorScheme: 'light',
  colors: {
    dark: ['#d5d7e0', '#acaebf', '#8c8fa3', '#666980', '#4d4f66', '#34354a', '#2b2c3d', '#1a1b2e', '#0f1015', '#01010a'],
    gray: ['#f8f9fa', '#e9ecef', '#dee2e6', '#ced4da', '#adb5bd', '#6c757d', '#495057', '#343a40', '#212529', '#000000'],
    blue: ['#e7f5ff', '#d0ebff', '#a5d8ff', '#74c0fc', '#4dabf7', '#339af0', '#228be6', '#1c7ed6', '#1971c2', '#1864ab'],
  },
  primaryColor: 'blue',
  components: {
    Button: {
      defaultProps: {
        variant: 'filled',
      },
    },
  },
  other: {
    background: '#ffffff',
    surface: '#f8f9fa',
    text: '#000000',
    textSecondary: '#6c757d',
    border: '#dee2e6',
    cardBackground: '#ffffff',
    inputBackground: '#ffffff',
    headerBackground: '#ffffff',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  },
});

const darkTheme = createTheme({
  colorScheme: 'dark',
  colors: {
    dark: ['#c1c2c5', '#a6a7ab', '#909296', '#5c5f66', '#373a40', '#2c2e33', '#25262b', '#1a1b1e', '#141517', '#101113'],
    gray: ['#f8f9fa', '#e9ecef', '#dee2e6', '#ced4da', '#adb5bd', '#6c757d', '#495057', '#343a40', '#212529', '#000000'],
    blue: ['#e7f5ff', '#d0ebff', '#a5d8ff', '#74c0fc', '#4dabf7', '#339af0', '#228be6', '#1c7ed6', '#1971c2', '#1864ab'],
  },
  primaryColor: 'blue',
  components: {
    Button: {
      defaultProps: {
        variant: 'filled',
      },
    },
  },
  other: {
    background: '#1a1b1e',
    surface: '#25262b',
    text: '#ffffff',
    textSecondary: '#adb5bd',
    border: '#373a40',
    cardBackground: '#2c2e33',
    inputBackground: '#2c2e33',
    headerBackground: '#1a1b1e',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  },
});

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('dark');

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  const currentTheme = theme === 'dark' ? darkTheme : lightTheme;

  useEffect(() => {
    // Save theme to localStorage
    localStorage.setItem('theme', theme);
  }, [theme]);

  useEffect(() => {
    // Load theme from localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      setTheme(savedTheme);
    }
  }, []);

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      <MantineProvider theme={currentTheme}>
        {children}
      </MantineProvider>
    </ThemeContext.Provider>
  );
};