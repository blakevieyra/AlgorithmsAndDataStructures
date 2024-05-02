
// Part 2: Sorting & Searching HashMap
// Now revise the code to store the pairs of each state and its capital in a Map using the HashMap function. Display the content of the Map, then use the TreeMap class to sort the map while using a binary search tree for storage. Next, your program should prompt the user to enter a state and it should then display the capital for the state.

import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
import java.util.TreeMap;

public class BinarySearch {
    public static void main(String[] args) {

        //initialize scanner for user input
        Scanner scanner = new Scanner(System.in);
        // initialze HashMap and insery the emptpy map object into the getStatesMap method to create map
        Map<String, String> stateCapitals = new HashMap<>();
        getStatesMap(stateCapitals);

        // for each key in map, print the presort map keys with corresponding values
        System.out.println("PRESORT:");
        for (Map.Entry<String, String> entry : stateCapitals.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }

        // Create a treemap, pass in the stateCapitcals to create a new Binary Tree map
        // for each key in map, print the postsorted map keys with corresponding values
        TreeMap<String, String> sortedStateCapitals = new TreeMap<>(stateCapitals);
        System.out.println("POSTSORT:");
        for (Map.Entry<String, String> entry2 : sortedStateCapitals.entrySet()) {
            System.out.println(entry2.getKey() + ": " + entry2.getValue());
        }
        // While map has data, user enter a state which matches to a map key and return the capital value
        try {
            while (true) {
                System.out.print("\nEnter a state to find its capital: ");
                String state = scanner.nextLine();
                if (state.isEmpty()) {
                    System.out.println("No input provided. Exiting.");
                    break;
                }
                //this return the capital from the map if their is a state match
                String capital = sortedStateCapitals.get(state);
                if (capital != null) {
                    System.out.println("The capital of " + state + " is " + capital);
                } else {
                    System.out.println("State not found. Please try again.");
                }
            }
        } catch (Exception e) {
            System.out.println("An error occurred: " + e.getMessage());
        } finally {
            scanner.close();
        }
    }

        private static void getStatesMap(Map<String, String> map) {
        map.put("Alabama", "Montgomery");
        map.put("Alaska", "Juneau");
        map.put("Arizona", "Phoenix");
        map.put("Arkansas", "Little Rock");
        map.put("California", "Sacramento");
        map.put("Colorado", "Denver");
        map.put("Connecticut", "Hartford");
        map.put("Delaware", "Dover");
        map.put("Florida", "Tallahassee");
        map.put("Georgia", "Atlanta");
        map.put("Hawaii", "Honolulu");
        map.put("Idaho", "Boise");
        map.put("Illinois", "Springfield");
        map.put("Indiana", "Indianapolis");
        map.put("Iowa", "Des Moines");
        map.put("Kansas", "Topeka");
        map.put("Kentucky", "Frankfort");
        map.put("Louisiana", "Baton Rouge");
        map.put("Maine", "Augusta");
        map.put("Maryland", "Annapolis");
        map.put("Massachusetts", "Boston");
        map.put("Michigan", "Lansing");
        map.put("Minnesota", "Saint Paul");
        map.put("Mississippi", "Jackson");
        map.put("Missouri", "Jefferson City");
        map.put("Montana", "Helena");
        map.put("Nebraska", "Lincoln");
        map.put("Nevada", "Carson City");
        map.put("New Hampshire", "Concord");
        map.put("New Jersey", "Trenton");
        map.put("New Mexico", "Santa Fe");
        map.put("New York", "Albany");
        map.put("North Carolina", "Raleigh");
        map.put("North Dakota", "Bismarck");
        map.put("Ohio", "Columbus");
        map.put("Oklahoma", "Oklahoma City");
        map.put("Oregon", "Salem");
        map.put("Pennsylvania", "Harrisburg");
        map.put("Rhode Island", "Providence");
        map.put("South Carolina", "Columbia");
        map.put("South Dakota", "Pierre");
        map.put("Tennessee", "Nashville");
        map.put("Texas", "Austin");
        map.put("Utah", "Salt Lake City");
        map.put("Vermont", "Montpelier");
        map.put("Virginia", "Richmond");
        map.put("Washington", "Olympia");
        map.put("West Virginia", "Charleston");
        map.put("Wisconsin", "Madison");
        map.put("Wyoming", "Cheyenne");
    }
}
