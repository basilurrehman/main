package app;

import java.awt.Image;

class Position {
    Image image;
    int x;
    int y;
    int width;
    int height;
    int startX;
    int startY;
    
    Position(Image image, int x, int y, int width, int height) {
        this.image = image;
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.startX = x;
        this.startY = y;
    }
}