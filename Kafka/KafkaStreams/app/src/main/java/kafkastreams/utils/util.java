package kafkastreams.utils;

import org.json.JSONObject;

import java.util.Stack;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class util {
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

    // user_Role 파싱하여 목적 변수 return
    public String getVarName(String user_Rule) {
        String var = user_Rule.split("=")[0].strip();

        if (var.contains(".") || var.contains("_")) {
            String[] split_String = var.split("[._]");
            var = split_String[split_String.length - 1];
            return var;
        }

        return var;
    }

    // user_Role 파싱하여 변환 수식 return
    public String getVarExpresstion(String user_Rule) {
        return user_Rule.split("=")[1].strip();
    }

    // user_Rule 파싱하고 변수 치환
    public ArrayList<String> parseUserRule(String user_Rule, String input_Data) {
        // var_Expresstion => 유저가 입력한 변환 수식
        String var_Expresstion = getVarExpresstion(user_Rule);

        // 입력 데이터 => json 타입 데이터형 변환, data json 추출
        JSONObject input_Json = new JSONObject(input_Data);
        JSONObject data_Json = input_Json.getJSONObject("data");

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
                regex_ArrayList.set(i, String.valueOf(data_Json.getDouble(token)));
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

    // pivot 값 파싱
    public double getPivot(String user_Role) {
        Pattern pattern = Pattern.compile("\\d+");
        Matcher matcher = pattern.matcher(user_Role);

        String pivot = "";

        if (matcher.find()) {
            pivot = matcher.group();
        }

        return Double.parseDouble(pivot);
    }

    public String getVarName2(String user_Rule) {
        String regex = "\\.(\\w+)";

        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(user_Rule);

        String result = "";

        while (matcher.find()) {
            result = matcher.group(1);
        }

        return result;
    }
    // --------------------> KafkaStreams.filter <------------------------------------ \\
}
