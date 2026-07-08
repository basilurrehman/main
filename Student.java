// import java.util.Scanner;
// import java.util.Random;

// class temp{
    
//     public static void main(String[] args) {
//         // System.out.printf("Hello World\n");
//         // int i = 2147483647;
//         // char ch = 'a';
//         // double d = 3.1415926535;
//         // float x = 3.14f;
//         // String s = "Hello World";

//         // System.out.printf("%.2f",d+i);

//         // Scanner sc = new Scanner(System.in);
//         // System.out.println("Enter 10-digit telephone number:  ");
//         // String tel = sc.next();
//         // System.out.printf("%s\n",tel);
//         // System.out.printf("%s\n",tel.substring(0,3));
//         // System.out.printf("%s\n",tel.substring(3,6));
//         // System.out.printf("%s\n",tel.substring(6));
//         // System.out.printf("%s\n",tel.substring(0,3)+"-"+tel.substring(3,6)+"-"+tel.substring(6));

//         // Random rd = new Random();
//         // int year = rd.nextInt(200)+1800;
//         // if ((year%400)==0 || ((year%4)==0&&(year%100)!=0))
//         // System.out.printf("leap year %d",year);
//         // else
//         // System.out.printf("not %d",year);

//         // int arr[] = {1,2,3};
//         // for(int i:arr)
//         // {
//         //     System.out.printf("%d\t\t%d",i,arr[i]);
//         // }

//         // int arr[]= new int[25];
//         // for(int i = 0; i <25;i++){
//         // arr[i]=i+1;
//         // System.out.printf("%d",arr[i]);}

//         // int arr[][];
//         // arr = new int[5][];
//         // arr[0]= new int[5];
//         // arr[1]= new int[5];
//         // arr[2]= new int[5];
//         // arr[3]= new int[5];
//         // arr[4]= new int[5];
//     }
// }

public class Student{
    String name = "Tariq"; // Student's name
    int ID = 123; // unique ID number for the student
    public Student(){}
    public Student(String name, int ID){ //why above line first then this and if constructor is a method then what is the return type
        this.name = name; // can i keep variable name same 2 name?
        this.ID=ID;
    }
    public void print(){ 
        System.out.printf("%s",name);
        System.out.println("Student ID : " +ID);
    }
     
}