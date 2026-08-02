import Dashboard from "./pages/Dashboard";
import { getLiveStock } from "./services/api";

function App() {

  getLiveStock("TCS").then(console.log);

  return <Dashboard />;
}

export default App;