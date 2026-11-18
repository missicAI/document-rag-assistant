# Chuẩn bị và chia dữ liệu

Trước khi huấn luyện, kiểm tra dữ liệu thiếu, nhãn sai và bản ghi trùng lặp.
Xóa tin nhắn trùng trước khi chia dữ liệu để tránh cùng một nội dung xuất hiện ở cả tập train và tập test.
Trong dự án mẫu, chia 80% dữ liệu cho huấn luyện và 20% cho kiểm tra, dùng stratify để giữ gần đúng tỷ lệ nhãn.
Chỉ fit TF-IDF trên tập train. Dùng vectorizer đã fit để transform tập test.
Không dùng kết quả trên test để lựa chọn tham số nhiều lần; nếu cần lựa chọn tham số, tách thêm tập validation hoặc dùng cross-validation trong tập train.
