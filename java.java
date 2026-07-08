public class java {  
public static void main(String[] args) {  
    String text = "Hello! I am string in Java. I have several Functions and I am very \"Important\" #string_is_important";
    int index1 = text.indexOf('!');  
    String part1 = text.substring(0, index1 + 1);  
    System.out.println("Splitting at ! : " + part1);
    int index2 = text.indexOf("Important");  
    String part2 = text.substring(index1 + 1, index2);  
    System.out.println("After ! till Important : " + part2);
    int index3 = text.indexOf('.');  
    int index4 = text.indexOf('#');  
    String part3 = text.substring(index3 + 1, index4);  
    System.out.println("After . till # : " + part3);
    String part4 = text.substring(index4);  
    System.out.println("After # till end : " + part4);
}  
}
