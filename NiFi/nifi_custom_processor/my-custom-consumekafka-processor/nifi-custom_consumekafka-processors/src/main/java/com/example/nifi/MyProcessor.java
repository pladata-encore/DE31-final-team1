package com.example.nifi;

import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.CommonClientConfigs;
import org.apache.kafka.common.config.SaslConfigs;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.nifi.processor.AbstractProcessor;
import org.apache.nifi.processor.ProcessContext;
import org.apache.nifi.processor.ProcessSession;
import org.apache.nifi.processor.Relationship;
import org.apache.nifi.processor.exception.ProcessException;
import org.apache.nifi.annotation.behavior.EventDriven;
import org.apache.nifi.annotation.documentation.CapabilityDescription;
import org.apache.nifi.annotation.documentation.Tags;
import org.apache.nifi.annotation.lifecycle.OnStopped;
import org.apache.nifi.components.PropertyDescriptor;
import org.apache.nifi.processor.io.StreamCallback;
import org.apache.nifi.processor.util.StandardValidators;
import org.apache.nifi.flowfile.FlowFile;


import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.*;

@EventDriven
@CapabilityDescription("Consumes messages from AWS MSK and routes them as flow files.")
@Tags({"kafka", "aws", "msk", "consume", "example"})
public class MyProcessor extends AbstractProcessor {
    
    private KafkaConsumer<String, String> consumer;

    // Define relationships for the processor
    public static final Relationship SUCCESS = new Relationship.Builder()
            .name("SUCCESS")
            .description("Successfully received messages from Kafka")
            .build();

    @Override
    public Set<Relationship> getRelationships() {
        return Collections.singleton(SUCCESS);
    }

    // Properties for configuring Kafka consumer
    public static final PropertyDescriptor bootstrapServers = new PropertyDescriptor.Builder()
            .name("bootstrapServers")
            .description("The Kafka bootstrapServers to consume from.")
            .required(true)
            .addValidator(StandardValidators.NON_EMPTY_VALIDATOR)
            .build();

    public static final PropertyDescriptor TOPIC_NAME = new PropertyDescriptor.Builder()
            .name("Topic Name")
            .description("The Kafka topic(s) to consume from.")
            .required(true)
            .addValidator(StandardValidators.NON_EMPTY_VALIDATOR)
            .build();

    public static final PropertyDescriptor GROUP_ID = new PropertyDescriptor.Builder()
            .name("Group ID")
            .description("The consumer group ID to use when consuming from Kafka.")
            .required(true)
            .addValidator(StandardValidators.NON_EMPTY_VALIDATOR)
            .build();

    public static final PropertyDescriptor AUTO_OFFSET_RESET = new PropertyDescriptor.Builder()
            .name("Auto Offset Reset")
            .description("What to do when there is no initial offset in Kafka or if the current offset does not exist.")
            .required(true)
            .allowableValues("earliest", "latest", "none")
            .defaultValue("earliest")
            .build();


    @Override
    public List<PropertyDescriptor> getSupportedPropertyDescriptors() {
        final List<PropertyDescriptor> properties = new ArrayList<>();
        properties.add(bootstrapServers);
        properties.add(TOPIC_NAME);
        properties.add(GROUP_ID);
        properties.add(AUTO_OFFSET_RESET);
        return properties;
    }

    // Kafka consumer 설정을 위한 Properties 메서드
    public Properties properties(String bootstrapServers, String groupId, String autoOffsetReset) {
        Properties props = new Properties();
        
        // Kafka 서버 설정
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, groupId);
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, autoOffsetReset);
        props.put(ConsumerConfig.MAX_POLL_RECORDS_CONFIG, "1");
        // props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, true);

        // 데이터 직렬화 설정
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, Serdes.String().deserializer().getClass());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, Serdes.String().deserializer().getClass());

        // AWS MSK IAM 인증 설정
        props.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        props.put(SaslConfigs.SASL_MECHANISM, "AWS_MSK_IAM");
        props.put(SaslConfigs.SASL_JAAS_CONFIG, "software.amazon.msk.auth.iam.IAMLoginModule required;");
        props.put(SaslConfigs.SASL_CLIENT_CALLBACK_HANDLER_CLASS, "software.amazon.msk.auth.iam.IAMClientCallbackHandler");

        return props;
    }

    @Override
    public void onTrigger(ProcessContext context, ProcessSession session) throws ProcessException {
        String bootstrapServersValue  = context.getProperty(bootstrapServers).getValue(); //bootstrapServers 주소
        String topicName = context.getProperty(TOPIC_NAME).getValue();  // 토픽 이름
        String groupId = context.getProperty(GROUP_ID).getValue();  // 그룹id
        String autoOffsetReset = context.getProperty(AUTO_OFFSET_RESET).getValue();  // earliest or latest or none
        // Kafka consumer가 초기화되지 않은 경우 설정
        if (consumer == null) {
            Properties props = properties(bootstrapServersValue, groupId, autoOffsetReset);
            consumer = new KafkaConsumer<>(props);
            consumer.subscribe(Arrays.asList(topicName.split(",")));
        }

        try {
            ConsumerRecords<String, String> records = consumer.poll(1000);  // 1초 동안 메시지 폴링
            getLogger().info("Polled {} records from Kafka", new Object[]{records.count()});
            
            // 첫 번째 레코드만 처리
            if (!records.isEmpty()) {
                ConsumerRecord<String, String> record = records.iterator().next();

                // NiFi FlowFile 생성
                FlowFile flowFile = session.create();

                // FlowFile에 Kafka 메시지 내용을 쓰기
                flowFile = session.write(flowFile, new StreamCallback() {
                    @Override
                    public void process(InputStream inputStream, OutputStream outputStream) throws IOException {
                        if (record.value() != null) {
                            outputStream.write(record.value().getBytes());
                        } else {
                            getLogger().warn("Record value is null for key: {}", new Object[]{record.key()});
                        }
                    }
                });

                // FlowFile을 성공 관계로 전송
                session.transfer(flowFile, SUCCESS);
                getLogger().info("Successfully processed message with key: {}, value: {}", new Object[]{record.key(), record.value()});
            }
            // for (ConsumerRecord<String, String> record : records) {
            //     // NiFi FlowFile 생성
            //     FlowFile flowFile = session.create();

            //     // FlowFile에 Kafka 메시지 내용을 쓰기
            //     flowFile = session.write(flowFile, new StreamCallback() {
            //         @Override
            //         public void process(InputStream inputStream, OutputStream outputStream) throws IOException {
            //             if (record.value() != null) {
            //                 outputStream.write(record.value().getBytes());
            //             } else {
            //                 getLogger().warn("Record value is null for key: {}", new Object[]{record.key()});
            //             }
            //         }
            //     });

            //     // FlowFile을 성공 관계로 전송
            //     session.transfer(flowFile, SUCCESS);
            //     getLogger().info("Successfully processed message with key: {}, value: {}", new Object[]{record.key(), record.value()});
            // }
        } catch (Exception e) {
            getLogger().error("Error consuming records from Kafka", e);
            throw new ProcessException(e);
        }
    }
    @OnStopped
    public void onStopped() {
        if (consumer != null) {
        consumer.close();  // Kafka consumer 안전하게 종료
    }
        // discard reference; leave controller service state intact
        consumer = null;
    }
    
}
