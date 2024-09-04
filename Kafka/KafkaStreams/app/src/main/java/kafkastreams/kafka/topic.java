package kafkastreams.kafka;

import org.apache.kafka.clients.admin.AdminClientConfig;
import org.apache.kafka.common.config.SaslConfigs;
import org.apache.kafka.clients.admin.AdminClient;
import org.apache.kafka.clients.admin.CreateTopicsResult;
import org.apache.kafka.clients.admin.NewTopic;
import org.apache.kafka.clients.admin.DeleteTopicsResult;
import org.apache.kafka.clients.admin.ListTopicsResult;
import org.apache.kafka.common.errors.TopicExistsException;
import org.apache.kafka.common.errors.UnknownTopicIdException;

import java.util.Collections;
import java.util.Properties;
import java.util.Set;
import java.util.concurrent.ExecutionException;

public class topic {
    static final String bootstrap_servers = "b-2-public.dp.ugprbm.c3.kafka.ap-northeast-2.amazonaws.com:9198,b-1-public.dp.ugprbm.c3.kafka.ap-northeast-2.amazonaws.com:9198";

    public static Properties topicProperties() {
        Properties props = new Properties();

        props.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrap_servers);
        props.put(AdminClientConfig.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        props.put(SaslConfigs.SASL_MECHANISM, "AWS_MSK_IAM");
        props.put(SaslConfigs.SASL_JAAS_CONFIG, "software.amazon.msk.auth.iam.IAMLoginModule required;");
        props.put(SaslConfigs.SASL_CLIENT_CALLBACK_HANDLER_CLASS, "software.amazon.msk.auth.iam.IAMClientCallbackHandler");

        return props;
    }

    public static void createTopic(Properties props, String topic_Name) {
        AdminClient admin_Client = AdminClient.create(props);

        NewTopic new_Topic = new NewTopic(topic_Name, 3, (short) 1);

        try {
            CreateTopicsResult result = admin_Client.createTopics(Collections.singleton(new_Topic));

            result.all().get();
            
            System.out.println("토픽 생성 완료 : " + topic_Name);
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
            admin_Client.close();
        }
    }

    public void deleteTopic(Properties props, String topic_Name) {
        AdminClient admin_Client = AdminClient.create(props);
        try {
            DeleteTopicsResult result = admin_Client.deleteTopics(Collections.singleton(topic_Name));
                
            result.all().get();
            
            System.err.println("토픽 삭제 완료 : " + topic_Name);
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
            admin_Client.close();
        }
    }

    public static void listTopics(Properties props) {
        AdminClient admin_Client = AdminClient.create(props);

        try {
            ListTopicsResult list_Topics = admin_Client.listTopics();

            Set<String> topics = list_Topics.names().get();

            for (String e : topics) {
                System.out.println("ListTopics : " + e);
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("토픽 리스트 조회 실패");
        } finally {
            admin_Client.close();
        }
    }

    public static void main(String[] args) {
        Properties props = topicProperties();
        //createTopic(props, "user1_device3");
        listTopics(props);
    }
}
