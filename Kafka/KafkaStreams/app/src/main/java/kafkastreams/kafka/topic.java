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
    public Properties topicProperties(String bootstrap_servers) {
        Properties props = new Properties();

        props.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrap_servers);
        props.put(AdminClientConfig.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        props.put(SaslConfigs.SASL_MECHANISM, "AWS_MSK_IAM");
        props.put(SaslConfigs.SASL_JAAS_CONFIG, "software.amazon.msk.auth.iam.IAMLoginModule required;");
        props.put(SaslConfigs.SASL_CLIENT_CALLBACK_HANDLER_CLASS, "software.amazon.msk.auth.iam.IAMClientCallbackHandler");

        return props;
    }

    public void createTopic(Properties props, String topic_Name) {
        AdminClient admin_Client = AdminClient.create(props);

        NewTopic new_Topic = new NewTopic(topic_Name, 3, (short) 1);

        try {
            // Topic 중복 확인
            ListTopicsResult list_Topic = admin_Client.listTopics();
            Set<String> topics = list_Topic.names().get();

            for (String e : topics) {
                if (e.equals(topic_Name)) {
                    System.out.println("토픽이 이미 존재합니다.");
                    break;
                } 
            }

            // 토픽 생성 비동기 처리로 진행, 하나의 토픽만을 포함하는 불변(Set) 컬렉션 생성
            CreateTopicsResult result = admin_Client.createTopics(Collections.singleton(new_Topic));
            // 비동기 처리가 무사히 완료될 때까지 기다리다 완료
            result.all().get();

            System.out.println("토픽 생성 완료 : " + topic_Name);
            
        } catch (ExecutionException e) {
            if (e.getCause() instanceof TopicExistsException) {
                System.err.println("토픽 중복 에러");
            } else {
                e.printStackTrace();
            }
        } catch (InterruptedException e) {
            // 상위 매서드가 해당 코드에서 인터럽트가 발생한 것을 알리기 위한 예외 처리
            Thread.currentThread().interrupt();
        } finally {
            admin_Client.close();
        }
    }

    public void deleteTopic(Properties props, String topic_Name) {
        AdminClient admin_Client = AdminClient.create(props);
        try {
            // 토픽 삭제 비동기 처리로 진행, 하나의 토픽만을 포함하는 불변(Set) 컬렉션 생성
            DeleteTopicsResult result = admin_Client.deleteTopics(Collections.singleton(topic_Name));
            // 비동기 처리가 무사히 완료될 때까지 기다리다 완료
            result.all().get();
            
            System.err.println("토픽 삭제 완료 : " + topic_Name);
        } catch (ExecutionException e) {
            if (e.getCause() instanceof UnknownTopicIdException) {
                System.out.println("토픽 검색 실패");
            } else {
                e.printStackTrace();
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            admin_Client.close();
        }
    }

    public void listTopics(Properties props) {
        AdminClient admin_Client = AdminClient.create(props);

        try {
            ListTopicsResult list_Topics = admin_Client.listTopics();

            Set<String> topics = list_Topics.names().get();

            for (String e : topics) {
                System.out.println("ListTopics : " + e);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            admin_Client.close();
        }
    }
}
