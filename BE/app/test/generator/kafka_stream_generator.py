import json
import random
import time
import os

JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'endpoint_list.json')
DATA_LIST = ["temperature", "humidity", "light", "noise", "dust", "co2", "voc", "pm1", "pm2.5", "pm10"]

def read_json_file(file_path):
  with open(file_path, 'r') as file:
    data = json.load(file)
  return data

def generate_random_data():
  # choose random data from DATA_LIST (1~3)
  data = {}
  for i in range(random.randint(1, 4)):
    data[random.choice(DATA_LIST)] = round(random.uniform(0, 100), 2)
  data['timestamp'] = int(time.time())
  return data

class TestDataGenerator:
    def __init__(self):
        self.endpoint_list = read_json_file(JSON_FILE_PATH)
        self.time_cursor = time.time()

    def get_data(self):
        if time.time() - self.time_cursor > 60:
            self.endpoint_list = read_json_file(JSON_FILE_PATH)
            self.time_cursor = time.time()

        endpoint = random.choice(self.endpoint_list)
        data = generate_random_data()
        return {
            "endpoint": endpoint['url'],
            "data": data
        }