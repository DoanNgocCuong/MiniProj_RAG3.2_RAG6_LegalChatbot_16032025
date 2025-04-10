// 2.50.0
import { useEffect, useState } from "react";
import NavBar from "./components/NavBar";
import HomePage from "./pages/HomePage";
import ChatBot from "./components/ChatBot";
import FAQPage from "./pages/FAQPage"
import IssuePage from "./pages/IssuePage";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
// import ImgGen from "./components/ImgGen";
import ScaleLoader from "react-spinners/ScaleLoader";
// import { decode as atob, encode as btoa } from "js-base64";
// import { themeChange } from 'theme-change'
import { AuthProvider } from './contexts/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import Login from "./pages/Login"

function App() {
  useEffect(() => {}, []);
  const [currentPage, SetCurrentPage] = useState("Home");
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="overflow-hidden">
          <NavBar />
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<HomePage />} />
            <Route 
              path="/chat" 
              element={
                <ProtectedRoute>
                  <ChatBot />
                </ProtectedRoute>
              } 
            />
            <Route path="/faq" element={<FAQPage />} />
            <Route path="/issue" element={<IssuePage />} />
          </Routes>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
