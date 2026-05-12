export default function PopulationPanel({ city }) {
  return (
    <div>
      <h3>Population</h3>
      <p>{city.population}</p>
    </div>
  );
}