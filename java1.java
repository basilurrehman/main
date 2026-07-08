import java.util.Scanner;

public class java1 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Enter a single letter: ");
        String letter = input.next();

        if (letter.length() > 1 || !Character.isLetter(letter.charAt(0))) {
            System.out.println("Invalid input! Enter a single letter from A to Z.");
        } else {
            char ch = Character.toLowerCase(letter.charAt(0));
            if ("aeiou".equals(String.valueOf(ch))) {
                System.out.println("Vowel");
            } else {
                System.out.println("Consonant");
            }
        }
        
        input.close();
    }
}
