# Hệ thống quản lý sự kiện và người tham dự

Đồ án môn Python Programming: xây dựng ứng dụng desktop giúp quản lý sự kiện, người tham dự, đăng ký tham dự, check-in và thống kê.

## Chức năng chính

- Quản lý sự kiện: thêm, xem, sửa, xóa, tìm kiếm sự kiện.
- Quản lý người tham dự: thêm, xem, sửa, xóa, tìm kiếm người tham dự.
- Quản lý đăng ký: đăng ký người tham dự vào sự kiện, hủy đăng ký, xác nhận lại, check-in, bỏ check-in.
- Tổng quan: hiển thị số lượng sự kiện, người tham dự, lượt đăng ký và lượt check-in.
- Thống kê: hiển thị bảng và biểu đồ số lượt đăng ký/check-in theo từng sự kiện.
- Kết nối cơ sở dữ liệu SQLite.
- Giao diện đồ họa bằng CustomTkinter.

## Công nghệ sử dụng

- Python
- CustomTkinter
- SQLite
- Matplotlib
- Pillow

## Cấu trúc thư mục

```text
controllers/   Xử lý logic và kiểm tra dữ liệu
models/        Làm việc với cơ sở dữ liệu
views/         Giao diện người dùng
database/      File kết nối database và database SQLite
utils/         Thư mục tiện ích dự phòng
main.py        File chạy chương trình
```

## Cách chạy chương trình

1. Cài các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

2. Chạy file chính:

```bash
python main.py
```

## Cách dùng nhanh

1. Vào trang **Sự kiện** để tạo ít nhất một sự kiện.
2. Vào trang **Người tham dự** để tạo ít nhất một người tham dự.
3. Vào trang **Đăng ký** để chọn sự kiện và người tham dự rồi bấm **Đăng ký**.
4. Có thể bấm **Check-in** khi người tham dự đến sự kiện.
5. Vào **Tổng quan** và **Thống kê** để xem số liệu.

## Lưu ý khi nộp bài

- Không cần nộp thư mục `.venv`.
- Không cần nộp thư mục `__pycache__`.
- Nên đẩy source code lên GitHub theo yêu cầu đồ án.
