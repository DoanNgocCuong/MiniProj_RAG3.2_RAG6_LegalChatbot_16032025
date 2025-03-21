// import avatar from "../assets/avatar.jpg";
import robot_img from "../assets/robot_image.png";
import { useState, useRef, useEffect } from "react";
import ScaleLoader from "react-spinners/ScaleLoader";
import { TypeAnimation } from "react-type-animation";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMessage } from "@fortawesome/free-regular-svg-icons";
import logger from '../utils/logger'

function ChatBot(props) {
  const messagesEndRef = useRef(null);
  const [timeOfRequest, SetTimeOfRequest] = useState(0);
  let [promptInput, SetPromptInput] = useState("");
  let [sourceData, SetSourceData] = useState("RAG");
  let [chatHistory, SetChatHistory] = useState([]);
  let [isLoading, SetIsLoad] = useState(false);
  let [isGen, SetIsGen] = useState(false);
  const [dataChat, SetDataChat] = useState([
    [
      "start",
      [
        "Xin chào! Đây là Trợ lý truy vấn thông tin Luật biển và Quy tắc tránh va quốc tế! Bạn muốn tìm kiếm thông tin về những gì, để mình giúp bạn tìm kiếm thông tin chính xác nhất nha. 😄",
        null,
      ],
    ],
  ]);
  const [isDarkMode, setIsDarkMode] = useState(
    document.documentElement.getAttribute('data-theme') === 'dark'
  );
  const [chatSessions, setChatSessions] = useState([
    { id: 'current', title: 'Cuộc trò chuyện hiện tại', messages: [] },
    { id: 'past1', title: 'Luật biển quốc tế', messages: [] },
    { id: 'past2', title: 'Quy định vùng đặc quyền kinh tế', messages: [] },
  ]);
  const [activeChatId, setActiveChatId] = useState('current');

  const commonQuestions = [
    "Trình bày khái niệm, chế độ pháp lý vùng nội thủy theo UNCLOS 1982? Liên hệ vùng nội thủy theo luật biển Việt Nam?",
    "Trình bày những quy định cấm trong vùng đặc quyền kinh tế, thềm lục địa và quyền truy đuổi tàu thuyền nước ngoài theo luật biển Việt Nam?",
    "Trình bày khái niệm, chế độ pháp lý biển theo UNCLOS 1982?",
  ];

  //  Sử dụng: isLoading để: Tự động cuộn xuống dưới khi có tin nhắn mới: ?
  useEffect(() => {
    ScrollToEndChat();
  }, [dataChat, isLoading]);
  useEffect(() => {
    const interval = setInterval(() => {
      SetTimeOfRequest((timeOfRequest) => timeOfRequest + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const checkTheme = () => {
      setIsDarkMode(document.documentElement.getAttribute('data-theme') === 'dark');
    };
    
    checkTheme();
    
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

  function ScrollToEndChat() {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
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

      logger.debug('Sending chat message', { prompt: promptInput, source: sourceData })
      logger.apiRequest('/api/v1/chat/completions', 'POST')

      // Updated API call to use the new backend
      fetch("/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          messages: [
            {"role": "user", "content": `[Nguồn: ${sourceData}] ${promptInput}`}
          ],
          model: "gpt-4o"
        })
      })
        .then((response) => {
          logger.apiResponse('/api/v1/chat/completions', response.status)
          return response.json()
        })
        .then((result) => {
          // Extract the response content from the OpenAI-compatible format
          const responseContent = result.choices[0].message.content;
          logger.debug('Received chat response', { responseLength: responseContent.length })
          
          // Parse source documents if available (assuming they might be in the response)
          let sourceDocuments = null;
          try {
            // Look for source documents in the response
            const sourceMatch = responseContent.match(/\(Nguồn: (.*?)\)/);
            if (sourceMatch) {
              sourceDocuments = [{
                metadata: {
                  page: sourceMatch[1].includes("trang") ? 
                    sourceMatch[1].replace(/[^0-9]/g, '') : undefined,
                  title: sourceMatch[1].includes("trang") ? 
                    "Sổ tay sinh viên 2023" : sourceMatch[1]
                },
                page_content: responseContent
              }];
            }
          } catch (e) {
            console.error("Error parsing source documents:", e);
          }
          
          SetDataChat((prev) => [
            ...prev,
            ["start", [responseContent, sourceDocuments, sourceData]],
          ]);
          SetIsLoad(false);
        })
        .catch((error) => {
          logger.error("API Error:", error);
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
        sources.metadata.page==undefined ? "Sổ tay luật pháp" : "Trang " + sources.metadata.page + " (Luật)",
      source: "RAG Database",
      url: "https://example.com/legal-reference",
      text: sources.page_content,
    });
  };

  // Function to start new chat
  const startNewChat = () => {
    // Create new chat session
    const newSession = {
      id: 'chat_' + Date.now(),
      title: 'Cuộc trò chuyện mới',
      messages: []
    };
    
    // Add to beginning of chat sessions
    setChatSessions([newSession, ...chatSessions]);
    setActiveChatId(newSession.id);
    
    // Reset chat state
    SetDataChat([
      [
        "start",
        [
          "Xin chào! Đây là Trợ lý truy vấn thông tin Luật biển và Quy tắc tránh va quốc tế! Bạn muốn tìm kiếm thông tin về những gì?",
          null,
        ],
      ],
    ]);
    SetPromptInput("");
  };

  return (
    <div className={`flex justify-center min-h-[85vh] h-auto w-full ${isDarkMode ? 'bg-gradient-to-br from-gray-900 to-blue-900' : 'bg-gradient-to-br from-blue-100 to-indigo-200'}`}>
      <div className="w-full flex gap-0">
        <div className={`hidden md:block w-1/5 bg-base-100 shadow-xl rounded-lg p-3 ${isDarkMode ? 'text-gray-200' : ''}`}>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold">Lịch sử chat</h2>
            <button 
              onClick={startNewChat}
              className="btn btn-sm btn-circle btn-primary"
              title="Tạo cuộc trò chuyện mới"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
              </svg>
            </button>
          </div>
          
          <div className="space-y-2 max-h-[40vh] overflow-y-auto mb-4">
            {chatSessions.map(chat => (
              <div 
                key={chat.id}
                onClick={() => setActiveChatId(chat.id)}
                className={`p-2 rounded-md cursor-pointer flex items-center gap-2 ${
                  activeChatId === chat.id 
                    ? (isDarkMode ? 'bg-blue-900' : 'bg-blue-100') 
                    : (isDarkMode ? 'hover:bg-gray-800' : 'hover:bg-gray-100')
                }`}
              >
                <FontAwesomeIcon icon={faMessage} className="text-blue-500" />
                <div className="truncate">{chat.title}</div>
              </div>
            ))}
          </div>
          
          {/* Reference questions section */}
          <div className="mt-6">
            <h2 className="text-lg font-semibold mb-3">Câu hỏi tham khảo</h2>
            <div className="space-y-2 max-h-[30vh] overflow-y-auto">
              {commonQuestions.map((question, index) => (
                <div 
                  key={index}
                  onClick={() => {
                    SetPromptInput(question);
                    // Optional: auto-send the question
                    // setTimeout(() => SendMessageChat(), 100);
                  }}
                  className={`p-2 rounded-md cursor-pointer text-sm ${
                    isDarkMode ? 'bg-gray-800 hover:bg-gray-700' : 'bg-gray-100 hover:bg-gray-200'
                  }`}
                >
                  {question.length > 80 ? question.substring(0, 80) + '...' : question}
                </div>
              ))}
            </div>
          </div>
        </div>
      
        <div className="w-full md:w-4/5 bg-base-100 shadow-xl rounded-lg flex flex-col justify-between relative">
          <div className="flex items-center justify-between p-2 border-b">
            <h1 className="text-xl font-semibold">
              <FontAwesomeIcon icon={faMessage} className="mr-2" />
              Trò chuyện với Trợ lý
            </h1>
            
            {/* Mobile: Show chat history button */}
            <button className="md:hidden btn btn-sm btn-circle" onClick={() => document.getElementById('history-drawer').checked = true}>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h7" />
              </svg>
            </button>
          </div>
          
          {/* Chat messages area */}
          {/*  Sử dụng: isLoading để: Tự động cuộn xuống dưới khi có tin nhắn mới: ? */}
          <div className="chat-container flex-1 overflow-y-auto p-2 pb-24 max-h-[75vh] scrollbar-thin scrollbar-thumb-blue-500 scrollbar-track-blue-100">
            {dataChat.map((dataMessages, i) =>
              dataMessages[0] === "start" ? (
                <div className="chat chat-start" key={i}>
                  <div className="chat-image avatar">
                    <div className="w-10 rounded-full border-2 border-blue-500">
                      <img src={robot_img} />
                    </div>
                  </div>
                  <div className={`chat-bubble ${isDarkMode ? 'bg-blue-900 text-white' : 'chat-bubble-info'} text-lg`}>
                    <TypeAnimation
                      style={{ whiteSpace: 'pre-line' }} 
                      sequence={[
                        dataMessages[1][0]
                        
                        ,
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
                        <p className={`font-semibold text-sm ${isDarkMode ? 'text-gray-300' : ''}`}>
                          Tham khảo:{" "}
                          {dataMessages[1][1].map((source, j) => (
                            <label
                              htmlFor="my_modal_6"
                              className={`kbd kbd-xs mr-1 hover:bg-sky-300 cursor-pointer ${isDarkMode ? 'text-gray-300' : ''}`}
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
                <div className="chat chat-end" key={i}>
                  <div className={`chat-bubble shadow-xl text-lg ${
                    isDarkMode 
                      ? 'bg-gradient-to-r from-purple-900 to-blue-900 text-white' 
                      : 'chat-bubble-primary bg-gradient-to-r from-purple-500 to-blue-500 text-white'
                  }`}>
                    {dataMessages[1][0]}
                    <p className={`font-light text-xs ${isDarkMode ? 'text-gray-300' : 'text-cyan-50'}`}>
                    </p>
                  </div>
                </div>
              )
            )}
            {isLoading ? (
              <div className="chat chat-start">
                <div className="chat-image avatar">
                  <div className="w-10 rounded-full border-2 border-blue-500">
                    <img src={robot_img} />
                  </div>
                </div>
                <div className="chat-bubble chat-bubble-info text-lg">
                  <ScaleLoader
                    color="#000000"
                    loading={true}
                    height={10}
                    width={10}
                    aria-label="Loading Spinner"
                    data-testid="loader"
                  />
                  <p className="text-xs font-medium">{timeOfRequest + "/60s"}</p>
                </div>
              </div>
            ) : (
              ""
            )}
            <div ref={messagesEndRef} className="pt-2" />
          </div>
          
          {/* Chat input area - fixing width and positioning */}
          {/* Sử dụng: isLoading để: Tự động cuộn xuống dưới khi có tin nhắn mới: ? */}
          <div className="absolute bottom-0 left-0 right-0 w-full px-4 grid grid-cols-12 gap-1 bg-base-100 pb-2 pt-1 border-t border-gray-200">
            <input
              type="text"
              placeholder="Nhập câu hỏi tại đây..."
              className={`shadow-xl border-2 focus:outline-none px-2 py-3 rounded-2xl text-lg ${
                isDarkMode 
                  ? 'bg-gray-800 text-white border-blue-700' 
                  : 'input-primary'
              } col-span-11`}
              onChange={onChangeHandler}
              onKeyDown={handleKeyDown}
              disabled={isGen}
              value={promptInput}
            />

            <button
              disabled={isGen}
              onClick={() => SendMessageChat()}
              className={
                "drop-shadow-md rounded-2xl col-span-1 btn btn-active btn-primary btn-square bg-gradient-to-tl from-transparent via-blue-600 to-indigo-500"
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
            <p className={`text-xs col-span-12 text-justify p-1 ${isDarkMode ? 'text-gray-300' : ''}`}>
              <b>Lưu ý:</b> Mô hình có thể đưa ra câu trả lời không chính xác ở
              một số trường hợp, vì vậy hãy luôn kiểm chứng thông tin bạn nhé!
            </p>
          </div>
        </div>
      </div>
      
      {/* Mobile: Chat history drawer */}
      <div className="drawer drawer-end md:hidden">
        <input id="history-drawer" type="checkbox" className="drawer-toggle" />
        <div className="drawer-side z-10">
          <label htmlFor="history-drawer" className="drawer-overlay"></label>
          <div className={`p-4 w-80 min-h-full ${isDarkMode ? 'bg-gray-900 text-gray-200' : 'bg-base-200'}`}>
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold">Lịch sử chat</h2>
              <button 
                onClick={startNewChat}
                className="btn btn-sm btn-circle btn-primary"
                title="Tạo cuộc trò chuyện mới"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
                </svg>
              </button>
            </div>
            
            <div className="space-y-2 max-h-[30vh] overflow-y-auto mb-6">
              {chatSessions.map(chat => (
                <div 
                  key={chat.id}
                  onClick={() => {
                    setActiveChatId(chat.id);
                    document.getElementById('history-drawer').checked = false;
                  }}
                  className={`p-2 rounded-md cursor-pointer flex items-center gap-2 ${
                    activeChatId === chat.id 
                      ? (isDarkMode ? 'bg-blue-900' : 'bg-blue-100') 
                      : (isDarkMode ? 'hover:bg-gray-800' : 'hover:bg-gray-100')
                  }`}
                >
                  <FontAwesomeIcon icon={faMessage} className="text-blue-500" />
                  <div className="truncate">{chat.title}</div>
                </div>
              ))}
            </div>
            
            {/* Mobile reference questions */}
            <div className="mt-4">
              <h2 className="text-lg font-semibold mb-3">Câu hỏi tham khảo</h2>
              <div className="space-y-2 max-h-[40vh] overflow-y-auto">
                {commonQuestions.map((question, index) => (
                  <div 
                    key={index}
                    onClick={() => {
                      SetPromptInput(question);
                      document.getElementById('history-drawer').checked = false;
                      // Optional: auto-send the question
                      // setTimeout(() => SendMessageChat(), 100);
                    }}
                    className={`p-2 rounded-md cursor-pointer text-sm ${
                      isDarkMode ? 'bg-gray-800 hover:bg-gray-700' : 'bg-gray-100 hover:bg-gray-200'
                    }`}
                  >
                    {question.length > 60 ? question.substring(0, 60) + '...' : question}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
export default ChatBot;
