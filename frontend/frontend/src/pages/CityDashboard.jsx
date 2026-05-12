import { useEffect, useState } from "react";
import client from "../api/client";

function App() {
  const [cities, setCities] = useState([]);

  useEffect(() => {
    client.get("/cities/37c939eb-8f0d-4d8f-b449-0fcb4cd0833e")
      .then(res => {
        console.log(res.data);
        setCities(res.data);
      })
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h1>City Test</h1>

      {cities.map(city => (
        <div key={city.id}>
            <h3>City Name: {city.name}</h3>

            <p>
            Coordinates: ({city.x}, {city.y})
            </p>

            <p>
            Nation ID: {city.nation_id}
            </p>
        </div>
        ))}
    </div>
  );
}

export default App;