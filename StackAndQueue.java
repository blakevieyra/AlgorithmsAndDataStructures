import java.util.LinkedList;
import java.util.Stack;
import java.util.Scanner;
import java.util.InputMismatchException;

// Class Queue using LinkedList to simulate a queue behavior.
class Queue {
  LinkedList<String> queue = new LinkedList<>();

  public void insert(String data) {
    queue.add(data);
  }

  public String retrieve() {
    if (!queue.isEmpty()) {
      String value = queue.getFirst();
      queue.removeFirst();
      return value;
    }
    return null; // Return null or throw an exception depending on your preference
  }

  public boolean isEmpty() {
    return queue.isEmpty();
  }
}

public class StackAndQueue {
  public static void main(String[] args) {
    Queue queue = new Queue();
    Stack<String> stack = new Stack<>();
    Scanner scanner = new Scanner(System.in);

    int items = 0;
    while (true) {
      System.out.println("How many items do you want?");
      try {
        items = scanner.nextInt();
        break;
      } catch (InputMismatchException e) {
        System.out.println("Please enter a valid integer.");
        scanner.next(); // Consume the incorrect input
      }
    }

    System.out.println("Start entering values:");
    for (int i = 0; i < items; i++) {
      String item = scanner.next();
      queue.insert(item);
      stack.push(item);
    }

    System.out.println("Retrieving Queue:");
    while (!queue.isEmpty()) {
      System.out.println(queue.retrieve());
    }

    System.out.println("<---------->");
    System.out.println("Retrieving Stack:");
    while (!stack.isEmpty()) {
      System.out.println(stack.pop());
    }

    scanner.close(); // Close the scanner to prevent resource leak
  }
}
