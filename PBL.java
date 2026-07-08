class Person {
    private String name;
    private String phoneNumber;
    public Person(String name, String phoneNumber) {
        this.name = name;
        this.phoneNumber = phoneNumber;
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }
}

class Sender extends Person {
    private String originAddress;

    public Sender(String name, String phoneNumber, String originAddress) {
        super(name, phoneNumber);
        this.originAddress = originAddress;
    }

    public String getOriginAddress() {
        return originAddress;
    }

    public void setOriginAddress(String originAddress) {
        this.originAddress = originAddress;
    }
}

class DeliveryWorker extends Person {
    private int deliveriesCompleted;
    private double payPerDelivery;

    public DeliveryWorker(String name, String phoneNumber, double payPerDelivery) {
        super(name, phoneNumber);
        this.deliveriesCompleted = 0;
        this.payPerDelivery = payPerDelivery;
    }

    public int getDeliveriesCompleted() {
        return deliveriesCompleted;
    }

    public void setDeliveriesCompleted(int deliveriesCompleted) {
        this.deliveriesCompleted = deliveriesCompleted;
    }

    public void incrementDeliveries() {
        this.deliveriesCompleted++;
    }

    public double getPayPerDelivery() {
        return payPerDelivery;
    }

    public void setPayPerDelivery(double payPerDelivery) {
        this.payPerDelivery = payPerDelivery;
    }

    public double calculatePay() {
        return deliveriesCompleted * payPerDelivery;
    }
}

abstract class Vehicle {
    private String vehicleId;
    private String type;

    public Vehicle(String vehicleId, String type) {
        this.vehicleId = vehicleId;
        this.type = type;
    }

    public String getVehicleId() {
        return vehicleId;
    }

    public void setVehicleId(String vehicleId) {
        this.vehicleId = vehicleId;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }
}

class Bike extends Vehicle {
    public Bike(String vehicleId) {
        super(vehicleId, "Bike");
    }
}

class Van extends Vehicle {
    public Van(String vehicleId) {
        super(vehicleId, "Van");
    }
}

class Truck extends Vehicle {
    public Truck(String vehicleId) {
        super(vehicleId, "Truck");
    }
}

class Route {
    private String originCity;
    private String destinationCity;

    public Route(String originCity, String destinationCity) {
        this.originCity = originCity;
        this.destinationCity = destinationCity;
    }

    public String getOriginCity() {
        return originCity;
    }

    public void setOriginCity(String originCity) {
        this.originCity = originCity;
    }

    public String getDestinationCity() {
        return destinationCity;
    }

    public void setDestinationCity(String destinationCity) {
        this.destinationCity = destinationCity;
    }
}

class Parcel {
    private String parcelId;
    private String contentDescription;
    private Sender sender;
    private DeliveryWorker deliveryWorker;
    private Vehicle vehicle;
    private Route route;
    private boolean delivered;

    public Parcel(String parcelId, String contentDescription, Sender sender,
                  DeliveryWorker deliveryWorker, Vehicle vehicle, Route route) {
        this.parcelId = parcelId;
        this.contentDescription = contentDescription;
        this.sender = sender;
        this.deliveryWorker = deliveryWorker;
        this.vehicle = vehicle;
        this.route = route;
        this.delivered = false;
    }

    public String getParcelId() {
        return parcelId;
    }

    public void setParcelId(String parcelId) {
        this.parcelId = parcelId;
    }

    public String getContentDescription() {
        return contentDescription;
    }

    public void setContentDescription(String contentDescription) {
        this.contentDescription = contentDescription;
    }

    public Sender getSender() {
        return sender;
    }

    public void setSender(Sender sender) {
        this.sender = sender;
    }

    public DeliveryWorker getDeliveryWorker() {
        return deliveryWorker;
    }

    public void setDeliveryWorker(DeliveryWorker deliveryWorker) {
        this.deliveryWorker = deliveryWorker;
    }

    public Vehicle getVehicle() {
        return vehicle;
    }

    public void setVehicle(Vehicle vehicle) {
        this.vehicle = vehicle;
    }

    public Route getRoute() {
        return route;
    }

    public void setRoute(Route route) {
        this.route = route;
    }

    public boolean isDelivered() {
        return delivered;
    }

    public void setDelivered(boolean delivered) {
        this.delivered = delivered;
    }

    public void markAsDelivered() {
        if (!this.delivered) {
            this.delivered = true;
            deliveryWorker.incrementDeliveries();
        }
    }
}

public class PBL {
    public static void main(String[] args) {
        Sender sender = new Sender("Basil", "0341-02-134242-113", "Garden West, Karachi");
        DeliveryWorker worker = new DeliveryWorker("Batman", "0336-404", 10.0);
        Vehicle van = new Van("V-Batmobile");
        Route route = new Route("Karachi", "Lahore");

        Parcel parcel = new Parcel("P-001", "Chicken Biryani", sender, worker, van, route);

        System.out.println(" Before Delivery");
        System.out.println("Parcel ID: " + parcel.getParcelId());
        System.out.println("Sender: " + parcel.getSender().getName());
        System.out.println("Delivering Worker: " + parcel.getDeliveryWorker().getName());
        System.out.println("Vehicle: " + parcel.getVehicle().getType() + " (ID: " + parcel.getVehicle().getVehicleId() + ")");
        System.out.println("Route: " + parcel.getRoute().getOriginCity() + " --> " + parcel.getRoute().getDestinationCity());
        System.out.println("Delivered: " + parcel.isDelivered());
        System.out.println("Worker's deliveries so far: " + worker.getDeliveriesCompleted());
        System.out.println();

        System.out.println("Simulating delivery...");
        parcel.markAsDelivered();
        System.out.println();

        System.out.println(" After Delivery ");
        System.out.println("Parcel ID: " + parcel.getParcelId());
        System.out.println("Delivered: " + parcel.isDelivered());
        System.out.println("Worker's deliveries so far: " + worker.getDeliveriesCompleted());
        System.out.println("Total pay for worker: " + worker.calculatePay());
    }
}
