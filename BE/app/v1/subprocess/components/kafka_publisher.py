from kafka import KafkaProducer
from kafka.errors import KafkaError
import socket
import json
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider


class MSKTokenProvider:
    def __init__(self, region_name):
        self.region_name = region_name

    def token(self):
        token, _ = MSKAuthTokenProvider.generate_auth_token(
            self.region_name
            )
        return token

class KafkaPublisher:
    def __init__(self, email, name, ds_id, bootstrap_servers, region_name):
        self.email = email
        self.name = name
        self.ds_id = ds_id
        self.region_name = region_name
        self.bootstrap_servers = bootstrap_servers

        
        # SASL/IAM을 위한 Kafka 클라이언트 설정
        self.token_provider = MSKTokenProvider(region_name=self.region_name)

        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            security_protocol='SASL_SSL',
            sasl_mechanism='OAUTHBEARER',
            sasl_oauth_token_provider=self.token_provider,
            client_id=socket.gethostname()
        )

    def publish_data(self, topic, data):
        try:
            self.producer.send(topic, value=data)
            self.producer.flush()
            print(f"Message sent: {data}")
        except KafkaError as e:
            print(f"Failed to send message: {e}")

    def close(self):
        self.producer.close()
