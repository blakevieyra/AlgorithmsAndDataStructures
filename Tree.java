import java.util.Random;
import java.util.Scanner;

public class Tree {
    // Class Node to store data and the children nodes
    class Node {
        int data;
        Node leftChild;
        Node rightChild;

        Node(int data) {
            this.data = data;
            leftChild = rightChild = null;
        }
    }

    Node root;

    // Tree class constructor
    public Tree() {
        root = null;
    }

    // Accessible insert method to call the recursive one
    public void insert(int data) {
        root = insertNode(root, data);
    }

    // Recursive insert method to define the nodes
    public Node insertNode(Node node, int key) {
        if (node == null) {
            node = new Node(key);
            return node;
        }
        if (key <= node.data) {
            node.leftChild = insertNode(node.leftChild, key);
        } else if (key > node.data) {
            node.rightChild = insertNode(node.rightChild, key);
        }
        return node;
    }

    // Accessible find method to call the recursive one
    public Node find(int data) {
        return findNode(root, data);
    }

    // Recursive find method to explore the children nodes
    public Node findNode(Node node, int data) {
        if (node == null) {
            return null; // Added to handle case where node is null
        }
        if (data == node.data) {
            return node;
        }
        return data < node.data ? findNode(node.leftChild, data) : findNode(node.rightChild, data);
    }

    public static void main(String[] args) {
        Random ran = new Random();
        int[] data = new int[10];
        System.out.println("Random Array:");
        for (int i = 0; i < data.length; i++) {
            data[i] = ran.nextInt(100);
            System.out.print(data[i] + " "); // Changed to double quotes
        }
        System.out.println("\nTree In Order:");
        Tree binaryTree = new Tree();
        for (int i = 0; i < data.length; i++) {
            binaryTree.insert(data[i]);
        }
        binaryTree.print();

        Scanner scanner = new Scanner(System.in);
        System.out.println("\nType a number to search: ");
        int item = scanner.nextInt();
        Node findItem = binaryTree.find(item);
        if (findItem == null) {
            System.out.println("Item Not Found");
        } else {
            System.out.println("Item " + findItem.data + " Found");
        }
        scanner.close();
    }

    public void print() {
        System.out.println("Tree In-Order:");
        printInOrder(root);
        System.out.println("\nTree Pre-Order:");
        printPreOrder(root);
        System.out.println("\nTree Post-Order:");
        printPostOrder(root);
    }

    public void printPreOrder(Node node) {
        if (node == null)
            return;
        System.out.print(node.data + " "); // Changed to double quotes
        printPreOrder(node.leftChild);
        printPreOrder(node.rightChild);
    }

    public void printPostOrder(Node node) {
        if (node == null)
            return;
        printPostOrder(node.leftChild);
        printPostOrder(node.rightChild);
        System.out.print(node.data + " "); // Changed to double quotes
    }

    public void printInOrder(Node node) {
        if (node == null)
            return;
        printInOrder(node.leftChild);
        System.out.print(node.data + " "); // Changed to double quotes
        printInOrder(node.rightChild);
    }
}
