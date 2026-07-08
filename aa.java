class Vehicle {
    double rentalPrice;
    String licensePlate;

    Vehicle(double rentalPrice, String licensePlate) {
        this.rentalPrice = rentalPrice;
        this.licensePlate = licensePlate;
    }

    double calculateRentalCost(int days) {
        return 0;
    }
}

class Car extends Vehicle {
    Car(double rentalPrice, String licensePlate) {
        super(rentalPrice, licensePlate);
    }

    @Override
    double calculateRentalCost(int days) {
        return rentalPrice * days; 
    }
}

class Bike extends Vehicle {
    Bike(double rentalPrice, String licensePlate) {
        super(rentalPrice, licensePlate);
    }

    @Override
    double calculateRentalCost(int days) {
        return (rentalPrice * days) - 5;
    }
}

// Truck class
class Truck extends Vehicle {
    Truck(double rentalPrice, String licensePlate) {
        super(rentalPrice, licensePlate);
    }

    @Override
    double calculateRentalCost(int days) {
        return rentalPrice * days + 50; 
    }
}

public class aa {
    public static void main(String[] args) {
        Vehicle[] vehicles = new Vehicle[3];
        vehicles[0] = new Car(100, "CAR123");
        vehicles[1] = new Bike(50, "BIKE456");
        vehicles[2] = new Truck(200, "TRUCK789");

        int rentalDays = 3;

        for (Vehicle v : vehicles) {
            System.out.println("License Plate: " + v.licensePlate);
            System.out.println("Rental Cost for " + rentalDays + " days: $" + v.calculateRentalCost(rentalDays));
            System.out.println("-----------------------------");
        }
    }
}
