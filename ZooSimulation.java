abstract class Animal {
    abstract void makeSound();}
class Lion extends Animal {
    void makeSound() {
       System.out.println("Roar");
    }}
class Elephant extends Animal {
    void makeSound() {
        System.out.println("Trumpet");
    }}
class Monkey extends Animal {
    void makeSound() {
        System.out.println("Chatter");
    }}
public class ZooSimulation {
    public static void main(String[] args) {
        Animal[] animals = {
            new Lion(),
            new Elephant(),
            new Monkey()
        };

        for (Animal a : animals) {
            a.makeSound();        }    } }
