package kafkastreams.streams;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.Topology;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.Produced;
import org.json.JSONObject;

import aws_msk_iam_auth_shadow.com.fasterxml.jackson.databind.util.JSONPObject;
import kafkastreams.utils.util;
import kafkastreams.kafka.topic;

import java.util.ArrayList;
import java.util.Properties;

public class topology {
    // 클래스 객체 생성
    static util ut = new util();
    static topic topic = new topic();
    static properties props = new properties();

    // 변환 수식을 이용하여 value 값 변환
    public KafkaStreams mathExpression(String bootstrap_servers, String topic_Name, String user_Role, String var_Name) {
        StreamsBuilder builder = new StreamsBuilder();

        KStream<String, String> topic_Data = builder.stream(topic_Name);
        
        KStream<String, String> calculate = topic_Data.mapValues(
            value -> {
                try {
                    // user_Role에 맞게 결과 도출
                    ArrayList<String> regex_ArrayList = ut.parseUserRole(user_Role, value);
                    double result = ut.parseCalculate(regex_ArrayList);

                    // 결과값 value_Json에 삽입
                    JSONObject value_Json = new JSONObject(value);
                    JSONObject data_Json = value_Json.optJSONObject("data").put(var_Name, result);
                    value_Json.put("data", data_Json);

                    // String 타입으로 리턴
                    return value_Json.toString();
                } catch (Exception e) {
                    e.printStackTrace();
                    return value;
                }      
            } 
        );
        
        Properties topic_Props = topic.topicProperties(bootstrap_servers);
        topic.createTopic(topic_Props, topic_Name+"_Math");
        calculate.to(topic_Name+"_Math", Produced.with(Serdes.String(), Serdes.String()));

        Topology topology = builder.build();
        KafkaStreams streams = new KafkaStreams(topology, props.properties(bootstrap_servers, "MathExpression-Application"));

        return streams;
    }

    // value가 pivot를 넘는 값만 전송
    public KafkaStreams recordFilter(String bootstrap_servers, String topic_Name, String user_Role, String var_Name) {
        StreamsBuilder builder = new StreamsBuilder();

        KStream<String, String> topic_Data = builder.stream(topic_Name);

        int comparsion = ut.getComparsion(user_Role);
        double pivot = ut.getPivot(user_Role);
        
        KStream<String, String> record_Filter = topic_Data.filter(
            (key, value) -> {
                try {
                    JSONObject value_Json = new JSONObject(value);
                    double var = value_Json.getJSONObject("data").getDouble(var_Name);

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

        Properties topicProps = topic.topicProperties(bootstrap_servers);
        topic.createTopic(topicProps, topic_Name+"_Filter");
        record_Filter.to(topic_Name+"_Filter", Produced.with(Serdes.String(), Serdes.String()));

        Topology topology = builder.build();
        KafkaStreams streams = new KafkaStreams(topology, props.properties(bootstrap_servers, "RecordFilter-Application"));

        return streams;
    }
}
