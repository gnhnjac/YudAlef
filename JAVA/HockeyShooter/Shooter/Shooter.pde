ArrayList<Puck> pucks = new ArrayList<Puck>();

Player player;

Player player2;

void setup() {

  size(1000, 1000);

  colorMode(HSB);

  player = new Player(0, 0, 'a', 'd', 'w', 's');
  player2 = new Player(width, height, 'j', 'l', 'i', 'k');
}

void draw() {

  background(255);

  for (int i = 0; i < pucks.size(); i++) {

    Puck puck = pucks.get(i);

    puck.fire();

    if (puck.out()) {

      pucks.remove(puck);
    }
  }


  
  player.move();
  player.show();
  player.bounce();

  player2.move();
  player2.show();
  player2.bounce();
  
  if (keyPressed) {

    if (key == ' ') {
      player.hockey();
    }

    if (keyCode == ENTER) {

      player2.hockey();
    }
  }
}

void keyReleased() {

  if (key == ' ') {

    player.release = true;
    player.hockey();
  }

  if (keyCode == ENTER) {

    player2.release = true;
    player2.hockey();
  }
}
