"""
Windows Time Synchronization Tool
Tự động đồng bộ thời gian Windows với API thời gian bên thứ 3
"""

import ctypes
import requests
from datetime import datetime
import time
import logging
from typing import Optional

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('time_sync.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class SYSTEMTIME(ctypes.Structure):
    """Cấu trúc SYSTEMTIME của Windows"""
    _fields_ = [
        ('wYear', ctypes.c_uint16),
        ('wMonth', ctypes.c_uint16),
        ('wDayOfWeek', ctypes.c_uint16),
        ('wDay', ctypes.c_uint16),
        ('wHour', ctypes.c_uint16),
        ('wMinute', ctypes.c_uint16),
        ('wSecond', ctypes.c_uint16),
        ('wMilliseconds', ctypes.c_uint16),
    ]


class TimeSync:
    """Class để đồng bộ thời gian Windows"""
    
    # Danh sách các API thời gian có thể sử dụng
    TIME_APIS = [
        {
            'name': 'WorldTimeAPI',
            'url': 'http://worldtimeapi.org/api/timezone/Asia/Ho_Chi_Minh',
            'parser': 'parse_worldtime'
        },
        {
            'name': 'TimeAPI.io',
            'url': 'https://timeapi.io/api/Time/current/zone?timeZone=Asia/Ho_Chi_Minh',
            'parser': 'parse_timeapi'
        },
        {
            'name': 'WorldClockAPI',
            'url': 'http://worldclockapi.com/api/json/utc/now',
            'parser': 'parse_worldclock'
        }
    ]
    
    def __init__(self, timezone: str = 'Asia/Ho_Chi_Minh'):
        """
        Khởi tạo TimeSync
        
        Args:
            timezone: Múi giờ cần đồng bộ (mặc định là Asia/Ho_Chi_Minh)
        """
        self.timezone = timezone
        self.kernel32 = ctypes.windll.kernel32
        
    def get_time_from_api(self) -> Optional[datetime]:
        """
        Lấy thời gian từ các API bên thứ 3
        
        Returns:
            datetime object hoặc None nếu thất bại
        """
        for api in self.TIME_APIS:
            try:
                logging.info(f"Đang thử lấy thời gian từ {api['name']}...")
                response = requests.get(api['url'], timeout=5)
                response.raise_for_status()
                
                # Gọi parser tương ứng
                parser_method = getattr(self, api['parser'])
                dt = parser_method(response.json())
                
                if dt:
                    logging.info(f"✓ Lấy thời gian thành công từ {api['name']}: {dt}")
                    return dt
                    
            except Exception as e:
                logging.warning(f"✗ Không thể lấy thời gian từ {api['name']}: {e}")
                continue
        
        logging.error("Không thể lấy thời gian từ bất kỳ API nào!")
        return None
    
    def parse_worldtime(self, data: dict) -> Optional[datetime]:
        """Parse response từ WorldTimeAPI"""
        try:
            dt_str = data['datetime']
            # Format: 2025-12-21T10:30:45.123456+07:00
            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            # Chuyển về naive datetime (bỏ timezone info)
            return dt.replace(tzinfo=None)
        except Exception as e:
            logging.error(f"Lỗi parse WorldTimeAPI: {e}")
            return None
    
    def parse_timeapi(self, data: dict) -> Optional[datetime]:
        """Parse response từ TimeAPI.io"""
        try:
            # Format: "2025-12-21T10:30:45.1234567"
            dt_str = data['dateTime']
            dt = datetime.fromisoformat(dt_str)
            return dt
        except Exception as e:
            logging.error(f"Lỗi parse TimeAPI.io: {e}")
            return None
    
    def parse_worldclock(self, data: dict) -> Optional[datetime]:
        """Parse response từ WorldClockAPI"""
        try:
            dt_str = data['currentDateTime']
            # Format: "2025-12-21T03:30Z"
            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            # Chbuzzển sang múi giờ Việt Nam (UTC+7) và bỏ timezone info
            from datetime import timedelta
            dt = dt + timedelta(hours=7)
            return dt.replace(tzinfo=None)
        except Exception as e:
            logging.error(f"Lỗi parse WorldClockAPI: {e}")
            return None
    
    def check_admin_rights(self) -> bool:
        """Kiểm tra quyền admin"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    
    def set_system_time(self, dt: datetime) -> bool:
        """
        Set thời gian hệ thống Windows
        
        Args:
            dt: datetime object cần set
            
        Returns:
            True nếu thành công, False nếu thất bại
        """
        if not self.check_admin_rights():
            logging.error("Cần quyền Administrator để thay đổi thời gian hệ thống!")
            logging.error("Hãy chạy script với quyền Administrator (Run as Administrator)")
            return False
        
        try:
            # Tạo SYSTEMTIME structure
            system_time = SYSTEMTIME()
            system_time.wYear = dt.year
            system_time.wMonth = dt.month
            system_time.wDayOfWeek = dt.weekday()
            system_time.wDay = dt.day
            system_time.wHour = dt.hour
            system_time.wMinute = dt.minute
            system_time.wSecond = dt.second
            system_time.wMilliseconds = dt.microsecond // 1000
            
            # Gọi SetLocalTime API (set local time, không phải UTC)
            result = self.kernel32.SetLocalTime(ctypes.byref(system_time))
            
            if result != 0:
                logging.info(f"✓ Đã cập nhật thời gian hệ thống thành công: {dt}")
                return True
            else:
                error_code = ctypes.get_last_error()
                logging.error(f"✗ Không thể set thời gian hệ thống. Error code: {error_code}")
                return False
                
        except Exception as e:
            logging.error(f"Lỗi khi set thời gian: {e}")
            return False
    
    def sync(self) -> bool:
        """
        Thực hiện đồng bộ thời gian
        
        Returns:
            True nếu thành công, False nếu thất bại
        """
        logging.info("=" * 60)
        logging.info("BẮT ĐẦU ĐỒNG BỘ THỜI GIAN")
        logging.info("=" * 60)
        
        # Hiển thị thời gian hiện tại
        current_time = datetime.now()
        logging.info(f"Thời gian hiện tại: {current_time}")
        
        # Lấy thời gian từ API
        api_time = self.get_time_from_api()
        if not api_time:
            logging.error("Không thể đồng bộ thời gian!")
            return False
        
        # Tính chênh lệch
        time_diff = abs((api_time - current_time).total_seconds())
        logging.info(f"Chênh lệch thời gian: {time_diff:.2f} giây")
        
        # Nếu chênh lệch nhỏ hơn 1 giây, không cần cập nhật
        if time_diff < 1:
            logging.info("Thời gian đã chính xác, không cần cập nhật!")
            return True
        
        # Set thời gian mới
        success = self.set_system_time(api_time)
        
        if success:
            logging.info("=" * 60)
            logging.info("ĐỒNG BỘ THỜI GIAN THÀNH CÔNG!")
            logging.info("=" * 60)
        else:
            logging.error("=" * 60)
            logging.error("ĐỒNG BỘ THỜI GIAN THẤT BẠI!")
            logging.error("=" * 60)
        
        return success


def main():
    """Hàm main"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   WINDOWS TIME SYNCHRONIZATION TOOL                      ║
    ║   Tool Đồng Bộ Thời Gian Windows                        ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Tạo instance
    time_sync = TimeSync()
    
    # Kiểm tra quyền admin
    if not time_sync.check_admin_rights():
        print("\n⚠️  CẢNH BÁO: Script đang chạy KHÔNG có quyền Administrator!")
        print("Để thay đổi thời gian hệ thống, cần chạy với quyền Administrator.")
        print("Nhấn Enter để tiếp tục (chỉ kiểm tra) hoặc Ctrl+C để thoát...")
        try:
            input()
        except KeyboardInterrupt:
            print("\nĐã hủy.")
            return
    
    # Thực hiện đồng bộ
    time_sync.sync()


if __name__ == "__main__":
    main()
