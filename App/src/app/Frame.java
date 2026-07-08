package app;

import java.awt.Component;
import java.awt.Image;
import javax.swing.ImageIcon;
import javax.swing.JFrame;

class Frame extends JFrame {
    ImageIcon logo = new ImageIcon(App.class.getResource("logo_1.png"));
    Map map;
    LoginSystem loginSystem;
    Sound sound;
    Frame() {
        loginSystem = new LoginSystem();
        
        if (!loginSystem.showLoginDialog(this)) {
            System.exit(0);
        }
        
        loginSystem.showHighScores(this);
       
        map = new Map(loginSystem);
       
       
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setResizable(false);
        this.setTitle("Pac-Man");
        this.setIconImage(logo.getImage());
        this.add(map);
        
        this.pack();
        this.setLocationRelativeTo(null);
        this.setVisible(true);
    }
    
    @Override
    public void dispose() {
        loginSystem.close();
        super.dispose();
    }
}