    package app;

    import java.awt.*;
    import java.awt.event.*;
    import javax.swing.*;



    class Pause extends JPanel implements KeyListener {
        private Map map;
        private JButton startButton;
        private JButton restartButton;
        private JButton exitButton;
        private JPanel buttonPanel;
        private Image pacmanAnimImage;
        private int animX = -100; // Starting position off-screen left
        private int animY;
        private Timer animationTimer;

        public Pause(Map map) {
            this.map = map;
            setLayout(new GridBagLayout());
            setOpaque(false);
            setFocusable(true);
            addKeyListener(this);

            // Load animation image
            pacmanAnimImage = new ImageIcon(getClass().getResource("./pacmanRight.png")).getImage()
                .getScaledInstance(50, 50, Image.SCALE_SMOOTH);

            createButtons();
            setVisible(false);

            // Setup animation timer
            animationTimer = new Timer(10, e -> {
                animX += 2;
                if (animX > getWidth()) {
                    animX = -100; // Reset to left when it goes off-scSreen right
                }
                repaint();
            });
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);

            // Draw semi-transparent overlay
            g.setColor(new Color(0, 0, 0, 180));
            g.fillRect(0, 0, getWidth(), getHeight());

            // Draw "PAUSED" text
            g.setColor(Color.YELLOW);
            g.setFont(new Font("Arial", Font.BOLD, 48));
            String text = "PAUSED";
            int textWidth = g.getFontMetrics().stringWidth(text);
            g.drawString(text, getWidth()/2 - textWidth/2, 100);

            // Draw moving animation
            animY = getHeight()/2 + 50;
            g.drawImage(pacmanAnimImage, animX, animY, this);
        }

        private void createButtons() {
            buttonPanel = new JPanel();
            buttonPanel.setLayout(new GridLayout(3, 1, 10, 10));
            buttonPanel.setOpaque(false);

            startButton = new JButton("Resume");
            restartButton = new JButton("Restart");
            exitButton = new JButton("Exit");

            // Style buttons
            styleButton(startButton);
            styleButton(restartButton);
            styleButton(exitButton);

            // Add action listeners
            startButton.addActionListener(e -> togglePause());
            restartButton.addActionListener(e -> restartGame());
            exitButton.addActionListener(e -> System.exit(0));

            buttonPanel.add(startButton);
            buttonPanel.add(restartButton);
            buttonPanel.add(exitButton);

            add(buttonPanel);
        }

        private void styleButton(JButton button) {
            button.setFont(new Font("Arial", Font.BOLD, 24));
            button.setBackground(new Color(255, 255, 150));
            button.setForeground(Color.BLACK);
            button.setFocusPainted(false);
            button.setPreferredSize(new Dimension(200, 60));
            button.setOpaque(true);
            button.setBorderPainted(true);
        }

     public void togglePause() {
    map.isPaused = !map.isPaused;
    setVisible(map.isPaused);
    
    if (map.isPaused) {
        animationTimer.start();
        requestFocusInWindow();
    } else {
        animationTimer.stop();
        map.requestFocusInWindow(); // Return focus to game
    }
}

        private void restartGame() {
            map.isPaused = false;
            setVisible(false);
            animationTimer.stop();
            map.resetGame();
             map.requestFocusInWindow();
        }

        @Override
        public void keyTyped(KeyEvent e) {}

        @Override
        public void keyPressed(KeyEvent e) {
            if (e.getKeyCode() == KeyEvent.VK_SPACE) {
                togglePause();
            }
        }

        @Override
        public void keyReleased(KeyEvent e) {}
    } 


