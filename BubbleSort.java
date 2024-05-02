// Part 1: Sorting Arrays
// Develop a program that asks the user to enter a capital for a U.S. state. 
// Upon receiving the user input, the program reports whether the user input is correct. 
// For this application, the 50 states and their capitals are stored in a two-dimensional array in order by state name.
// Display the current contents of the array then use a bubble sort to sort the content by capital. 
// Next, prompt the user to enter answers for all the state capitals and then display the total correct count. 
// The user's answer is not case-sensitive.


// part1: Bubble Sort

import java.util.Arrays;
import java.util.Collections;
import java.util.Scanner;


//Create a bubble sort class that takes a string array as an argument
public class BubbleSort {
    public static void main(String[] args) {

        // assigns the 2d array be calling the get_states_array
        String[][] allStates = get_states_array();
        // shuffle the rows of the array so that the order is randomized
        Collections.shuffle(Arrays.asList(allStates));

        // print the presorted array
        for (String[] state : allStates) {
            System.out.println("Presort: " + state[0] + ": " + state[1]);
        }

        // call bubblesort method, print the postedsorted array
        bubbleSort(allStates);
        for (String[] state : allStates) {
            System.out.println("Postsort: " + state[0] + ": " + state[1]);
        }
        // initialize counters and iterate over the whole array. U
        int n = allStates.length;
        int correct = 0;
        int incorrect = 0;
        Scanner sc = new Scanner(System.in);
        for (int i = 0; i <= n - 1; i++) {
            // User input correct capital for state, incriment and print correct and
            // incorrect
            System.out.println("What is the capital of " + allStates[i][0] + ": ");
            String answer = sc.next();
            if (answer.equalsIgnoreCase(allStates[i][1])) {
                correct++;
            } else {
                incorrect++;
            }
            System.out.println("Correct = " + correct + " Incorrect = " + incorrect);
        }
        // Calculate accuracy by dividing correct by the total, print the percent
        // correct
        double accuracy = ((double) correct / (correct + incorrect) * 100);
        System.out.println("Your percent correct: " + accuracy + "%");
        sc.close();
    }

    public static String[][] get_states_array() {
        //2d array of states and their capitals, len 50
        String[][] statesAndCapitals = {
                { "Alabama", "Montgomery" },
                { "Alaska", "Juneau" },
                { "Arizona", "Phoenix" },
                { "Arkansas", "Little Rock" },
                { "California", "Sacramento" },
                { "Colorado", "Denver" },
                { "Connecticut", "Hartford" },
                { "Delaware", "Dover" },
                { "Florida", "Tallahassee" },
                { "Georgia", "Atlanta" },
                { "Hawaii", "Honolulu" },
                { "Idaho", "Boise" },
                { "Illinois", "Springfield" },
                { "Indiana", "Indianapolis" },
                { "Iowa", "Des Moines" },
                { "Kansas", "Topeka" },
                { "Kentucky", "Frankfort" },
                { "Louisiana", "Baton Rouge" },
                { "Maine", "Augusta" },
                { "Maryland", "Annapolis" },
                { "Massachusetts", "Boston" },
                { "Michigan", "Lansing" },
                { "Minnesota", "Saint Paul" },
                { "Mississippi", "Jackson" },
                { "Missouri", "Jefferson City" },
                { "Montana", "Helena" },
                { "Nebraska", "Lincoln" },
                { "Nevada", "Carson City" },
                { "New Hampshire", "Concord" },
                { "New Jersey", "Trenton" },
                { "New Mexico", "Santa Fe" },
                { "New York", "Albany" },
                { "North Carolina", "Raleigh" },
                { "North Dakota", "Bismarck" },
                { "Ohio", "Columbus" },
                { "Oklahoma", "Oklahoma City" },
                { "Oregon", "Salem" },
                { "Pennsylvania", "Harrisburg" },
                { "Rhode Island", "Providence" },
                { "South Carolina", "Columbia" },
                { "South Dakota", "Pierre" },
                { "Tennessee", "Nashville" },
                { "Texas", "Austin" },
                { "Utah", "Salt Lake City" },
                { "Vermont", "Montpelier" },
                { "Virginia", "Richmond" },
                { "Washington", "Olympia" },
                { "West Virginia", "Charleston" },
                { "Wisconsin", "Madison" },
                { "Wyoming", "Cheyenne" }
        };
        return statesAndCapitals;
    }

    public static void bubbleSort(String[][] arr) {
        //assign the length of the string array to a variable
        int array_length = arr.length;
        //iterate over the each element i of array to the length of array minus one, incriment i
        for (int i = 0; i < array_length -1; i++) {
            // create a conditional check boolean. default false if array is already sorted
            boolean swap = false;
            //iterate for each element j of the array for j minus i minus one iterations, incriment j
            for (int j = 0; j < array_length - i - 1; j++) {
                //swap condition: if string element at array in j is greater letter value that the next element j + 1
                    if (arr[j][0].compareTo(arr[j + 1][0]) > 0) {
                        //assign j  to a temporary variable
                        String[] temp = arr[j];
                        //the reassign arr at j to each the value of arr at j + 1
                        arr[j] = arr[j + 1];
                        //and array at j + 1 become the value of the temp, swap complete
                        arr[j + 1] = temp;
                        //swap is now true 
                        swap = true;
                    }
            }
            //break loop if already sorted
            if (!swap) {
                break;
             }
            }
        }
    }
