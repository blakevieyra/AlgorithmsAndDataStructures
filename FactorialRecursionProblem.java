import java.util.*;

public class FactorialRecursionProblem {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        boolean keepGoing = true;

        while (keepGoing) {
            System.out.println("Enter an integer between 1 and 10 for factorial: ");
            int tester;
            do {
                tester = scanner.nextInt();
                if (tester < 1 || tester > 10) {
                    System.out.println("Invalid Number: Please enter an integer between 1 and 10.");
                }
            } while (tester < 1 || tester > 10);
            System.out.println("The factorial of " + tester + " = " + calcFactorial(tester));

            System.out.println("Do you want to calculate another factorial? (yes/no): ");
            String choice = scanner.next();
            if (!choice.equalsIgnoreCase("yes")) {
                keepGoing = false;
            }
        }

        scanner.close(); // Close the scanner to prevent resource leak
    }

    public static long calcFactorial(int input) {
        if (input == 1) {
            return 1;
        }
        return input * calcFactorial(input - 1);
    }
}
