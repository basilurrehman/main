import java.util.Scanner;

public class java2 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("How many elements you want to enter: ");
        int size = input.nextInt();
        int[] numbers = new int[size];
        int max = Integer.MIN_VALUE, min = Integer.MAX_VALUE;
        int maxIndex = -1, minIndex = -1;
        for (int i = 0; i < size; i++) {
            System.out.print("Enter element " + (i + 1) + ": ");
            numbers[i] = input.nextInt();
            
            if (numbers[i] > max) {
                max = numbers[i];
                maxIndex = i;
            }
            if (numbers[i] < min) {
                min = numbers[i];
                minIndex = i;
            }
        }

        System.out.println("\n----------------Max element----------------");
        System.out.println("max number is " + max);
        System.out.println("Index of max number is " + (maxIndex + 1));

        System.out.println("\n----------------Minimum element----------------");
        System.out.println("Minimum number is " + min);
        System.out.println("Index of min number is " + (minIndex + 1));

        System.out.println("\n----------------Diff. b/w min and max----------------");
        System.out.println("The difference is : " + Math.abs(max - min));

        System.out.println("\n----------------Diff. b/w min and max indexes----------------");
        System.out.println("The difference of indices is : " + Math.abs(maxIndex - minIndex));

        input.close();
    }
}
