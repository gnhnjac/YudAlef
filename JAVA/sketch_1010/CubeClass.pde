
class Cube {
   
  PVector pos;
  float w;
  
  boolean matched = false;
  
  color Color;
  
  Cube(float x, float y, float w, color cs) {
    this.pos = new PVector(x, y);
    
    this.w = w;
    
    this.Color = cs;
  }
  
  void render() {
    
     fill(this.Color);
    
     rect(this.pos.x, this.pos.y, this.w, this.w);
    
  }
  
}
