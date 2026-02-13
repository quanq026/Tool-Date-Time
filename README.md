# Windows Time Synchronization Tool

Tool tự động đồng bộ thời gian cho Windows sử dụng API bên thứ 3.

## Các API được sử dụng

1. **WorldTimeAPI** - http://worldtimeapi.org
2. **TimeAPI.io** - https://timeapi.io
3. **WorldClockAPI** - http://worldclockapi.com

## Cài đặt

### 1. Cài đặt Python
Python 3.7 trở lên.

### 2. Cài đặt thư viện
```powershell
pip install -r requirements.txt
```

## Sử dụng

### Chế độ 1: Đồng bộ một lần

Chạy file `time_sync.py` với quyền Administrator:

### Chế độ 2: Tự động đồng bộ theo lịch

Chạy file `auto_sync.py` với quyền Administrator:

## Lưu ý quan trọng

**Cần quyền Administrator**: Tool cần quyền Administrator để thay đổi thời gian hệ thống Windows.

**Firewall**: Đảm bảo cho phép kết nối internet để truy cập các API.

**Múi giờ**: Mặc định tool sử dụng múi giờ `Asia/Ho_Chi_Minh` (UTC+7). Bạn có thể thay đổi trong code.
mục đích.
