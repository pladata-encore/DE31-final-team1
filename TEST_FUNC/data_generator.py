import requests
import json
import random
import time
import os
import sys

#################### VARIABLES ####################
JSON_FILE_PATH = './endpoint_list.json'
DATA_LIST = ["temperature", "humidity", "light", "noise", "dust", "co2", "voc", "pm1", "pm2.5", "pm10"]
#################### VARIABLES ####################


#################### FUNCTIONS ####################
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

#################### FUNCTIONS ####################


####################### MAIN ######################
if __name__ == '__main__':
  # get current time
  time_cursor = time.time()

  # Read JSON file(initially)
  # endpoint_list = read_json_file(JSON_FILE_PATH)

  # do forever
  while True:
    # Read JSON file, if time_cursor is greater than 30min, read JSON file again
    if time.time() - time_cursor > 1800:
      endpoint_list = read_json_file(JSON_FILE_PATH)
      time_cursor = time.time()

    # for endpoint in endpoint_list:
      # Generate random data
    data = generate_random_data()
    print(f"Generate random data: {data}")

      # Send data to endpoint
      # response = requests.post(endpoint['url'], json=data)
      # print(f"Send data to {endpoint['url']}: {response.status_code}")

      # Sleep
    time.sleep(1)

####################### MAIN ######################