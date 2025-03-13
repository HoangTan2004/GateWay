import serial.tools.list_ports
import json

class Uart:
    def __init__(self,port,client):
        self.port = port
        self.serial = None
        self.client = client
        self.message = ''

    def init_connection(self):
        self.serial = serial.Serial( port=self.port, baudrate=115200)
        print('Uart connection is already!')

    def write_message(self,data):
        self.serial.write((str(data)).encode('utf-8'))

    def read_serial(self):
        bytesToRead = self.serial.inWaiting()
        if (bytesToRead > 0):
            self.message = self.message + self.serial.read(bytesToRead).decode("UTF-8")
            while('!' in self.message and '#' in self.message):
                start = self.message.find('!')
                end = self.message.find('#')
                self.process_data(self.message[start:end+1])
                self.message = self.message[end+1:]

    def process_data(self, data):
        """Xử lý dữ liệu cảm biến từ UART và gửi lên Adafruit IO."""
        data = data[1:-1]  # Loại bỏ ký tự '!' và '#'
        print(f"Raw Data Received: {data}")

        try:
            data_from_sensor = json.loads(data)  # Chuyển đổi JSON thành dict
            print(f"Parsed Sensor Data: {data_from_sensor}")

            # Gửi dữ liệu lên Adafruit IO theo từng loại cảm biến
            if "temperature" in data_from_sensor:
                self.client.publish("temperature", data_from_sensor['temperature'])
            if "soil-humidity" in data_from_sensor:
                self.client.publish("soil-humidity", data_from_sensor['soil-humidity'])
            if "air-humidity" in data_from_sensor:
                self.client.publish("air-humidity", data_from_sensor['air-humidity'])
            if "light-intensity" in data_from_sensor:
                self.client.publish("light-intensity", data_from_sensor['light-intensity'])

        except json.JSONDecodeError:
            print("Error: Invalid JSON format received")
