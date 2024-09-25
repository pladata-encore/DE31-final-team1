package kafkastreams;

// dotenv 라이브러리
import io.github.cdimascio.dotenv.Dotenv;

// Java 라이브러리
import java.util.ArrayList;

// Kafka 라이브러리
import org.apache.kafka.streams.KafkaStreams;

// 내부 라이브러리
import kafkastreams.utils.util;
import kafkastreams.streams.topology;

public class Main {
    static util ut = new util();
    static topology topo = new topology();
    public static void main(String[] args) {
        Dotenv dotenv = Dotenv.load();

        String bootstrap_servers = dotenv.get("BOOTSTRAP_SERVER");
        String topic_Name = "user1_device1";
        String user_Rule = "pm1 < 20, result = (pm1 + 20) / 0.5";

        // <------------------------------ case 1: Filter.MapValues 통합 ----------------------------------> \\
        KafkaStreams streams = topo.createKafkaStreams(bootstrap_servers, topic_Name, user_Rule);

        streams.cleanUp();
        streams.start();

        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
        // ------------------------------> case 1: Filter.MapValues 통합 <---------------------------------- \\


        // <------------------------------ case 2: Filter, MapValues 분리 ---------------------------------> \\
        // String[] patterns = {">", ">=", "<", "<=", "!=", "=="};

        // boolean pattern_Found = false;

        // for (String e : patterns) {
        //     if (user_Rule.contains(e)) {
        //         pattern_Found = true;
        //         break;
        //     }
        // }

        // if (pattern_Found == false) {
        //     if (user_Rule.contains("=")) {
        //         // KafkaStreams Experssion
        //         String var_Name = ut.getVarName(user_Rule);

        //         KafkaStreams streams = topo.mathExpression(bootstrap_servers, topic_Name, user_Rule, var_Name);

        //         streams.cleanUp();
        //         streams.start();

        //         Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
        //     } else {
        //         System.out.println("KafkaStreams 기능 없음");
        //     }
        // } else {
        //     // KafkaStreams Filter
        //     String var_Name = ut.getVarName2(user_Rule);

        //     KafkaStreams streams = topo.recordFilter(bootstrap_servers, topic_Name, user_Rule, var_Name);

        //     streams.cleanUp();
        //     streams.start();

        //     Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
        // }
        // ------------------------------> case 1: Filter.MapValues 분리 <---------------------------------- \\
    }
}
