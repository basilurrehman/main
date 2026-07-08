import java.util.Scanner;

public class Weekdays {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Enter the day number: ");
        int day = input.nextInt();
        String[] days = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
        if (day >= 1 && day <= 7) {
            System.out.println("The " + day + (day == 1 ? "st" : day == 2 ? "nd" : day == 3 ? "rd" : "th") + " day of the week is " + days[day - 1]);
        } else {
            System.out.println("Invalid input! Enter a number between 1 and 7.");
        }
        input.close();
    }
}
