import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import client from './api/client'
import CityDashboard from "./pages/CityDashboard";

function App() {
  return <CityDashboard />;
}


export default App;
