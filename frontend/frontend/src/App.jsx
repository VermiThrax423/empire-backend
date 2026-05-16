import {
  BrowserRouter,
  Routes,
  Route,
  Link
} from "react-router-dom";

import OverviewPage from "./pages/OverviewPage";
import BuildingsPage from "./pages/BuildingsPage";
import MilitaryPage from "./pages/MilitaryPage";
import ResearchPage from "./pages/ResearchPage";
import MarketPage from "./pages/MarketPage";
import BattleReportsPage from "./pages/BattleReportsPage";

function App() {
  return (
    <BrowserRouter>

      <div
        style={{
          minHeight: "100vh",
          backgroundColor: "#1a1a1a",
          color: "white"
        }}
      >

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
              element={<BuildingsPage />}
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