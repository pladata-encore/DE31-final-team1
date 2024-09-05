package kafkastreams.kafka;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.CommonClientConfigs;
import org.apache.kafka.common.config.SaslConfigs;
import org.apache.kafka.common.serialization.Serdes;
import org.json.JSONObject;
import org.json.JSONArray;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Properties;
import java.nio.file.Files;
import java.nio.file.Paths;

public class producer {
    // 토픽 클래스 생성
    static topic topic = new topic();

    // Producer Properties 설정
    public Properties producerProperties(String bootstrap_servers) {
        Properties props = new Properties();

        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrap_servers);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, Serdes.String().serializer().getClass());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, Serdes.String().serializer().getClass());
        props.put(ProducerConfig.ACKS_CONFIG, "all");
        props.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        props.put(SaslConfigs.SASL_MECHANISM, "AWS_MSK_IAM");
        props.put(SaslConfigs.SASL_JAAS_CONFIG, "software.amazon.msk.auth.iam.IAMLoginModule required;");
        props.put(SaslConfigs.SASL_CLIENT_CALLBACK_HANDLER_CLASS, "software.amazon.msk.auth.iam.IAMClientCallbackHandler");
        
        return props;
    }

    public void kafkaProducer(String bootstrap_servers, Properties props, String file_Path) {
        // Properties 적용한 KafkaProducer 객체 생성
        // <String, String> --> <Key type, Value type>
        KafkaProducer<String, String> producer = new KafkaProducer<String, String>(props);

        // 파일 확장자 추출
        String[] split_String = file_Path.split("/");
        String last = split_String[split_String.length - 1];
        String type = last.split("\\.")[1];
        
        try {
            if (type.equals("json")) {
                // json 배열 파일 읽기
                String json_String = new String(Files.readAllBytes(Paths.get(file_Path)));
                JSONArray json_Array = new JSONArray(json_String);
                JSONObject json_Object = json_Array.getJSONObject(0);

                // 토픽 이름 생성
                String topic_Name = json_Object.getString("user") + "_" + json_Object.getString("device");

                // 토픽 생성
                Properties topic_Props = topic.topicProperties(bootstrap_servers);
                topic.createTopic(topic_Props, topic_Name);

                // json array의 레코드 한 줄씩 적재
                for (Object obj : json_Array) {
                    JSONObject d = (JSONObject) obj;
                    String reco = d.toString();
                    ProducerRecord<String, String> record = new ProducerRecord<String,String>(topic_Name, reco);
                    System.out.println("Send Massage <Key, Value> : " + record.key() + ", " + record.value());

                    // 내부 버퍼에 record 적재
                    producer.send(record);

                    // 내부 버퍼의 record가 Partitioner와 Accumulator를 통해 broker 토픽 적재
                    producer.flush();
                }
            } else if (type.equals("py")) {
                ProcessBuilder processBuilder = new ProcessBuilder("python3", file_Path);

                Process process = processBuilder.start(); 
                
                BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));

                // String r = reader.readLine();
                // JSONObject json_Object  = new JSONObject(r);
                
                // String topic_Name = json_Object.getString("user") + "_" + json_Object.getString("device");
 
                Properties topic_Props = topic.topicProperties(bootstrap_servers);
                topic.createTopic(topic_Props, "user1_device1");

                while(true) {
                    ProducerRecord<String, String> record = new ProducerRecord<String,String>("user1_device1", reader.readLine());
                    System.out.println("Send Massage <Key, Value> : " + record.key() + ", " + record.value());
                    
                    // 내부 버퍼에 record 적재
                    producer.send(record);

                    // 내부 버퍼의 record가 Partitioner와 Accumulator를 통해 broker 토픽 적재
                    producer.flush();
                }
            } else {
                System.out.println("파일 확장자 식별 실패");
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            producer.close();
        }
    }

    public static void main(String[] args) {
        // String bootstrap_servers = "b-2-public.dp.qp8s9a.c3.kafka.ap-northeast-2.amazonaws.com:9198,b-1-public.dp.qp8s9a.c3.kafka.ap-northeast-2.amazonaws.com:9198";        
        // Properties props = producerProperties(bootstrap_servers);
 
        // String file_Path = "/home/kkh/workspace/DE31-final-team1/TEST_FUNC/data_generator.py";
        // kafkaProducer(bootstrap_servers, props, file_Path);
    }
}
