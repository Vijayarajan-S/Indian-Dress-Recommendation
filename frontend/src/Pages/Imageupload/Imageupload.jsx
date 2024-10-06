import React, { useState } from "react";
import axios from "axios";
import "./Imageupload.css";

const Imageupload = () => {
  const [data, setData] = useState({
    email: "",
    image: null,
    preference: "", // State for the preference
  });

  const [result, setResult] = useState([]);

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (name === "image") {
      setData({ ...data, image: files[0] });
    } else {
      setData({ ...data, [name]: value }); // Update preference
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("file", data.image);
    formData.append("email", data.email);
    formData.append("preference", data.preference); // Append the preference to FormData

    try {
      const response = await axios.post(
        "http://127.0.0.1:8888/getCelebrityData",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      if (response.data && response.data.data) {
        alert(response.data.message);
        setResult(response.data.data); // Store all recommendations
        console.log("Response:", response.data.data);
      } else {
        alert("No recommendations found.");
        setResult([]); // Clear previous results
      }
    } catch (error) {
      alert(
        "Unsuccessful upload: " + error.response?.data?.error || "Unknown error"
      );
      console.error("Error:", error);
    }
  };

  return (
    <div className="image-upload">
      <form onSubmit={handleSubmit}>
        <label htmlFor="email">Email ID</label>
        <input type="email" name="email" onChange={handleChange} required />

        <label htmlFor="image">Image</label>
        <input
          type="file"
          name="image"
          onChange={handleChange}
          accept="image/*"
          required
        />

        <label htmlFor="preference">Preference</label>
        <select
          name="preference"
          value={data.preference}
          onChange={handleChange}
          required
        >
          <option value="" disabled>
            Select your preference
          </option>
          <option value="Traditional">Traditional</option>
          <option value="Red Carpet">Red Carpet</option>
          <option value="Casual">Casual</option>
        </select>

        <button type="submit">Upload</button>
      </form>

      <div className="recommendation">
        <center>
          {result.length > 0 ? (
            result.map((val, index) => (
              <div key={index} className="recommendation-item">
                <div className="image">
                  <img src={val["Image Link"]} alt="Not found" />
                </div>
                <div className="details">
                  <p>
                    Dress Type : <span>{val["Dress Type"]}</span>
                  </p>
                  <p>
                    Celebrity Name : <span>{val["Celebrity Name"]}</span>
                  </p>
                  <p>
                    Costume Theme : <span>{val["Costume Theme"]}</span>
                  </p>
                  <p>
                    Color Palette : <span>{val["Color Palette"]}</span>
                  </p>
                  <p>
                    Accessories : <span>{val["Accessories"]}</span>
                  </p>
                  <p>
                    Style Elements : <span>{val["Style Elements"]}</span>
                  </p>
                </div>
              </div>
            ))
          ) : (
            <h6>No recommendations available.</h6>
          )}
        </center>
      </div>
    </div>
  );
};

export default Imageupload;
