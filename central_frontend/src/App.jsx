import { Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import Creator from "./components/Creator";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/creator" element={<Creator />} />
      </Routes>
    </>
  );
}

export default App;
