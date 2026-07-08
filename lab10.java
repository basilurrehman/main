interface Payable {
    double getPayment();
}

abstract class Person {
    private String firstName;
    private String lastName;
    private int age;

    public Person(String fn, String ln, int age) {
        this.firstName = fn;
        this.lastName = ln;
        this.age = age;
    }

    public String getFirstName() { return firstName; }
    public String getLastName() { return lastName; }
    public int getAge() { return age; }

    public abstract String toString();
}

class Student extends Person {
    private char grades;

    public Student(String fn, String ln, int age, char grades) {
        super(fn, ln, age);
        this.grades = grades;
    }

    @Override
    public String toString() {
        return "Student: " + getFirstName() + ", " + getLastName() + ", " + getAge() + ", " + grades;
    }
}

class Staff extends Person implements Payable {
    private double salary;

    public Staff(String fn, String ln, int age, double salary) {
        super(fn, ln, age);
        this.salary = salary;
    }

    public double getPayment() {
        return salary * 12; 
    }

    @Override
    public String toString() {
        return "Staff: " + getFirstName() + ", " + getLastName() + ", " + getAge() + ", " + salary;
    }
}

public class lab10 {
    public static void main(String[] args) {
        Student s1 = new Student("Ali", "Khan", 20, 'A');
        Student s2 = new Student("Sara", "Ahmed", 21, 'B');
        Student s3 = new Student("Bilal", "Raza", 22, 'C');

        Staff st1 = new Staff("Ahmed", "Hussain", 35, 50000);
        Staff st2 = new Staff("Nida", "Farooq", 40, 60000);
        Staff st3 = new Staff("Usman", "Iqbal", 30, 55000);
        System.out.println(s1);
        System.out.println(s2);
        System.out.println(s3);
        System.out.println(st1);
        System.out.println("Annual Payment: " + st1.getPayment());
        System.out.println(st2);
        System.out.println("Annual Payment: " + st2.getPayment());
        System.out.println(st3);
        System.out.println("Annual Payment: " + st3.getPayment());    }}
