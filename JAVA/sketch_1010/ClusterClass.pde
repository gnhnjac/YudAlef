
class Cluster {
 
 int h_cubes;
 int v_cubes;
 
 float cubeSize;
 
 PVector originalPos;
 
 color cubeColor;
 
 boolean decintegrated = false;
  
 Cube cube_cluster[][] = new Cube[3][3];;
  
 Cluster(int vc, int hc, float cs, color ccolor) {
   
   v_cubes = vc;
   h_cubes = hc;
   
   cubeSize = cs;
   
   cubeColor = ccolor;
   
   originalPos = new PVector(0, 600);
   
   for(int i = 0; i < v_cubes; i++) {
     
     for (int j = 0; j < h_cubes; j++) {
       cube_cluster[i][j] = new Cube(originalPos.x+i*cubeSize,originalPos.y+j*cubeSize,cubeSize, cubeColor);
     }
   }
   
 }
 
 void show() {
   
   for(int i = 0; i < v_cubes; i++) {
     
     for (int j = 0; j < h_cubes; j++) {
       cube_cluster[i][j].render();
     }
     
   }
   
 }
 
 void rePos(float x, float y) {
   
   for(int i = 0; i < v_cubes; i++) {
     
     for (int j = 0; j < h_cubes; j++) {
       cube_cluster[i][j].pos = new PVector(x + i*cubeSize, y+j*cubeSize);
     }
   }
   
 }
 
 boolean collision(float x, float y) {
   for(int i = 0; i < v_cubes; i++) {
     
     for (int j = 0; j < h_cubes; j++) {
       if (y >= cube_cluster[i][j].pos.y && y <= cube_cluster[i][j].pos.y+cube_cluster[i][j].w && x >= cube_cluster[i][j].pos.x && x <= cube_cluster[i][j].pos.x+cube_cluster[i][j].w) {
         return true;
       }
     }
     
   }
   return false;
 }
 
 boolean fit(float x, float y) {
   for(int i = 0; i < v_cubes; i++) {
     
     for (int j = 0; j < h_cubes; j++) {
       if (y <= cube_cluster[i][j].pos.y && y+cubeSize >= cube_cluster[i][j].pos.y && x <= cube_cluster[i][j].pos.x && x+cubeSize >= cube_cluster[i][j].pos.x) {
          cube_cluster[i][j].pos = new PVector(x, y);
          return true;
       }
     }
     
   }
   
   return false;
 }
 
 void decintegrate(ArrayList<Cube> cubes) {
   
   for(int i = 0; i < v_cubes; i++) {
     
     for (int j = 0; j < h_cubes; j++) {
       cubes.add(cube_cluster[i][j]);
     }
     
   }
   
   decintegrated = true;
   
 }
  
}
