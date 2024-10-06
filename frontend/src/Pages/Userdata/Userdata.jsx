import React, { useState } from 'react';
import './Userdata.css';
import axios from 'axios';
// import { useNavigate } from 'react-router-dom'; // If using react-router-dom for navigation

const Userdata = () => {
  const [data, setData] = useState({
    name: '',
    email: '',
    password:'',
    age: '',
    gender: '',
    height: '',
    weight: '',
  });

  // const navigate = useNavigate(); // To handle navigation

  const handleChange = (e) => {
    const { name, value } = e.target;
    setData({ ...data, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      
      const response = await axios.post('http://127.0.0.1:8888/userData', data); 
      if (response) {
        // navigate('/'); 
        alert("Data Uploaded");
        console.log('Form submitted successfully:', response.data);
      }
    } catch (error) {
      alert('Unsuccessful upload');
      console.log('Error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="name">Name</label>
      <input
        type="text"
        name="name"
        value={data.name}
        placeholder="Enter your name"
        onChange={handleChange}
        required
      />

      <label htmlFor="email">Email</label>
      <input
        type="email"
        name="email"
        value={data.email}
        placeholder="Enter your email"
        onChange={handleChange}
        required
      />
      <label htmlFor="password">Password</label>
      <input
        type="password"
        name="password"
        value={data.password}
        placeholder="Enter your password"
        onChange={handleChange}
        required
      />

      <label htmlFor="age">Age</label>
      <input
        type="number"
        name="age"
        value={data.age}
        placeholder="Enter your age"
        onChange={handleChange}
        required
      />

      <label htmlFor="gender">Gender</label>
      <input
        type="text"
        name="gender"
        value={data.gender}
        placeholder="Enter your gender"
        onChange={handleChange}
        required
      />

      <label htmlFor="height">Height</label>
      <input
        type="number"
        name="height"
        value={data.height}
        placeholder="Enter your height"
        onChange={handleChange}
        required
      />

      <label htmlFor="weight">Weight</label>
      <input
        type="number"
        name="weight"
        value={data.weight}
        placeholder="Enter your weight"
        onChange={handleChange}
        required
      />

      <button type="submit">Submit</button>
    </form>
  );
};

export default Userdata;
