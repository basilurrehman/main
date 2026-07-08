public class Java7 {
    public static void main(String[] args) {
        int start = 1;
        int end = 20;
        System.out.println("Sum of numbers between " + start + " and " + end + " is: " + sumBetween(start, end));
    }
    public static int sumBetween(int start, int end) {
        if (start > end) {
            return 0;
        }
        return start + sumBetween(start + 1, end);
    }
}
