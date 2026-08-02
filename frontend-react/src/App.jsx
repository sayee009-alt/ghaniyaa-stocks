import { Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Screener from "./pages/Screener";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/screener" element={<Screener />} />
    </Routes>
  );
}

export default App;