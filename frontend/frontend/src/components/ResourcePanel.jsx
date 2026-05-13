export default function ResourcePanel({ resources }) {
  
  if (!resources) {
    return <div>Loading resources...</div>;
  }
  
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
      <div>💰 {Math.floor(resources.money)}</div>
      <div>🌾 {Math.floor(resources.food)}</div>
      <div>🛢 {Math.floor(resources.oil)}</div>
      <div>🔬 {Math.floor(resources.tech)}</div>
    </div>
  );
}