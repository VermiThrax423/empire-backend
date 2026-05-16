import { useEffect, useState } from "react";
import client from "../api/client";

import CityCard from "../components/CityCard";
import ResourcePanel from "../components/ResourcePanel";

export default function BuildingsPage({selectedCity, setSelectedCity}) {

  const CURRENT_NATION_ID =
    "37c939eb-8f0d-4d8f-b449-0fcb4cd0833e";

  const [cities, setCities] = useState([]);

  // LOAD CITIES
  useEffect(() => {

    client.get(
      `/cities/${CURRENT_NATION_ID}`
    )
    .then(res => {

      setCities(res.data);

      if (res.data.length > 0) {
        setSelectedCity(res.data[0]);
      }

    })
    .catch(err => console.error(err));

  }, []);


  return (
    <div>

      <h1>Buildings</h1>

      {/* City Selector */}
      <div
        style={{
          marginTop: "20px",
          marginBottom: "20px"
        }}
      >

        {cities.map(city => (
          <button
            key={city.id}
            onClick={() =>
              setSelectedCity(city)
            }
            style={{
              marginRight: "10px",
              padding: "8px 14px",
              cursor: "pointer"
            }}
          >
            {city.name}
          </button>
        ))}

      </div>

      {/* Selected City */}
      {selectedCity && (
        <CityCard city={selectedCity} />
      )}

    </div>
  );
}