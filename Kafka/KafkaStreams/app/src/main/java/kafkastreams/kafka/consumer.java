package kafkastreams.kafka;

import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.CommonClientConfigs;
import org.apache.kafka.common.config.SaslConfigs;
import org.apache.kafka.common.serialization.Serdes;

import java.util.Properties;
import java.util.Arrays;

public class consumer {

    public static void main(String[] args) {
        Properties props = new Properties();
        
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "MSK-IP:PORT");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "test_group_id");
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earlist");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, Serdes.String().deserializer().getClass());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, Serdes.String().deserializer().getClass());
        props.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        props.put(SaslConfigs.SASL_MECHANISM, "AWS_MSK_IAM");
        props.put(SaslConfigs.SASL_JAAS_CONFIG, "software.amazon.msk.auth.iam.IAMLoginModule required;");
        props.put(SaslConfigs.SASL_CLIENT_CALLBACK_HANDLER_CLASS, "software.amazon.msk.auth.iam.IAMClientCallbackHandler");

        KafkaConsumer<String, String> consumer = new KafkaConsumer<String, String>(props);

        consumer.subscribe(Arrays.asList("Topic_Name"));

        try {
            while(true) {
                ConsumerRecords<String, String> records = consumer.poll(100);
                for(ConsumerRecord<String, String> record : records) {
                    System.out.println("Simple String Massage: " + String.valueOf(record.value()));
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
