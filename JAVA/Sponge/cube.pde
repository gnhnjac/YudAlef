class Cube {

  PVector pos;
  float size;

  Cube(float x, float y, float z, float s) {

    pos = new PVector(x, y, z);
    size = s;
  }

  void show() {

    pushMatrix();
    translate(pos.x, pos.y, pos.z);
    box(size);
    popMatrix();
  }

  ArrayList<Cube> divide() {

    ArrayList<Cube> next = new ArrayList<Cube>();

    for (int i = -1; i < 2; i++) {
      for (int j = -1; j < 2; j++) {
        for (int k = -1; k < 2; k++) {

          float newSize = size/3;

          if (abs(i)+ abs(j) +abs(k) > 1) {
            next.add(new Cube(pos.x+i*newSize, pos.y+j*newSize, pos.z+k*newSize, newSize));
          }
        }
      }
    }

    return next;
  }
}
