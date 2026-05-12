export default function ResourcePanel({ city }) {
  return (
    <div>
      <h3>Resources</h3>
      <ul>
        <li>Money: {city.money}</li>
        <li>Oil: {city.oil}</li>
        <li>Tech: {city.tech}</li>
        <li>Food: {city.food}</li>
      </ul>
    </div>
  );
}