import java.math.BigDecimal;
import java.math.MathContext;

MathContext mc = new MathContext(16);

BigDecimal mapBigDecimal(BigDecimal OldValue, BigDecimal OldMin, BigDecimal OldMax, BigDecimal NewMin, BigDecimal NewMax) {
  BigDecimal OldRange = OldMax.subtract(OldMin,mc);
  BigDecimal NewRange = NewMax.subtract(NewMin,mc);
  BigDecimal NewValue = OldValue.subtract(OldMin,mc).multiply(NewRange,mc).divide(OldRange,mc).add(NewMin,mc);
  
  return NewValue;
}

int iterations = 100;

BigDecimal minZoom = new BigDecimal(-2.5);

BigDecimal maxZoom = new BigDecimal(2.5);

BigDecimal IminZoom = new BigDecimal(-2.5);

BigDecimal ImaxZoom = new BigDecimal(2.5);

float zoomRectWidth = 0;

float originalmouseX = mouseX;
float originalmouseY = mouseY;

BigDecimal decimalZero = new BigDecimal(0);

float brightness[][];

void setup() {

  size(500, 500);
  colorMode(HSB);

  brightness = new float[width][height];

  for (int x = 0; x < width; x++) {

    for (int y = 0; y < height; y++) {

      BigDecimal a = mapBigDecimal(BigDecimal.valueOf(x), decimalZero, BigDecimal.valueOf(width), minZoom, maxZoom);
      BigDecimal b = mapBigDecimal(BigDecimal.valueOf(y), decimalZero, BigDecimal.valueOf(height), IminZoom, ImaxZoom);

      BigDecimal originalA = a;
      BigDecimal originalB = b;

      int bounded = 0;

      while (bounded < iterations) {

        BigDecimal newR = a.multiply(a, mc).subtract(b.multiply(b, mc), mc);
        BigDecimal newB = a.multiply(BigDecimal.valueOf(2), mc).multiply(b, mc);

        a = newR.add(originalA, mc);
        b = newB.add(originalB, mc);
        if (a.add(b, mc).abs().compareTo(BigDecimal.valueOf(16)) == 1) {
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
  
  BigDecimal minZoomNew = mapBigDecimal(BigDecimal.valueOf(originalmouseX), decimalZero, BigDecimal.valueOf(width), minZoom, maxZoom);
  BigDecimal maxZoomNew = mapBigDecimal(BigDecimal.valueOf(mouseX), decimalZero, BigDecimal.valueOf(width), minZoom, maxZoom);

  minZoom = minZoomNew;
  maxZoom = maxZoomNew;

  BigDecimal IminZoomNew = mapBigDecimal(BigDecimal.valueOf(originalmouseY), decimalZero, BigDecimal.valueOf(height), IminZoom, ImaxZoom);
  BigDecimal ImaxZoomNew = mapBigDecimal(BigDecimal.valueOf(originalmouseY+zoomRectWidth), decimalZero, BigDecimal.valueOf(height), IminZoom, ImaxZoom);

  IminZoom = IminZoomNew;
  ImaxZoom = ImaxZoomNew;

  for (int x = 0; x < width; x++) {

    for (int y = 0; y < height; y++) {

      BigDecimal a = mapBigDecimal(BigDecimal.valueOf(x), decimalZero, BigDecimal.valueOf(width), minZoom, maxZoom);
      BigDecimal b = mapBigDecimal(BigDecimal.valueOf(y), decimalZero, BigDecimal.valueOf(height), IminZoom, ImaxZoom);

      BigDecimal originalA = a;
      BigDecimal originalB = b;

      int bounded = 0;

      while (bounded < iterations) {

        BigDecimal newR = a.multiply(a, mc).subtract(b.multiply(b, mc), mc);
        BigDecimal newB = a.multiply(BigDecimal.valueOf(2), mc).multiply(b, mc);

        a = newR.add(originalA, mc);
        b = newB.add(originalB, mc);
        if (a.add(b, mc).abs().compareTo(BigDecimal.valueOf(16)) == 1) {
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
