import robot_img from "../assets/robot_image.png";
import { Link } from "react-router-dom";

function HomePage() {
  return (
    <div className="flex items-center justify-center hero h-[85vh] w-full bg-apple-lightgray">
      <div className="hero-content text-center min-w-[200px]">
        <div className="max-w-md flex-1">
          <img
            className="block w-[200px] h-auto mx-auto mb-8"
            src={robot_img}
            alt="Naval Technical College Chatbot"
          />
          <h1 className="text-2xl lg:text-4xl font-medium text-apple-black mb-2">Xin chào! Mình là</h1>
          <h1 className="text-3xl lg:text-5xl font-bold text-apple-blue mb-6">
            Naval Technical College Chatbot
          </h1>
          <p className="py-6 text-apple-gray lg:text-lg text-sm max-w-sm mx-auto">
            Giúp bạn giải đáp thắc mắc, tra cứu thông tin một cách nhanh chóng
            và chính xác nhất!
          </p>
          <Link to="/chat">
            <button className="btn bg-apple-blue hover:bg-apple-darkblue text-white border-none rounded-full px-8 py-3 font-medium shadow-md transition-all">
              Bắt đầu ngay
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
