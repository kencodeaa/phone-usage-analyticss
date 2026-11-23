# \# Mini App Nhóm B – PHONE USAGE ANALYTICS (Màn hình thông minh, giấc ngủ an lành)

# 

# \## 1. Mục đích

# Ứng dụng STEM Tin học 9 giúp học sinh thực hành xử lý dữ liệu về thời gian sử dụng màn hình và giấc ngủ của lớp 9B. Đây là công cụ học tập/truyền thông, không phải công cụ chẩn đoán sức khỏe.

# 

# \## 2. Cấu trúc thư mục

# \- `app.py`: giao diện Streamlit (Dashboard tối, 6 tab chức năng, biểu đồ Plotly, xuất Excel).

# \- `logic.py`: các hàm tính toán, dữ liệu mô phỏng mặc định 30 HS lớp 9B, kiểm tra và xuất file Excel.

# \- `requirements.txt`: thư viện cần cài (`streamlit`, `pandas`, `openpyxl`, `plotly`).

# \- `.streamlit/config.toml`: cấu hình giao diện tối đồng bộ màu sắc bảng điều khiển.

# \- `data/mau\_khao\_sat\_nhom\_B.csv`: mẫu trống 30 mã HS để nhập dữ liệu thật.

# \- `data/du\_lieu\_mo\_phong\_30\_HS.csv`: dữ liệu mô phỏng để thử app; không phải kết quả khảo sát.

# 

# \## 3. Chạy trên Windows

# 1\. Cài Python 3.10 trở lên.

# 2\. Mở Terminal/PowerShell tại thư mục dự án.

# 3\. Tạo môi trường ảo: `python -m venv .venv`

# 4\. Kích hoạt: `.venv\\Scripts\\activate`

# 5\. Cài thư viện: `pip install -r requirements.txt`

# 6\. Chạy ứng dụng: `streamlit run app.py`

# 

# \## 4. Các chức năng chính trên Web

# \- \*\*Dashboard Tổng Quan\*\*: Hiển thị 5 thẻ KPI (Tổng HS, Thời gian dùng ĐT TB, Thời lượng ngủ TB, Màn hình trước ngủ, Cần lưu ý cảnh báo), 3 thẻ phân nhóm (`< 2h`, `2h – 4h`, `> 4h`) và 2 biểu đồ trực quan tương tác.

# \- \*\*Tự Kiểm Tra Thói Quen\*\*: Nhập thông tin cá nhân minh họa để tính thời lượng ngủ và cho phép thêm trực tiếp kết quả ẩn danh vào bảng dữ liệu lớp.

# \- \*\*Bảng Dữ Liệu Khảo Sát\*\*: Tải file Excel Nhóm B (sheet `Du\_lieu\_khao\_sat`, tiêu đề dòng 3) hoặc CSV ẩn danh, lọc/tìm kiếm theo mã HS và tải file mẫu.

# \- \*\*Tiêu Chí \& Điều Kiện\*\*: Bảng tổng hợp quy ước phân nhóm và các chỉ tiêu đếm/tính tổng.

# \- \*\*Khu Vực Công Thức Excel\*\*: Đối chiếu trực tiếp các công thức `MOD`, `IF`, `OR`, `COUNTIF`, `SUMIF` trong chương trình Tin học 9.

# \- \*\*Báo Cáo \& Kiến Thức\*\*: Lưu ý đạo đức dữ liệu học đường, vai trò của AI và khung tóm tắt báo cáo lớp 9B.

# \- \*\*Thanh công cụ nhanh\*\*: Nút \*\*Khôi phục gốc\*\* (đưa về 30 HS mô phỏng ban đầu) và \*\*Xuất Excel\*\* (tải về file `.xlsx` gồm 2 sheet dữ liệu \& thống kê).

