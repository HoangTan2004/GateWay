from adafruit_api import Adafruit_API
import time
from threading import Thread
import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Lấy thông tin từ biến môi trường
USERNAME = os.getenv('USERNAME')
KEY = os.getenv('KEY')

# Danh sách feed ID cần kết nối
feed_id_list = [
    'temperature',
    'soil_humidity',
    'air_humidity',
    'light_sensor',
    'rgb_led',
    'pumper'
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

# Vòng lặp chính
while True:
    time.sleep(1)
