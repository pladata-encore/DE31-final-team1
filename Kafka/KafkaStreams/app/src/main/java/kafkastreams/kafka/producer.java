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
    // 토픽 클래스 변수 생성
    static final String bootstrap_servers = "b-2-public.dp.ugprbm.c3.kafka.ap-northeast-2.amazonaws.com:9198,b-1-public.dp.ugprbm.c3.kafka.ap-northeast-2.amazonaws.com:9198";

    // Producer Properties 설정
    public Properties producerProperties() {
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

    public void kafkaProducer(Properties props, String file_Path) {
        // Properties 적용한 KafkaProducer 객체 생성
        // <String, String> --> <Key type, Value type>
        KafkaProducer<String, String> producer = new KafkaProducer<String, String>(props);

        try {
            String json_String = new String(Files.readAllBytes(Paths.get(file_Path)));
            JSONArray json_Array = new JSONArray(json_String);
            JSONObject json_Object = json_Array.getJSONObject(0);
            String topic_Name = json_Object.getString("user") + "_" + json_Object.getString("device");

            Properties topic_Props = topic.topicProperties();
            topic.createTopic(topic_Props, topic_Name);

            for (Object obj : json_Array) {
                JSONObject d = (JSONObject) obj;
                String rec = d.toString();
                ProducerRecord<String, String> record = new ProducerRecord<String,String>(topic_Name, rec);
                System.out.println("Send Massage <Key, Value> : " + record.key() + ", " + record.value());
                // 내부 버퍼에 record 적재
                producer.send(record);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            // 내부 버퍼의 record가 Partitioner와 Accumulator를 통해 broker 토픽 적재
            producer.flush();
            producer.close();
        }
    }

    public static void main(String[] args) {
        Properties props = new Properties();

        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrap_servers);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, Serdes.String().serializer().getClass());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, Serdes.String().serializer().getClass());
        props.put(ProducerConfig.ACKS_CONFIG, "all");
        props.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        props.put(SaslConfigs.SASL_MECHANISM, "AWS_MSK_IAM");
        props.put(SaslConfigs.SASL_JAAS_CONFIG, "software.amazon.msk.auth.iam.IAMLoginModule required;");
        props.put(SaslConfigs.SASL_CLIENT_CALLBACK_HANDLER_CLASS, "software.amazon.msk.auth.iam.IAMClientCallbackHandler");
        
        KafkaProducer<String, String> producer = new KafkaProducer<String, String>(props);
        
        // String data_Generator_Path = "/home/kkh/workspace/DE31-final-team1/TEST_FUNC/data_generator.py";
        // ProcessBuilder processBuilder = new ProcessBuilder("python3", data_Generator_Path);
        
        String data_Path = "/home/kkh/workspace/DE31-final-team1/Kafka/KafkaStreams/app/src/main/resources/test_data.json";
        
        try {
            // Process process = processBuilder.start(); 
            // BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            // while(true) {
            //     ProducerRecord<String, String> record = new ProducerRecord<String,String>("receive-test-topic", reader.readLine());
            //     producer.send(record);
            // }
            String jsonString = new String(Files.readAllBytes(Paths.get(data_Path, args)));
            JSONArray jsonArray = new JSONArray(jsonString);
            JSONObject jsonObject = jsonArray.getJSONObject(0);
            String topicName = jsonObject.getString("user") + "_" + jsonObject.getString("device");

            Properties topicProps = topic.topicProperties();
            topic.createTopic(topicProps, topicName);

            for (Object obj : jsonArray) {
                JSONObject d = (JSONObject) obj;
                String rec = d.toString();
                ProducerRecord<String, String> record = new ProducerRecord<String,String>(topicName, rec);
                System.out.println("Send Massage <Key, Value> : " + record.key() + ", " + record.value());
                producer.send(record);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            producer.flush();
            producer.close();
        }
    }    
}
