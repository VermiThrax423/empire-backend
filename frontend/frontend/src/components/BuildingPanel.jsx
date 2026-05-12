import client from "../api/client";

export default function BuildingPanel({ buildings = [], onUpgrade }) {
  async function upgradeBuilding(building) {
    try {
        const res = await client.post(`/build/${building.city_id}`, null, {
        params: {
            building_type: building.type
        }
        });

        console.log("Upgrade response:", res.data);

    } catch (err) {
        console.error("Upgrade failed:", err);
    }
  }

  return (
    <div
      style={{
        marginTop: "15px",
        borderTop: "1px solid #555",
        paddingTop: "10px"
      }}
    >
      <h3>Buildings</h3>

      {buildings.map(building => (
        <div
          key={building.id}
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginBottom: "10px"
          }}
        >
          <div>
            {building.type} — Level {building.level}
          </div>

          <button onClick={() => onUpgrade(building)}>
            Upgrade
          </button>
        </div>
      ))}
    </div>
  );
}