package kafkastreams;

import org.apache.kafka.streams.KafkaStreams;

import kafkastreams.utils.util;
import kafkastreams.streams.topology;

public class Main {
    static util ut = new util();
    static topology topo = new topology();
    public static void main(String[] args) {
        // args[0] --> bootstrap_Servers
        // args[1] --> topic_Name
        // args[2] --> user_Role

        String bootstrap_servers = "b-2-public.dp.qp8s9a.c3.kafka.ap-northeast-2.amazonaws.com:9198,b-1-public.dp.qp8s9a.c3.kafka.ap-northeast-2.amazonaws.com:9198";
        String topic_Name = "user1_device4";
        String user_Role = "voc > 40";

        String[] patterns = {">", ">=", "<", "<=", "!=", "=="};

        boolean pattern_Found = false;

        for (String e : patterns) {
            if (user_Role.contains(e)) {
                pattern_Found = true;
                break;
            }
        }

        if (pattern_Found == false) {
            if (args[1].contains("=")) {
                // KafkaStreams Experssion
                String[] var_Name = ut.getVarName(args[2]);

                KafkaStreams streams = topo.mathExpression(args[0], args[1], args[2], var_Name[1]);

                streams.cleanUp();
                streams.start();

                Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
            } else {
                System.out.println("KafkaStreams 기능 없음");
            }
        } else {
            // KafkaStreams Filter
            String var_Name = ut.getVarName2(user_Role);

            KafkaStreams streams = topo.recordFilter(bootstrap_servers, topic_Name, user_Role, var_Name);

            streams.cleanUp();
            streams.start();

            Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
        }


        // user_Role 예시 = 유저가 저장하고 싶은 변수명 = 변환 수식
        // String user_Role = "data.temp1 = (data.temp1 * 9/5) + 32";
        // String[] var_Name = ut.getVarName(user_Role);
        
        // KafkaStreams Expression
        // KafkaStreams streams = topo.mathExpression(user_Role, var_Name[1], "user1_device1");

        // KafkaStreams filter
        // KafkaStreams streams = topo.recordFilter(35, "temp2", "user1_device1");

        // 자원, 상태 청소 및 데이터 처리 시작
        // streams.cleanUp();
        // streams.start();

        // jvm 종료 시 실행될 스레드 추가 => streams.close()
        // streams 객체 데이터 스트림, 네트워크 소켓, 파일 핸들러 종료
        // Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    } 
}
