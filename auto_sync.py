"""
Auto Time Sync Service
Tự động đồng bộ thời gian theo lịch trình
"""

import time
import schedule
from time_sync import TimeSync
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_sync.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)


def sync_job():
    """Job đồng bộ thời gian"""
    time_sync = TimeSync()
    time_sync.sync()


def main():
    """Hàm main cho auto sync"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   AUTO TIME SYNC SERVICE                                 ║
    ║   Dịch vụ Tự động Đồng bộ Thời gian                     ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Đồng bộ ngay khi bắt đầu
    logging.info("Đồng bộ thời gian lần đầu...")
    sync_job()
    
    # Lên lịch đồng bộ mỗi 1 giờ
    schedule.every(1).hours.do(sync_job)
    
    logging.info("Dịch vụ đang chạy. Đồng bộ mỗi 1 giờ.")
    logging.info("Nhấn Ctrl+C để dừng...")
    
    # Chạy vòng lặp
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Kiểm tra mỗi phút
    except KeyboardInterrupt:
        logging.info("Dịch vụ đã dừng.")


if __name__ == "__main__":
    main()
