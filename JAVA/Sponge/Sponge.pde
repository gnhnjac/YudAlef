
float a = 0.01;

ArrayList<Cube> sponge;

void setup() {
  
  size(500,500,P3D);
  
  sponge = new ArrayList<Cube>();
  
  sponge.add(new Cube(0,0,0,200));
  
  
}

void mousePressed() {
   
  ArrayList<Cube> next = new ArrayList<Cube>();
  
  for(Cube cube : sponge) {
   
    next.addAll(cube.divide());
    
  }
  
  sponge = next;
  
}

void draw() {
  
  background(0);
  lights();
  translate(width/2,height/2);
  rotateX(a);
  rotateY(a);
  rotateZ(a);
  for(Cube cube : sponge) {
   
    cube.show();
    
  }
  
  a+=0.01;
  
}
