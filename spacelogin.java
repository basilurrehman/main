import javax.swing.*;import java.awt.*;import java.awt.event.*;

public class spacelogin extends JFrame{JLabel l1,l2,l3;JTextField t1;JPasswordField p1;JButton b1;

public spacelogin(){
setTitle("Space Station Login");
setSize(400,300);
setLayout(null);
getContentPane().setBackground(new Color(10,10,30));
l1=new JLabel("Space Station Control");l1.setBounds(90,20,250,30);l1.setForeground(Color.cyan);
l2=new JLabel("Commander ID:");l2.setBounds(50,80,100,30);l2.setForeground(Color.white);
l3=new JLabel("Access Code:");l3.setBounds(50,120,100,30);l3.setForeground(Color.white);
t1=new JTextField();t1.setBounds(160,80,160,25);
p1=new JPasswordField();p1.setBounds(160,120,160,25);
b1=new JButton("Engage");b1.setBounds(140,180,100,30);b1.setBackground(Color.green);
b1.addActionListener(new ActionListener(){public void actionPerformed(ActionEvent e){
String u=t1.getText();String p=new String(p1.getPassword());
if(u.equals("Alpha1")&&p.equals("Gal@xy99")){JOptionPane.showMessageDialog(null,"Access Granted Captain");}
else{JOptionPane.showMessageDialog(null,"Unauthorized Entry");}
}});
add(l1);add(l2);add(l3);add(t1);add(p1);add(b1);
setDefaultCloseOperation(EXIT_ON_CLOSE);
setVisible(true);
}
public static void main(String[]args){new spacelogin();}
}
