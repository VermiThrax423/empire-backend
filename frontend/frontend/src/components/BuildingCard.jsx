import React from "react";

export default function BuildingCard({
  building,
  activeUpgrade,
  onUpgrade,
  remaining
}) {

  return (
    <div
      style={{
        border: "1px solid #555",
        borderRadius: "8px",
        padding: "12px",
        marginBottom: "10px",
        backgroundColor: "#2d2d2d",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center"
      }}
    >

      {/* LEFT SIDE */}
      <div style={{ width: "35%" }}>

        <div
          style={{
            fontSize: "12px",
            color: "#888",
            textTransform: "uppercase"
          }}
        >
          {building.config.category}
        </div>

        <div
          style={{
            fontSize: "20px",
            fontWeight: "bold"
          }}
        >
          {building.type.replaceAll("_", " ").toUpperCase()}
        </div>

      </div>

      {/* CENTER */}
      <div
        style={{
          width: "35%",
          textAlign: "center"
        }}
      >

        <div
          style={{
            fontSize: "20px",
            fontWeight: "bold"
          }}
        >
          Level {building.level}
        </div>

         
          <div
            style={{
              fontSize: "12px",
              marginBottom: "8px",
              color: "#bbb",
              display: "flex",
              flexWrap: "wrap",
              alignItems: "center",
              justifyContent: "center",
              gap: "4px"
            }}
          >
            {Object.entries(
              building.config.base_cost
            ).map(([resource, amount], index, arr) => (
              <React.Fragment key={resource}>
                <span>
                  {resource}: {amount.toLocaleString()}
                </span>
                {index < arr.length - 1 && <span> --- </span>}
              </React.Fragment>
            ))}
          </div>
        

      </div>

      {/* RIGHT SIDE */}
      <div
        style={{
          width: "30%",
          textAlign: "right"
        }}
      >

        

        <button
          disabled={remaining > 0}
          onClick={() => onUpgrade(building)}
        >
          {remaining > 0
            ? "Building..."
            : building.level === 0
              ? "Build"
              : "Upgrade"}
        </button>

        {remaining > 0 ? (
          <div style={{ color: "orange" }}>
            Upgrading to Level {activeUpgrade?.target_level}

            <br />

            ({remaining}s remaining)
          </div>
        ) : (
          <div
            style={{
              fontSize: "13px",
              color: "#aaa"
            }}
          >
            Next Level:
            {" "}
            {building.config.base_time}s
          </div>
        )}

      </div>

    </div>
  );                          
}