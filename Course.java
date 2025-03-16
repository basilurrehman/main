import java.util.ArrayList;

// Course Class
class Course {
    private String courseCode;
    private String courseName;
    private String courseCreditHours;

    public Course(String courseCode, String courseName, String courseCreditHours) {
        this.courseCode = courseCode;
        this.courseName = courseName;
        this.courseCreditHours = courseCreditHours;
    }

    public String getCourseCode() {
        return courseCode;
    }

    public String getCourseName() {
        return courseName;
    }

    public String getCourseCreditHours() {
        return courseCreditHours;
    }

    @Override
    public String toString() {
        return "CourseCode: " + courseCode + ", CourseName: " + courseName + ", CreditHours: " + courseCreditHours;
    }
}

// Faculty Class
class Faculty {
    private String facultyName;
    private String facultyDesignation;
    private String facultyEmail;
    private String facultyContact;
    private int facultySalary;
    private int facultyId;
    private ArrayList<Course> courseList;

    public Faculty(String facultyName, String facultyDesignation, String facultyEmail, String facultyContact, int facultySalary, int facultyId) {
        this.facultyName = facultyName;
        this.facultyDesignation = facultyDesignation;
        this.facultyEmail = facultyEmail;
        this.facultyContact = facultyContact;
        this.facultySalary = facultySalary;
        this.facultyId = facultyId;
        this.courseList = new ArrayList<>();
    }

    public void assignCourse(Course course) {
        courseList.add(course);
    }

    @Override
    public String toString() {
        return "Faculty Name: " + facultyName + ", Designation: " + facultyDesignation + ", Salary: " + facultySalary;
    }
}

// Department Class
class Department {
    private String departmentName;
    private ArrayList<Faculty> departmentFaculty;
    private ArrayList<Course> offeredCourses;

    public Department(String departmentName) {
        this.departmentName = departmentName;
        this.departmentFaculty = new ArrayList<>();
        this.offeredCourses = new ArrayList<>();
    }

    public void addFaculty(Faculty faculty) {
        departmentFaculty.add(faculty);
    }

    public void addCourse(Course course) {
        offeredCourses.add(course);
    }

    @Override
    public String toString() {
        return "Department Name: " + departmentName;
    }
}

// Main Class to test the code
public class Java6 {
    public static void main(String[] args) {
        // Create courses
        Course course1 = new Course("CS101", "Introduction to Computer Science", "3");
        Course course2 = new Course("CS102", "Data Structures", "3");

        // Create faculty
        Faculty faculty1 = new Faculty("John Doe", "Professor", "johndoe@gmail.com", "1234567890", 70000, 1);
        Faculty faculty2 = new Faculty("Jane Smith", "Assistant Professor", "janesmith@gmail.com", "0987654321", 50000, 2);

        // Assign courses to faculty
        faculty1.assignCourse(course1);
        faculty2.assignCourse(course2);

        // Create a department
        Department department = new Department("Computer Science");

        // Add faculty to the department
        department.addFaculty(faculty1);
        department.addFaculty(faculty2);

        // Add courses to the department
        department.addCourse(course1);
        department.addCourse(course2);

        // Print department, faculty, and courses
        System.out.println(department);
        System.out.println(faculty1);
        System.out.println(faculty2);
        System.out.println(course1);
        System.out.println(course2);
    }
}
