# Windows Time Synchronization Tool

Tool tự động đồng bộ thời gian cho Windows sử dụng API bên thứ 3.

## Tính năng

- ✅ Tự động lấy thời gian chính xác từ nhiều API bên thứ 3
- ✅ Không phụ thuộc vào Windows Time Service
- ✅ Hỗ trợ nhiều nguồn API (tự động chuyển đổi nếu một API bị lỗi)
- ✅ Ghi log chi tiết
- ✅ Chế độ tự động chạy theo lịch trình
- ✅ Kiểm tra quyền Administrator

## Các API được sử dụng

1. **WorldTimeAPI** - http://worldtimeapi.org
2. **TimeAPI.io** - https://timeapi.io
3. **WorldClockAPI** - http://worldclockapi.com

Tool sẽ tự động thử từng API cho đến khi tìm được API hoạt động.

## Cài đặt

### 1. Cài đặt Python
Đảm bảo bạn đã cài Python 3.7 trở lên.

### 2. Cài đặt thư viện
```powershell
pip install -r requirements.txt
```

## Sử dụng

### Chế độ 1: Đồng bộ một lần

Chạy file `time_sync.py` với quyền Administrator:

```powershell
# Cách 1: Click chuột phải vào PowerShell -> Run as Administrator
python time_sync.py

# Cách 2: Hoặc từ Command Prompt Administrator
python time_sync.py
```

### Chế độ 2: Tự động đồng bộ theo lịch

Chạy file `auto_sync.py` với quyền Administrator:

```powershell
python auto_sync.py
```

Tool sẽ:
- Đồng bộ ngay lập tức khi khởi động
- Sau đó tự động đồng bộ mỗi 1 giờ
- Chạy liên tục cho đến khi bạn dừng (Ctrl+C)

### Tùy chỉnh tần suất đồng bộ

Mở file `auto_sync.py` và sửa dòng:

```python
# Đồng bộ mỗi 1 giờ
schedule.every(1).hours.do(sync_job)

# Các tùy chọn khác:
# schedule.every(30).minutes.do(sync_job)  # Mỗi 30 phút
# schedule.every(2).hours.do(sync_job)     # Mỗi 2 giờ
# schedule.every().day.at("09:00").do(sync_job)  # Mỗi ngày lúc 9h sáng
```

## Chạy tự động khi khởi động Windows

### Cách 1: Task Scheduler

1. Mở Task Scheduler (Windows + R -> `taskschd.msc`)
2. Create Basic Task
3. Tên: "Auto Time Sync"
4. Trigger: "When the computer starts"
5. Action: "Start a program"
   - Program: `pythonw.exe` (đường dẫn đầy đủ, VD: `C:\Python311\pythonw.exe`)
   - Arguments: `"C:\QuanNewData\Tool Date Time\auto_sync.py"`
   - Start in: `C:\QuanNewData\Tool Date Time`
6. Tick "Run with highest privileges"

### Cách 2: Startup folder

Tạo file `.bat`:

```batch
@echo off
cd /d "C:\QuanNewData\Tool Date Time"
pythonw auto_sync.py
```

Lưu thành `start_time_sync.bat` và copy vào:
```
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
```

## Log files

Tool tạo 2 file log:
- `time_sync.log` - Log của đồng bộ một lần
- `auto_sync.log` - Log của tự động đồng bộ

## Lưu ý quan trọng

⚠️ **Cần quyền Administrator**: Tool cần quyền Administrator để thay đổi thời gian hệ thống Windows.

⚠️ **Firewall**: Đảm bảo cho phép kết nối internet để truy cập các API.

⚠️ **Múi giờ**: Mặc định tool sử dụng múi giờ `Asia/Ho_Chi_Minh` (UTC+7). Bạn có thể thay đổi trong code.

## Xử lý sự cố

### Lỗi "Cần quyền Administrator"
- Chạy PowerShell/CMD với quyền Administrator
- Hoặc click chuột phải vào Python script -> Run as Administrator

### Lỗi "Không thể lấy thời gian từ API"
- Kiểm tra kết nối internet
- Kiểm tra firewall
- Các API có thể tạm thời không hoạt động, tool sẽ tự động thử API khác

### Lỗi "Module not found"
```powershell
pip install -r requirements.txt
```

## Giấy phép

MIT License - Sử dụng tự do cho mọi mục đích.
