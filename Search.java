//Binary Search Tree

// class TreeNode:
//     def __init__(self, val):
//         self.val = val
//         self.left = None
//         self.right = None

// def search(root, target):
//     if not root:
//         return False
    
//     if target > root.val:
//         return search(root.right, target)
//     elif target < root.val:
//         return search(root.left, target)
//     else:
//         return True

// class TreeNode {
//     constructor(val) {
//         this.val = val; 
//         this.left = null;
//         this.right = null; 
//     }
// }

// function search(root, target) {
//     if (root == null) {
//         return false;
//     }

//     if (target > root.val) {
//         return search(root.right, target);
//     } else if (target < root.val) {
//         return search(root.left, target);
//     } else {
//         return true;
//     }    
// }
// Definiton of TreeNode in Java
/*
public class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;

    public TreeNode(int val) {
        this.val = val; 
        left = null;
        right = null; 
    }
}
*/

import javax.swing.tree.TreeNode;

public class Search {
    
    public boolean search(TreeNode root, int target) {
        if (root == null) {
            return false;
        }

        if (target > root.val) {
            return search(root.right, target);
        } else if (target < root.val) {
            return search(root.left, target);
        } else {
            return true;
        }
    }
}
//BST INSERT 
// Insert a new node and return the root of the BST.
public TreeNode insert(TreeNode root, int val) {
    if (root == null) {
        return new TreeNode(val);
    }

    if (val > root.val) {
        root.right = insert(root.right, val);
    } else  if (val < root.val) {
        root.left = insert(root.left, val);
    }
    return root;
}

//Binary Tree Remove
public TreeNode minValueNode(TreeNode root) {
    TreeNode curr = root;
    while(curr != null && curr.left != null) {
        curr = curr.left;
    }
    return curr;
}

// Remove a node and return the root of the BST.
public TreeNode remove(TreeNode root, int val) {
    if (root == null) {
        return null;
    }
    if (val > root.val) {
        root.right = remove(root.right, val);
    } else if (val < root.val) {
        root.left = remove(root.left, val);
    } else {
        if (root.left == null) {
            return root.right;
        } else if (root.right == null) {
            return root.left;
        } else {
            TreeNode minNode = minValueNode(root.right);
            root.val = minNode.val;
            root.right = remove(root.right, minNode.val);
        }
    }
    return root;
}

//DFS
public void inorder(TreeNode root) {
    if (root == null) {
        return;
    }
    inorder(root.left);
    System.out.println(root.val);
    inorder(root.right);
}

public void preorder(TreeNode root) {
    if (root == null) {
        return;
    }
    System.out.println(root.val);
    preorder(root.left);
    preorder(root.right);
}

public void postorder(TreeNode root) {
    if (root == null) {
        return;
    }  
    postorder(root.left);
    postorder(root.right);
    System.out.println(root.val);

 
//Breath First Search
public void bfs(TreeNode root) { 
    Deque<TreeNode> queue = new ArrayDeque<TreeNode>();
    if (root != null) {
        queue.add(root);
    }    
    int level = 0;
    while(!queue.isEmpty()) {
        System.out.print("level " + level + ": ");
        int levelLength = queue.size();
        for (int i = 0; i < levelLength; i++) {
            TreeNode curr = queue.removeFirst(); 
            System.out.print(curr.val + " ");
            if(curr.left != null) {
                queue.add(curr.left);  
            }
            if(curr.right != null) {
                queue.add(curr.right);
            }  
        }
        level++;
        System.out.println();
    }
}

}
/*
public class ListNode {
    int val;
    ListNode next;

    public ListNode(int val) {
        this.val = val;
        this.next = null;
    }
}
*/

// Implementation for Singly Linked List
public class SinglyLinkedList {
    ListNode head;
    ListNode tail;

    public SinglyLinkedList() {
        head = new ListNode(-1);
        tail = head;
    }

    public void insertEnd(int val) {
        tail.next = new ListNode(val);
        tail = tail.next; 
    }

    public void remove(int index) {
        int i = 0;
        ListNode curr = head;
        while (i < index && curr != null) {
            i++;
            curr = curr.next;
        }
        
        // Remove the node ahead of curr
        if (curr != null && curr.next != null) {
            if (curr.next == tail) {
                tail = curr;
            }
            curr.next = curr.next.next;
        }
    }

    public void print() {
        ListNode curr = head.next;
        while (curr != null) {
            System.out.print(curr.val + " -> ");
            curr = curr.next;
        }

        System.out.println();
    }
    
}


public class DoublyLinkedListNode {
    
    int val;
    DoublyLinkedListNode next;
    DoublyLinkedListNode prev;

    public DoublyLinkedListNode(int val) {
        this.val = val;
        this.next = null;
        this.prev = null;
    }
}


// Implementation for Doubly Linked List
public class DoublyLinkedList {
    DoublyLinkedListNode head;
    DoublyLinkedListNode tail;

    public DoublyLinkedList() {
        head = new DoublyLinkedListNode(-1);
        tail = new DoublyLinkedListNode(-1);
        head.next = tail;
        tail.prev = head;
    }

    public void insertFront(int val) {
        DoublyLinkedListNode newNode = new DoublyLinkedListNode(val);
        newNode.prev = head;
        newNode.next = head.next;
        
        head.next.prev = newNode;
        head.next = newNode;
    }

    public void insertEnd(int val) {
        DoublyLinkedListNode newNode = new DoublyLinkedListNode(val);
        newNode.next = tail;
        newNode.prev = tail.prev;
        
        tail.prev.next = newNode;
        tail.prev = newNode;
    }

    public void removeFront() {
        head.next.next.prev = head;
        head.next = head.next.next;
    }   

    public void removeEnd() {
        tail.prev.prev.next = tail;
        tail.prev = tail.prev.prev;
    }   
    
    public void print() {
        DoublyLinkedListNode curr = head.next;
        while (curr != tail) {
            System.out.print(curr.val + " -> ");
            curr = curr.next;
        }           
        System.out.println();
    }
}

public class ListNode {
    int val;
    ListNode next;

    public ListNode(int val) {
        this.val = val;
        this.next = null;
    }
}

public class Queue {
    ListNode left;  // front of Queue   front -> [1,2,3]
    ListNode right; // back of Queue   [1,2,3] <- back
    
    public Queue() {
        this.left  = null;
        this.right = null;
    }

    public void enqueue(int val) {
        ListNode newNode = new ListNode(val);
        if (this.right != null) {  
        // Queue is not empty 
            this.right.next = newNode;
            this.right = this.right.next;
        } else {       
        // Queue is empty             
            this.left = newNode;
            this.right = newNode;
        }
    }

    public int dequeue() {
        if (this.left == null) {
            // Queue is empty 
            System.exit(0);
        }
        int val = this.left.val;
        this.left = this.left.next;
        if (this.left == null) {
            this.right = null;
        }
        return val;
    }

    public void print() {
        ListNode cur = this.left;
        while(cur != null) {
            System.out.print(cur.val + " -> ");
            cur = cur.next;
        }
        System.out.println();
    }

}



//Insertion Sort 
public class Main {
  public static void main (String [] args) {
   int [] array = {45,12,85,32,89,39,69,44,42,1,6,8};
   int temp;
   for (int i = 1; i < array.length; i++) {
    for (int j = i; j > 0; j--) {
     if (array[j] < array [j - 1]) {
      temp = array[j];
      array[j] = array[j - 1];
      array[j - 1] = temp;
     }
    }
   }
   for (int i = 0; i < array.length; i++) {
     System.out.println(array[i]);
   }
  }
} 

public static int recursiveBinarySearch(int[] sortedArray, int begin, int end, int key) {
  if (begin < end) {
   int middle = begin + (end - begin) / 2;
   if(key < sortedArray[middle]) {
    return recursiveBinarySearch(sortedArray, begin, middle, key);
   } else if (key > sortedArray[middle]) {
    return recursiveBinarySearch(sortedArray, middle+1, end, key);
   } else {
    return middle;
   }
  }
   return -(begin = 1);
   
} 


public static void main(String[] args) {
  //establish our sorted array
  int[] sortedArr = {1, 53, 62, 133, 384, 553, 605, 897, 1035, 1234};
  int searchIndex = recursiveBinarySearch(sortedArr, 0, sortedArr.length, 605);
 System.out.println("I Found 605 at index " + searchIndex);
}

// """Synthesizes speech from the input string of text."""
// from google.cloud import texttospeech

// client = texttospeech.TextToSpeechClient()

// input_text = texttospeech.SynthesisInput(text="I want to make this work.")

// # Note: the voice can also be specified by name.
// # Names of voices can be retrieved with client.list_voices().
// voice = texttospeech.VoiceSelectionParams(
//     language_code="en-US",
//     name="en-US-Studio-O",
// )

// audio_config = texttospeech.AudioConfig(
//     audio_encoding=texttospeech.AudioEncoding.LINEAR16,
//     speaking_rate=1.85
// )

// response = client.synthesize_speech(
//     request={"input": input_text, "voice": voice, "audio_config": audio_config}
// )

// # The response's audio_content is binary.
// with open("output.mp3", "wb") as out:
//     out.write(response.audio_content)
//     print('Audio content written to file "output.mp3"')

