
class Player {

  PVector pos;
  PVector velocity = new PVector(0, 0);
  float rotation = 0;
  float rotationvelocity = 0;

  PVector front;

  boolean hitPositive = true;

  float strength = 1;

  boolean release = false;

  char left;
  char right;
  char up;
  char down;
  
  Player(float x, float y, char l, char r, char u, char d) {

    pos = new PVector(x, y);

    front = new PVector(0, 0);

    left = l;
    right = r;
    up = u;
    down = d;
  }

  void show() {

    if (velocity.x > 0) {

      velocity.add(-0.1, 0);
    }

    if (velocity.y > 0) {

      velocity.add(0, -0.1);
    }

    if (velocity.x < 0) {

      velocity.add(0.1, 0);
    }

    if (velocity.y < 0) {

      velocity.add(0, 0.1);
    }

    if (rotationvelocity > 0) {

      rotationvelocity-=PI/1800;
    }

    if (rotationvelocity < 0) {


      rotationvelocity+=PI/1800;
    }

    if (rotationvelocity < 0.01 && rotationvelocity > 0) {

      rotationvelocity = 0;
    }

    if (velocity.x < 0.1 && velocity.x > 0) {

      velocity.x = 0;
    }

    if (velocity.y < 0.1 && velocity.y > 0) {

      velocity.y = 0;
    }

    if (abs(rotation) >= PI*2) {

      rotation = 0;
    }

    rotation+=rotationvelocity;
    pos.add(velocity);

    pushMatrix();
    
    fill(0, 255, 255);
    
    translate(pos.x, pos.y);

    rotate(rotation);

    rect(-25, -25, 50, 50);

    popMatrix();

    pushMatrix();

    translate(pos.x, pos.y);

    PVector v = new PVector(0, -100);

    v.rotate(rotation);

    front = v;

    rect(v.x, v.y, 1, 1);

    popMatrix();
  }

  void move() {

    if (keyPressed) {

      if (key == left) {
        rotationvelocity -= PI/120;
      }
      if (key == right) {
        rotationvelocity += PI/120;
      } 
      if (key == down) {


        velocity.add(-0.005*front.x, -0.005*front.y);
      } 
      if (key == up) {

        velocity.add(0.005*front.x, 0.005*front.y);
      }
    }

    rotationvelocity = constrain(rotationvelocity, -PI/20, PI/20);
  }

  void bounce() {

    if (pos.x >= width) {

      velocity.add(-3, 0);
    }

    if (pos.x <= 0) {

      velocity.add(3, 0);
    }

    if (pos.y >= height) {

      velocity.add(0, -3);
    }

    if (pos.y <= 0) {

      velocity.add(0, 3);
    }
  }

  void hockey() {



    pushMatrix();

    fill(4*strength, 255, 255);

    translate(pos.x, pos.y);

    rotate(rotation);

    rect(50, -75/2, 15, 75/15*strength);

    popMatrix();

    if (hitPositive) {
      strength++;

      if (strength > 15) {

        strength = 15;
        hitPositive = false;
      }
    } else {

      strength--;

      if (strength < 1) {

        strength = 1;
        hitPositive = true;
      }
    }

    if (release) {
      pucks.add(new Puck(pos.x, pos.y, new PVector(front.x*0.01*strength, front.y*0.01*strength)));
      release = false;
      strength = 1;
    }
  }
}
