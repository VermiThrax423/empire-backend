import { useEffect, useState } from "react";
import client from "../api/client";
import BuildingPanel from "./BuildingPanel";

export default function CityCard({ city }) {
    const [buildings, setBuildings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [buildQueue, setBuildQueue] = useState([]);

    async function fetchBuildings(showLoading = false) {
      
      try {
            if (showLoading) {
              setLoading(true);
            }
            
            const res = await client.get(`/buildings/${city.id}`);
            console.log("Buildings loaded:", res.data);
            setBuildings(res.data);

            const queueRes = await client.get(
              `/build-queue/${city.id}`
            );

            setBuildQueue(queueRes.data);
        } catch (err) {
            console.error("Failed to load buildings:", err);
        } finally {
            if (showLoading) {
              setLoading(false);
            }
        }
    }

    useEffect(() => {
        fetchBuildings(true);

        const interval = setInterval(() => {
          fetchBuildings();
        }, 5000);

        return () => clearInterval(interval);
    }, [city.id]);    
    
    async function upgradeBuilding(building) {
        try {
            console.log("Upgrading:", building.type);

            await client.post(`/build/${building.city_id}`, null, {
                params: {
                    building_type: building.type,
                },
            });

            await fetchBuildings();
        } catch (err) {
            console.error("Upgrade failed:", err);
        }
    }

  
  return (
    <div
      style={{
        border: "1px solid gray",
        padding: "15px",
        marginBottom: "15px",
        borderRadius: "8px"
      }}
    >
      <h2>{city.name}</h2>

      <p>
        Coordinates: ({city.x}, {city.y})
      </p>

      <p>
        Nation ID: {city.nation_id}
      </p>

      {loading ? (
        <p>Loading buildings...</p>
      ) : (
        <BuildingPanel 
            buildings={buildings}
            buildQueue={buildQueue}
            onUpgrade={upgradeBuilding}
        />
      )}

      
    </div>
  );
}