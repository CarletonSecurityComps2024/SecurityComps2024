import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './pages/Login';  // Import the Login component

// Home Component
const Home: React.FC = () => {
  return <h1>Welcome to the Home Page!</h1>;
};

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />  {/* Default path to login */}
        <Route path="/login" element={<Login />} /> {/* Login route */}
        <Route path="/home" element={<Home />} /> {/* Home route after successful login */}
      </Routes>
    </Router>
  );
};

export default App;
