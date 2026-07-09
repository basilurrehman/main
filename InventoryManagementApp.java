import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

class Product {
    private String id;
    private String name;
    private int quantity;
    private double price;

    public Product(String id, String name, int quantity, double price) {
        this.id = id;
        this.name = name;
        this.quantity = quantity;
        this.price = price;
    }

    public String getId() {
        return id;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    public String toString() {
        return "ID: " + id + ", Name: " + name + ", Quantity: " + quantity + ", Price: $" + price;
    }
}

public class InventoryManagementApp {
    private static Map<String, Product> inventory = new HashMap<>();

    public static void main(String[] args) {
        // Sample products added initially
        inventory.put("P001", new Product("P001", "Apple", 50, 0.5));
        inventory.put("P002", new Product("P002", "Banana", 30, 0.2));
        inventory.put("P003", new Product("P003", "Orange", 20, 0.3));

        Scanner scanner = new Scanner(System.in);

        System.out.println("Inventory Management - Update Product Info");

        try {
            System.out.print("Enter Product ID to update: ");
            String productId = scanner.nextLine();

            // Check if product exists
            if (!inventory.containsKey(productId)) {
                throw new Exception("Product ID " + productId + " does not exist.");
            }

            Product product = inventory.get(productId);

            System.out.print("Enter new quantity: ");
            String quantityInput = scanner.nextLine();

            System.out.print("Enter new price: ");
            String priceInput = scanner.nextLine();
            int quantity;
            double price;

            try {
                quantity = Integer.parseInt(quantityInput);
            } catch (NumberFormatException e) {
                throw new Exception("Quantity must be a valid integer number.");
            }

            try {
                price = Double.parseDouble(priceInput);
            } catch (NumberFormatException e) {
                throw new Exception("Price must be a valid number.");
            }

            product.setQuantity(quantity);
            product.setPrice(price);

            System.out.println("Product updated successfully:");
            System.out.println(product);

        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        } finally {
            scanner.close();
        }
    }
}
