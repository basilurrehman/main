public class TestShapes {
    public static void main(String[] args) {
        Shape square = new Square(10);
        Shape ellipse = new Ellipse(10, 7);
        Shape circle = new Circle(5);
        System.out.println(square);
        System.out.println();
        System.out.println(ellipse);
        System.out.println();
        System.out.println(circle);    }}

interface Eccentric {
    double getEccentricity();}

abstract class Shape {
    abstract double getArea();
    abstract double getPerimeter();
    public String toString() {
        return getClass().getSimpleName() + " Area=" + getArea() + " Perimeter=" + getPerimeter();}}

class Rectangle extends Shape {
    protected double width, height;

    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;}

    public double getArea() {
        return width * height;    }

    public double getPerimeter() {
        return 2 * (width + height);    }
}
class Square extends Rectangle {
    public Square(double side) {
        super(side, side);}}

class Ellipse extends Shape implements Eccentric {
    protected double a, b;

    public Ellipse(double a, double b) {
        this.a = a;
        this.b = b;}

    public double getArea() {
        return Math.PI * a * b;}

    public double getPerimeter() {
        return Math.PI * Math.sqrt(2 * (a * a + b * b)); }

    public double getEccentricity() {
        return Math.sqrt(1 - (Math.min(a, b) * Math.min(a, b)) / (Math.max(a, b) * Math.max(a, b)));}

    public String toString() {
        return getClass().getSimpleName() +
               " Area=" + getArea() +
               " Perimeter=" + getPerimeter() +
               " Eccentricity=" + getEccentricity();}}

class Circle extends Ellipse {
    public Circle(double radius) {
        super(radius, radius);}

    public String toString() {
        return getClass().getSimpleName() +
               " Area=" + getArea() +
               " Perimeter=" + getPerimeter();}}
