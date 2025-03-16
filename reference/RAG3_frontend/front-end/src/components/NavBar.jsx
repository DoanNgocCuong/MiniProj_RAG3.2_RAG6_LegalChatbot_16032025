import { useLocation,useNavigate,Link } from 'react-router-dom';
function NavBar() {
  const navigate = useNavigate ();
  const location = useLocation();
  return (
    <div className="navbar bg-apple-white shadow-sm w-full px-4 md:px-8">
      <div className="navbar-start">
        <div className="dropdown">
          <label tabIndex={0} className="btn btn-ghost lg:hidden">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5 text-apple-black"
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
            className="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow-lg bg-apple-white rounded-xl w-52"
          >
            <li>
              <Link to="/" className="text-apple-black font-medium py-2">
                Trang chủ
              </Link>
            </li>
            <li>
              <Link to="/chat" className="text-apple-black font-medium py-2">
                Trò chuyện
              </Link>
            </li>
            <li>
              <Link to="/faq" className="text-apple-black font-medium py-2">
                FAQs
              </Link>
            </li>
            <li>
              <Link to="/issue" className="text-apple-black font-medium py-2">
                Báo lỗi/ Góp ý
              </Link>
            </li>
          </ul>
        </div>
        <a onClick={()=>navigate("/")} className="btn btn-ghost normal-case font-bold text-xl text-apple-blue">
          Naval Technical College Chatbot
        </a>
      </div>
      <div className="navbar-center hidden lg:flex">
        <ul className="menu menu-horizontal px-1 font-medium">
          <li className='p-1'>
            <button 
              onClick={()=>navigate("/")} 
              className={location.pathname=="/"
                ? "px-4 py-2 text-apple-blue border-b-2 border-apple-blue"
                : "px-4 py-2 text-apple-black hover:text-apple-blue transition-colors"
              }
            >
              Trang chủ
            </button>
          </li>
          <li className='p-1'>
            <button 
              onClick={()=>navigate("/chat")} 
              className={location.pathname=="/chat"
                ? "px-4 py-2 text-apple-blue border-b-2 border-apple-blue"
                : "px-4 py-2 text-apple-black hover:text-apple-blue transition-colors"
              }
            >
              Trò chuyện
            </button>
          </li>
          <li className='p-1'>
            <button 
              onClick={()=>navigate("/faq")} 
              className={location.pathname=="/faq"
                ? "px-4 py-2 text-apple-blue border-b-2 border-apple-blue"
                : "px-4 py-2 text-apple-black hover:text-apple-blue transition-colors"
              }
            >
              FAQs
            </button>
          </li>
          <li className='p-1'>
            <button 
              onClick={()=>navigate("/issue")} 
              className={location.pathname=="/issue"
                ? "px-4 py-2 text-apple-blue border-b-2 border-apple-blue"
                : "px-4 py-2 text-apple-black hover:text-apple-blue transition-colors"
              }
            >
              Báo lỗi/ Góp ý
            </button>
          </li>
        </ul>
      </div>
      <div className="navbar-end">
        {/* <a className="btn btn-outline btn-primary md:flex hidden">
            Đăng nhập
          </a> */}
      </div>
    </div>
  );
}
export default NavBar;
