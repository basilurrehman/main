import java.io.*;
import java.util.*;

abstract class Person {
    protected String name;
    protected int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public abstract void displayInfo();
}

class Patient extends Person {
    private String patientID;

    public Patient(String name, int age, String patientID) {
        super(name, age);
        this.patientID = patientID;
    }

    public String getPatientID() {
        return patientID;
    }

    @Override
    public void displayInfo() {
        System.out.println("Patient: " + name + " | Age: " + age + " | ID: " + patientID);
    }
}

class Doctor extends Person {
    private String specialization;

    public Doctor(String name, int age, String specialization) {
        super(name, age);
        this.specialization = specialization;
    }

    public String getSpecialization() {
        return specialization;
    }

    @Override
    public void displayInfo() {
        System.out.println("Doctor: " + name + " | Specialization: " + specialization);
    }
}

class Appointment {
    private Patient patient;
    private Doctor doctor;
    private String date;

    public Appointment(Patient patient, Doctor doctor, String date) {
        this.patient = patient;
        this.doctor = doctor;
        this.date = date;
    }

    public String getDate() {
        return date;
    }

    public Doctor getDoctor() {
        return doctor;
    }

    public String toString() {
        return "Appointment: " + patient.getPatientID() + " with Dr. " + doctor.name + " on " + date;
    }
}

public class HospitalManagementSystem {
    static Scanner scanner = new Scanner(System.in);
    static ArrayList<Doctor> doctors = new ArrayList<>();
    static ArrayList<Patient> patients = new ArrayList<>();
    static ArrayList<Appointment> appointments = new ArrayList<>();

    public static void main(String[] args) {
        loadDoctors();
        boolean exit = false;

        while (!exit) {
            System.out.println("\n--- Hospital Management ---");
            System.out.println("1. Register Patient");
            System.out.println("2. Schedule Appointment");
            System.out.println("3. View Appointments");
            System.out.println("4. Exit");
            System.out.print("Choose: ");
            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {
                case 1: registerPatient(); break;
                case 2: scheduleAppointment();break;
                case 3: viewAppointments();break;
                case 4: {
                    saveAppointmentsToFile();
                    exit = true;
                }
                default: System.out.println("Invalid choice.");
            }
        }
    }

    public static void loadDoctors() {
        doctors.add(new Doctor("Ali", 45, "Cardiologist"));
        doctors.add(new Doctor("Sara", 38, "Dermatologist"));
        doctors.add(new Doctor("Khan", 50, "Surgeon"));
    }

    public static void registerPatient() {
        System.out.print("Enter patient name: ");
        String name = scanner.nextLine();
        System.out.print("Enter age: ");
        int age = scanner.nextInt();
        scanner.nextLine();
        System.out.print("Enter patient ID: ");
        String id = scanner.nextLine();

        patients.add(new Patient(name, age, id));
        System.out.println("Patient registered successfully.");
    }

    public static void scheduleAppointment() {
        System.out.print("Enter patient ID: ");
        String patientID = scanner.nextLine();
        Patient patient = findPatientByID(patientID);
        if (patient == null) {
            System.out.println("Patient not found.");
            return;
        }

        System.out.println("Available Doctors:");
        for (int i = 0; i < doctors.size(); i++) {
            System.out.println((i + 1) + ". " + doctors.get(i).name + " - " + doctors.get(i).getSpecialization());
        }
        System.out.print("Choose doctor (number): ");
        int docIndex = scanner.nextInt() - 1;
        scanner.nextLine();

        if (docIndex < 0 || docIndex >= doctors.size()) {
            System.out.println("Invalid doctor selected.");
            return;
        }

        Doctor doctor = doctors.get(docIndex);
        System.out.print("Enter appointment date (YYYY-MM-DD): ");
        String date = scanner.nextLine();

        if (isDoctorBooked(doctor, date)) {
            System.out.println("Error: Doctor already has an appointment on that date.");
            return;
        }

        Appointment appt = new Appointment(patient, doctor, date);
        appointments.add(appt);
        System.out.println("Appointment scheduled successfully.");
    }

    public static void viewAppointments() {
        if (appointments.isEmpty()) {
            System.out.println("No appointments scheduled.");
        } else {
            for (Appointment appt : appointments) {
                System.out.println(appt);
            }
        }
    }

    public static boolean isDoctorBooked(Doctor doctor, String date) {
        for (Appointment appt : appointments) {
            if (appt.getDoctor().equals(doctor) && appt.getDate().equals(date)) {
                return true;
            }
        }
        return false;
    }

    public static Patient findPatientByID(String id) {
        for (Patient p : patients) {
            if (p.getPatientID().equals(id)) {
                return p;
            }
        }
        return null;
    }

    public static void saveAppointmentsToFile() {
        try (PrintWriter writer = new PrintWriter(new FileWriter("appointments.txt"))) {
            for (Appointment appt : appointments) {
                writer.println(appt);
            }
            System.out.println("Appointments saved to appointments.txt");
        } catch (IOException e) {
            System.out.println("Error saving appointments: " + e.getMessage());
        }
    }
}
