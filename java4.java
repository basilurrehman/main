import java.util.Scanner;
public class java4 {
    static int pNumber;
    static String pName;
    static int pAge;
    static String pEmail;
    static String pContact;
    static String pComplain;
    static double pBill;
    public static void main(String[] args) {
        Take_Patient_data();
        Print_Receipt();    }
    public static void Take_Patient_data() {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter Patient's Number please: ");
        pNumber = scanner.nextInt();
        scanner.nextLine(); 
        System.out.print("Enter Patient's Name please: ");
        pName = scanner.nextLine();
        System.out.print("Enter Patient's age please: ");
        pAge = scanner.nextInt();
        scanner.nextLine(); 
        System.out.print("Enter Patient's Email please: ");
        pEmail = scanner.nextLine();
        System.out.print("Enter Patient's Contact please: ");
        pContact = scanner.nextLine();
        System.out.print("Enter Patient's Complain please: ");
        pComplain = scanner.nextLine();
        System.out.print("Enter Patient's Bill please: ");
        pBill = scanner.nextDouble();
        scanner.close();    }
    public static void Print_Receipt() {
        System.out.println("---------------Patient's Receipt---------------");
        System.out.println("Patient's Number ----------- " + pNumber);
        System.out.println("Patient's Name ------------- " + pName);
        System.out.println("Patient's Age -------------- " + pAge);
        System.out.println("Patient's Email ------------ " + pEmail);
        System.out.println("Patient's Contact ---------- " + pContact);
        System.out.println("Patient's Complain --------- " + pComplain);
        System.out.println("Patient's Bill ------------- " + pBill);
        System.out.println("---------------------------------------------");
    }
}
