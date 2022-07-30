import static java.lang.Math.*;

double mapDouble(double OldValue, double OldMin, double OldMax, double NewMin, double NewMax) {

  double OldRange = (OldMax - OldMin);
  double NewRange = (NewMax - NewMin);
  double NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin;

  return NewValue;
}

int iterations = 2000;

double minZoom = -2.5;

double maxZoom = 2.5;

double IminZoom = -2.5;

double ImaxZoom = 2.5;

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
      
      double a = mapDouble(x, 0, width, minZoom, maxZoom);
      double b = mapDouble(y, 0, height, IminZoom, ImaxZoom);

      double originalA = a;
      double originalB = b;

      int bounded = 0;

      while (bounded < iterations) {

        //double newR = a*a - b*b;
        //double newB = abs((float)(2 * a * b));
        //double newB = (float)(2 * a * b);
        
        // double newR = a*a*a - 2*a*b*b;
        // double newB = 3 * a*a * b - b*b*b;
        
         double newR = a*a*a*a + b*b*b*b - 6*a*a*b*b;
         double newB = 4 * a*a * b - 4 * a * b *b;

        a = newR + originalA;
        b = newB + originalB;
        if (Math.abs(a+b) > 16) {
          break;
        }

        bounded++;
      }
      
      // float bright = map(bounded, 0, iterations, 0, 255);
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

  for (int x = 0; x < width; x++) {

    for (int y = 0; y < height; y++) {

      set(x, y, int(brightness[x][y]));
    }
  }

  if (mousePressed) {
    zoomRectWidth = mouseX-originalmouseX;
    stroke(255);
    noFill();
    rect(originalmouseX, originalmouseY, zoomRectWidth, zoomRectWidth);
  }
}

void mousePressed() {
  originalmouseX = mouseX;
  originalmouseY = mouseY;
}



void mouseReleased() {

  double minZoomNew = mapDouble(originalmouseX, 0, width, minZoom, maxZoom);
  double maxZoomNew = mapDouble(mouseX, 0, width, minZoom, maxZoom);

  minZoom = minZoomNew;
  maxZoom = maxZoomNew;

  double IminZoomNew = mapDouble(originalmouseY, 0, height, IminZoom, ImaxZoom);
  double ImaxZoomNew = mapDouble(originalmouseY+zoomRectWidth, 0, height, IminZoom, ImaxZoom);

  IminZoom = IminZoomNew;
  ImaxZoom = ImaxZoomNew;

  for (int x = 0; x < width; x++) {

    for (int y = 0; y < height; y++) {
      
      double a = mapDouble(x, 0, width, minZoom, maxZoom);
      double b = mapDouble(y, 0, height, IminZoom, ImaxZoom);

      double originalA = a;
      double originalB = b;

      int bounded = 0;

      while (bounded < iterations) {

        //double newR = a*a - b*b;
        ////double newB = abs((float)(2 * a * b));
        //double newB = (float)(2 * a * b);
        // double newR = a*a*a - 2*a*b*b;
        // double newB = 3 * a*a * b - b*b*b;
        
         double newR = a*a*a*a + b*b*b*b - 6*a*a*b*b;
         double newB = 4 * a*a * b - 4 * a * b *b;

        a = newR + originalA;
        b = newB + originalB;
        if (Math.abs(a+b) > 16) {
          break;
        }

        bounded++;
      }
      
      // float bright = map(bounded, 0, iterations, 0, 255);
      float bright = map(bounded, 0, iterations, 0, 1);
      bright = map(sqrt(bright), 0, 1, 0, 255);

      if (bounded == iterations) {
        bright = 0;
      }

      brightness[x][y] = color(bright);
    }
  }
}
