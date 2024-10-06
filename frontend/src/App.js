import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ImageUpload from './Pages/Imageupload/Imageupload';
import Navbar from './Components/Navbar/Navbar';
import Footer from './Components/Footer/Footer';
import UserData from './Pages/Userdata/Userdata';
import Home from './Pages/Home/Home';
function App() {
  return (
    <div className="App">
      <Router>
        <Navbar />
        
        <Routes>
        <Route path="/" element={<Home />} />
          <Route path="/signup" element={<UserData />} />
          <Route path="/upload" element={<ImageUpload />} />
          {/* Add more routes here if needed */}
        </Routes>

        <Footer />
      </Router>
    </div>
  );
}

export default App;
