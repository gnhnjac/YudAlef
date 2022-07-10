PImage earth; 
PShape globe;

float a = 0;
 
void setup() { 
  size(600, 600, P3D); 
  background(0); 
  earth = loadImage("download.png");
  globe = createShape(SPHERE, 200); 
  globe.setTexture(earth);
  globe.setStroke(color(255, 255, 255, 0));
}
 
void draw() { 
  
  lights();
  
  translate(width/2, height/2); 
  rotateY(a);
  sphereDetail(mouseX / 4);
  shape(globe);
  
  a += 0.01;
}
