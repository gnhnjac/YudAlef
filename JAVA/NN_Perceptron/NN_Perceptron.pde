
Point points[];

Perceptron brain;

void setup() {
  
  size(500, 500);
  
  points = new Point[100];
  
  brain = new Perceptron(3);
  
  for(int i = 0; i < points.length; i++) {
     
    points[i] = new Point();
    
  }
  
}

void draw() {
  
  background(200);
  
  Point p1 = new Point(-1, f(-1));
  
  Point p2 = new Point(1, f(1));
  
  stroke(0);
  line(p1.pixelX(), p1.pixelY(), p2.pixelX(), p2.pixelY());
  
  Point p3 = new Point(-1, brain.guessY(-1));
  
  Point p4 = new Point(1, brain.guessY(1));
  
  stroke(255, 0, 0);
  line(p3.pixelX(), p3.pixelY(), p4.pixelX(), p4.pixelY());
  
  for(Point point : points) {
      
    point.show();
    
    float[] inputs = {point.x, point.y, point.bias};
    
    int guess = brain.guess(inputs);
    
    if(guess == point.label) {
       
      fill(0, 255, 0);
      
    } else {
       
      fill(255, 0, 0);
      
    }
    
    ellipse(point.pixelX(), point.pixelY(), 10, 10);
      
  }
  
  textSize(22);
  fill(255, 0, 0);
  text(brain.guessM() + "x + " + brain.guessB(), 0, 22); 
  
  
}

void mousePressed() {
   
  for(Point point : points) {
    
    float[] inputs = {point.x, point.y, point.bias};
    
    brain.train(inputs, point.label);
    
    
  }
  
  
}
