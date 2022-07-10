
float f(float x) {
  
   return 0.3 * x + 0.2; 
  
}

class Point {
  
  float x;
  float y;
  float bias = 1;
  
  int label;
  
  Point(float x_, float y_) {
    
    x = x_;
    y = y_;

  }
  
  Point() {
    
    x = random(-1, 1);
    y = random(-1, 1);
    
    if(y > f(x)) {
       
       label = 1;
      
    } else {
       
      label = -1;
      
    }
  }
  
  float pixelX() {
     
    return map(x, -1, 1, 0, width);
    
  }
  
  float pixelY() {
     
    return map(y, -1, 1, height, 0);
    
  }
  
  void show() {
    
    noStroke();
    
    if(label == 1) {
      
       fill(255); 
      
    } else {
       
      fill(0);
      
    }
    
    ellipse(pixelX(), pixelY(), 20, 20);
    
  }
  
  
  
  
}
