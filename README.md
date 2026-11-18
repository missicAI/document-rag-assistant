# Hỏi đáp tài liệu tiếng Việt

Tải một tài liệu ngắn lên, đặt câu hỏi bằng tiếng Việt và đọc câu trả lời. Ứng dụng yêu cầu mô hình dựa vào nội dung tệp, kèm một câu trích ngắn để bạn kiểm tra lại.

Bản này được Việt hóa từ ví dụ File Q&A của Streamlit. Chỉ giữ TXT và Markdown để code dễ đọc và việc chạy trên máy đơn giản hơn.

## Chạy ứng dụng

Cài Python 3.12. Trên Windows, mở `CAI_DAT.bat` rồi chạy `CHAY_DEMO.bat`.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Ứng dụng cần mô hình thật để trả lời. Nếu dùng thiết lập mặc định, cài [Ollama](https://ollama.com/download) và chạy:

```bash
ollama pull qwen2.5:1.5b
```

Bạn cũng có thể đổi địa chỉ máy chủ, tên mô hình và khóa truy cập trong phần bên trái. Dịch vụ cần hỗ trợ cách gọi tương thích OpenAI; dịch vụ bên ngoài có thể tính phí.

## Dùng thử

Chọn tệp `du_lieu_mau/huong_dan_phong_van.txt`, rồi hỏi: “Trước buổi phỏng vấn, ứng viên cần chuẩn bị những gì?”

Bạn có thể thay bằng tệp tiếng Việt của mình. Tệp cần lưu với mã UTF-8, tối đa 200 KB và 20.000 ký tự. Câu hỏi tối đa 2.000 ký tự.

## Cách hoạt động

Code gửi toàn bộ tài liệu ngắn cùng câu hỏi đến mô hình. Bản gọn này không chia đoạn để tìm kiếm, không dùng cơ sở dữ liệu vector và không được mô tả là một hệ thống RAG đầy đủ. Tên repository được giữ để các đường dẫn cũ vẫn dùng được.

Mô hình được yêu cầu nói rõ khi tài liệu không có thông tin. Câu trả lời vẫn có thể sai hoặc trích chưa đúng, nên tài liệu gốc là nơi cần đối chiếu.

Mở `app.py` để đọc từ phần tải tệp, nhập câu hỏi đến phần gửi yêu cầu. Không có câu trả lời tạo sẵn được dùng thay mô hình thật. Kiểm tra tự động dùng phản hồi giả lập để thử giao diện, chưa đo chất lượng mô hình.

Nguồn và phần đã chỉnh nằm tại [NGUON.md](NGUON.md). Giữ giấy phép Apache 2.0 của Streamlit.
