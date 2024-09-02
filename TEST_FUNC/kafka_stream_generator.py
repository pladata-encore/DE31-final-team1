import requests
import json
import random
import time
import os
import sys
import threading
import confluent_kafka

#################### VARIABLES ####################
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'user_device_list.json')
DATA_LIST = ["temperature", "humidity", "light", "noise", "dust", "co2", "voc", "pm1", "pm2.5", "pm10"] # co2: 이산화탄소, voc: 휘발성유기화합물, pm: 미세먼지


# @@@@@@@@@@@@@@@@@@@@@@@ CHANGE HERE @@@@@@@@@@@@@@@@@@@@@@@
endpoints = ['140.238.153.4:10000', '140.238.153.4:10001', '140.238.153.4:10002']
# @@@@@@@@@@@@@@@@@@@@@@@ CHANGE HERE @@@@@@@@@@@@@@@@@@@@@@@


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

def meta_wrapper(endpoints, user, device, data):
  meta_data = {
    'endpoints': ','.join(endpoints),
    'topic': f'{user}_{device}',
    'user': user,
    'device': device,
    'timestamp': int(time.time()),
    'data': data
  }
  return meta_data

def kafka_producer(endpoints, user, devices):
  loop_limit = 200
  # kafka producer
  producer = confluent_kafka.Producer({'bootstrap.servers': ','.join(endpoints)})
  while loop_limit > 0:
    try:
      for device in devices:
        data = generate_random_data()
        wrap_data = meta_wrapper(endpoints, user, device, data)
        print(f'wrap_data: {wrap_data}')
        producer.produce(wrap_data['topic'], json.dumps(wrap_data))
        producer.flush()
      loop_limit -= 1
      time.sleep(0.05)
    except Exception as e:
      print(f'Error: {e}')
      loop_limit -= 1
      time.sleep(1)
#################### FUNCTIONS ####################


####################### MAIN ######################
if __name__ == '__main__':
  # get current time
  time_cursor = time.time()

  # Read JSON file(initially)
  user_device_list = read_json_file(JSON_FILE_PATH)

  # make thread list by user_device_list
  thread_list = []


  for _ in user_device_list:
    # get devices list(value)
    print(f'user: {_['user']}, devices: {_['devices']}')
    thread = threading.Thread(target=kafka_producer, args=(endpoints, _['user'], _['devices']))
    thread_list.append(thread)
    thread.start()

  # join all threads
  for thread in thread_list:
    thread.join()

  print(f'Elapsed time: {time.time() - time_cursor}')
####################### MAIN ######################