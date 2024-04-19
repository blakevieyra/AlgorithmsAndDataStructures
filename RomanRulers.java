import java.util.PriorityQueue;

public class RomanRulers implements Comparable<RomanRulers> {

    private int rulerID;
    private String rulerName;

    // Constructor
    public RomanRulers(int id, String name) {
        this.rulerID = id;
        this.rulerName = name;
    }

    // Getter for rulerID
    public int getRulerID() {
        return rulerID;
    }

    // Getter for rulerName
    public String getRulerName() {
        return rulerName;
    }

    // equals method
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        RomanRulers that = (RomanRulers) obj;
        return rulerID == that.rulerID;
    }

    // compareTo method
    @Override
    public int compareTo(RomanRulers theOther) {
        return Integer.compare(this.rulerID, theOther.rulerID);
    }

    // toString method
    @Override
    public String toString() {
        return "Ruler Succession # " + getRulerID() + "\tRuler Name: " + getRulerName();
    }

    public static void main(String[] args) {
        PriorityQueue<RomanRulers> theRulers = new PriorityQueue<>();
        theRulers.add(new RomanRulers(1, "Augustus"));
        theRulers.add(new RomanRulers(2, "Tiberius"));
        theRulers.add(new RomanRulers(3, "Caligula"));
        theRulers.add(new RomanRulers(4, "Claudius"));
        theRulers.add(new RomanRulers(5, "Nero"));
        theRulers.add(new RomanRulers(6, "Galba"));
        theRulers.add(new RomanRulers(7, "Otho"));
        theRulers.add(new RomanRulers(8, "Aulus Vitellius"));
        theRulers.add(new RomanRulers(9, "Vespasian"));
        theRulers.add(new RomanRulers(10, "Titus"));
        theRulers.add(new RomanRulers(11, "Domitian"));
        theRulers.add(new RomanRulers(12, "Nerva"));

        while (!theRulers.isEmpty()) {
            System.out.println("Rulers Deceased: " + theRulers.remove());
        }
    }
}
