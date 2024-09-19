import multiprocessing
from app.v1.subprocess.components.kafka_publisher import KafkaPublisher
from app.test.generator.kafka_stream_generator import TestDataGenerator
import os
from datetime import datetime, timedelta
import time
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from .kafka_publisher import MSKTokenProvider
import socket
import logging


def run_kafka_publisher(email, name, ds_id, bootstrap_servers, region_name):
    publisher = KafkaPublisher(email, name, ds_id, bootstrap_servers, region_name)
    topic = f'{email.split("@")[0]}_{name}_{ds_id}'
    token_provider = MSKTokenProvider(region_name)

    try:
        admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers,
                                        security_protocol='SASL_SSL',
                                        sasl_mechanism='OAUTHBEARER',
                                        sasl_oauth_token_provider=token_provider,
                                        client_id=socket.gethostname(),
                                        )
        topic_list = [NewTopic(name=topic, num_partitions=2, replication_factor=1)]
        admin_client.create_topics(new_topics=topic_list, validate_only=False)

    except TopicAlreadyExistsError:
        print(f"{topic} 토픽이 이미 존재합니다. 토픽 생성이 중지됩니다.")  

    # 테스트 데이터 생성
    data_generator = TestDataGenerator()

    try:
        while True:
            try:
                data_list = data_generator.get_data()
                enriched_data = {
                    "endpoint": data_list['endpoint'],
                    "topic": topic,
                    "email": email,
                    "name" : name, 
                    "ds_id": ds_id,
                    "timestamp": datetime.now().isoformat(),
                    "data": data_list['data']
                }
                publisher.publish_data(enriched_data)
                print(enriched_data)
                time.sleep(1)
            except Exception as e:
                logging.error(f"Error publishing data: {str(e)}")
                # 잠시 대기 후 계속 진행
                time.sleep(5)

    except Exception as e:
        print(f"Error in Kafka publisher: {str(e)}")
    finally:
        publisher.close()

class SubprocessManager:
    def __init__(self):
        self.processes = {}

    def start_process(self, email, name, ds_id):
        topic = f'{email.split("@")[0]}_{name}_{ds_id}'
        if email in self.processes and topic in self.processes[email]:
            return False
        
        bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        region_name = os.getenv("AWS_REGION")
        
        process = multiprocessing.Process(
            target=run_kafka_publisher,
            args=(email, name, ds_id, bootstrap_servers, region_name)
        )
        process.start()
        
        if email not in self.processes:
            self.processes[email] = {}
        self.processes[email][topic] = {'process': process}
        return True

    def stop_process(self, email, topic):
        try:
            if email not in self.processes or topic not in self.processes[email]:
                return False
        
            process_info = self.processes[email][topic]
            process = process_info['process']
            process.terminate()
            process.join(timeout=5)

            if process.is_alive():
                process.kill()  # 강제 종료
        
            del self.processes[email][topic]
            if not self.processes[email]:
                del self.processes[email]
            
            return True
        except Exception as e:
            logging.error(f"Error stopping process: {str(e)}")
            return False

subprocess_manager = SubprocessManager()
