import robot_img from "../assets/robot_image.png";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";

function HomePage() {
  const [isDarkMode, setIsDarkMode] = useState(
    document.documentElement.getAttribute('data-theme') === 'dark'
  );
  
  // Listen for theme changes
  useEffect(() => {
    const checkTheme = () => {
      setIsDarkMode(document.documentElement.getAttribute('data-theme') === 'dark');
    };
    
    // Check on mount
    checkTheme();
    
    // Set up observer to detect theme attribute changes
    const observer = new MutationObserver(mutations => {
      mutations.forEach(mutation => {
        if (mutation.attributeName === 'data-theme') {
          checkTheme();
        }
      });
    });
    
    observer.observe(document.documentElement, { attributes: true });
    
    return () => observer.disconnect();
  }, []);

  return (
    <div className={`flex items-center justify-center hero h-[85vh] w-full ${
      isDarkMode 
        ? 'bg-gradient-to-r from-gray-900 to-blue-900' 
        : 'bg-gradient-to-r from-teal-100 to-blue-100'
    }`}>
      <div className="hero-content text-center min-w-[200px] ">
        <div className="max-w-md flex-1">
          <img
            className={`block w-[200px] h-auto mx-auto ${isDarkMode ? 'drop-shadow-[0_0_15px_rgba(59,130,246,0.5)]' : ''}`}
            src={robot_img}
          ></img>
          <h1 className={`text-2xl lg:text-5xl font-bold ${
            isDarkMode 
              ? 'text-white' 
              : '[&::selection]:text-base-content brightness-100 contrast-150 [&::selection]:bg-blue-950'
          }`}>Xin chào! Mình là</h1>
          <h1 className="text-3xl lg:text-5xl font-bold bg-[linear-gradient(90deg,hsl(var(--s))_0%,hsl(var(--sf))_9%,hsl(var(--pf))_42%,hsl(var(--p))_47%,hsl(var(--a))_100%)] bg-clip-text will-change-auto [-webkit-text-fill-color:transparent] [transform:translate3d(0,0,0)] motion-reduce:!tracking-normal max-[1280px]:!tracking-normal [@supports(color:oklch(0_0_0))]:bg-[linear-gradient(90deg,hsl(var(--s))_4%,color-mix(in_oklch,hsl(var(--sf)),hsl(var(--pf)))_22%,hsl(var(--p))_45%,color-mix(in_oklch,hsl(var(--p)),hsl(var(--a)))_67%,hsl(var(--a))_100.2%)]">
            RAG Chatbot
          </h1>
          <p className={`py-6 font-semibold lg:text-lg text-sm ${isDarkMode ? 'text-gray-300' : ''}`}>
            Giúp bạn giải đáp thắc mắc, tra cứu thông tin một cách nhanh chóng
            và chính xác nhất!
          </p>
          <Link to="/chat">
            <button className={`btn ${isDarkMode ? 'btn-primary' : 'btn-info'}`}>Bắt đầu ngay</button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
