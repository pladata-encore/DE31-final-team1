package kafkastreams.streams;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.Topology;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.Produced;
import org.json.JSONObject;

import kafkastreams.utils.util;

import java.util.ArrayList;

public class topology {
    // 다른 로컬 패키지에서 클래스 불러오기
    static util ut = new util();
    static properties props = new properties();

    // 변환 수식을 이용하여 value 값 변환
    public KafkaStreams mathExpression(String user_Role, String var_Name) {
        StreamsBuilder builder = new StreamsBuilder();

        KStream<String, String> topic_Data = builder.stream("receive_test_topic");
        
        KStream<String, String> calculate = topic_Data.mapValues(
            value -> {
                try {
                    ArrayList<String> regex_ArrayList = ut.parseUserRole(user_Role, var_Name);
                    double result = ut.parseCalculate(regex_ArrayList);

                    JSONObject value_Json = new JSONObject(value);
                    JSONObject data_Json = value_Json.optJSONObject("data").put(var_Name, result);
                    value_Json.put("data", data_Json);

                    return value_Json.toString();
                } catch (Exception e) {
                    e.printStackTrace();
                    return value;
                }      
            } 
        );
        
        calculate.to("send_test_topic", Produced.with(Serdes.String(), Serdes.String()));

        Topology topology = builder.build();
        KafkaStreams streams = new KafkaStreams(topology, props.properties("MathExpression-Application"));

        return streams;
    }

    // value가 pivot를 넘는 값만 전송
    public KafkaStreams recordFilter(String var_Name, double pivot) {
        StreamsBuilder builder = new StreamsBuilder();

        KStream<String, String> topic_Data = builder.stream("receive_test_topic");

        KStream<String, String> record_Filter = topic_Data.filter(
            (key, value) -> new JSONObject(value).getJSONObject("data").getDouble(var_Name) > pivot
        );

        record_Filter.to("send_test_topic", Produced.with(Serdes.String(), Serdes.String()));

        Topology topology = builder.build();
        KafkaStreams streams = new KafkaStreams(topology, props.properties("RecordFilter-Application"));

        return streams;
    }
}
