import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;


class Node {
    String name;
    List<Edge> edges;

    public Node(String name) {
        this.name = name;
        edges = new ArrayList<>();
    }

    public void addEdge(Edge edge) {
        edges.add(edge);
    }

    public String getName() {
        retu
       }
    
    

    ass Edge {
        Node source;
        Node destination;
        int weight;
        
      public Edge(Node source, Node destination, int weight) {
        this.source = source;
        this.destination = destination;
        this.weight

        Syste
      }

    
        
    a

      List<Edge> graph; 
        
         public Graph
     

     } 
        
       public void insertEdge(Edge edge) {
 

    }

    public List<Edge> getGraph() {
        System.out.println(graph.toString());
        return graph;
    }

    public int findRoute(String src, String dst) {
        for (Edge e : graph) {
            if (e.source.getName().equals(src) && e.destination.getName().equals(dst)) {
                return e.weight;
            }
        }
        return 0;
    }

    public void changeRoute(String src, String dst, int value) {
        for (Edge e : graph) {
            if (e.source.getName().equals(src) && e.destination.getName().equals(dst)) {
                e.weight = value;
            }
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Graph graph = new Graph();

        // Initializing nodes and adding them to the graph
        Node washington = new Node("Washington");
        Node indiana = new Node("Indiana");
        Node newyork = new Node("New York");
        Node california = new Node("California");
        Node florida = new Node("Florida");

        // Initializing edges and adding them to nodes and graph
        // Similar for other connections...
        Edge ws2in = new Edge(washington, indiana, 5);
        washington.addEdge(ws2in);
        graph.insertEdge(ws2in);

        // List and print all edges
        List<Edge> edges = graph.getGraph();
        for (int i = 0; i < edges.size(); i++) {
            Edge edge = edges.get(i);

               System.out.rintln("Rou t
              }
    

           // Additional interaction to find and  
               // Ensure to close your Scanner  
                 scanner.close();
             }
              
            