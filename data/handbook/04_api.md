# API dự đoán

API dự đoán nhận yêu cầu POST tại /predict, với JSON chứa trường text.
Phản hồi có nhãn ham hoặc spam và điểm xác suất do mô hình ước lượng.
Yêu cầu có text trống hoặc dài hơn giới hạn bị từ chối với mã HTTP 422.
Endpoint /health báo trạng thái sẵn sàng của dịch vụ.
Tài liệu tương tác của FastAPI có tại /docs khi chạy ứng dụng cục bộ.
API tải mô hình một lần khi khởi động, không huấn luyện lại cho từng yêu cầu.
