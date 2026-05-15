import client from "../api/client";
import { useEffect, useState } from "react";
import BuildingCard from "./BuildingCard";

export default function BuildingPanel({ buildings = [], buildingConfig, buildQueue = [], onUpgrade }) {
  const [now, setNow] = useState(Date.now());

  const mergedBuildings = buildingConfig
    ? Object.keys(buildingConfig).map(type => {

        const existing = buildings.find(
          b => b.type === type
        );

        return {
          type,
          level: existing ? existing.level : 0,
          config: buildingConfig[type]
        };
      })
    : [];
  
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
        console.log(building);
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

      {mergedBuildings.map((building) => {

        const activeUpgrade = buildQueue.find(
          queueItem =>
            queueItem.building_type === building.type
        );

        const remaining = activeUpgrade
          ? getRemainingSeconds(activeUpgrade.completes_at)
          : null;

        return (
          <BuildingCard
            key={building.type}

            building={building}

            activeUpgrade={activeUpgrade}

            remaining={remaining}

            onUpgrade={onUpgrade}
          />
        );
      })}                                 
    </div>
  );
}