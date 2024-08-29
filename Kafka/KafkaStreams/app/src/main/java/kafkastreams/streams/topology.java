package kafkastreams.streams;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.Topology;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.processor.api.ProcessorSupplier;
import org.apache.kafka.streams.state.KeyValueStore;
import org.apache.kafka.streams.state.StoreBuilder;
import org.apache.kafka.streams.state.Stores;
import org.json.JSONObject;

import kafkastreams.utils.util;
import kafkastreams.utils.util.*;
import kafkastreams.streams.properties.*;

public class topology {
    static util ut = new util();
    static properties props = new properties();

    public KafkaStreams mathExpression() {
        StreamsBuilder builder = new StreamsBuilder();

        KStream<String, String> topic_Data = builder.stream("receive_test_topic");
        StoreBuilder<KeyValueStore<String, String>> keyvalueBuilder = Stores.keyValueStoreBuilder(
                                                                    Stores.persistentKeyValueStore("myProcessorState"), 
                                                                    Serdes.String(), 
                                                                    Serdes.String()
                                                                );
        KStream<String, String> calculate = topic_Data.processValues(
            new ProcessorSupplier() {
                public Processor get() {
                    ut.parseUserRole(null, null);
                    ut.parseCalculate(null)
                    return 
                }
            },
            "myProcessorState");
    }

    public KafkaStreams recordFilter(String var_Name, int pivot) {
        StreamsBuilder builder = new StreamsBuilder();

        KStream<String, String> topic_Data = builder.stream("receive_test_topic");

        KStream<String, String> record_Filter = topic_Data.filter((key, value),
        JSONObject(value).getJSONObject("data").getDouble(var_Name) > pivot);

        record_Filter.to("send_test_topic");

        Topology topology = builder.build();
        KafkaStreams streams = new KafkaStreams(topology, props.properties("RecordFilter-Application"));
    }
}
