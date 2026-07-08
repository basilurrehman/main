    package app;

    import javax.swing.*;
    import java.awt.*;
    import java.awt.event.*;
    import java.sql.*;

    class LoginSystem {
        private static final String DB_URL = "jdbc:ucanaccess://pacman_scores.accdb";
        private Connection conn;
        private String currentUser;
        private int currentHighScore;

        public LoginSystem() {
            initializeDatabase();
        }

        private void initializeDatabase() {
            try {
                Class.forName("net.ucanaccess.jdbc.UcanaccessDriver");
                conn = DriverManager.getConnection(DB_URL);

                DatabaseMetaData meta = conn.getMetaData();

                // Create users table if missing, now including password column
                ResultSet tables = meta.getTables(null, null, "users", null);
                if (!tables.next()) {
                    Statement stmt = conn.createStatement();
                    stmt.execute("CREATE TABLE users (" +
                            "id COUNTER CONSTRAINT PK_users PRIMARY KEY, " +
                            "usernajavac -cp .:lib/mysql-connector-j-8.0.29.jar SampleDBApp.java\r\n" + //
                                                                "java -cp .:lib/mysql-connector-j-8.0.29.jar SampleDBApp\r\n" + //
                                                                "e TEXT(50) CONSTRAINT username_unique UNIQUE, " +
                            "password TEXT(50), " +  // password column added here
                            "highscore INTEGER DEFAULT 0)");
                    stmt.close();
                }

                // Create scores table if missing
                tables = meta.getTables(null, null, "scores", null);
                if (!tables.next()) {
                    Statement stmt = conn.createStatement();
                    stmt.execute("CREATE TABLE scores (" +
                            "id COUNTER CONSTRAINT PK_scores PRIMARY KEY, " +
                            "user_id LONG NOT NULL, " +
                            "score INTEGER NOT NULL, " +
                            "game_date DATETIME DEFAULT NOW(), " +
                            "CONSTRAINT FK_user FOREIGN KEY (user_id) REFERENCES users(id))");
                    stmt.close();
                }
            } catch (Exception e) {
                JOptionPane.showMessageDialog(null,
                        "Database error: " + e.getMessage(),
                        "Error", JOptionPane.ERROR_MESSAGE);
                e.printStackTrace();
            }
        }

        /**
         * Shows combined Login / Sign Up dialog.
         * Returns true if user logged in or signed up successfully.
         */
        public boolean showLoginDialog(Component parent) {
            JPanel panel = new JPanel(new GridBagLayout());
            panel.setBackground(Color.BLACK);
            panel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

            GridBagConstraints gbc = new GridBagConstraints();
            gbc.insets = new Insets(10, 10, 10, 10);
            gbc.fill = GridBagConstraints.HORIZONTAL;

            // Title
            JLabel titleLabel = new JLabel("PAC-MAN");
            titleLabel.setFont(new Font("Arial", Font.BOLD, 32));
            titleLabel.setForeground(Color.YELLOW);
            titleLabel.setHorizontalAlignment(SwingConstants.CENTER);
            gbc.gridx = 0; gbc.gridy = 0; gbc.gridwidth = 2;
            panel.add(titleLabel, gbc);

            // Subtitle
            JLabel subtitleLabel = new JLabel("ENTER YOUR CREDENTIALS");
            subtitleLabel.setFont(new Font("Arial", Font.BOLD, 18));
            subtitleLabel.setForeground(Color.WHITE);
            subtitleLabel.setHorizontalAlignment(SwingConstants.CENTER);
            gbc.gridy = 1;
            panel.add(subtitleLabel, gbc);

            // Username label & field
            JLabel userLabel = new JLabel("Username:");
            userLabel.setForeground(Color.YELLOW);
            userLabel.setFont(new Font("Arial", Font.BOLD, 14));
            gbc.gridwidth = 1; gbc.gridy = 2; gbc.gridx = 0;
            panel.add(userLabel, gbc);

            JTextField usernameField = new JTextField(15);
            styleTextField(usernameField);
            gbc.gridx = 1;
            panel.add(usernameField, gbc);

            // Password label & field
            JLabel passLabel = new JLabel("Password:");
            passLabel.setForeground(Color.YELLOW);
            passLabel.setFont(new Font("Arial", Font.BOLD, 14));
            gbc.gridy = 3; gbc.gridx = 0;
            panel.add(passLabel, gbc);

            JPasswordField passwordField = new JPasswordField(15);
            styleTextField(passwordField);
            gbc.gridx = 1;
            panel.add(passwordField, gbc);

            // Buttons panel with Login and Sign Up
            JPanel buttonsPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 15, 0));
            buttonsPanel.setBackground(Color.BLACK);

            JButton loginButton = createPacmanButton("LOGIN");
            JButton signUpButton = createPacmanButton("SIGN UP");
            buttonsPanel.add(loginButton);
            buttonsPanel.add(signUpButton);

            gbc.gridy = 4; gbc.gridx = 0; gbc.gridwidth = 2;
            gbc.insets = new Insets(20, 10, 0, 10);
            panel.add(buttonsPanel, gbc);

            // Dialog setup
            JDialog dialog = new JDialog();
            dialog.setTitle("PAC-MAN Login");
            dialog.setModal(true);
            dialog.getContentPane().add(panel);
            dialog.pack();
            dialog.setLocationRelativeTo(parent);
            dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);

            // Login button action
            loginButton.addActionListener(e -> {
                String username = usernameField.getText().trim();
                String password = new String(passwordField.getPassword());

                if (username.isEmpty() || password.isEmpty()) {
                    showError(dialog, "Please enter both username and password!");
                    return;
                }
                if (loginUser(username, password)) {
                    dialog.dispose();
                } else {
                    showError(dialog, "Invalid username or password!");
                }
            });

            // Sign Up button action
            signUpButton.addActionListener(e -> {
                String username = usernameField.getText().trim();
                String password = new String(passwordField.getPassword());

                if (username.isEmpty() || password.isEmpty()) {
                    showError(dialog, "Please enter both username and password!");
                    return;
                }
                if (signUpUser(username, password)) {
                    JOptionPane.showMessageDialog(dialog,
                            "Sign Up successful! You can now log in.",
                            "Success", JOptionPane.INFORMATION_MESSAGE);
                }
            });

            // Enter key triggers login
            passwordField.addActionListener(e -> loginButton.doClick());
            usernameField.addActionListener(e -> passwordField.requestFocus());

            dialog.setVisible(true);
            return currentUser != null;
        }

        // Style for username and password fields
        private void styleTextField(JTextField field) {
            field.setFont(new Font("Arial", Font.PLAIN, 16));
            field.setBackground(Color.DARK_GRAY);
            field.setForeground(Color.WHITE);
            field.setCaretColor(Color.YELLOW);
            field.setBorder(BorderFactory.createCompoundBorder(
                    BorderFactory.createLineBorder(Color.YELLOW, 2),
                    BorderFactory.createEmptyBorder(8, 10, 8, 10)
            ));
        }

        private JButton createPacmanButton(String text) {
            JButton button = new JButton(text);
            button.setFont(new Font("Arial", Font.BOLD, 18));
            button.setBackground(Color.YELLOW);
            button.setForeground(Color.BLACK);
            button.setFocusPainted(false);
            button.setBorder(BorderFactory.createCompoundBorder(
                    BorderFactory.createLineBorder(Color.WHITE, 3),
                    BorderFactory.createEmptyBorder(8, 25, 8, 25)
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

        private void showError(Component parent, String message) {
            JOptionPane.showMessageDialog(parent,
                    message,
                    "PAC-MAN Error",
                    JOptionPane.ERROR_MESSAGE);
        }

        // Login user by verifying username & password in DB
        private boolean loginUser(String username, String password) {
            try {
                PreparedStatement checkStmt = conn.prepareStatement(
                        "SELECT id, highscore FROM users WHERE username = ? AND password = ?");
                checkStmt.setString(1, username);
                checkStmt.setString(2, password);

                ResultSet rs = checkStmt.executeQuery();
                if (rs.next()) {
                    currentUser = username;
                    currentHighScore = rs.getInt("highscore");
                    checkStmt.close();
                    return true;
                }
                checkStmt.close();
            } catch (SQLException e) {
                showError(null, "Database error: " + e.getMessage());
                e.printStackTrace();
            }
            return false;
        }

        // Sign up a new user, insert username & password into DB
       private boolean signUpUser(String username, String password) {
        try {
            // Try to insert directly - let the UNIQUE constraint handle duplicates
            PreparedStatement insertStmt = conn.prepareStatement(
                    "INSERT INTO users (username, password, highscore) VALUES (?, ?, 0)");
            insertStmt.setString(1, username);
            insertStmt.setString(2, password);

            try {
                insertStmt.executeUpdate();
                return true;
            } catch (SQLException e) {
                if (e.getMessage().contains("unique constraint") || e.getMessage().contains("username_unique")) {
                    showError(null, "Username already taken!");
                    return false;
                }
                // For other database errors
                showError(null, "Database error: " + e.getMessage());
                e.printStackTrace();
                return false;
            } finally {
                insertStmt.close();
            }
        } catch (SQLException e) {
            showError(null, "Database error: " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }

        /**
         * Show top 10 high scores in a dialog.
         */
        public void showHighScores(Component parent) {
            try {
                String query = "SELECT username, highscore FROM users ORDER BY highscore DESC LIMIT 10";
                PreparedStatement stmt = conn.prepareStatement(query);
                ResultSet rs = stmt.executeQuery();

                StringBuilder sb = new StringBuilder("<html><h2 style='color:yellow; text-align:center;'>Top 10 High Scores</h2><ol>");
                while (rs.next()) {
                    String username = rs.getString("username");
                    int score = rs.getInt("highscore");
                    sb.append("<li>").append(username).append(": ").append(score).append("</li>");
                }
                sb.append("</ol></html>");

                JLabel label = new JLabel(sb.toString());
                label.setFont(new Font("Arial", Font.BOLD, 16));
                label.setHorizontalAlignment(SwingConstants.CENTER);
                label.setOpaque(true);
                label.setBackground(Color.BLACK);
                label.setForeground(Color.YELLOW);
                label.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

                JOptionPane.showMessageDialog(parent, label, "PAC-MAN High Scores", JOptionPane.PLAIN_MESSAGE);

                rs.close();
                stmt.close();

            } catch (SQLException e) {
                JOptionPane.showMessageDialog(parent, "Failed to load high scores: " + e.getMessage(),
                        "Error", JOptionPane.ERROR_MESSAGE);
                e.printStackTrace();
            }
        }

        public void close() {
        try {
            if (conn != null && !conn.isClosed()) {
                conn.close();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
        public int getCurrentHighScore() {
    if (currentUser == null) return 0;
    return currentHighScore;
}
    public void saveScore(int score) {
        if (currentUser == null) {
            System.err.println("No user is currently logged in. Score not saved.");
            return;
        }

        try {
            // Get the user's ID
            PreparedStatement getUserId = conn.prepareStatement(
                    "SELECT id, highscore FROM users WHERE username = ?");
            getUserId.setString(1, currentUser);
            ResultSet rs = getUserId.executeQuery();

            if (rs.next()) {
                int userId = rs.getInt("id");
                int existingHighScore = rs.getInt("highscore");

                // Insert the score into the scores table
                PreparedStatement insertScore = conn.prepareStatement(
                        "INSERT INTO scores (user_id, score, game_date) VALUES (?, ?, NOW())");
                insertScore.setInt(1, userId);
                insertScore.setInt(2, score);
                insertScore.executeUpdate();
                insertScore.close();

                // Update user's high score if this is higher
                if (score > existingHighScore) {
                    PreparedStatement updateHighScore = conn.prepareStatement(
                            "UPDATE users SET highscore = ? WHERE id = ?");
                    updateHighScore.setInt(1, score);
                    updateHighScore.setInt(2, userId);
                    updateHighScore.executeUpdate();
                    updateHighScore.close();

                    // Also update the in-memory value
                    currentHighScore = score;
                }
            }

            rs.close();
            getUserId.close();

        } catch (SQLException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(null, "Failed to save score: " + e.getMessage(),
                    "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    }
