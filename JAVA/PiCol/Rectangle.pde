class Cube {

  int x;
  int y;
  
  int w;

  int m;

  float v;


  Cube(int x, int w, float v) {

    this.x = x;

    this.y = height-w;

    this.w = w;

    this.v = v;
  }
  
  void Update() {
    this.x += this.v;
  }
  
  void Show() {
    
    fill(0,255,0);
    
    rect(this.x, this.y, this.w, this.w);
    
  }
  
}
