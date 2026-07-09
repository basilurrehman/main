package app;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Cursor;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.GridLayout;
import java.awt.Image;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.HashSet;
import java.util.Random;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JPanel;
import javax.swing.OverlayLayout;
import javax.swing.Timer;
import javax.swing.BorderFactory;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.SwingConstants;


class Map extends JPanel implements KeyListener, ActionListener {
    //tile variables
    protected int blockSize = 32;
    protected int columns = 19;
    protected int rows = 21;
    protected int width = columns * blockSize;
    protected int height = rows * blockSize;
    
    // game variables
    protected boolean gameOver = false;
    protected int life = 3;
    protected int score = 0;
    
    // Movement variables
    private char currentDirection = 'w'; // Current moving direction
    private char nextDirection = 'w';    // Next attempted direction
    //blue ghost movement
    private char blueGhostDir = 'a';
private int blueGhostStepCount = 0;
//red ghost movement
 private char redGhostDir = 'w';
private int redGhostStepCount = 0;
//Pink ghost movement
 private char pinkGhostDir = 's';
private int pinkGhostStepCount = 0;
//orange ghost movement
 private char orangeGhostDir = 'd';
private int orangeGhostStepCount = 0;
//pause screen vaiables
public boolean isPaused = false;
private Pause pauseMenu;
  //login system variable
private LoginSystem loginSystem;
//sound variable
private Sound sound;
 private boolean foodCollected = false;//takay food collect wali sound play ho
    
    HashSet<Position> walls;
    HashSet<Position> foods;
    Position blueGhost;
    Position redGhost;
    Position pinkGhost;
    Position orangeGhost;
    Position Pacman;
    
    private Image wallImage;
    private Image blueGhostImage;
    private Image orangeGhostImage;
    private Image pinkGhostImage;
    private Image redGhostImage;
    private Image pacmanUpImage;
    private Image pacmanDownImage;
    private Image pacmanLeftImage;
    private Image pacmanRightImage;

    Map(LoginSystem loginSystem) {
        //initilizing
        this.loginSystem = loginSystem;
        this.sound = new Sound();
         sound.playGameStart();
        //setting window
        setPreferredSize(new Dimension(width, height));
        setBackground(Color.BLACK);
        setDoubleBuffered(true);
        addKeyListener(this);
        setFocusable(true);
        requestFocusInWindow();
        

        // Load images
        wallImage = new ImageIcon(getClass().getResource("./wall.png")).getImage();
        blueGhostImage = new ImageIcon(getClass().getResource("./blueGhost.png")).getImage();
        orangeGhostImage = new ImageIcon(getClass().getResource("./orangeGhost.png")).getImage();
        pinkGhostImage = new ImageIcon(getClass().getResource("./pinkGhost.png")).getImage();
        redGhostImage = new ImageIcon(getClass().getResource("./redGhost.png")).getImage();
        pacmanUpImage = new ImageIcon(getClass().getResource("./pacmanUp.png")).getImage();
        pacmanDownImage = new ImageIcon(getClass().getResource("./pacmanDown.png")).getImage();
        pacmanLeftImage = new ImageIcon(getClass().getResource("./pacmanLeft.png")).getImage();
        pacmanRightImage = new ImageIcon(getClass().getResource("./pacmanRight.png")).getImage();
        //pause menu
       pauseMenu = new Pause(this);
    this.setLayout(new OverlayLayout(this));
    this.add(pauseMenu);
    pauseMenu.setFocusable(true);
//loading map
        loadMap();
        
        // Game loop 
        Timer gameLoop = new Timer(10, this);
        gameLoop.start();
    }

    private String[] tileMap = {
        "XXXXXXXXXXXXXXXXXXX",
        "X        X        X",
        "X XX XXX X XXX XX X",
        "X                 X",
        "X XX X XXXXX X XX X",
        "X    X       X    X",
        "XXXX XXXX XXXX XXXX",
        "OOOX X       X XOOO",
        "XXXX X XXrXX X XXXX",
        "        bpo        ",
        "XXXX X XXXXX X XXXX",
        "OOOX X       X XOOO",
        "XXXX X XXXXX X XXXX",
        "X        X        X",
        "X XX XXX X XXX XX X",
        "X  X     P     X  X",
        "XX X X XXXXX X X XX",
        "X    X   X   X    X",
        "X XXXXXX X XXXXXX X",
        "X                 X",
        "XXXXXXXXXXXXXXXXXXX" 
    };

    protected void loadMap() {
        walls = new HashSet<>(); 
        foods = new HashSet<>(); 
        
        for(int r = 0; r < rows; r++) {
            String currentRow = tileMap[r];
            for(int c = 0; c < columns; c++) {
                char currentTile = currentRow.charAt(c);
                int x = c * blockSize;
                int y = r * blockSize;
                
                switch(currentTile) {
                    case 'X':
                        walls.add(new Position(wallImage, x, y, blockSize, blockSize));
                        break;
                    case ' ':
                        foods.add(new Position(null, x + 14, y + 14, 4, 4));
                        break;
                    case 'P':
                        Pacman = new Position(pacmanRightImage, x, y, blockSize, blockSize);
                        break;
                    case 'b':
                        blueGhost = new Position(blueGhostImage, x, y, blockSize, blockSize);
                        break;
                    case 'o':
                        orangeGhost = new Position(orangeGhostImage, x, y, blockSize, blockSize);
                        break;
                    case 'r':
                        redGhost = new Position(redGhostImage, x, y, blockSize, blockSize);
                        break;
                    case 'p':
                        pinkGhost = new Position(pinkGhostImage, x, y, blockSize, blockSize);
                        break;
                }
            }
        }
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        draw(g);
        
    }

    public void draw(Graphics g) {
        if (Pacman != null) {
            g.drawImage(Pacman.image, Pacman.x, Pacman.y, Pacman.width, Pacman.height, null);
        }

       if(blueGhost != null){
            g.drawImage(blueGhost.image, blueGhost.x, blueGhost.y, blueGhost.width, blueGhost.height, null);
       }
        if(redGhost != null){
            g.drawImage(redGhost.image, redGhost.x, redGhost.y, redGhost.width, redGhost.height, null);
       }
         if(orangeGhost != null){
            g.drawImage(orangeGhost.image, orangeGhost.x, orangeGhost.y, orangeGhost.width, orangeGhost.height, null);
       }
          if(pinkGhost != null){
            g.drawImage(pinkGhost.image, pinkGhost.x, pinkGhost.y, pinkGhost.width, pinkGhost.height, null);
       }

        for (Position wall : walls) {
            g.drawImage(wall.image, wall.x, wall.y, wall.width, wall.height, null);
        }

        g.setColor(Color.ORANGE);
        for (Position food : foods) {
            g.fillRect(food.x, food.y, food.width, food.height);
        }
        g.setFont(new Font(Font.MONOSPACED, Font.BOLD, 15));
        if (gameOver) {
            g.drawString("Game Over: " + String.valueOf(score), blockSize/2, blockSize/2);
            loginSystem.saveScore(score);
        }
        else {
            g.drawString("x" + String.valueOf(life) + " Score: " + String.valueOf(score), blockSize/2, blockSize/2);
        }
    }

    public void move() {
        // pehley check kero k new button say collusion to nai horha
        if (tryMove(nextDirection)) {
            currentDirection = nextDirection;
            
         
        
            return;
        }
        
        // If next direction fails, keep the current direction
        tryMove(currentDirection);
        
   

    }

   private boolean tryMove(char direction) {
    int nextX = Pacman.x;
    int nextY = Pacman.y;

    switch(direction) {
        case 'a':  
            nextX -= blockSize/12;
            Pacman.image = pacmanLeftImage;
            break;
        case 'd':
            nextX += blockSize/12;
            Pacman.image = pacmanRightImage;
            break;
        case 'w':
            nextY -= blockSize/12;
            Pacman.image = pacmanUpImage;
            break;
        case 's':
            nextY += blockSize/12;
            Pacman.image = pacmanDownImage;
            break;
    }

 
    // Check wall collision first (if wall, movement fails)
    Position nextPacman = new Position(null, nextX, nextY, Pacman.width, Pacman.height);
    for (Position wall : walls) {
        if (collision(nextPacman, wall)) {
            return false; // Wall collision → movement blocked
        }
    }

    // If no wall collision, check if next position has food
    Position foodToRemove = null;
    for (Position food : foods) {
        // Check if food is at (nextX, nextY) before Pacman moves
        if (food.x + food.width/2 >= nextX && 
            food.x <= nextX + Pacman.width &&
            food.y + food.height/2 >= nextY && 
            food.y <= nextY + Pacman.height) {
            foodToRemove = food;
            sound.playChomp(); 
            score += 10;
            gameWon();
            break; 
        }
    }

    // Remove food before moving
    if (foodToRemove != null) {
        foods.remove(foodToRemove);
    }
       if(nextX == 0 && Pacman.image == pacmanLeftImage){
        Pacman.x = 608;   
    }
       else if(nextX == 608 && Pacman.image == pacmanRightImage){
           Pacman.x = 0;
       }

    // move Pacman to the new position
       else{
    Pacman.x = nextX;}
    Pacman.y = nextY;
    repaint();
    return true;
}
//main collision formula
    public boolean collision(Position a, Position b) {
        return a.x < b.x + b.width &&
               a.x + a.width > b.x &&
               a.y < b.y + b.height &&
               a.y + a.height > b.y;
    }

 public void ghostMovementBlue() {
    int nextX = blueGhost.x;
    int nextY = blueGhost.y;

    switch(blueGhostDir) {
        case 'a': nextX -= blockSize / 12; break;
        case 'd': nextX += blockSize / 12; break;
        case 'w': nextY -= blockSize / 12; break;
        case 's': nextY += blockSize / 12; break;
    }


    Position nextBlue = new Position(null, nextX, nextY, blueGhost.width, blueGhost.height);

    boolean collided = false;
    for (Position wall : walls) {
        if (collision(nextBlue, wall)) {
            collided = true;
            break;
        }
    }

    if (collided || blueGhostStepCount >= 5 * blockSize) {
        // change direction on collision or after 5 tiles
        Random rand = new Random();
        char[] keys = {'w','a','s','d'};
        char newDir;

        do {
            newDir = keys[rand.nextInt(keys.length)];
        } while (newDir == blueGhostDir);

        blueGhostDir = newDir;
        blueGhostStepCount = 0;
    } else {
       
        blueGhost.x = nextX;
        blueGhost.y = nextY;
        blueGhostStepCount += blockSize / 12;
    }
    if(nextX == 0 ){
        blueGhost.x = 608;   
    }
       else if(nextX == 608 ){
           blueGhost.x = 0;
       }
}//ghostMovementBlue ends here
public void ghostMovementPink() {
    int nextX = pinkGhost.x;
    int nextY = pinkGhost.y;

    switch(pinkGhostDir) {
        case 'a': nextX -= blockSize / 12; break;
        case 'd': nextX += blockSize / 12; break;
        case 'w': nextY -= blockSize / 12; break;
        case 's': nextY += blockSize / 12; break;
    }

    Position nextPink = new Position(null, nextX, nextY, pinkGhost.width, pinkGhost.height);

    boolean collided = false;
    for (Position wall : walls) {
        if (collision(nextPink, wall)) {
            collided = true;
            break;
        }
    }

    if (collided || pinkGhostStepCount >= 5 * blockSize) {
        // change direction on collision or after 5 tiles
        Random rand = new Random();
        char[] keys = {'w','a','s','d'};
        char newDir;

        do {
            newDir = keys[rand.nextInt(keys.length)];
        } while (newDir == pinkGhostDir);

        pinkGhostDir = newDir;
        pinkGhostStepCount = 0;
    } else {
       
        pinkGhost.x = nextX;
        pinkGhost.y = nextY;
        pinkGhostStepCount += blockSize / 12;
    }
    if(nextX == 0 ){
        pinkGhost.x = 608;   
    }
       else if(nextX == 608 ){
           pinkGhost.x = 0;
       }
}
public void ghostMovementRed() {
    int nextX = redGhost.x;
    int nextY = redGhost.y;

    switch(redGhostDir) {
        case 'a': nextX -= blockSize / 12; break;
        case 'd': nextX += blockSize / 12; break;
        case 'w': nextY -= blockSize / 12; break;
        case 's': nextY += blockSize / 12; break;
    }

    Position nextRed = new Position(null, nextX, nextY, redGhost.width, redGhost.height);

    boolean collided = false;
    for (Position wall : walls) {
        if (collision(nextRed, wall)) {
            collided = true;
            break;
        }
    }

    if (collided || redGhostStepCount >= 7 * blockSize) {
        // change direction on collision or after 7 tiles
        Random rand = new Random();
        char[] keys = {'w','a','s','d'};
        char newDir;

        do {
            newDir = keys[rand.nextInt(keys.length)];
        } while (newDir == redGhostDir);

        redGhostDir = newDir;
        redGhostStepCount = 0;
    } else {
       
        redGhost.x = nextX;
        redGhost.y = nextY;
        redGhostStepCount += blockSize / 12;
    }
    if(nextX == 0 ){
        redGhost.x = 608;   
    }
       else if(nextX == 608 ){
           redGhost.x = 0;
       }
}
public void ghostMovementOrange() {
    int nextX = orangeGhost.x;
    int nextY = orangeGhost.y;

    switch(orangeGhostDir) {
        case 'a': nextX -= blockSize / 12; break;
        case 'd': nextX += blockSize / 12; break;
        case 'w': nextY -= blockSize / 12; break;
        case 's': nextY += blockSize / 12; break;
    }

    Position nextOrange = new Position(null, nextX, nextY, orangeGhost.width, orangeGhost.height);

    boolean collided = false;
    for (Position wall : walls) {
        if (collision(nextOrange, wall)) {
            collided = true;
            break;
        }
    }

    if (collided || orangeGhostStepCount >= 4 * blockSize) {
        // change direction on collision or after 5 tiles
        Random rand = new Random();
        char[] keys = {'w','a','s','d'};
        char newDir;

        do {
            newDir = keys[rand.nextInt(keys.length)];
        } while (newDir == orangeGhostDir);

        orangeGhostDir = newDir;
        orangeGhostStepCount = 0;
    } else {
       
        orangeGhost.x = nextX;
        orangeGhost.y = nextY;
        orangeGhostStepCount += blockSize / 12;
    }
    if(nextX == 0 ){
        orangeGhost.x = 608;   
    }
       else if(nextX == 608 ){
           orangeGhost.x = 0;
       }
}
//to access pauseMenu and change the isPaused condition will run when space is clicked
public void togglePause() {
    isPaused = !isPaused;
    pauseMenu.setVisible(isPaused);
    if (isPaused) {
        pauseMenu.requestFocusInWindow();
        System.out.println("Game Paused"); // Debug line
    } else {
        requestFocusInWindow();
        System.out.println("Game Resumed"); // Debug line
    }
    repaint();
}
//jab restart button pause menu mein press ho mouse listener mein ye method run keray ga
public void resetGame() {
    gameOver = false;
    isPaused = false;

    life  = 3;
    score = 0;

    // 1️⃣  Let Pac-Man start idle
    currentDirection = ' ';
    nextDirection    = ' ';

    // 2️⃣  Rebuild the map FIRST – this gives you fresh Position objects
    walls.clear();
    foods.clear();
    loadMap();          // <-- creates new Pacman / ghost instances

    // 3️⃣  Now snap the *new* instances to their spawn coordinates
    resetPositions();   

    // If you ever stopped the timer when gameOver==true, restart it here
    // gameLoop.start();

    requestFocusInWindow();   // regain keyboard input
    repaint();
}

    private void resetPositions() {
   
    Pacman.x = Pacman.startX;
    Pacman.y = Pacman.startY;
    
    blueGhost.x = blueGhost.startX;
    blueGhost.y = blueGhost.startY;
    
    redGhost.x = redGhost.startX;
    redGhost.y = redGhost.startY;
    
    pinkGhost.x = pinkGhost.startX;
    pinkGhost.y = pinkGhost.startY;
    
    orangeGhost.x = orangeGhost.startX;
    orangeGhost.y = orangeGhost.startY;
    
    repaint(); 
}//reset position ends here
    
    
// Add these methods to your Map class
private void showGameOverDialog() {
    // Get high score from login system
    int highScore = loginSystem.getCurrentHighScore();
    
    // Create custom dialog
    JDialog gameOverDialog = new JDialog();
    gameOverDialog.setTitle("Game Over");
    gameOverDialog.setSize(400, 300);
    gameOverDialog.setLayout(new BorderLayout(10, 10));
    gameOverDialog.setLocationRelativeTo(this);
    gameOverDialog.setModal(true);
    
    // Main panel with game over message
    JPanel mainPanel = new JPanel(new GridLayout(3, 1, 10, 10));
    mainPanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
    mainPanel.setBackground(Color.BLACK);
    
    // Game over label
    JLabel gameOverLabel = new JLabel("GAME OVER", SwingConstants.CENTER);
    gameOverLabel.setFont(new Font("Arial", Font.BOLD, 32));
    gameOverLabel.setForeground(Color.RED);
    
    // Score labels
    JLabel scoreLabel = new JLabel("Your Score: " + score, SwingConstants.CENTER);
    JLabel highScoreLabel = new JLabel("High Score: " + highScore, SwingConstants.CENTER);
    
    Font scoreFont = new Font("Arial", Font.BOLD, 20);
    scoreLabel.setFont(scoreFont);
    scoreLabel.setForeground(Color.WHITE);
    highScoreLabel.setFont(scoreFont);
    highScoreLabel.setForeground(Color.YELLOW);
    
    // Add components to main panel
    mainPanel.add(gameOverLabel);
    mainPanel.add(scoreLabel);
    mainPanel.add(highScoreLabel);
    
    // Button panel
    JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 20, 10));
    buttonPanel.setBackground(Color.BLACK);
    
    // Restart button
    JButton restartButton = createPacmanButton("Play Again");
    restartButton.addActionListener(e -> {
        resetGame();
        gameOverDialog.dispose();
    });
    
    // High scores button
    JButton highScoresButton = createPacmanButton("View High Scores");
    highScoresButton.addActionListener(e -> {
        loginSystem.showHighScores(gameOverDialog);
    });
    
    buttonPanel.add(restartButton);
    buttonPanel.add(highScoresButton);
    
    // Add panels to dialog
    gameOverDialog.add(mainPanel, BorderLayout.CENTER);
    gameOverDialog.add(buttonPanel, BorderLayout.SOUTH);
    
    // Show dialog
    gameOverDialog.setVisible(true);
}

public void gameWon() {
    if (score >= 1860) {
        // Getting high score from login system
        int highScore = loginSystem.getCurrentHighScore();
        
        //  dialog
        JDialog winDialog = new JDialog();
        winDialog.setTitle("Congratulations!");
        winDialog.setSize(450, 300);
        winDialog.setLayout(new BorderLayout(10, 10));
        winDialog.setLocationRelativeTo(this);
        winDialog.setModal(true);
        
        // Main panel with win message
        JPanel mainPanel = new JPanel(new GridLayout(4, 1, 10, 10));
        mainPanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
        mainPanel.setBackground(Color.BLACK);
        
        // Win label
        JLabel winLabel = new JLabel("YOU WIN!", SwingConstants.CENTER);
        winLabel.setFont(new Font("Arial", Font.BOLD, 32));
        winLabel.setForeground(Color.GREEN);
        
        // Message label
        JLabel messageLabel = new JLabel("You reached 1860 points!", SwingConstants.CENTER);
        messageLabel.setFont(new Font("Arial", Font.PLAIN, 18));
        messageLabel.setForeground(Color.WHITE);
        
        // Score labels
        JLabel scoreLabel = new JLabel("Final Score: " + score, SwingConstants.CENTER);
        JLabel highScoreLabel = new JLabel("High Score: " + highScore, SwingConstants.CENTER);
        
        Font scoreFont = new Font("Arial", Font.BOLD, 20);
        scoreLabel.setFont(scoreFont);
        scoreLabel.setForeground(Color.YELLOW);
        highScoreLabel.setFont(scoreFont);
        highScoreLabel.setForeground(Color.YELLOW);
        
        // Add to main panel
        mainPanel.add(winLabel);
        mainPanel.add(messageLabel);
        mainPanel.add(scoreLabel);
        mainPanel.add(highScoreLabel);
        
        // Button panel
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 20, 10));
        buttonPanel.setBackground(Color.BLACK);
        
        // Restart button
        JButton restartButton = createPacmanButton("Play Again");
        restartButton.addActionListener(e -> {
            resetGame();
            winDialog.dispose();
        });
        
        // High scores button
        JButton highScoresButton = createPacmanButton("View High Scores");
        highScoresButton.addActionListener(e -> {
            loginSystem.showHighScores(winDialog);
        });
        
        buttonPanel.add(restartButton);
        buttonPanel.add(highScoresButton);
        
        // Add panels to dialog
        winDialog.add(mainPanel, BorderLayout.CENTER);
        winDialog.add(buttonPanel, BorderLayout.SOUTH);
        
        // Show dialog
         gameOver = true;
         loginSystem.saveScore(score);
        winDialog.setVisible(true);
        
       
        
    }
}

//buttons Design
private JButton createPacmanButton(String text) {
    JButton button = new JButton(text);
    button.setFont(new Font("Arial", Font.BOLD, 16));
    button.setBackground(Color.YELLOW);
    button.setForeground(Color.BLACK);
    button.setFocusPainted(false);
    button.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(Color.WHITE, 2),
            BorderFactory.createEmptyBorder(8, 20, 8, 20)
    ));
    
    button.addMouseListener(new MouseAdapter() {
        public void mouseEntered(MouseEvent e) {
            button.setBackground(Color.ORANGE);
            button.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        }
        public void mouseExited(MouseEvent e) {
            button.setBackground(Color.YELLOW);
        }
    });
    
    return button;
}
    @Override
    public void keyTyped(KeyEvent e) {}

    @Override
    public void keyPressed(KeyEvent e) {
        char key = Character.toLowerCase(e.getKeyChar());
        if (key == 'w' || key == 'a' || key == 's' || key == 'd') {
            nextDirection = key; 
        }
         else if (e.getKeyCode() == KeyEvent.VK_SPACE) {
        togglePause();//map class wala not pause class
    }
    }

    @Override
    public void keyReleased(KeyEvent e) {}
//jab bhi koi action listener milay move will be applied
    @Override
    public void actionPerformed(ActionEvent e) {
         if (isPaused || gameOver) {
        return; // Skip all game logic when paused or game over
    }
            move();
            ghostMovementBlue();
ghostMovementRed();
ghostMovementPink();
ghostMovementOrange();
repaint();

//now for collusion between pacman and ghost
if (collision(Pacman, blueGhost) || collision(Pacman, redGhost) ||
        collision(Pacman, pinkGhost) || collision(Pacman, orangeGhost)) {
        
        life--;
         sound.playDeath();
       
        Pacman.x = Pacman.startX;
        Pacman.y = Pacman.startY;

        blueGhost.x = blueGhost.startX;
        blueGhost.y = blueGhost.startY;

        redGhost.x = redGhost.startX;
        redGhost.y = redGhost.startY;

        pinkGhost.x = pinkGhost.startX;
        pinkGhost.y = pinkGhost.startY;

        orangeGhost.x = orangeGhost.startX;
        orangeGhost.y = orangeGhost.startY;

        if (life == 0) {
            gameOver = true;
            showGameOverDialog();
            sound.playGameOver();
             resetPositions(); 
    repaint(); 
        }
    }

    repaint();
        
    }//action performed ends here
    }



public class App {
    public static void main(String[] args) {
    new Frame();
    }
}