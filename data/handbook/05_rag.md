# Hỏi đáp tài liệu bằng RAG

RAG là quy trình tìm các đoạn tài liệu liên quan rồi cung cấp chúng cho mô hình ngôn ngữ để tạo câu trả lời.
Chia văn bản thành đoạn giúp lấy đúng phần cần thiết thay vì gửi toàn bộ tài liệu.
Overlap là phần nội dung lặp giữa các đoạn để giảm mất ngữ cảnh ở ranh giới.
TF-IDF tìm theo sự giống nhau về từ hoặc ký tự; semantic embeddings có thể tìm theo ý nghĩa.
Nếu tài liệu không có câu trả lời, hệ thống nên thông báo thiếu thông tin thay vì tự bổ sung.
Dẫn nguồn giúp người dùng kiểm tra, nhưng không đảm bảo mọi câu trả lời đều đúng.
