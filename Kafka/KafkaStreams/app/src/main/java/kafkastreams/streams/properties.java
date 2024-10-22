package kafkastreams.streams;

import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.common.config.SaslConfigs;
import org.apache.kafka.common.serialization.Serdes;

import java.util.Properties;

public class properties {
    public Properties properties(String bootstrap_servers, String application_Id) {
        Properties props = new Properties();

        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrap_servers);
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, application_Id);
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        props.put(SaslConfigs.SASL_MECHANISM, "AWS_MSK_IAM");
        props.put(SaslConfigs.SASL_JAAS_CONFIG, "software.amazon.msk.auth.iam.IAMLoginModule required;");
        props.put(SaslConfigs.SASL_CLIENT_CALLBACK_HANDLER_CLASS, "software.amazon.msk.auth.iam.IAMClientCallbackHandler");

        return props;
    }    
}
