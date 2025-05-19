# import os
# import torch
# from sentence_transformers import SentenceTransformer
# from pathlib import Path
# import transformers # Import thư viện transformers để kiểm tra lớp model

# def convert_to_onnx():
#     print("=== Bắt đầu chuyển đổi model sang ONNX ===")

#     # Đường dẫn model (đảm bảo thư mục này có chứa model đã tải về hoặc sẽ tải về)
#     # Sử dụng Path để xử lý đường dẫn tốt hơn giữa các OS
#     base_dir = Path(__file__).resolve().parent.parent # Giả định cấu trúc dự án
#     # Điều chỉnh base_dir nếu cấu trúc thư mục của bạn khác
#     # Ví dụ: base_dir = Path(__file__).resolve().parent # nếu script nằm cùng cấp với thư mục model
    
#     model_storage_path = base_dir / "model"
#     onnx_output_dir = model_storage_path / "onnx"

#     model_name = 'paraphrase-multilingual-mpnet-base-v2'

#     print(f"Đang tải model {model_name} hoặc load từ cache: {model_storage_path}...")
#     # SentenceTransformer sẽ tự động tải về model vào cache_folder nếu chưa có
#     try:
#         # Sử dụng str(model_storage_path) để đảm bảo tương thích với cache_folder
#         model = SentenceTransformer(model_name, cache_folder=str(model_storage_path))
#         print(f"Model {model_name} đã tải/load thành công.")
#     except Exception as e:
#         print(f"Lỗi khi tải hoặc load model: {e}")
#         print("Đảm bảo bạn có kết nối internet hoặc model đã được tải về đầy đủ vào thư mục cache_folder.")
#         # print("Thử xóa thư mục cache_folder và chạy lại.") # Có thể thử nếu nghi ngờ cache bị hỏng
#         return

#     # Debug info
#     print("Cấu trúc model SentenceTransformer:", type(model))

#     # Lấy model transformer từ SentenceTransformer
#     # Model Transformer thường là module đầu tiên trong SentenceTransformer (index 0)
#     # Kiểm tra lại cấu trúc model._modules để chắc chắn
#     if '0' in model._modules and hasattr(model._modules['0'], 'auto_model'):
#          transformer_model = model._modules['0'].auto_model
#     else:
#          print("Không tìm thấy auto_model trong module đầu tiên của SentenceTransformer.")
#          print("Cấu trúc modules:", model._modules.keys())
#          raise AttributeError("Không thể lấy transformer_model từ SentenceTransformer.")


#     print("Loại underlying transformer model:", type(transformer_model))

#     # Tạo thư mục onnx nếu chưa tồn tại
#     os.makedirs(onnx_output_dir, exist_ok=True)
#     print(f"Thư mục output ONNX: {onnx_output_dir}")

#     # Chuyển model về CPU để export (nếu model đang ở GPU)
#     transformer_model = transformer_model.cpu()
#     transformer_model.eval()  # Chuyển sang chế độ evaluation

#     # Chuẩn bị input mẫu trên CPU
#     # RoBERTa và MPNet thường không dùng token_type_ids
#     dummy_input = {
#         "input_ids": torch.ones(1, 128, dtype=torch.long),
#         "attention_mask": torch.ones(1, 128, dtype=torch.long),
#         # "token_type_ids": torch.ones(1, 128, dtype=torch.long) # Bỏ token_type_ids
#     }

#     # Export sang ONNX
#     print("Đang export sang ONNX...")
#     onnx_file_path = onnx_output_dir / "model.onnx"

#     # Kiểm tra xem model có sử dụng token_type_ids không (phòng trường hợp đặc biệt)
#     # Bằng cách kiểm tra signature của forward method hoặc config của model
#     requires_token_type_ids = False
#     # Có thể kiểm tra: 'token_type_ids' in transformer_model.forward.__code__.co_varnames
#     # hoặc dựa vào model config nếu biết rõ kiến trúc
#     # Đối với XLMRobertaModel/MPNet base thường là False


#     try:
#         # Tạo một class wrapper để export
#         # Chỉ nhận input_ids và attention_mask nếu model không dùng token_type_ids
#         if not requires_token_type_ids:
#             class ModelWrapper(torch.nn.Module):
#                 def __init__(self, model):
#                     super().__init__()
#                     self.model = model

#                 def forward(self, input_ids, attention_mask):
#                     outputs = self.model(
#                         input_ids=input_ids,
#                         attention_mask=attention_mask,
#                         # token_type_ids được bỏ qua hoặc set mặc định bên trong model nếu cần
#                         return_dict=True
#                     )
#                     # Output của transformer model thường là tuple hoặc BaseModelOutput
#                     # outputs.last_hidden_state là hidden states cuối cùng
#                     return outputs.last_hidden_state

#             wrapped_model = ModelWrapper(transformer_model)
#             inputs_tuple = (dummy_input["input_ids"], dummy_input["attention_mask"])
#             input_names = ["input_ids", "attention_mask"]
#             dynamic_axes = {
#                 "input_ids": {0: "batch_size", 1: "sequence"},
#                 "attention_mask": {0: "batch_size", 1: "sequence"},
#                 "last_hidden_state": {0: "batch_size", 1: "sequence"}
#             }
#         else:
#              # Trường hợp model cần token_type_ids (ít xảy ra với MPNet/RoBERTa base)
#              # Bạn sẽ cần uncomment phần token_type_ids ở dummy_input
#              class ModelWrapperWithTokenType(torch.nn.Module):
#                 def __init__(self, model):
#                     super().__init__()
#                     self.model = model

#                 def forward(self, input_ids, attention_mask, token_type_ids):
#                     outputs = self.model(
#                         input_ids=input_ids,
#                         attention_mask=attention_mask,
#                         token_type_ids=token_type_ids,
#                         return_dict=True
#                     )
#                     return outputs.last_hidden_state

#              wrapped_model = ModelWrapperWithTokenType(transformer_model)
#              inputs_tuple = (dummy_input["input_ids"], dummy_input["attention_mask"], dummy_input["token_type_ids"])
#              input_names = ["input_ids", "attention_mask", "token_type_ids"]
#              dynamic_axes = {
#                 "input_ids": {0: "batch_size", 1: "sequence"},
#                 "attention_mask": {0: "batch_size", 1: "sequence"},
#                 "token_type_ids": {0: "batch_size", 1: "sequence"},
#                 "last_hidden_state": {0: "batch_size", 1: "sequence"}
#             }


#         wrapped_model.eval()

#         # Export
#         torch.onnx.export(
#             wrapped_model,
#             inputs_tuple, # Truyền tuple input mẫu
#             str(onnx_file_path), # Chuyển Path object sang string
#             input_names=input_names, # Cập nhật input_names
#             output_names=["last_hidden_state"], # Tên output từ forward method
#             dynamic_axes=dynamic_axes,
#             opset_version=12, # opset_version 12 thường hoạt động tốt, có thể thử 14 hoặc cao hơn nếu cần
#             do_constant_folding=True
#         )
#         print(f"Model đã được chuyển đổi thành công và lưu tại: {onnx_file_path}")

#     except Exception as e:
#         print(f"Chi tiết lỗi khi export ONNX: {str(e)}")
#         # In thêm thông tin debug về input shape và device
#         print(f"Input sample shapes:")
#         for name, tensor in dummy_input.items():
#              print(f"- {name}: {tensor.shape}")
#         print(f"Device của model: {next(transformer_model.parameters()).device}")
#         print(f"Device của dummy inputs:")
#         for name, tensor in dummy_input.items():
#              print(f"- {name}: {tensor.device}")

#         # Thêm debug để kiểm tra forward pass trực tiếp
#         # try:
#         #     print("\n--- Kiểm tra forward pass trực tiếp với dummy input ---")
#         #     if not requires_token_type_ids:
#         #         output_check = transformer_model(input_ids=dummy_input["input_ids"], attention_mask=dummy_input["attention_mask"], return_dict=True)
#         #     else:
#         #         output_check = transformer_model(input_ids=dummy_input["input_ids"], attention_mask=dummy_input["attention_mask"], token_type_ids=dummy_input["token_type_ids"], return_dict=True)
#         #     print("Forward pass thành công!")
#         #     print("Output type:", type(output_check))
#         #     print("Output last_hidden_state shape:", output_check.last_hidden_state.shape)
#         # except Exception as forward_e:
#         #      print(f"Lỗi khi chạy forward pass trực tiếp: {forward_e}")
#         # print("-----------------------------------------------------")


#         raise e # Re-raise exception để chương trình dừng lại

#     # Kiểm tra file đã được tạo
#     if onnx_file_path.exists():
#         print("Kiểm tra: File ONNX đã được tạo thành công!")
#     else:
#         raise Exception("Lỗi: Không thể tạo file ONNX!")

# if __name__ == "__main__":
#     try:
#         convert_to_onnx()
#     except Exception as e:
#         print(f"Quá trình chuyển đổi ONNX thất bại: {str(e)}")
#         exit(1)