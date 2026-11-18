# Quy trình Git cho thực tập sinh

Đây là sổ tay giả lập dùng làm dữ liệu thử nghiệm, không phải quy định của một doanh nghiệp.
Thực tập sinh tạo nhánh Git theo mẫu feature/ten-cong-viec trước khi sửa code.
Sau khi sửa, chạy kiểm tra, dùng git add để chọn thay đổi và git commit để ghi lại.
Đẩy nhánh bằng git push rồi mở pull request vào nhánh main.
Mỗi pull request cần mô tả thay đổi và cách kiểm tra. Một thành viên trong nhóm xem xét trước khi merge.
Không commit khóa API hoặc tệp .env. Chỉ commit tệp .env.example với giá trị mẫu.
