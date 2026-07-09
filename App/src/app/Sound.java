package app;

import javax.sound.sampled.*;
import java.net.URL;

public class Sound {
    private Clip beginSound, chompSound, deathSound, gameOverSound;
    private boolean soundsPaused = false;

    public Sound() {
        loadSounds();
        playGameStart();
    }

    private void loadSounds() {
        beginSound = loadClip("/app/pacman_beginning.wav");
        chompSound = loadClip("/app/pacman_chomp.wav"); // Used for both movement and eating
        deathSound = loadClip("/app/pacman_death.wav");
        gameOverSound = loadClip("/app/pacman_intermission.wav");
        
        if (chompSound != null) {
            chompSound.loop(Clip.LOOP_CONTINUOUSLY);
            chompSound.stop();
        }
    }

    private Clip loadClip(String filename) {
        try {
            URL soundURL = getClass().getResource(filename);
            if (soundURL == null) {
                System.err.println("Sound file not found: " + filename);
                return null;
            }
            AudioInputStream audioIn = AudioSystem.getAudioInputStream(soundURL);
            Clip clip = AudioSystem.getClip();
            clip.open(audioIn);
            return clip;
        } catch (Exception e) {
            System.err.println("Error loading sound: " + filename);
            return null;
        }
    }

    public void playGameStart() {
        playSound(beginSound);
    }

  public void playChomp() {
    if (!soundsPaused && chompSound != null) {
        try {
            // Rewind and play if not already playing
            if (!chompSound.isActive()) {
                chompSound.setFramePosition(0);
                chompSound.start();
            }
        } catch (Exception e) {
            System.err.println("Error playing chomp sound: " + e.getMessage());
        }
    }
}

    public void playDeath() {
        if (!soundsPaused) {
            if (chompSound != null) chompSound.stop();
            playSound(deathSound);
        }
    }

    public void playGameOver() {
        if (!soundsPaused) {
            pauseAllSounds();
            playSound(gameOverSound);
        }
    }

    private void playSound(Clip clip) {
        if (clip != null) {
            clip.setFramePosition(0);
            clip.start();
        }
    }

    public void toggleSounds(boolean pause) {
        soundsPaused = pause;
        if (pause) {
            pauseAllSounds();
        } else if (chompSound != null) {
            chompSound.start();
        }
    }

    private void pauseAllSounds() {
        if (beginSound != null && beginSound.isRunning()) beginSound.stop();
        if (chompSound != null && chompSound.isRunning()) chompSound.stop();
        if (deathSound != null && deathSound.isRunning()) deathSound.stop();
        if (gameOverSound != null && gameOverSound.isRunning()) gameOverSound.stop();
    }

    public void close() {
        pauseAllSounds();
        if (beginSound != null) beginSound.close();
        if (chompSound != null) chompSound.close();
        if (deathSound != null) deathSound.close();
        if (gameOverSound != null) gameOverSound.close();
    }
}