abstract class Course {
    String courseName;

    Course(String courseName) {
        this.courseName = courseName;
    }

    abstract double calculateFinalGrade();
}

class TheoreticalCourse extends Course {
    double midterm;
    double finalExam;

    TheoreticalCourse(String courseName, double midterm, double finalExam) {
        super(courseName);
        this.midterm = midterm;
        this.finalExam = finalExam;
    }

    double calculateFinalGrade() {
        return (midterm * 0.4) + (finalExam * 0.6);
    }
}

class LabCourse extends Course {
    double labWork;
    double viva;

    LabCourse(String courseName, double labWork, double viva) {
        super(courseName);
        this.labWork = labWork;
        this.viva = viva;
    }

    double calculateFinalGrade() {
        return (labWork * 0.7) + (viva * 0.3);
    }
}

class ProjectCourse extends Course {
    double proposal;
    double implementation;
    double presentation;

    ProjectCourse(String courseName, double proposal, double implementation, double presentation) {
        super(courseName);
        this.proposal = proposal;
        this.implementation = implementation;
        this.presentation = presentation;
    }

    double calculateFinalGrade() {
        return (proposal * 0.2) + (implementation * 0.5) + (presentation * 0.3);
    }
}

public class GradingSystem {
    public static void main(String[] args) {
        Course[] courses = {
            new TheoreticalCourse("Math", 78, 85),
            new LabCourse("Physics Lab", 90, 80),
            new ProjectCourse("Software Project", 70, 88, 75)
        };

        for (Course c : courses) {
            System.out.println(c.courseName + " Final Grade: " + c.calculateFinalGrade());
        }
    }
}