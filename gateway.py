from adafruit_api import Adafruit_API
import time
from threading import Thread
import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Lấy thông tin từ biến môi trường
USERNAME = "htann04"
KEY = "aio_byLc21OberVRA2alJMLpkdzxcvXt"
print(USERNAME, KEY)


# Danh sách feed ID cần kết nối
feed_id_list = [
    'temperature',
    'soil-humidity',
    'air-humidity',
    'light-intensity',
    'led',
    'water-pump',
    'fan',
]

# Khởi tạo client Adafruit API
client = Adafruit_API(USERNAME, KEY, feed_id_list)
client.connect()

def read_sensors():
    """Đọc dữ liệu từ cảm biến."""
    while True:
        client.read_serial()
        time.sleep(1)

# Tạo luồng để đọc dữ liệu từ cảm biến
sensor_thread = Thread(target=read_sensors)
sensor_thread.daemon = True
sensor_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nProgram terminated.")

