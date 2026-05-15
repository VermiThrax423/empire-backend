export default function BuildingCard({
  building,
  onUpgrade
}) {

  return (
    <div
      style={{
        border: "1px solid #555",
        borderRadius: "8px",
        padding: "12px",
        marginBottom: "10px",
        background: "#2b2b2b",
        color: "white"
      }}
    >

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center"
        }}
      >

        <div>

          <div
            style={{
              fontWeight: "bold",
              fontSize: "18px"
            }}
          >
            {building.type.replaceAll("_", " ")}
          </div>

          <div>
            Level {building.level}
          </div>

          <div
            style={{
              fontSize: "12px",
              color: "#aaa"
            }}
          >
            Category: {building.config.category}
          </div>

        </div>

        <button
          onClick={() => onUpgrade(building)}
        >
          {building.level === 0
            ? "Build"
            : "Upgrade"}
        </button>

      </div>

    </div>
  );
}