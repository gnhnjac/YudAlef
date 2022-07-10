
class Puck {
  
 PVector pos;
 PVector velocity;
  
 Puck(float x, float y, PVector vel) {
   
   pos = new PVector(x, y);
   velocity = vel;
   
 }
  
 void fire() {
   
   pos.add(velocity);
   
   fill(0);
   circle(pos.x, pos.y, 20);
   
 }
 
 boolean out() {
  
   if(pos.y <= 0 || pos.y >= height || pos.x <= 0 || pos.x >= width) {
    
     return true;
     
   }
   
   return false;
   
 }
 
 boolean hit(float x, float y) {
   
   return false;
   
 }

}
