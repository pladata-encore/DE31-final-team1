package kafkastreams.kafka;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.CommonClientConfigs;
import org.apache.kafka.common.config.SaslConfigs;
import org.apache.kafka.common.serialization.Serdes;

import java.util.Properties;

public class producer {
    public static void main(String[] args) {
        Properties props = new Properties();

        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "MSK-IP:PORT");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, Serdes.String().serializer().getClass());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, Serdes.String().serializer().getClass());
        props.put(ProducerConfig.ACKS_CONFIG, "all");
        props.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        props.put(SaslConfigs.SASL_MECHANISM, "AWS_MSK_IAM");
        props.put(SaslConfigs.SASL_JAAS_CONFIG, "software.amazon.msk.auth.iam.IAMLoginModule required;");
        props.put(SaslConfigs.SASL_CLIENT_CALLBACK_HANDLER_CLASS, "software.amazon.msk.auth.iam.IAMClientCallbackHandler");
        
        KafkaProducer<String, String> producer = new KafkaProducer<String, String>(props);

        try {
            for(int i=0; i<100; i++) {
                ProducerRecord<String, String> record = new ProducerRecord<String,String>("Topic_Name", "Key"+i, "Value"+i);
                producer.send(record);
                System.out.println("Message Send: " + record.key() + ":" + record.value());
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            producer.close();
        }
    }    
}
