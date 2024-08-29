package kafkastreams;

import kafkastreams.utils.util;

import java.util.ArrayList;

public class Main {
    static util ut = new util();
    public static void main(String[] args) {
        // user_Role 예시 = 유저가 저장하고 싶은 변수명 = 변환 수식
        String user_Role = "data.temp = (data.temp * 9/5) + 32";
        String input_Data = "{timestamp: 2024-01-01T01290123, user: elvldbwj, data: {temp: 36.5,humid: 89}}"; 
        
        ArrayList<String> regex_ArrayList = ut.parseUserRole(user_Role, input_Data);
        double result = ut.parseCalculate(regex_ArrayList);
        System.out.println(result);
    } 
}
