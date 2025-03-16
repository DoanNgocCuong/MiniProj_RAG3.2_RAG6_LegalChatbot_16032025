// import avatar from "../assets/avatar.jpg";
import robot_img from "../assets/robot_image.png";
import { useState, useRef, useEffect } from "react";
import ScaleLoader from "react-spinners/ScaleLoader";
import { TypeAnimation } from "react-type-animation";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMessage } from "@fortawesome/free-regular-svg-icons";
function ChatBot(props) {
  const messagesEndRef = useRef(null);
  const [timeOfRequest, SetTimeOfRequest] = useState(0);
  let [promptInput, SetPromptInput] = useState("");
  let [sourceData, SetSourceData] = useState("RAG");
  let [chatHistory, SetChatHistory] = useState([]);

  const commonQuestions=[
    "Trình bày khái niệm, chế độ pháp lý vùng nội thủy theo UNCLOS 1982?",
    "Trình bày khái niệm, chế độ pháp lý vùng Lãnh hải theo UNCLOS 1982?", 
    "Trình bày khái niệm, chế độ pháp lý vùng Đặc quyền kinh tế theo UNCLOS 1982?",
    "Trình bày khái niệm, chế độ pháp lý Thềm lục địa theo UNCLOS 1982?",
    "Trình bày quy định về thềm lục địa mở rộng theo UNCLOS1982?",
    "Trình bày khái niệm, chế độ pháp lý biển theo UNCLOS 1982?",
    "Trình bày Quyền hạn và nghĩa vụ của nước trung lập theo Luật chiến tranh trên biển?",
    "Liên hệ vùng nội thủy theo luật biển Việt Nam?",
    "Liên hệ vùng Lãnh hải theo luật biển Việt Nam?", 
    "Liên hệ vùng ĐQKT theo luật biển Việt Nam?",
    "Liên hệ Thềm lục địa theo luật biển Việt Nam?",
    "Việc tranh chấp thềm lục địa mở rộng được quy định như thế nào?",
  ]
  let [isLoading, SetIsLoad] = useState(false);
  let [isGen, SetIsGen] = useState(false);
  const [dataChat, SetDataChat] = useState([
    [
      "start",
      [
        "Xin chào! Đây là Naval Technical College Chatbot, trợ lý đắc lực dành cho bạn! Bạn muốn tìm kiếm thông tin về những gì? Đừng quên chọn nguồn tham khảo phù hợp để mình có thể giúp bạn tìm kiếm thông tin chính xác nhất nha. 😄",
        null,
      ],
    ],
  ]);
  useEffect(() => {
    ScrollToEndChat();
  }, [isLoading]);
  useEffect(() => {
    const interval = setInterval(() => {
      SetTimeOfRequest((timeOfRequest) => timeOfRequest + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  function ScrollToEndChat() {
    messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
  }
  const onChangeHandler = (event) => {
    SetPromptInput(event.target.value);
  };

  async function SendMessageChat() {
    if (promptInput !== "" && isLoading === false) {
      SetTimeOfRequest(0);
      SetIsGen(true), SetPromptInput("");
      SetIsLoad(true);
      SetDataChat((prev) => [...prev, ["end", [promptInput, sourceData]]]);
      SetChatHistory((prev) => [promptInput, ...prev]);

      // fetch("https://toad-vast-civet.ngrok-free.app/rag/" + sourceData + "?q=" + promptInput,
      // Cuong thay base crul mới
      fetch("https://briefly-knowing-treefrog.ngrok-free.app/rag/" + sourceData + "?q=" + promptInput,
      {
        method: "get",
        headers: new Headers({
          "ngrok-skip-browser-warning": "69420",
        }),
      })
        .then((response) => response.json())
        .then((result) => {
          SetDataChat((prev) => [
            ...prev,
            ["start", [result.result, result.source_documents, sourceData]],
          ]);
          SetIsLoad(false);
        })
        .catch((error) => {
          SetDataChat((prev) => [
            ...prev,
            ["start", ["Lỗi, không thể kết nối với server", null]],
          ]);
          SetIsLoad(false);
        });
    }
  }

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      SendMessageChat();
    }
  };
  let [reference, SetReference] = useState({
    title: "",
    source: "",
    url: "",
    text: ``,
  });
  const handleReferenceClick = (sources, sourceType) => {
    SetReference({
      title:
        sourceType == "wiki"
          ? sources.metadata.title
          : sources.metadata.page==undefined? "Sổ tay sinh viên 2023" : "Trang " + sources.metadata.page + " (sổ tay SV)",
      source: sourceType == "wiki" ? "Wikipedia" : "Trường Cao Đẳng Kỹ thuật Hải Quân",
      url:
        sourceType == "wiki"
          ? sources.metadata.source
          : "https://ctsv.ntt.edu.vn/sinh-vien-can-biet/",
      text:
        sourceType == "wiki" ? sources.metadata.summary : sources.page_content,
    });
  };
  return (
    <div className="bg-apple-lightgray h-[85vh]">
      <div className="hidden lg:block drawer-side absolute w-64 h-[20vh] left-3 mt-2">
        <div className="menu p-4 w-full min-h-full bg-white text-base-content rounded-2xl mt-3 overflow-auto scroll-y-auto max-h-[80vh] shadow-sm">
          {/* Sidebar content here */}
          <ul className="menu text-sm">
            <h2 className="font-bold mb-4 text-apple-blue">
              Lịch sử trò chuyện
            </h2>
            {chatHistory.length == 0 ? (
              <p className="text-sm text-apple-gray">
                Hiện chưa có cuộc hội thoại nào
              </p>
            ) : (
              ""
            )}
            {chatHistory.map((mess, i) => (
              <li key={i}>
                <p className="py-2 text-apple-black hover:text-apple-blue transition-colors">
                  <FontAwesomeIcon icon={faMessage} className="mr-2" />
                  {mess.length < 20 ? mess : mess.slice(0, 20) + "..."}
                </p>
              </li>
            ))}
          </ul>
        </div>
      </div>
      
      <div className="hidden lg:block drawer-side absolute w-64 h-[20vh] mt-2 right-3">
        <div className="menu p-4 w-full min-h-full bg-white text-base-content rounded-2xl mt-3 shadow-sm">
          {/* Sidebar content here */}
          <h2 className="font-bold text-sm mb-4 text-apple-blue">
            Nguồn tham khảo
          </h2>
          <ul className="menu">
            <li>
              <label className="label cursor-pointer">
                <span className="label-text font-medium text-apple-black">
                  Bách khoa toàn thư Wikipedia
                </span>
                <input
                  type="radio"
                  name="radio-10"
                  value={"wiki"}
                  checked={sourceData === "wiki"}
                  onChange={(e) => {
                    SetSourceData(e.target.value);
                  }}
                  className="radio checked:bg-apple-blue"
                />
              </label>
            </li>
            <li>
              <label className="label cursor-pointer">
                <span className="label-text font-medium text-apple-black">
                  Trường Cao Đẳng Kỹ thuật Hải Quân
                </span>
                <input
                  value={"RAG"}
                  type="radio"
                  checked={sourceData === "RAG"}
                  onChange={(e) => {
                    SetSourceData(e.target.value);
                  }}
                  name="radio-10"
                  className="radio checked:bg-apple-blue"
                />
              </label>
            </li>
          </ul>
        </div>
        
        <div
          className="menu p-4 w-full min-h-full bg-white text-base-content 
          rounded-2xl mt-3 overflow-auto scroll-y-auto max-h-[43vh]
          scrollbar-thin scrollbar-thumb-apple-gray 
          scrollbar-thumb-rounded-full scrollbar-track-rounded-full shadow-sm"
        >
          {/* Sidebar content here */}
          <ul className="menu text-sm">
            <h2 className="font-bold mb-4 text-apple-blue">
              Những câu hỏi phổ biến
            </h2>

            {commonQuestions.map((mess, i) => (
              <li key={i} onClick={() => SetPromptInput(mess)}>
                <p className="max-w-64 py-2 text-apple-black hover:text-apple-blue transition-colors">
                  <FontAwesomeIcon icon={faMessage} className="mr-2" />
                  {mess}
                </p>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className={"flex justify-center h-[80vh]"}>
        {/* Modal */}
        <input type="checkbox" id="my_modal_6" className="modal-toggle" />
        <div className="modal">
          <div className="modal-box bg-white rounded-2xl shadow-lg">
            <h3 className="font-bold text-lg text-apple-black">{reference.title}</h3>
            <p className="font-normal text-sm text-apple-gray">Nguồn: {reference.source}</p>
            <p className="py-4 text-sm text-apple-black">
              {reference.text.slice(0, 700) + "..."}
            </p>
            <p className="text-apple-blue truncate">
              <a href={reference.url} target="_blank">
                {reference.url}
              </a>
            </p>
            <div className="modal-action">
              <label htmlFor="my_modal_6" className="btn bg-apple-blue text-white border-none rounded-full px-6">
                ĐÓNG
              </label>
            </div>
          </div>
        </div>

        <div
          id="chat-area"
          className="
          mt-5 text-sm 
          scrollbar-thin scrollbar-thumb-apple-gray bg-white  
          scrollbar-thumb-rounded-full scrollbar-track-rounded-full
          rounded-3xl shadow-md md:w-[50%] md:p-3 p-1 w-full overflow-auto scroll-y-auto h-[80%]"
        >
          {dataChat.map((dataMessages, i) =>
            dataMessages[0] === "start" ? (
              <div className="chat chat-start" key={i}>
                <div className="chat-image avatar">
                  <div className="w-10 rounded-full border-2 border-apple-blue">
                    <img className="scale-150" src={robot_img} />
                  </div>
                </div>
                <div className="chat-bubble bg-apple-lightgray text-apple-black break-words shadow-sm">
                  <TypeAnimation
                    style={{ whiteSpace: 'pre-line' }} 
                    sequence={[
                      dataMessages[1][0],
                      () => SetIsGen(false),
                    ]}
                    cursor={false}
                    speed={100}
                  />
                  {dataMessages[1][1] === null ||
                  dataMessages[1][1].length == 0 ? (
                    ""
                  ) : (
                    <>
                      <div className="divider m-0"></div>
                      <p className="font-semibold text-xs">
                        Tham khảo:{" "}
                        {dataMessages[1][1].map((source, j) => (
                          <label
                            htmlFor="my_modal_6"
                            className="inline-block px-2 py-1 mr-1 bg-apple-blue text-white text-xs rounded-full hover:bg-apple-darkblue cursor-pointer transition-colors"
                            onClick={() =>
                              handleReferenceClick(source, dataMessages[1][2])
                            }
                            key={j}
                          >
                            {dataMessages[1][2] == "wiki"
                              ? source.metadata.title
                              : source.metadata.page==undefined? "Sổ tay sinh viên 2023" : "Trang " +
                                source.metadata.page +
                                " (sổ tay SV)"}
                          </label>
                        ))}
                      </p>
                    </>
                  )}
                </div>
              </div>
            ) : (
              <div className="chat chat-end">
                <div className="chat-bubble bg-apple-blue text-white shadow-sm">
                  {dataMessages[1][0]}
                  <>
                    <div className="divider m-0"></div>
                    <p className="font-light text-xs text-white opacity-80">
                      Tham khảo:{" "}
                      {dataMessages[1][1] == "wiki" ? "Wikipedia" : "RAG"}
                    </p>
                  </>
                </div>
              </div>
            )
          )}
          {isLoading ? (
            <div className="chat chat-start">
              <div className="chat-image avatar">
                <div className="w-10 rounded-full border-2 border-apple-blue">
                  <img src={robot_img} />
                </div>
              </div>
              <div className="chat-bubble bg-apple-lightgray text-apple-black">
                <ScaleLoader
                  color="#0071e3"
                  loading={true}
                  height={10}
                  width={10}
                  aria-label="Loading Spinner"
                  data-testid="loader"
                />
                <p className="text-xs font-medium text-apple-gray">{timeOfRequest + "/60s"}</p>
              </div>
            </div>
          ) : (
            ""
          )}
          <div ref={messagesEndRef} />
          <div className="absolute bottom-[0.2rem] md:w-[50%] grid">
            <input
              type="text"
              placeholder="Nhập câu hỏi tại đây..."
              className="mr-1 shadow-sm border border-gray-200 focus:outline-none focus:border-apple-blue px-4 py-3 rounded-full input-primary col-start-1 md:col-end-12 col-end-11"
              onChange={onChangeHandler}
              onKeyDown={handleKeyDown}
              disabled={isGen}
              value={promptInput}
            />

            <button
              disabled={isGen}
              onClick={() => SendMessageChat()}
              className={
                "shadow-sm md:col-start-12 rounded-full col-start-11 col-end-12 md:col-end-13 btn bg-apple-blue hover:bg-apple-darkblue text-white border-none"
              }
            >
              <svg
                stroke="currentColor"
                fill="none"
                strokeWidth="2"
                viewBox="0 0 24 24"
                color="white"
                height="15px"
                width="15px"
                xmlns="http://www.w3.org/2000/svg"
              >
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
            <p className="text-xs col-start-1 col-end-12 text-justify p-1 text-apple-gray">
              <b>Lưu ý: </b>Mô hình có thể đưa ra câu trả lời không chính xác ở
              một số trường hợp, vì vậy hãy luôn kiểm chứng thông tin bạn nhé!
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
export default ChatBot;
