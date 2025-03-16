import java.util.Scanner;
public class java5 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int input;

        while (true) {
            System.out.print("Enter a number (negative to quit): ");
            input = scanner.nextInt();
            
            if (input < 0) {
                break;
            }
            
            System.out.println("Sum of odd numbers less than " + input + ": " + ComputeOddSum(input));
            System.out.println("Sum of even numbers less than " + input + ": " + ComputeEvenSum(input));
        }
        scanner.close();
    }
    public static int ComputeOddSum(int input) {
        if (input <= 0) {
            return 0;
        }
        if (input % 2 == 1) {
            return input - 1 + ComputeOddSum(input - 1);
        } else {
            return ComputeOddSum(input - 1);
        }
    }
    public static int ComputeEvenSum(int input) {
        if (input <= 0) {
            return 0;
        }
        if (input % 2 == 0) {
            return input - 2 + ComputeEvenSum(input - 2);
        } else {
            return ComputeEvenSum(input - 1);
        }
    }
}
