import { useLocation,useNavigate,Link } from 'react-router-dom';
import schoolLogo from '../assets/school.jpg';
import { useState, useEffect } from 'react';

function NavBar() {
  const navigate = useNavigate ();
  const location = useLocation();
  const [theme, setTheme] = useState('winter'); // Default light theme
  
  // Function to toggle theme
  const toggleTheme = () => {
    const newTheme = theme === 'winter' ? 'dark' : 'winter';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
  };
  
  // Initialize theme from localStorage on component mount
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'winter';
    setTheme(savedTheme);
    document.documentElement.setAttribute('data-theme', savedTheme);
  }, []);
  
  return (
    <div className="navbar bg-base-100 w-[95%] ">
      <div className="navbar-start">
        <div className="dropdown">
          <label tabIndex={0} className="btn btn-ghost lg:hidden">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M4 6h16M4 12h8m-8 6h16"
              />
            </svg>
          </label>
          <ul
            tabIndex={0}
            className="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52"
          >
            <li>
              <Link to="/">
                <a>Trang chủ</a>
              </Link>
            </li>
            <li>
              <Link to="/chat">
                <a>Trò chuyện</a>
              </Link>
            </li>
            <li>
              <Link to="/faq">
              <a>FAQs</a>
              </Link>
            </li>
            <li>
              <Link to="/issue">
              <a>Báo lỗi/ Góp ý</a>
              </Link>
            </li>
          </ul>
        </div>
        <a  onClick={()=>navigate("/")}  className="btn btn-ghost normal-case font-extrabold text-xl bg-[linear-gradient(90deg,hsl(var(--s))_0%,hsl(var(--sf))_9%,hsl(var(--pf))_42%,hsl(var(--p))_47%,hsl(var(--a))_100%)] bg-clip-text will-change-auto [-webkit-text-fill-color:transparent] [transform:translate3d(0,0,0)] motion-reduce:!tracking-normal max-[1280px]:!tracking-normal [@supports(color:oklch(0_0_0))]:bg-[linear-gradient(90deg,hsl(var(--s))_4%,color-mix(in_oklch,hsl(var(--sf)),hsl(var(--pf)))_22%,hsl(var(--p))_45%,color-mix(in_oklch,hsl(var(--p)),hsl(var(--a)))_67%,hsl(var(--a))_100.2%)]">
RAG Chatbot
        </a>
      </div>
      <div className="navbar-center hidden lg:flex">
        <ul className="menu menu-horizontal px-1 font-semibold ">
          <li className='p-1'>
              <button onClick={()=>navigate("/")} className={location.pathname=="/"?"btn btn-outline btn-primary":""}>Trang chủ</button>
          </li>
          <li className='p-1'>
              <button onClick={()=>navigate("/chat")} className={location.pathname=="/chat"?"btn btn-outline btn-primary":""}>Trò chuyện</button>
          </li>
          <li className='p-1'>
              <button onClick={()=>navigate("/faq")} className={location.pathname=="/faq"?"btn btn-outline btn-primary":""}>FAQs</button>
          </li>
          <li className='p-1'>
              <button onClick={()=>navigate("/issue")} className={location.pathname=="/issue"?"btn btn-outline btn-primary":""}>Báo lỗi/ Góp ý</button>
          </li>
        </ul>
      </div>
      <div className="navbar-end flex items-center gap-3">
        {/* Theme toggle button */}
        <button 
          onClick={toggleTheme} 
          className="btn btn-circle btn-sm"
          aria-label="Toggle theme"
        >
          {theme === 'winter' ? (
            // Moon icon for dark mode
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          ) : (
            // Sun icon for light mode
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          )}
        </button>
        
        {/* School logo */}
        <img 
          src={schoolLogo} 
          alt="School Logo" 
          className="w-12 h-12 rounded-full border-2 border-blue-500 shadow-md object-cover"
        />
      </div>
    </div>
  );
}
export default NavBar;
