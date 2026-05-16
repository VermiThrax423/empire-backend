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

      const finishedBuild = buildQueue.some(queueItem =>
        getRemainingSeconds(
          queueItem.completes_at
        ) <= 0
      );

      if (finishedBuild) {
        fetchBuildings();
        fetchBuildQueue();
      }

    }, 1000);

    return () => clearInterval(interval);

  }, [buildQueue]);

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
    const completeTime = new Date(completesAt + "Z");

    const diff = completeTime.getTime() - now;

    return Math.max(
      0, Math.floor(diff / 1000)
    );
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