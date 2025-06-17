import { BrowserRouter, Routes, Route } from "react-router";
import Welcome from "./pages/Welcome";
function App() {

  return (
    <>
     <BrowserRouter>
     <Routes>
      <Route path="/" element={<Welcome />} />
     </Routes>
     </BrowserRouter>
    </>
  )
}

export default App
