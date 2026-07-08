public class Java6 {
    public static void main(String[] args) {
        int number = 5;
        System.out.println("Product of numbers from 1 to " + number + " is: " + multiplyUpTo(number));
    }
    public static int multiplyUpTo(int n) {
        if (n == 1) {
            return 1;
        }
        return n * multiplyUpTo(n - 1);
    }
}
