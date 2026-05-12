export default function ResourcePanel() {
  return (
    <div
      style={{
        display: "flex",
        gap: "20px",
        backgroundColor: "#111",
        color: "white",
        padding: "15px",
        borderBottom: "2px solid #444",
        marginBottom: "20px"
      }}
    >
      <div>💰 Gold: 1000</div>
      <div>🌲 Wood: 500</div>
      <div>🪨 Stone: 300</div>
      <div>🌾 Food: 800</div>
    </div>
  );
}