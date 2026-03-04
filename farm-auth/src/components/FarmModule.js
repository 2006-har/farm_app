import React, { useEffect, useState } from "react";
import axios from "axios";

function Dashboard() {
  const [farms, setFarms] = useState([]);
  const [form, setForm] = useState({
    farm_name: "",
    soil_type: "",
    acreage: ""
  });

  const token = localStorage.getItem("token");

  const config = {
    headers: {
      Authorization: `Bearer ${token}`
    }
  };

  // Fetch farms
  const fetchFarms = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:5000/api/farm/all",
        config
      );
      setFarms(res.data);
    } catch (err) {
      alert("Error fetching farms");
    }
  };

  useEffect(() => {
    fetchFarms();
  }, []);

  // Add farm
  const handleAdd = async (e) => {
    e.preventDefault();
    await axios.post(
      "http://127.0.0.1:5000/api/farm/add",
      form,
      config
    );
    setForm({ farm_name: "", soil_type: "", acreage: "" });
    fetchFarms();
  };

  // Delete farm
  const handleDelete = async (id) => {
    await axios.delete(
      `http://127.0.0.1:5000/api/farm/delete/${id}`,
      config
    );
    fetchFarms();
  };

  // Update farm
  const handleUpdate = async (id) => {
    const newName = prompt("Enter new farm name:");
    const newSoil = prompt("Enter new soil type:");
    const newAcreage = prompt("Enter new acreage:");

    await axios.put(
      `http://127.0.0.1:5000/api/farm/update/${id}`,
      {
        farm_name: newName,
        soil_type: newSoil,
        acreage: newAcreage
      },
      config
    );
    fetchFarms();
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
      <h2>Farm Dashboard</h2>

      <div style={styles.card}>
        <h3>Add Farm</h3>
        <form onSubmit={handleAdd}>
          <input
            style={styles.input}
            placeholder="Farm Name"
            value={form.farm_name}
            onChange={(e) => setForm({ ...form, farm_name: e.target.value })}
          />
          <input
            style={styles.input}
            placeholder="Soil Type"
            value={form.soil_type}
            onChange={(e) => setForm({ ...form, soil_type: e.target.value })}
          />
          <input
            style={styles.input}
            placeholder="Acreage"
            type="number"
            value={form.acreage}
            onChange={(e) => setForm({ ...form, acreage: e.target.value })}
          />
          <button style={styles.button}>Add</button>
        </form>
      </div>

      <div style={styles.card}>
        <h3>Your Farms</h3>
        {farms.map((farm) => (
          <div key={farm.farm_id}>
            <p>
              <b>{farm.farm_name}</b> | Soil: {farm.soil_type} | Acreage:{" "}
              {farm.acreage}
            </p>
            <button
              style={{ ...styles.button, backgroundColor: "#007bff" }}
              onClick={() => handleUpdate(farm.farm_id)}
            >
              Update
            </button>
            <button
              style={{ ...styles.button, backgroundColor: "#dc3545" }}
              onClick={() => handleDelete(farm.farm_id)}
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;