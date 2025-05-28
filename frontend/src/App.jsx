import { BrowserRouter, Routes, Route } from "react-router-dom";
import SignWrapper from "./components/SignWrapper/SignWrapper";
import SignIn from "./pages/SignIn";
import SignUp from "./pages/SingUp";
import './App.css'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/signup" element={<SignUp />} />
        <Route path="/signin" element={<SignIn />} />
        {/* Add more routes as needed */}
      </Routes>
    </BrowserRouter>
  );
}



