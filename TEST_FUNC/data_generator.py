import requests
import json
import random
import time
import os
import sys
import threading

#################### VARIABLES ####################
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'endpoint_list.json')
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

def threading_data_transfer(endpoint):
  # Generate random data
  data = generate_random_data()
  # response = requests.post(endpoint['url'], json=data)
  # print(f"Send data to {endpoint['url']}, data: {data}")
  print(f"{{'user':'user1', 'device':'device1', 'data':{data}}}")

#################### FUNCTIONS ####################


####################### MAIN ######################
if __name__ == '__main__':
  # get current time
  time_cursor = time.time()

  # Read JSON file(initially)
  endpoint_list = read_json_file(JSON_FILE_PATH)

  # do forever
  for i in range(2):
    # Read JSON file, if time_cursor is greater than 1min, read JSON file again
    if time.time() - time_cursor > 60:
      endpoint_list = read_json_file(JSON_FILE_PATH)
      time_cursor = time.time()

    # get endpoint list length
    endpoint_list_length = len(endpoint_list)

    # make thread list
    thread_list = []

    # add job to thread list
    for i in range(endpoint_list_length):
      thread = threading.Thread(target=threading_data_transfer, args=(endpoint_list[i],))
      thread_list.append(thread)
      thread.start()

    # join all threads
    for thread in thread_list:
      thread.join()
    
    # Sleep
    time.sleep(1)

####################### MAIN ######################