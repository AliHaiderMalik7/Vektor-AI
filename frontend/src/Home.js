import React from 'react';
import logo from './logo.svg';
import './App.css';

function Home() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="Vektor.ai logo" />
        <h1>Welcome to Vektor.ai</h1>
        <p>Your AI-powered platform</p>
        <div>
          <a href="/login">Login</a> | <a href="/signup">Sign Up</a>
        </div>
      </header>
    </div>
  );
}

export default Home;