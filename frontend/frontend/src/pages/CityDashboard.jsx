import { useEffect, useState } from "react";
import client from "../api/client";
import CityCard from "../components/CityCard";
import ResourcePanel from "../components/ResourcePanel";

function App() {
  const CURRENT_NATION_ID =
  "37c939eb-8f0d-4d8f-b449-0fcb4cd0833e";
  const [cities, setCities] = useState([]);

  useEffect(() => {
    client.get(`/cities/${CURRENT_NATION_ID}`)
      .then(res => {
        console.log(res.data);
        setCities(res.data);
      })
      .catch(err => console.error(err));
  }, []);

  return (
    <div
      style={{
          border: "2px solid #444",
          backgroundColor: "#222",
          color: "white",
          padding: "15px",
          marginBottom: "15px",
          borderRadius: "8px"
        }}
    >
      <ResourcePanel />

      <h1>City Test</h1>

      {cities.map(city => (
        <CityCard
          key={city.id}
          city={city}
        />
      ))}

    </div>
  );
}

export default App;