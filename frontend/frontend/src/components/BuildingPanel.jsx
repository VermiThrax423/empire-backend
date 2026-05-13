import client from "../api/client";
import { useEffect, useState } from "react";

export default function BuildingPanel({ buildings = [], buildQueue = [], onUpgrade }) {
  const [now, setNow] = useState(Date.now());

  useEffect(() => {

    const interval = setInterval(() => {
      setNow(Date.now());
    }, 1000);

    return () => clearInterval(interval);

  }, []);

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

  function getRemainingSeconds(completesAt) {

    const diff =
      new Date(completesAt).getTime()
      - now;

    if (diff <= 0) {
      return 0;
    }

    return Math.ceil(diff / 1000);
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

      {buildings.map((building) => {

        const activeUpgrade = buildQueue.find(
          queueItem =>
            queueItem.building_type === building.type
        );

        const remaining = activeUpgrade
          ? getRemainingSeconds(activeUpgrade.completes_at)
          : null;

        return (
          <div
            key={building.id}
            style={{
              display: "flex",
              justifyContent: "space-between",
              marginBottom: "10px"
            }}
          >
            <div>
              <div>
                {building.type} — Level {building.level}
              </div>

              {remaining > 0 && (
                <div style={{ color: "orange" }}>
                  Upgrading to Level {activeUpgrade.target_level}

                  ({remaining}s remaining)
                </div>
              )}
            </div>

            <button
              disabled={remaining > 0}
              onClick={() => onUpgrade(building)}
            >
              {remaining > 0
                ? "Upgrading..."
                : "Upgrade"}
            </button>
          </div>
        );
      })}
    </div>
  );
}