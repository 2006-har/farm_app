import React, { useEffect, useState } from "react";
import axios from "axios";

function CropsModule() {
  const [crops, setCrops] = useState([]);
  const [form, setForm] = useState({
    crop_name: "",
    growth_duration: ""
  });

  const token = localStorage.getItem("token");

  const config = {
    headers: {
      Authorization: `Bearer ${token}`
    }
  };

  // Fetch crops
  const fetchCrops = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:5000/api/crops/list",
        config
      );
      setCrops(res.data);
    } catch (err) {
      alert("Error fetching crops");
      console.error(err);
    }
  };

  useEffect(() => {
    fetchCrops();
  }, []);

  // Add crop
  const handleAdd = async (e) => {
    e.preventDefault();
    try {
      await axios.post(
        "http://127.0.0.1:5000/api/crops/add",
        form,
        config
      );
      setForm({ crop_name: "", growth_duration: "" });
      fetchCrops();
    } catch (err) {
      alert("Error adding crop");
      console.error(err);
    }
  };

  // Delete crop
  const handleDelete = async (id) => {
    try {
      await axios.delete(
        `http://127.0.0.1:5000/api/crops/delete/${id}`,
        config
      );
      fetchCrops();
    } catch (err) {
      alert("Error deleting crop");
      console.error(err);
    }
  };

  // Update crop
  const handleUpdate = async (id) => {
    const newName = prompt("Enter new crop name:");
    const newDuration = prompt("Enter new growth duration (days):");

    if (!newName || !newDuration) return;

    try {
      await axios.put(
        `http://127.0.0.1:5000/api/crops/update/${id}`,
        { crop_name: newName, growth_duration: newDuration },
        config
      );
      fetchCrops();
    } catch (err) {
      alert("Error updating crop");
      console.error(err);
    }
  };

  const styles = {
    container: {
      padding: "30px",
      fontFamily: "Arial",
      backgroundColor: "#f4f6f8",
      minHeight: "100vh"
    },
    card: {
      backgroundColor: "white",
      padding: "20px",
      borderRadius: "10px",
      boxShadow: "0 0 10px rgba(0,0,0,0.1)",
      marginBottom: "20px"
    },
    input: {
      padding: "10px",
      margin: "5px",
      borderRadius: "5px",
      border: "1px solid #ccc"
    },
    button: {
      padding: "10px 15px",
      margin: "5px",
      borderRadius: "5px",
      border: "none",
      cursor: "pointer",
      backgroundColor: "#28a745",
      color: "white"
    }
  };

  return (
    <div style={styles.container}>
      <h2>Crops Dashboard</h2>

      <div style={styles.card}>
        <h3>Add Crop</h3>
        <form onSubmit={handleAdd}>
          <input
            style={styles.input}
            placeholder="Crop Name"
            value={form.crop_name}
            onChange={(e) => setForm({ ...form, crop_name: e.target.value })}
          />
          <input
            style={styles.input}
            placeholder="Growth Duration (days)"
            type="number"
            value={form.growth_duration}
            onChange={(e) =>
              setForm({ ...form, growth_duration: e.target.value })
            }
          />
          <button style={styles.button}>Add</button>
        </form>
      </div>

      <div style={styles.card}>
        <h3>All Crops</h3>
        {crops.map((crop) => (
          <div key={crop.crop_id}>
            <p>
              <b>{crop.crop_name}</b> | Duration: {crop.growth_duration} days
            </p>
            <button
              style={{ ...styles.button, backgroundColor: "#007bff" }}
              onClick={() => handleUpdate(crop.crop_id)}
            >
              Update
            </button>
            <button
              style={{ ...styles.button, backgroundColor: "#dc3545" }}
              onClick={() => handleDelete(crop.crop_id)}
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CropsModule;