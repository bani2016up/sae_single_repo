import { BrowserRouter, Routes, Route } from "react-router-dom";
import Editor from "./pages/Editor"
import SignIn from "./pages/SignIn";
import SignUp from "./pages/SingUp";
import './App.css'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SignUp />} />
        <Route path="/editor" element={<Editor />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/signin" element={<SignIn />} />
      </Routes>
    </BrowserRouter>
  );
}



