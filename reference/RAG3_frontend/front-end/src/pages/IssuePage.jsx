import emailjs from "@emailjs/browser";
import { useRef } from "react";

function IssuePage() {

  let templateParams = {
    from_name: "James",
    message: "Check this out!",
  };
  function sendMail() {
    emailjs
      .send(
        "<>",
        "template_azmnoyw",
        templateParams,
        "<>"
      )
      .then(
        function (response) {
          console.log("SUCCESS!", response.status, response.text);
        },
        function (error) {
          console.log("FAILED...", error);
        }
      );
  }

  return (
    <div className="flex justify-center h-[85vh] bg-apple-lightgray">
      {/* Modal */}
      <input type="checkbox" id="my-modal" className="modal-toggle" />
      <div className="modal">
        <div className="modal-box bg-white rounded-2xl shadow-lg">
          <h3 className="font-bold text-lg text-apple-black">Gửi thành công 🥳</h3>
          <p className="py-4 text-apple-gray">
            Cảm ơn bạn đã gửi góp ý / báo lỗi 🤗. Chúng tôi sẽ xem xét những ý
            kiến của người dùng để ngày càng hoàn thiện sản phẩm hơn nhé!
          </p>
          <div className="modal-action">
            <label htmlFor="my-modal" className="btn bg-apple-blue text-white border-none rounded-full px-6">
              Đóng
            </label>
          </div>
        </div>
      </div>
      
      <div className="md:w-[50%] px-4 py-8">
        <h1 className="text-3xl text-center font-bold p-5 text-apple-blue mb-6">
          Báo lỗi hoặc góp ý
        </h1>
        <p className="text-center font-medium text-apple-gray mb-8 px-4">
          Sự đóng góp ý kiến từ các bạn sẽ là sự hỗ trợ đắc lực giúp chúng tôi
          ngày càng hoàn thiện sản phẩm hơn.
        </p>

        <textarea
          placeholder="Nhập phản hồi của bạn tại đây!"
          className="mt-5 mb-6 h-[30%] p-4 border border-gray-200 rounded-2xl w-full focus:outline-none focus:border-apple-blue shadow-sm"
        ></textarea>
        
        <input 
          type="text" 
          placeholder="Email của bạn" 
          className="input w-full p-4 border border-gray-200 rounded-full mb-6 focus:outline-none focus:border-apple-blue shadow-sm" 
        />
        
        <label
          htmlFor="my-modal"
          className="block w-full btn bg-apple-blue hover:bg-apple-darkblue text-white border-none rounded-full py-3 font-medium shadow-sm transition-all"
        >
          Gửi ý kiến
        </label>
      </div>
    </div>
  );
}

export default IssuePage;
