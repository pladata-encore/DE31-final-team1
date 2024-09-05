package kafkastreams.utils;

import org.json.JSONObject;

import java.util.Stack;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class util {
    public double calculate(String operator, double x, double y) {
        switch (operator) {
            case "+": return x + y;
            case "-": return x - y;
            case "*": return x * y;
            case "/": return x / y;
            default: throw new IllegalArgumentException("틀린 연산자 : " + operator);
        }
    }

    public String[] getVarName(String user_Role) {
        return user_Role.split("=")[0].strip().split("\\.");
    }

    public String getVarExpresstion(String user_Role) {
        return user_Role.split("=")[1].strip();
    }

    public ArrayList<String> parseUserRole(String user_Role, String input_Data) {
        // var_Name => 유저가 저장하고 싶은 변수명, var_Expresstion => 유저가 입력한 변환 수식
        String[] var_Name = getVarName(user_Role);
        String var_Expresstion = getVarExpresstion(user_Role);

        // 입력 데이터 => json 타입 데이터 변환, data json 추출
        JSONObject input_Json = new JSONObject(input_Data);
        JSONObject data_Json = input_Json.getJSONObject("data");

        // 데이터 변수를 숫자로 변환
        var_Expresstion = var_Expresstion.replace(user_Role.split("=")[0].strip(), String.valueOf(data_Json.getDouble(var_Name[1])));

        // 문자열 수식을 정규표현식을 사용하여 ArrayList에 적재
        Pattern pattern = Pattern.compile("\\d+\\.\\d+|\\d+|[+\\-*/()]");
        Matcher matcher = pattern.matcher(var_Expresstion);

        ArrayList<String> regex_ArrayList = new ArrayList<>();

        while (matcher.find()) {
            regex_ArrayList.add(matcher.group());
        }

        return regex_ArrayList;
    }

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

    public int getComparsion(String user_Role) {
        if (user_Role.contains(">")) {
            return 1;
        } else if (user_Role.contains(">=")) {
            return 2;
        } else if (user_Role.contains("<")) {
            return 3;
        } else if (user_Role.contains("<=")) {
            return 4;
        } else if (user_Role.contains("!=")) {
            return 5;
        } else if (user_Role.contains("==")) {
            return 6;
        } else {
            return 0;
        }
    }

    public double getPivot(String user_Role) {
        String[] split_String = user_Role.split(" ");

        Pattern pattern = Pattern.compile("\\d+");
        Matcher matcher = pattern.matcher(user_Role);

        String pivot = "";

        if (matcher.find()) {
            pivot = matcher.group();
        } else {
            System.out.println("Not Found...");
        }

        return Double.parseDouble(pivot);
    }

    public String getVarName2(String user_Role) {
        String regex = "\\.(\\w+)";

        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(user_Role);

        String result = "";

        while (matcher.find()) {
            result = matcher.group(1);
        }

        return result;
    }
}
