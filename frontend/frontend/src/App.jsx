import {
  BrowserRouter,
  Routes,
  Route,
  Link
} from "react-router-dom";

import { useEffect, useState } from "react";
import client from "./api/client";

import OverviewPage from "./pages/OverviewPage";
import BuildingsPage from "./pages/BuildingsPage";
import MilitaryPage from "./pages/MilitaryPage";
import ResearchPage from "./pages/ResearchPage";
import MarketPage from "./pages/MarketPage";
import BattleReportsPage from "./pages/BattleReportsPage";
import ResourcePanel from "./components/ResourcePanel";


function App() {
  const CURRENT_NATION_ID =
    "37c939eb-8f0d-4d8f-b449-0fcb4cd0833e";

  const [selectedCity, setSelectedCity] =
    useState(null);

  const [resources, setResources] =
    useState(null);

  useEffect(() => {
    async function loadNation() {
      try {
        const cityRes = await client.get(
          `/cities/${CURRENT_NATION_ID}`
        );

        if (cityRes.data.length > 0) {
          setSelectedCity(cityRes.data[0]);
        }
      } catch (err) {
        console.error(err);
      }
    }

    loadNation();

  }, []);

  useEffect(() => {

    if (!selectedCity) return;

    fetchResources();

    const interval = setInterval(() => {
      fetchResources();
    }, 5000);

    return () => clearInterval(interval);

  }, [selectedCity]);

  async function fetchResources() {

    try {

      const res = await client.get(
        `/resources/${selectedCity.id}`
      );

      setResources(res.data);

    } catch (err) {

      console.error(err);

    }
  }

  return (
    <BrowserRouter>

      <div
        style={{
          minHeight: "100vh",
          backgroundColor: "#1a1a1a",
          color: "white"
        }}
      >

        <ResourcePanel
          resources={resources}
        />

        {/* NAVBAR */}
        <nav
          style={{
            display: "flex",
            gap: "20px",
            padding: "20px",
            borderBottom: "1px solid #444",
            backgroundColor: "#222"
          }}
        >

          <Link to="/">Overview</Link>

          <Link to="/buildings">
            Buildings
          </Link>

          <Link to="/military">
            Military
          </Link>

          <Link to="/research">
            Research
          </Link>

          <Link to="/market">
            Market
          </Link>

          <Link to="/reports">
            Battle Reports
          </Link>

        </nav>

        {/* PAGE CONTENT */}
        <div style={{ padding: "20px" }}>

          <Routes>

            <Route
              path="/"
              element={<OverviewPage />}
            />

            <Route
              path="/buildings"
              element={
                <BuildingsPage 
                  selectedCity={selectedCity}
                  setSelectedCity={
                    setSelectedCity
                  }
                />
              }
            />

            <Route
              path="/military"
              element={<MilitaryPage />}
            />

            <Route
              path="/research"
              element={<ResearchPage />}
            />

            <Route
              path="/market"
              element={<MarketPage />}
            />

            <Route
              path="/reports"
              element={<BattleReportsPage />}
            />

          </Routes>

        </div>
      </div>

    </BrowserRouter>
  );
}

export default App;