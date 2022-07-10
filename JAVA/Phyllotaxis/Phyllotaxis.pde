
float n = 0;
float c = 5;

float aa = 137.3;

void setup() {
  size(500,500);
}

void draw() {
  
  translate(width/2,height/2);
  
  float a = n * radians(aa);
  
  float r = c * sqrt(n);
  
  float x = cos(a) * r;
  float y = sin(a) * r;
  
  ellipse(x,y,10,10);
  
  n++;
  
}
