import java.io.*;
import java.util.*;

class Student {
    private String name;
    private String rollNumber;
    private String course;
    private String department;
    private int year;
    private double gpa;

    public Student(String name, String rollNumber, String course, String department, int year, double gpa) {
        this.name = name;
        this.rollNumber = rollNumber;
        this.course = course;
        this.department = department;
        this.year = year;
        this.gpa = gpa;
    }

    public void setGpa(double gpa) {
        this.gpa = gpa;
    }

    @Override
    public String toString() {
        return name + "," + rollNumber + "," + course + "," + department + "," + year + "," + gpa;
    }

    public static Student fromString(String line) {
        String[] parts = line.split(",");
        return new Student(parts[0], parts[1], parts[2], parts[3], Integer.parseInt(parts[4]), Double.parseDouble(parts[5]));
    }
}

public class StudentSystem {
    private static final String ORIGINAL_FILE = "StudentRecords.txt";
    private static final String UPDATED_FILE = "UpdatedStudentRecords.txt";

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        List<Student> students = new ArrayList<>();

        // Input 4 students
        for (int i = 0; i < 4; i++) {
            System.out.println("Enter details for student " + (i + 1) + ":");
            System.out.print("Name: ");
            String name = sc.nextLine();

            System.out.print("Roll Number: ");
            String rollNumber = sc.nextLine();

            System.out.print("Course: ");
            String course = sc.nextLine();

            System.out.print("Department: ");
            String department = sc.nextLine();

            System.out.print("Year: ");
            int year = Integer.parseInt(sc.nextLine());

            System.out.print("GPA: ");
            double gpa = Double.parseDouble(sc.nextLine());

            students.add(new Student(name, rollNumber, course, department, year, gpa));
        }

        // Write to original file
        writeToFile(ORIGINAL_FILE, students);

        // Read and display original file
        System.out.println("\nOriginal Student Records:");
        List<Student> originalStudents = readFromFile(ORIGINAL_FILE);
        for (Student s : originalStudents) {
            System.out.println(s);
        }

        // Update GPA for 1st and 4th students
        if (originalStudents.size() >= 4) {
            System.out.print("\nEnter new GPA for 1st student: ");
            double newGpa1 = Double.parseDouble(sc.nextLine());
            originalStudents.get(0).setGpa(newGpa1);

            System.out.print("Enter new GPA for 4th student: ");
            double newGpa4 = Double.parseDouble(sc.nextLine());
            originalStudents.get(3).setGpa(newGpa4);
        }

        // Write updated records to new file
        writeToFile(UPDATED_FILE, originalStudents);

        // Display updated records
        System.out.println("\nUpdated Student Records:");
        List<Student> updatedStudents = readFromFile(UPDATED_FILE);
        for (Student s : updatedStudents) {
            System.out.println(s);
        }
    }

    private static void writeToFile(String filename, List<Student> students) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
            for (Student s : students) {
                writer.write(s.toString());
                writer.newLine();
            }
        } catch (IOException e) {
            System.out.println("Error writing to file: " + filename);
        }
    }

    private static List<Student> readFromFile(String filename) {
        List<Student> students = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = reader.readLine()) != null) {
                students.add(Student.fromString(line));
            }
        } catch (IOException e) {
            System.out.println("Error reading file: " + filename);
        }
        return students;
    }
}
