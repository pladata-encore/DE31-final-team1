import multiprocessing
from app.v1.subprocess.components.kafka_publisher import KafkaPublisher
from app.test.generator.kafka_stream_generator import TestDataGenerator
import os
from datetime import time, datetime, timedelta
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError


def run_kafka_publisher(email, name, ds_id, bootstrap_servers, region_name):
    publisher = KafkaPublisher(email, name, ds_id, bootstrap_servers, region_name)
    topic = f'{email.split("@")[0]}_{name}_{ds_id}'

    try:
        admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        topic_list = [NewTopic(name=topic, num_partitions=3, replication_factor=3)]
        admin_client.create_topics(new_topics=topic_list, validate_only=False)

    except TopicAlreadyExistsError:
        print(f"{topic} 토픽이 이미 존재합니다. 토픽 생성이 중지됩니다.")  

    # 테스트 데이터 생성
    data_generator = TestDataGenerator()

    try:
        while True:
            data_list = data_generator.get_data()
            enriched_data = {
                "endpoint": data_list['endpoint'],
                "topic": topic,
                "email": email,
                "name" : name, 
                "ds_id": ds_id,
                "timestamp": datetime.now()+ timedelta(hours=9),
                "data": data_list['data']
            }
            publisher.publish_data(topic, enriched_data)
            print(enriched_data)
            time.sleep(1)
            
    except Exception as e:
        print(f"Error in Kafka publisher: {str(e)}")
    finally:
        publisher.close()

class SubprocessManager:
    def __init__(self):
        self.processes = {}

    def start_process(self, email, name, ds_id):
        if email in self.processes:
            return False
        
        bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        region_name = os.getenv("AWS_REGION")
        
        process = multiprocessing.Process(
            target=run_kafka_publisher,
            args=(email, name, ds_id, bootstrap_servers, region_name)
        )
        process.start()
        self.processes[email] = process
        return True

    def stop_process(self, email, topic):
        if email not in self.processes or topic not in self.processes[email]:
            return False
        
        self.processes[email][topic].terminate()
        self.processes[email][topic].join()
        del self.processes[email][topic]
        
        # 해당 이메일에 대한 모든 토픽이 삭제되었다면, 이메일 키도 삭제
        if not self.processes[email]:
            del self.processes[email]
        
        return True

subprocess_manager = SubprocessManager()