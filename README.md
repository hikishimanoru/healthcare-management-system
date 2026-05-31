# HỆ THỐNG QUẢN LÝ DỊCH VỤ CHĂM SÓC SỨC KHỎE

## Giới thiệu

Đây là dự án xây dựng hệ thống quản lý dịch vụ chăm sóc sức khỏe bằng ngôn ngữ Python.
Ứng dụng sử dụng giao diện Tkinter/CustomTkinter và cơ sở dữ liệu SQLite để hỗ trợ các nghiệp vụ cơ bản của một phòng khám.

Hệ thống hỗ trợ quản lý:

- Bệnh nhân
- Bác sĩ
- Lịch khám / lịch hẹn
- Bệnh án
- Dịch vụ y tế
- Tài khoản người dùng và phân quyền
- Thanh toán demo và thống kê doanh thu

---

## Chức năng chính

- Đăng nhập hệ thống với mật khẩu được mã hóa MD5 trước khi lưu vào cơ sở dữ liệu.
- Phân quyền người dùng theo vai trò: Admin, Bác sĩ, Kế toán, Lễ tân, Bệnh nhân.
- Quản lý bệnh nhân: thêm, sửa, tìm kiếm, xuất hồ sơ CSV.
- Quản lý bác sĩ: thêm, sửa, xóa, tìm kiếm, lọc trạng thái sẵn sàng.
- Quản lý lịch khám: đặt lịch, kiểm tra trùng lịch, cập nhật trạng thái, hủy/xóa, tìm kiếm.
- Thanh toán demo cho lịch hẹn: khi xác nhận thanh toán, lịch hẹn được chuyển sang trạng thái "Hoàn thành" và doanh thu được cập nhật.
- Quản lý bệnh án: quy trình Bệnh nhân -> Lịch hẹn -> Bệnh án, hỗ trợ xuất bệnh án CSV.
- Quản lý dịch vụ: thêm, sửa, xóa dịch vụ y tế.
- Quản lý tài khoản: thêm, sửa mật khẩu, đổi vai trò, xóa tài khoản.
- Báo cáo thống kê: tổng bệnh nhân, bác sĩ hoạt động, lịch hẹn hôm nay, doanh thu động.
- Tối ưu UI/UX: giao diện hiện đại, menu theo phân quyền, bảng dữ liệu có phân trang tự động.

---

## Tài khoản demo

| Vai trò | Email | Mật khẩu |
|---|---|---|
| Admin | `admin@healthcare.com` | `admin123` |
| Bác sĩ | `doctor@healthcare.com` | `doctor123` |
| Kế toán | `ketoan@healthcare.com` | `ketoan123` |
| Lễ tân | `letan@healthcare.com` | `letan123` |
| Bệnh nhân | `patient@healthcare.com` | `patient123` |

---

## Phân quyền chức năng

| Vai trò | Chức năng chính |
|---|---|
| Admin | Quản lý toàn bộ hệ thống, tài khoản, bệnh nhân, bác sĩ, lịch hẹn, bệnh án, dịch vụ và thống kê |
| Bác sĩ | Xem bệnh nhân, quản lý lịch hẹn, cập nhật bệnh án, xem dịch vụ |
| Kế toán | Xem tổng quan doanh thu, xử lý thanh toán lịch hẹn, xem dịch vụ |
| Lễ tân | Tiếp nhận bệnh nhân, xem bác sĩ, đặt và quản lý lịch hẹn, xem dịch vụ |
| Bệnh nhân | Xem lịch hẹn, bệnh án và dịch vụ |

---

## Công nghệ sử dụng

- Python
- Tkinter / CustomTkinter
- SQLite
- CSV
- GitHub

---

## Hướng dẫn chạy chương trình

1. Cài đặt Python 3.x.
2. Cài đặt thư viện cần thiết nếu máy chưa có:

```bash
pip install customtkinter
```

3. Chạy ứng dụng:

```bash
python src/main.py
```

Hoặc chạy bằng Python trong môi trường ảo nếu dự án đã cấu hình `.venv`.

---

## Cấu trúc thư mục

```text
healthcare-management-system/
├── assets/       # Chứa hình ảnh
├── database/     # Chứa file SQLite database
├── docs/         # Chứa tài liệu, sơ đồ và mô tả chức năng
├── src/          # Chứa mã nguồn Python
├── ui_design/    # Chứa ảnh giao diện / thiết kế
└── README.md     # Thông tin dự án
```

---

## Ghi chú

- Chức năng thanh toán trong hệ thống là thanh toán demo, dùng để cập nhật trạng thái lịch hẹn và ghi nhận doanh thu thống kê.
- Mật khẩu hiện được hash bằng MD5 để phục vụ yêu cầu đồ án; trong hệ thống thực tế nên nâng cấp lên thuật toán mạnh hơn như PBKDF2 hoặc bcrypt.

---

## Thông tin sinh viên

Thành viên: Phạm Minh Quang, Phạm Quang Huy, Vũ Văn Linh  
Môn học: Lập trình ứng dụng với Python  
Đề tài: Hệ thống quản lý dịch vụ chăm sóc sức khỏe
