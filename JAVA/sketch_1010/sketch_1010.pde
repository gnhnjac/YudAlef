Cluster cluster_types[][] = new Cluster[3][3]; //<>//

int grids = 10;

int board[][] = new int[grids][grids];

int horizontalboard[][] = new int[grids][grids];

float gridSize;

ArrayList<Cluster> clusters = new ArrayList<Cluster>();

ArrayList<Cube> cubes = new ArrayList<Cube>();

int priorityClusterIndex = 0;

int score = 0;

boolean gameOver = false;

void reset() {

  Cluster cluster_types[][] = new Cluster[3][3];

  board = new int[grids][grids];

  horizontalboard = new int[grids][grids];

  clusters = new ArrayList<Cluster>();

  cubes = new ArrayList<Cube>();

  priorityClusterIndex = 0;

  score = 0;

  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {

      cluster_types[i][j] = new Cluster(i+1, j+1, gridSize, color(100*j, 100*i, 100*j));
    }
  }


  for (int i = 0; i < grids; i++) {
    for (int j = 0; j < grids; j++) {

      board[i][j] = 0; 
      horizontalboard[i][j] = 0;
    }
  }

  reCluster(clusters);
}

void reCluster(ArrayList<Cluster> arrlist) {

  for (int i = 0; i < 3; i++) {

    Cluster clusterModel = cluster_types[int(random(3))][int(random(3))];

    Cluster cluster = new Cluster(clusterModel.v_cubes, clusterModel.h_cubes, gridSize, clusterModel.cubeColor);
    cluster.rePos(width/3*i, 600);

    cluster.originalPos = new PVector(width/3*i, 600);

    arrlist.add(cluster);
  }
}

void match() {

  // Vertical

  for (int i = 0; i < grids; i++) {

    int finished = 0;

    for (int j = 0; j < grids-1; j++) {

      if (board[i][j] == board[i][j+1] && board[i][j] == 1) {

        finished++;
      }
    }

    if (finished == grids-1) {

      for (int j = 0; j < grids; j++) {

        for (Cube cube : cubes) {

          if (cube.pos.x == i*gridSize && cube.pos.y == j*gridSize) {

            cube.matched = true;
          }
        }

        board[i][j] = 0;
        horizontalboard[j][i] = 0;
      }

      score+= 10;
    }
  }

  // Horizontal
  for (int i = 0; i < grids; i++) {

    int finished = 0;

    for (int j = 0; j < grids-1; j++) {

      if (horizontalboard[i][j] == horizontalboard[i][j+1] && horizontalboard[i][j] == 1) {

        finished++;
      }
    }

    if (finished == grids-1) {

      for (int j = 0; j < grids; j++) {

        for (Cube cube : cubes) {

          if (cube.pos.y == i*gridSize && cube.pos.x == j*gridSize) {

            cube.matched = true;
          }
        }

        board[j][i] = 0;
        horizontalboard[i][j] = 0;
      }

      score+= 10;
    }
  }
}

void gameOver() {

  int finished = 0;
  for (Cluster cluster : clusters) {
    for (int i = 0; i < grids-cluster.v_cubes+1; i++) {

      for (int j = 0; j < grids-cluster.h_cubes+1; j++) {

        int approved = 0;

        Cluster tester = new Cluster(cluster.v_cubes, cluster.h_cubes, gridSize, cluster.cubeColor);
        tester.rePos(i*gridSize, j*gridSize);

        for (int k = 0; k < 3; k++) {

          for (int m = 0; m < 3; m++) {
            if (tester.fit(i*gridSize+k*gridSize, j*gridSize+m*gridSize) && board[i+k][j+m] == 0) {

              approved++;
            }
          }
        }

        if (approved == cluster.v_cubes * cluster.h_cubes) {
          finished++;
        }
      }
    }
  }

  if (finished == 0) {

    gameOver = true;
  }
}

void setup() {
  size(500, 800); 

  frameRate(10000); 
  
  colorMode(HSB);

  gridSize = width/grids; 

  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {

      cluster_types[i][j] = new Cluster(i+1, j+1, gridSize, color(map(i*j, 0, 9, 0, 255), 255, 255));
    }
  }


  for (int i = 0; i < grids; i++) {
    for (int j = 0; j < grids; j++) {

      board[i][j] = 0; 
      horizontalboard[i][j] = 0;
    }
  }

  reCluster(clusters);
}


void draw() {
  
  if (!gameOver) {
    background(255);
    for (int i = 0; i < grids; i++) {

      for (int j = 0; j < grids; j++) {
        noFill(); 
        rect(i*gridSize, j*gridSize, gridSize, gridSize);
      }
    }

    for (Cluster cluster : clusters) {

      cluster.show(); 


      if (cluster.collision(mouseX, mouseY) && mousePressed) {
        cluster.rePos(mouseX-cluster.v_cubes*cluster.cubeSize/2, mouseY-cluster.h_cubes*cluster.cubeSize/2); 
        priorityClusterIndex = clusters.indexOf(cluster);
      }

      int finished = 0; 
      if (!(mousePressed)) {
        for (int i = 0; i < grids; i++) {

          for (int j = 0; j < grids; j++) {

            if (cluster.fit(i*gridSize, j*gridSize) && board[i][j] == 0) {
              board[i][j] = 2; 
              horizontalboard[j][i] = 2; 
              finished++;
            }
          }
        }

        if (finished == cluster.v_cubes*cluster.h_cubes) {

          for (int i = 0; i < grids; i++) {

            for (int j = 0; j < grids; j++) {
              if ((board[i][j] == 2)) {
                board[i][j] = 1; 
                horizontalboard[j][i] = 1;
              }
            }
          }

          cluster.decintegrate(cubes);
        } else {

          for (int i = 0; i < grids; i++) {

            for (int j = 0; j < grids; j++) {
              if (board[i][j] == 2) {
                if (cluster.fit(i*gridSize, j*gridSize)) {
                  board[i][j] = 0; 
                  horizontalboard[j][i] = 0;
                }
              }
            }
          }

          cluster.rePos(cluster.originalPos.x, cluster.originalPos.y);
        }
      }
    }


    for (int i = 0; i < cubes.size(); i++) {

      if (cubes.get(i).matched) {
        cubes.remove(i);
      }
    }



    for (Cube cube : cubes) {

      cube.render();
    }

    for (Cluster cluster : clusters) {

      if (priorityClusterIndex == clusters.indexOf(cluster)) {

        cluster.show();
      }
    }

    match(); 

    for (int i = 0; i < clusters.size(); i++) {

      if (clusters.get(i).decintegrated) {
        score += clusters.get(i).v_cubes * clusters.get(i).h_cubes;
        clusters.remove(i);

        if (clusters.size() == 0) {

          reCluster(clusters);
        }

        gameOver();
      }
    }

    fill(0);
    textSize(50);
    text(score, width/2-25, height-5);
  } else {
    fill(255, 0, 0);
    textSize(50);
    text("Game Over", width/2-125, (height-300)/2);
    
    fill(0, 255, 0);
    
    float circleX = width/2;
    float circleY = height/2;
    float circleR = 50;
    
    circle(circleX, circleY, circleR);
    
    if (sqrt(pow(mouseX-circleX, 2) + pow(mouseY-circleY, 2)) < circleR && mousePressed) {
       reset();
       gameOver = false;
    }
    
  }
  
}
