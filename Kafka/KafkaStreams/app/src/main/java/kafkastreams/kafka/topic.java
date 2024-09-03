package kafkastreams.kafka;

import org.apache.kafka.clients.admin.AdminClientConfig;
import org.apache.kafka.common.config.SaslConfigs;
import org.apache.kafka.clients.admin.AdminClient;
import org.apache.kafka.clients.admin.CreateTopicsResult;
import org.apache.kafka.clients.admin.NewTopic;
import org.apache.kafka.clients.admin.DeleteTopicsResult;
import org.apache.kafka.common.errors.TopicExistsException;
import org.apache.kafka.common.errors.UnknownTopicIdException;

import java.util.Collections;
import java.util.Properties;
import java.util.concurrent.ExecutionException;

public class topic {
    public Properties propertire(String bootstrap_servers) {
        Properties props = new Properties();

        props.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrap_servers);
        props.put(AdminClientConfig.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        props.put(SaslConfigs.SASL_MECHANISM, "AWS_MSK_IAM");
        props.put(SaslConfigs.SASL_JAAS_CONFIG, "software.amazon.msk.auth.iam.IAMLoginModule required;");
        props.put(SaslConfigs.SASL_CLIENT_CALLBACK_HANDLER_CLASS, "software.amazon.msk.auth.iam.IAMClientCallbackHandler");

        return props;
    }

    public void createTopic(Properties props, String topicName) {
        AdminClient adminClient = AdminClient.create(props);

        NewTopic newTopic = new NewTopic(topicName, 3, (short) 1);

        try {
            CreateTopicsResult result = adminClient.createTopics(Collections.singleton(newTopic));

            result.all().get();
            
            System.out.println("토픽 생성 완료");
        } catch (ExecutionException e) {
            if (e.getCause() instanceof TopicExistsException) {
                System.out.println("토픽 중복 에러");
            } else {
                e.printStackTrace();
                System.out.println("토픽 생성 실패");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            e.printStackTrace();
        } finally {
            adminClient.close();
        }
    }

    public void deleteTopic(Properties props, String topicName) {
        AdminClient adminClient = AdminClient.create(props);
        try {
            DeleteTopicsResult result = adminClient.deleteTopics(Collections.singleton(topicName));
                
            result.all().get();
            
            System.err.println("토픽 삭제 완료");
        } catch (ExecutionException e) {
            if (e.getCause() instanceof UnknownTopicIdException) {
                System.out.println("토픽 검색 실패");
            } else {
                e.printStackTrace();
                System.out.println("토픽 삭제 실패");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            e.printStackTrace();
        } finally {
            adminClient.close();
        }
    }
}
