
int iterations = 500;
float zoomRectWidth = 0;

float originalmouseX = mouseX;
float originalmouseY = mouseY;

float brightness[][];

void setup() {

  size(500, 500);
  colorMode(HSB);

  brightness = new float[width][height];

  for (int x = 0; x < width; x++) {

    for (int y = 0; y < height; y++) {

      float a = map(x, 0, width, -2.5, 2.5);
      float b = map(y, 0, height, -2.5, 2.5);

      float originalA = a;
      float originalB = b;

      int bounded = 0;

      while (bounded < iterations) {

        float newR = a*a - b*b;
        float newB = 2*a*b;

        a = newR + originalA;
        b = newB + originalB;
        if (abs(a+b) > 16) {
          break;
        }

        bounded++;
      }

      //float bright = map(bounded, 0, iterations, 0, 255);
      float bright = map(bounded, 0, iterations, 0, 1);
      bright = map(sqrt(bright), 0, 1, 0, 255);

      if (bounded == iterations) {
        bright = 0;
      }

      brightness[x][y] = color(bright);
    }
  }
}

void draw() {

  background(255);

  pixelDensity(1);
  loadPixels();
  for (int x = 0; x < width; x++) {

    for (int y = 0; y < height; y++) {

      set(x, y, int(brightness[x][y]));
    }
  }
  
  stroke(255);
  line(width/2,0,width/2,height);
  line(0,height/2,width,height/2);
  
  text("Im = " + map(mouseY,0,height,-2.5,2.5), mouseX, mouseY);
  text("Re = " + map(mouseX,0,width, -2.5, 2.5), mouseX, mouseY-20);
  
  for (int x = mouseX; x < mouseX+200; x++) {

    for (int y = mouseY; y < mouseY+200; y++) {

      float a = map(x, mouseX, mouseX+200, -2.5, 2.5);
      float b = map(y, mouseY, mouseY+200, -2.5, 2.5);

      float originalA = a;
      float originalB = b;

      int bounded = 0;

      while (bounded < iterations) {

        float newR = a*a - b*b;
        float newB = 2*a*b;

        a = newR + map(mouseX,0,width,-2.5,2.5);
        b = newB + map(mouseY,0,height,-2.5,2.5);
        if (abs(a+b) > 16) {
          break;
        }

        bounded++;
      }

      float bright = map(bounded, 0, iterations, 0, 1);
      bright = map(sqrt(bright), 0, 1, 0, 255);

      if (bounded == iterations) {
        bright = 0;
      }

      set(x,y,color(bright));
    }
  }
}
