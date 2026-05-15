import { useEffect, useState } from "react";

export default function ResourcePanel({ resources }) {
  
  const [displayedResources, setDisplayedResources] = useState(null);

  useEffect(() => {
    if (!resources) return;

    setDisplayedResources(resources);
  }, [resources]);

  useEffect(() => {

    if (!resources) return;

    const interval = setInterval(() => {

      setDisplayedResources(prev => {

        if (!prev) return prev;

        return {
          ...prev,

          money:
            prev.money + (prev.money_per_hour / 3600),

          food:
            prev.food + (prev.food_per_hour / 3600),

          oil:
            prev.oil + (prev.oil_per_hour / 3600),

          tech:
            prev.tech + (prev.tech_per_hour / 3600),
        };
      });

    }, 1000);

    return () => clearInterval(interval);

  }, [resources]);

  if (!displayedResources) {
    return <div>Loading resources...</div>;
  }

  
  return (
    <div
      style={{
        fontFamily: "Arial",
        fontSize: "14px",
        fontWeight: "bold",
        letterSpacing: "0.5px",
        display: "flex",
        justifyContent: "center",
        alignContent: "center",
        gap: "30px",
        backgroundColor: "#222",
        color: "white",
        padding: "12px 20px",
        borderBottom: "1px solid #444",
        marginBottom: "20px",
        width: "95%"
      }}
    >
      <div>💰 {Math.floor(displayedResources.money).toLocaleString() || 0}
        <span style={{ color: "#0f0", marginLeft: "6px"}}>
          (+{resources.money_per_hour.toLocaleString()}/hr)
        </span>
      </div>
      <div>🌾 {Math.floor(displayedResources.food).toLocaleString() || 0}
        <span style={{ color: "#0f0", marginLeft: "6px"}}>
          (+{resources.food_per_hour.toLocaleString()}/hr)
        </span>
      </div>
      <div>🛢 {Math.floor(displayedResources.oil).toLocaleString() || 0}
        <span style={{ color: "#0f0", marginLeft: "6px"}}>
          (+{resources.oil_per_hour.toLocaleString()}/hr)
        </span>
      </div>
      <div>🔬 {Math.floor(displayedResources.tech).toLocaleString() || 0}
        <span style={{ color: "#0f0", marginLeft: "6px"}}>
          (+{resources.tech_per_hour.toLocaleString()}/hr)
        </span>
      </div>
    </div>
  );
}