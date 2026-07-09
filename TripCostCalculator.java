import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class TripCostCalculator {
    public static double calculateTripCost(double distance, double rate) {
        if (distance < 0 || rate < 0) {
            throw new IllegalArgumentException("Distance and rate must be non-negative.");        }
        if (distance == 0) {
            throw new ArithmeticException("Distance cannot be zero for cost calculation.");        }
        return distance * rate;    }
    public static void saveTripSummary(String summary) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("trip_history.txt", true))) {
            writer.write(summary);
            writer.newLine();       }    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        try {
            System.out.print("Enter trip distance (km): ");
            double distance = scanner.nextDouble();
            System.out.print("Enter rate per km: ");
            double rate = scanner.nextDouble();
            double cost = calculateTripCost(distance, rate);
            String summary = "Trip distance: " + distance + " km, Rate: " + rate + ", Cost: " + cost;
            System.out.println(summary);
            saveTripSummary(summary);
            System.out.println("Trip summary saved successfully.");
        } catch (IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        } catch (ArithmeticException e) {
            System.out.println("Error: Cannot calculate cost for zero distance.");
        } catch (IOException e) {
            System.out.println("Error saving trip summary: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("Unexpected error occurred: " + e.getMessage());
        } finally {
            scanner.close();       }    }}
