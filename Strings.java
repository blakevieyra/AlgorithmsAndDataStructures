
// String sign = "STOP";
//   //convert to char array
// char[] newSign = sign.toCharArray();
//   //cycle through chars
// for (char c : newSign) {
//   System.out.println(c);
//   System.out.println(sign);
//   }
// charArray[2] = '!';
// for (char c : charArray) {
//   System.out.println(c);
// }  
// char[] charArray = {"S", "T", "O", "P"};
// String newArray = new String(charArray);
// System.out.println(newArray);

public class Strings {
public static void main(String[] args) {
   StringBuilder s1 = new StringBuilder("STO");
   System.out.println(s1);
   //append the P
   s1.append("P");
   System.out.println(s1);
   //insert an exclamation point
   s1.insert(0, "!");
   System.out.println(s1);
   //reverse, reverse!
   s1.reverse();
   System.out.println(s1);
  }
}