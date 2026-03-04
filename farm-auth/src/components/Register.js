import React, { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("farmer");
  const [message, setMessage] = useState("");

  const handleRegister = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:5000/api/auth/register", {
        name,
        email,
        password,
        role,
      });
      setMessage(res.data.message);
    } catch (err) {
      setMessage(err.response?.data?.message || "Registration failed");
    }
  };

  // Inline styles
  const containerStyle = {
    maxWidth: "400px",
    margin: "80px auto",
    padding: "40px",
    borderRadius: "12px",
    boxShadow: "0 8px 20px rgba(0,0,0,0.1)",
    backgroundColor: "#fff",
    textAlign: "center",
    fontFamily: "'Arial', sans-serif",
  };

  const titleStyle = { marginBottom: "20px", color: "#333" };

  const inputStyle = {
    width: "100%",
    padding: "12px 15px",
    margin: "10px 0",
    borderRadius: "8px",
    border: "1px solid #ccc",
    fontSize: "16px",
    outline: "none",
  };

  const buttonStyle = {
    width: "100%",
    padding: "12px",
    marginTop: "10px",
    borderRadius: "8px",
    border: "none",
    fontSize: "16px",
    backgroundColor: "#28a745",
    color: "#fff",
    cursor: "pointer",
  };

  const linkStyle = { display: "block", marginTop: "15px", color: "#007bff", textDecoration: "none" };

  const messageStyle = {
    marginTop: "10px",
    fontWeight: "bold",
    color: message.includes("successfully") ? "green" : "red",
  };

  return (
    <div style={containerStyle}>
      <h2 style={titleStyle}>Register</h2>
      <input
        type="text"
        placeholder="Full Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        style={inputStyle}
        onFocus={(e) => (e.target.style.borderColor = "#28a745")}
        onBlur={(e) => (e.target.style.borderColor = "#ccc")}
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        style={inputStyle}
        onFocus={(e) => (e.target.style.borderColor = "#28a745")}
        onBlur={(e) => (e.target.style.borderColor = "#ccc")}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={inputStyle}
        onFocus={(e) => (e.target.style.borderColor = "#28a745")}
        onBlur={(e) => (e.target.style.borderColor = "#ccc")}
      />
      <input
        type="text"
        placeholder="Role (farmer/admin)"
        value={role}
        onChange={(e) => setRole(e.target.value)}
        style={inputStyle}
        onFocus={(e) => (e.target.style.borderColor = "#28a745")}
        onBlur={(e) => (e.target.style.borderColor = "#ccc")}
      />
      <button style={buttonStyle} onClick={handleRegister}>
        Register
      </button>
      <p style={messageStyle}>{message}</p>
      <Link to="/" style={linkStyle}>
        Already have an account? Login
      </Link>
    </div>
  );
}

export default Register;