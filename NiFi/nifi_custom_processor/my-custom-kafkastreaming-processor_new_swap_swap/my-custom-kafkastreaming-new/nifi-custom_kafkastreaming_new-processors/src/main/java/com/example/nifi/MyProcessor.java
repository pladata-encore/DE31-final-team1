/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.example.nifi;

// Nifi 라이브러리
import org.apache.nifi.components.PropertyDescriptor;
import org.apache.nifi.flowfile.FlowFile;
import org.apache.nifi.logging.ComponentLog;
import org.apache.nifi.annotation.behavior.ReadsAttribute;
import org.apache.nifi.annotation.behavior.ReadsAttributes;
import org.apache.nifi.annotation.behavior.WritesAttribute;
import org.apache.nifi.annotation.behavior.WritesAttributes;
import org.apache.nifi.annotation.lifecycle.OnScheduled;
import org.apache.nifi.annotation.lifecycle.OnStopped;
import org.apache.nifi.annotation.documentation.CapabilityDescription;
import org.apache.nifi.annotation.documentation.SeeAlso;
import org.apache.nifi.annotation.documentation.Tags;
import org.apache.nifi.processor.exception.ProcessException;
import org.apache.nifi.processor.AbstractProcessor;
import org.apache.nifi.processor.ProcessContext;
import org.apache.nifi.processor.ProcessSession;
import org.apache.nifi.processor.ProcessorInitializationContext;
import org.apache.nifi.processor.Relationship;
import org.apache.nifi.processor.util.StandardValidators;
import org.apache.nifi.annotation.behavior.SupportsBatching;
import org.apache.nifi.annotation.documentation.CapabilityDescription;
import org.apache.nifi.annotation.documentation.Tags;
import org.apache.nifi.annotation.lifecycle.OnScheduled;
import org.apache.nifi.processor.AbstractProcessor;
import org.apache.nifi.processor.ProcessContext;
import org.apache.nifi.processor.ProcessSession;
import org.apache.nifi.processor.Relationship;

// Kafka 라이브러리
import org.apache.kafka.clients.admin.AdminClient;
import org.apache.kafka.clients.admin.AdminClientConfig;
import org.apache.kafka.clients.admin.NewTopic;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.Topology;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.Produced;
import org.apache.kafka.common.config.SaslConfigs;
import org.apache.kafka.common.serialization.Serdes;

// GSON 라이브러리
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

// Java 라이브러리
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Properties;
import java.util.Set;
import java.util.Stack;
import java.util.regex.Pattern;
import java.util.regex.Matcher;


@SeeAlso({})
@Tags({"Kafka", "Streams", "Custom", "KKH"})
@CapabilityDescription("Custom Kafka Streams Processor for NiFi")
@ReadsAttributes({@ReadsAttribute(attribute="", description="")})
@WritesAttributes({@WritesAttribute(attribute="", description="")})
public class MyProcessor extends AbstractProcessor {
    private ComponentLog logger;
    private KafkaStreams kafkaStreams;

    public static final PropertyDescriptor BOOTSTRAP_SERVERS = new PropertyDescriptor.Builder()
            .name("BOOTSTRAP_SERVERS")
            .required(true)
            .addValidator(StandardValidators.NON_EMPTY_VALIDATOR)
            .build();

    public static final PropertyDescriptor TOPIC_NAME = new PropertyDescriptor.Builder()
            .name("Topic Name")
            .required(true)
            .addValidator(StandardValidators.NON_EMPTY_VALIDATOR)
            .build();

    public static final PropertyDescriptor USER_RULE = new PropertyDescriptor.Builder()
            .name("User Rule")
            .required(true)
            .addValidator(StandardValidators.NON_EMPTY_VALIDATOR)
            .build();

    public static final PropertyDescriptor APPLICATION_ID = new PropertyDescriptor.Builder()
            .name("Application ID")
            .required(true)
            .addValidator(StandardValidators.NON_EMPTY_VALIDATOR)
            .build();

    public static final Relationship REL_SUCCESS = new Relationship.Builder()
            .name("success")
            .description("Successfully processed FlowFiles")
            .build();

    public static final Relationship REL_FAILURE = new Relationship.Builder()
            .name("failure")
            .description("Failed to process FlowFiles")
            .build();

    @Override
    public List<PropertyDescriptor> getSupportedPropertyDescriptors() {
        final List<PropertyDescriptor> properties = new ArrayList<>();
        properties.add(BOOTSTRAP_SERVERS);
        properties.add(USER_RULE);
        properties.add(APPLICATION_ID);
        properties.add(TOPIC_NAME);
        return properties;
    }

    private Set<Relationship> relationships;

    @Override
    protected void init(final ProcessorInitializationContext context) {
        // 관계 설정
        final Set<Relationship> relationships = new HashSet<>();
        relationships.add(REL_SUCCESS);
        relationships.add(REL_FAILURE);
        this.relationships = Collections.unmodifiableSet(relationships);
        
    }

    @Override
    public Set<Relationship> getRelationships() {
        return this.relationships;
    }

    // 프로세서가 실행되기 전에 한 번 호출
    // 프로세서가 시작되기 전에 초기화 작업이나 한 번만 설정해야 할 리소스를 설정하는데 사용
    @OnScheduled
    public void onScheduled(final ProcessContext context) { //프로세서가 시작되거나 스케쥴될때 한번 프로세서 준비 broker연결
        logger = getLogger();
        logger.info("Starting Kafka Streams");
        String bootstrap_servers = context.getProperty(BOOTSTRAP_SERVERS).getValue();
        String application_id = context.getProperty(APPLICATION_ID).getValue();
        String topic_name = context.getProperty(TOPIC_NAME).getValue();
        String user_rule = context.getProperty(USER_RULE).getValue();

        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, application_id);
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrap_servers);
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        props.put(SaslConfigs.SASL_MECHANISM, "AWS_MSK_IAM");
        props.put(SaslConfigs.SASL_JAAS_CONFIG, "software.amazon.msk.auth.iam.IAMLoginModule required;");
        props.put(SaslConfigs.SASL_CLIENT_CALLBACK_HANDLER_CLASS, "software.amazon.msk.auth.iam.IAMClientCallbackHandler");

        KafkaStreams streams = createKafkaStreams(props, topic_name , user_rule,context);

        streams.cleanUp();
        streams.start();

        // Runtime.getRuntime().addShutdownHook(new Thread(streams::close));

        logger.info("Kafka Streams started successfully");
    }

    // 프로세서가 트리거될 때마다 호출
    // 데이터가 도착할 때마다 실행되는 코드
    // 실제로 데이터 처리를 수행하는 로직
    @Override
    public void onTrigger(final ProcessContext context, final ProcessSession session) throws ProcessException {
        // 데이터가 도착할 때마다 실행되는 로직을 작성
        // FlowFile flowFile = session.get();
        // if (flowFile == null) {
        //     return;
        // }

        // Kafka Streams 처리된 결과를 NiFi의 플로우파일로 변환 및 저장
        // String processedData = "Processed Kafka Stream Data";  // 여기서 Kafka 결과를 가져옴
        // flowFile = session.write(flowFile, outputStream -> {
        //     outputStream.write(processedData.getBytes());
        // });

        // 완료된 플로우파일을 전송
        // session.transfer(flowFile, REL_SUCCESS);
    }

    @OnStopped
    public void onStopped() {
        if (kafkaStreams != null) {
            logger.info("Stopping Kafka Streams");
            kafkaStreams.close();
            logger.info("Kafka Streams stopped successfully");
        }
    }

    public KafkaStreams createKafkaStreams(Properties props, String topic_Name, String user_Rule,ProcessContext context) {
        // user_Rule 파싱
        String[] rule = user_Rule.split(",");
        
        // KafkaStreams Processor Builder
        StreamsBuilder builder = new StreamsBuilder();

        // Input Stream Processor
        KStream<String, String> topic_Data = builder.stream(topic_Name);

        int comparsion = getComparsion(rule[0]);
        double pivot = getPivot(rule[0]);

        String var_Name1 = getVarName2(rule[0]);
        String var_Name2 = getVarName(rule[1]);

        KStream<String, String> calculate = topic_Data.filter(
            (key, value) -> {
                if (rule[0] == null) {
                    return value != null;
                }

                try {
                    JsonObject value_Json = JsonParser.parseString(value).getAsJsonObject();
                    double var = value_Json.getAsJsonObject("data").get(var_Name1).getAsDouble();

                    switch (comparsion) {
                        case 1:
                            return var >= pivot;
                        case 2:
                            return var > pivot;
                        case 3:
                            return var <= pivot;
                        case 4:
                            return var < pivot;
                        case 5:
                            return var != pivot;
                        case 6:
                            return var == pivot;
                        default:
                            throw new IllegalArgumentException("Invalid comparison operator: " + comparsion);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                    return false;
                }
            }
        ).mapValues(
            (key,value) -> {
                try {   
                    // user_Role에 맞게 결과 도출
                    ArrayList<String> regex_ArrayList = parseUserRule(rule[1], value);
                    double result = parseCalculate(regex_ArrayList);
                    
                    // 결과값 value_Json에 삽입
                    JsonObject value_Json = JsonParser.parseString(value).getAsJsonObject();
                    JsonObject data_Json = value_Json.getAsJsonObject("data");
                    // logger.info("Processed Kafka Record - Key: " + key + ", Processed Value: " + jsonObject.toString());
                    data_Json.addProperty(var_Name2, result);
                    value_Json.add("data", data_Json);

                    // String 타입으로 리턴
                    return value_Json.toString();
                } catch (Exception e) {
                    e.printStackTrace();
                    return value;
                }      
            }
        );

        createTopicIfNotExists(topic_Name+"_Application", context);
        calculate.to(topic_Name+"_Application", Produced.with(Serdes.String(), Serdes.String()));

        
        Topology topology = builder.build();
        KafkaStreams streams = new KafkaStreams(topology, props);
        return streams;
    }

    // 변환 수식을 이용하여 value 값 변환
    public KafkaStreams mathExpression(String topic_Name, String user_Rule, String var_Name, Properties props,ProcessContext context) {
        StreamsBuilder builder = new StreamsBuilder();

        KStream<String, String> topic_Data = builder.stream(topic_Name);
        
        KStream<String, String> calculate = topic_Data.mapValues(
            value -> {
                try {
                    // user_Role에 맞게 결과 도출
                    ArrayList<String> regex_ArrayList = parseUserRule(user_Rule, value);
                    double result = parseCalculate(regex_ArrayList);

                    // 결과값 value_Json에 삽입
                    JsonObject value_Json = JsonParser.parseString(value).getAsJsonObject();
                    JsonObject data_Json = value_Json.getAsJsonObject("data");
                    data_Json.addProperty(var_Name, result);
                    value_Json.add("data", data_Json);

                    // String 타입으로 리턴
                    return value_Json.toString();
                } catch (Exception e) {
                    e.printStackTrace();
                    return value;
                }      
            } 
        );
        
        createTopicIfNotExists(topic_Name+"_Math",context);
        calculate.to(topic_Name+"_Math", Produced.with(Serdes.String(), Serdes.String()));

        Topology topology = builder.build();
        KafkaStreams streams = new KafkaStreams(topology, props);

        return streams;
    }

    // value가 pivot를 넘는 값만 전송
    public KafkaStreams recordFilter(String topic_Name, String user_Rule, String var_Name, Properties props,ProcessContext context) {
        StreamsBuilder builder = new StreamsBuilder();

        KStream<String, String> topic_Data = builder.stream(topic_Name);

        int comparsion = getComparsion(user_Rule);
        double pivot = getPivot(user_Rule);
        
        KStream<String, String> record_Filter = topic_Data.filter(
            (key, value) -> {
                try {
                    JsonObject value_Json = JsonParser.parseString(value).getAsJsonObject();
                    double var = value_Json.getAsJsonObject("data").get(var_Name).getAsDouble();

                    switch (comparsion) {
                        case 1:
                            return var > pivot;
                        case 2:
                            return var >= pivot;
                        case 3:
                            return var < pivot;
                        case 4:
                            return var <= pivot;
                        case 5:
                            return var != pivot;
                        case 6:
                            return var == pivot;
                        default:
                            throw new IllegalArgumentException("Invalid comparison operator: " + comparsion);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                    return false;
                }
            }
        );

        createTopicIfNotExists(topic_Name+"_Filter", context);
        record_Filter.to(topic_Name+"_Filter", Produced.with(Serdes.String(), Serdes.String()));

        Topology topology = builder.build();
        KafkaStreams streams = new KafkaStreams(topology, props);

        return streams;
    }

    public void createTopicIfNotExists(String topicName, ProcessContext context) {
        Properties props =  new Properties();
        String bootstrap_servers = context.getProperty(BOOTSTRAP_SERVERS).getValue(); 
        props.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrap_servers);
        props.put(AdminClientConfig.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        props.put(SaslConfigs.SASL_MECHANISM, "AWS_MSK_IAM");
        props.put(SaslConfigs.SASL_JAAS_CONFIG, "software.amazon.msk.auth.iam.IAMLoginModule required;");
        props.put(SaslConfigs.SASL_CLIENT_CALLBACK_HANDLER_CLASS, "software.amazon.msk.auth.iam.IAMClientCallbackHandler");
        try (AdminClient adminClient = AdminClient.create(props)) {
            // 토픽이 없으면 생성
            if (!adminClient.listTopics().names().get().contains(topicName)) {
                NewTopic newTopic = new NewTopic(topicName, 2, (short) 1); // 파티션 수와 복제본 수 설정
                adminClient.createTopics(Collections.singleton(newTopic));
                logger.info("Created topic: " + topicName);
            }
        } catch (Exception e) {
            logger.error("Failed to create topic " + topicName, e);
        }
    }

    // --------------------> KafkaStreams.Math_Expresstion <-------------------------- \\
    // 사칙계산
    public double calculate(String operator, double x, double y) {
        switch (operator) {
            case "+": return x + y;
            case "-": return x - y;
            case "*": return x * y;
            case "/": return x / y;
            default: throw new IllegalArgumentException("틀린 연산자 : " + operator);
        }
    }

    // user_Rule 파싱하여 목적 변수 return
    public String getVarName(String user_Rule) {
        String var = user_Rule.split("=")[0].strip();

        if (var.contains(".") || var.contains("_")) {
            String[] split_String = var.split("[._]");
            var = split_String[split_String.length - 1];
            return var;
        }

        return var;
    }

    // user_Rule 파싱하여 변환 수식 return
    public String getVarExpresstion(String user_Rule) {
        return user_Rule.split("=")[1].strip();
    }

    // user_Rule 파싱하고 변수 치환
    public ArrayList<String> parseUserRule(String user_Rule, String input_Data) {
        // var_Expresstion => 유저가 입력한 변환 수식
        String var_Expresstion = getVarExpresstion(user_Rule);

        // 입력 데이터 => json 타입 데이터형 변환, data json 추출
        JsonObject input_Json = JsonParser.parseString(input_Data).getAsJsonObject();
        JsonObject data_Json = input_Json.getAsJsonObject("data");

        // 문자열 수식을 정규표현식을 사용하여 ArrayList에 적재
        Pattern pattern = Pattern.compile("([a-zA-Z][a-zA-Z0-9_\\.]*|\\+|\\-|\\*|\\/|\\=|\\(|\\))");
        Matcher matcher = pattern.matcher(var_Expresstion);

        ArrayList<String> regex_ArrayList = new ArrayList<>();

        while (matcher.find()) {
            regex_ArrayList.add(matcher.group());
        }

        // 변수를 value 값으로 치환
        for (int i=0; i<regex_ArrayList.size(); i++) {
            String token = regex_ArrayList.get(i);

            if (token.contains(".") || token.contains("_")) {
                String[] split_String = token.split("[._]");
                token = split_String[split_String.length - 1];
            }

            if (token.matches("[a-zA-Z][a-zA-Z0-9]+")) {
                regex_ArrayList.set(i, String.valueOf(data_Json.get(token).getAsDouble()));
            }
        }

        return regex_ArrayList;
    }

    // 파싱된 수식 계산
    public double parseCalculate(ArrayList<String> regex_ArrayList) {
        Stack<String> stack = new Stack<>();
        ArrayList<String> arrayList = new ArrayList<>();
        
        // 연산 우선순위에 맞게 arrayList 적재
        for (String e : regex_ArrayList) {
            if (e.equals("(")) {
                stack.push(e);
            } else if (e.equals(")")) {
                while (!stack.empty() && !stack.peek().equals("(")) {
                    arrayList.add(stack.pop());
                }
            } else if (e.equals("+") || e.equals("-")) {
                while (!stack.empty() && stack.peek().equals("*") || stack.peek().equals("/")) {
                    arrayList.add(stack.pop());
                }
                stack.push(e);
            } else if (e.equals("*") || e.equals("/")) {
                stack.push(e);
            } else {
                arrayList.add(e);
            }
        }

        while (!stack.empty()) {
            if (!stack.peek().equals("(")) {
                arrayList.add(stack.pop());
            } else {
                stack.pop();
            }
        }

        double x = 0.0, y = 0.0;
        Stack<Double> stack2 = new Stack<>();
        // 후열계산법
        for (String e : arrayList) {
            if (!e.equals("+") && !e.equals("-") && !e.equals("*") && !e.equals("/")) {
                stack2.push(Double.parseDouble(e));
            } else {
                y = stack2.pop();
                x = stack2.pop();
                stack2.push(calculate(e, x, y));
            }
        }
        return stack2.pop();
    }
    // --------------------> KafkaStreams.Math_Expresstion <-------------------------- \\

    // --------------------> KafkaStreams.filter <------------------------------------ \\
    // 비교연산자 치환
    public int getComparsion(String user_Rule) {
        if (user_Rule.contains(">=")) {
            return 1;
        } else if (user_Rule.contains(">")) {
            return 2;
        } else if (user_Rule.contains("<=")) {
            return 3;
        } else if (user_Rule.contains("<")) {
            return 4;
        } else if (user_Rule.contains("!=")) {
            return 5;
        } else if (user_Rule.contains("==")) {
            return 6;
        } else {
            return 0;
        }
    }

    // pivot 값 파싱
    public double getPivot(String user_Rule) {
        String[] split_String = user_Rule.split("\\s*(>=|<=|!=|==|>|<)\\s*");

        String pivot = split_String[1];

        return Double.parseDouble(pivot);
    }

    public String getVarName2(String user_Rule) {
        String var = user_Rule.split("\\s*(>=|<=|!=|==|>|<)\\s*")[0].strip();

        if (var.contains(".") || var.contains("_")) {
            String[] split_String = var.split("[._]");
            var = split_String[split_String.length - 1];
            return var;
        }

        return var;
    }
    // --------------------> KafkaStreams.filter <------------------------------------ \\
}
