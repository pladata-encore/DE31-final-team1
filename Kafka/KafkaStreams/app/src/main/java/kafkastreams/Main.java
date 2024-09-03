package kafkastreams;

import org.apache.kafka.streams.KafkaStreams;

import kafkastreams.utils.util;
import kafkastreams.streams.topology;

public class Main {
    static util ut = new util();
    static topology topo = new topology();
    public static void main(String[] args) {
        // user_Role 예시 = 유저가 저장하고 싶은 변수명 = 변환 수식
        String user_Role = "data.temp1 = (data.temp1 * 9/5) + 32";
        String[] var_Name = ut.getVarName(user_Role);
        
        // kafka topic value 값 변환 kafkastreams 기능 선언
        KafkaStreams streams = topo.mathExpression(user_Role, var_Name[1], "user1_device1");

        // 자원, 상태 청소 및 데이터 처리 시작
        streams.cleanUp();
        streams.start();

        // jvm 종료 시 실행될 스레드 추가 => streams.close()
        // streams 객체 데이터 스트림, 네트워크 소켓, 파일 핸들러 종료
        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    } 
}
