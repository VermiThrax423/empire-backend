import { useEffect, useState } from "react";
import client from "../api/client";

function App() {
  const [cities, setCities] = useState([]);

  useEffect(() => {
    client.get("/cities/94369303-dde1-48c8-8f6f-0c64a2408686")
      .then(res => {
        console.log(res.data);
        setCities(res.data);
      })
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h1>City Test</h1>

      <pre>
        {JSON.stringify(cities, null, 2)}
      </pre>
    </div>
  );
}

export default App;