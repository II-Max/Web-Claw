# Hướng Dẫn Sử Dụng DataMine V5

Chào mừng bạn đến với **DataMine V5** — Công cụ trích xuất dữ liệu web toàn diện.
DataMine V5 cho phép bạn cào 18 loại dữ liệu khác nhau từ bất kỳ website nào và tự động phân loại, xuất ra các định dạng chuẩn (`Markdown` và `JSON`) để dễ dàng đọc và xử lý tiếp.

---

## 🚀 1. Cài đặt và Chuẩn bị

### Yêu cầu hệ thống:
- Python 3.10 trở lên.
- Git (nếu muốn clone từ kho lưu trữ).

### Các bước cài đặt:

**Bước 1:** Clone mã nguồn hoặc tải thư mục mã nguồn về máy:
```bash
git clone https://github.com/yourusername/DataMine.git
cd DataMine
```

**Bước 2:** (Khuyến nghị) Tạo môi trường ảo (virtual environment) để tránh xung đột thư viện:
```bash
# Trên Windows
python -m venv venv
venv\Scripts\activate

# Trên Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

**Bước 3:** Cài đặt các thư viện phụ thuộc:
```bash
pip install -r web_miner/requirements.txt
```

---

## 🛠 2. Hướng Dẫn Chạy Công Cụ

DataMine V5 cung cấp 3 chế độ chạy chính:

### Chế độ 1: Quét một URL (Tương tác trực tiếp)
Nếu bạn chỉ muốn quét một trang web và muốn công cụ hỏi URL khi chạy, hãy dùng lệnh sau:
```bash
python -m web_miner.main
```
- Khi chạy, công cụ sẽ hiện dấu nhắc: `🌐 Nhập URL website cần cào: `
- Bạn dán đường link trang web vào (ví dụ: `https://quotes.toscrape.com`) và nhấn Enter. Công cụ sẽ tự động làm phần còn lại.

### Chế độ 2: Quét một URL (Headless - Trực tiếp qua tham số)
Rất hữu ích khi bạn muốn tích hợp công cụ vào một script khác hoặc không muốn bị hỏi lại:
```bash
python -m web_miner.main --url https://example.com --no_prompt
```
- Cờ `--no_prompt` báo cho hệ thống biết không cần hiện bảng hỏi nhập URL nữa. Cần phải đi kèm với tham số `--url`.

### Chế độ 3: Quét nhiều website cùng lúc (Batch Mode)
Dành cho việc quét hàng loạt danh sách các website đã chuẩn bị sẵn.

**Bước 1:** Mở file `web_miner/targets.txt` (nếu chưa có, chạy công cụ 1 lần nó sẽ tự tạo) và điền danh sách các URL cần quét, mỗi URL một dòng. Bạn có thể thêm ký tự `#` ở đầu dòng để comment (bỏ qua dòng đó).
Ví dụ nội dung file `targets.txt`:
```text
https://quotes.toscrape.com
https://books.toscrape.com
# https://ignore-this-site.com
```

**Bước 2:** Chạy lệnh batch mode:
```bash
python -m web_miner.main --batch
```
Công cụ sẽ lần lượt quét từng URL trong danh sách và báo cáo tiến độ.

---

## 📂 3. Hiểu Cấu Trúc Dữ Liệu Đầu Ra (Output)

Sau khi chạy xong, dữ liệu sẽ được lưu tại thư mục: `web_miner/outputs/`
Bên trong thư mục này có 2 thư mục con là `markdown/` và `json/`. Mỗi website được quét sẽ tạo ra một thư mục mang tên miền của nó.

Ví dụ, quét `https://quotes.toscrape.com`, bạn sẽ có:

### Thư mục `markdown/quotes_toscrape_com/`
Dành cho việc đọc trực tiếp (Human-readable). Dễ dàng xem bằng các editor như VSCode, Obsidian hoặc GitHub:
- `full_content.md`: Tổng hợp thông tin cốt lõi (Title, thống kê số lượng), nội dung chính (đã loại bỏ quảng cáo, footer) và cấu trúc các thẻ Heading (H1-H6).
- `metadata.md`: Chứa Title, Description, Keywords, các thẻ Open Graph (Facebook), Twitter Cards và cả Structured Data (JSON-LD).
- `tables.md`: Tất cả các bảng HTML đã được cào, chuyển thành bảng dạng Markdown.
- `links.md`: Phân loại danh sách link thành: Internal, External, Social Media (Facebook, Twitter...) và Link tải file (PDF, Zip...).
- `media.md`: Hình ảnh (kèm kích thước, thẻ alt), Videos và Audio.
- `contacts.md`: Email, Số điện thoại (tự động chuẩn hóa), liên kết mạng xã hội và địa chỉ.
- `forms_and_code.md`: Thông tin các form nhập liệu, mã nguồn (code blocks) và các tài nguyên CSS/JS.

### Thư mục `json/quotes_toscrape_com/`
Dành cho máy đọc, tiện lợi để nạp vào Database, API hoặc phân tích bằng Pandas:
- `full_data.json`: File tổng chứa TẤT CẢ mọi dữ liệu cào được từ trang.
- `metadata.json`, `tables.json`, `links.json`, `media.json`, `contacts.json`, `text_content.json`, `forms_and_code.json`: Chứa dữ liệu tương ứng đã được cấu trúc dưới dạng JSON chuẩn.

---

## 📌 4. Khắc phục sự cố & Lưu ý

- **Lỗi Encoding Unicode trên Windows:** Nếu bạn chạy trên Windows Terminal/Command Prompt và gặp lỗi in ký tự (ví dụ: lỗi với các icon Emoji), bạn hãy thiết lập biến môi trường UTF-8 trước khi chạy:
  - PowerShell:
    ```powershell
    $env:PYTHONUTF8="1"
    $env:PYTHONIOENCODING="utf-8"
    python -m web_miner.main
    ```
  - CMD:
    ```cmd
    set PYTHONUTF8=1
    set PYTHONIOENCODING=utf-8
    python -m web_miner.main
    ```
- **Không kết nối được website:** Công cụ có chế độ tự động thử lại (retry) 3 lần. Nếu cả 3 lần đều thất bại, nguyên nhân có thể do website bị sập, hoặc có hệ thống chặn bot (Cloudflare, CAPTCHA).

---
*Chúc bạn khai thác dữ liệu hiệu quả với DataMine V5!*