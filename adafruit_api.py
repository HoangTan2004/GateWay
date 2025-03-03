from Adafruit_IO import MQTTClient
import sys
from uart import Uart

class Adafruit_API:
    def __init__(self, username, key, feed_id_list, port="COM4"):
        self.username = username
        self.feed_id_list = feed_id_list
        self.key = key
        self.mqtt_client = None
        self.uart = None
        self.port = port

    def connected(self, client):
        """Hàm gọi khi kết nối thành công."""
        print("Connected to Adafruit IO!")
        for feed_id in self.feed_id_list:
            print("Subscribing to:", feed_id)
            client.subscribe(feed_id)

    def subscribe(self, client, userdata, mid, granted_qos):
        """Xác nhận đăng ký feed thành công."""
        print("Subscribed successfully!")

    def disconnected(self, client):
        """Hàm gọi khi mất kết nối."""
        print("Disconnected from Adafruit IO!")
        sys.exit(1)

    def message(self, client, feed_id, payload):
        """Xử lý tin nhắn từ Adafruit IO để điều khiển thiết bị."""
        print(f"Received command for {feed_id}: {payload}")

        # Điều khiển nhiệt độ (giả lập quạt/máy sưởi)
        if feed_id == "temperature":
            print(f"Setting Temperature Device to {payload}°C")
            self.uart.write_message(f"TEMP:{payload}")  # Ví dụ: "TEMP:30"

        # Điều khiển cảm biến độ ẩm đất
        elif feed_id == "soil_humidity":
            print(f"Setting Soil Humidity Level to {payload}%")
            self.uart.write_message(f"SOIL:{payload}")  # Ví dụ: "SOIL:50"

        # Điều khiển độ ẩm không khí
        elif feed_id == "air_humidity":
            print(f"Setting Air Humidity Level to {payload}%")
            self.uart.write_message(f"AIR:{payload}")  # Ví dụ: "AIR:60"

        # Điều khiển cảm biến ánh sáng
        elif feed_id == "light_sensor":
            print(f"Adjusting Light Sensor Sensitivity to {payload}")
            self.uart.write_message(f"LIGHT:{payload}")  # Ví dụ: "LIGHT:200"

        # Điều khiển đèn LED RGB
        elif feed_id == "rgb_led":
            print(f"Setting RGB LED color to {payload}")
            self.uart.write_message(f"RGB:{payload}")  # Ví dụ: "RGB:255,0,0"

        # Điều khiển máy bơm nước
        elif feed_id == "pumper":
            if payload == "1":
                print("Turning ON Pumper")
                self.uart.write_message("PUMP:ON")
            else:
                print("Turning OFF Pumper")
                self.uart.write_message("PUMP:OFF")

    def publish(self, feed_id, data):
        """Gửi dữ liệu lên Adafruit IO."""
        print(f"Publishing to {feed_id}: {data}")
        self.mqtt_client.publish(feed_id, data)

    def connect(self):
        """Kết nối tới Adafruit IO."""
        self.mqtt_client = MQTTClient(self.username, self.key)
        self.mqtt_client.on_connect = self.connected
        self.mqtt_client.on_disconnect = self.disconnected
        self.mqtt_client.on_message = self.message
        self.mqtt_client.on_subscribe = self.subscribe
        self.mqtt_client.connect()

        self.uart = Uart(self.port, self)
        self.uart.init_connection()

        self.mqtt_client.loop_background()

    def process_sensor_data(self, sensor_data):
        """Xử lý và gửi dữ liệu từ cảm biến."""
        for key, value in sensor_data.items():
            if key in self.feed_id_list:
                self.publish(key, value)

    def read_serial(self):
        """Đọc dữ liệu từ cảm biến qua UART."""
        sensor_data = self.uart.read_serial()
        if sensor_data:
            self.process_sensor_data(sensor_data)
        #print("Read serial")
