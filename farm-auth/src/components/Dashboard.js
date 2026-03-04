import React, { useState } from "react";
import FarmModule from "./FarmModule";
import CropsModule from "./CropsModule";

function Dashboard() {
  const [activeTab, setActiveTab] = useState("farm");

  const styles = {
    container: {
      display: "flex",
      height: "100vh",
      fontFamily: "Arial"
    },
    sidebar: {
      width: "220px",
      backgroundColor: "#2c3e50",
      color: "white",
      padding: "20px"
    },
    menuItem: {
      padding: "10px",
      cursor: "pointer",
      marginBottom: "10px",
      borderRadius: "5px"
    },
    content: {
      flex: 1,
      padding: "30px",
      backgroundColor: "#ecf0f1"
    }
  };

  const renderContent = () => {
    if (activeTab === "farm") return <FarmModule />;
    if (activeTab === "crops") return <CropsModule />;
    if (activeTab === "expenses") return <h2>Expenses Module - Coming Soon</h2>;
    if (activeTab === "mandi") return <h2>Mandi Module - Coming Soon</h2>;
    if (activeTab === "crop advisory") return <h2>Crop Advisory Module - Coming Soon</h2>;
  };
 

  return (
    <div style={styles.container}>
      <div style={styles.sidebar}>
        <h2>AgroMed</h2>

        <div
          style={styles.menuItem}
          onClick={() => setActiveTab("farm")}
        >
          🌾 Farm
        </div>

        <div
          style={styles.menuItem}
          onClick={() => setActiveTab("crops")}
        >
          🌱 Crops
        </div>

        <div
          style={styles.menuItem}
          onClick={() => setActiveTab("expenses")}
        >
          💰 Expenses
        </div>
        <div
          style={styles.menuItem}
          onClick={() => setActiveTab("crop advisory")}
        >
         🧠  Crop Advisory
        </div>

        <div
          style={styles.menuItem}
          onClick={() => setActiveTab("mandi")}
        >
          🏪 Mandi
        </div>
      </div>

      <div style={styles.content}>
        {renderContent()}
      </div>
    </div>
  );
}

export default Dashboard;