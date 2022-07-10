PrintWriter output;
float xoff = 0;
float yoff = 0;
OpenSimplexNoise noise;

void setup() {
  size(80,25);
  noise = new OpenSimplexNoise();
  output = createWriter("positions.txt"); 
  background(0);
  noStroke();
}

void draw()
{
  
  for(int k = 0; k < 100; k++)
  {
    
    
    for (int i = 0; i < 80; i++)
    {
    yoff += 0.01;
    float xoff = 0;
     for (int j = 0; j < 25; j++)
     {
     
     float n = (float)noise.eval(xoff, yoff);
      
     int toFile = (int)map(n, -1, 1, 0, 9);
     
     set(i, j, color((int)map(toFile, 0, 9, 0, 255)));
     
     
     print(toFile);
      
     output.print(toFile); // Write the coordinate to the file
     
     xoff+=0.01;
     
     }
    
    }
    
  }
  
  exit();
  
}
