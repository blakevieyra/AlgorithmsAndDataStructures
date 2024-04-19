import java.util.PriorityQueue;

public class Main {
  public static void main(String[] args) {
    PriorityQueue<String> myPriorityQueue = new PriorityQueue<>();
    myPriorityQueue.add("Augustus");
    myPriorityQueue.add("Tiberius");
    myPriorityQueue.add("Caligula");
    myPriorityQueue.add("Claudius");
    myPriorityQueue.add("Nero");
    myPriorityQueue.add("Galba");
    myPriorityQueue.add("Otho");
    myPriorityQueue.add("Aulus Vitellius");
    myPriorityQueue.add("Vespasian");
    myPriorityQueue.add("Titus");
    myPriorityQueue.add("Domitian");
    myPriorityQueue.add("Nerva");

    // Remove and print each element in the priority queue
    while (!myPriorityQueue.isEmpty()) {
      System.out.println(myPriorityQueue.remove());
    }
  }
}
