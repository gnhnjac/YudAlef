
int sign(float n) {
   
  if(n > 0) {
     
    return 1;
    
  } else {
     
    return -1;
    
  }
  
}

class Perceptron {

  float weights[];
  float lr = 0.1;
  
  Perceptron(int n) {
     
    weights = new float[n];
    
    for(int i = 0; i < weights.length; i++) {
       
      weights[i] = random(1);
      
    }
    
    
  }
  
  int guess(float[] inputs) {
    
    float sum = 0;
    for(int i = 0; i < weights.length; i++) {
       
      
      sum += weights[i] * inputs[i];
      
    }
    
    return sign(sum);
    
  }
  
  void train(float[] inputs, int target) {
    
      int error = target - guess(inputs);
      
      for(int i = 0; i < weights.length; i++) {
         
         weights[i] += error * inputs[i] * lr;
        
      }
    
    
  }
  
  float guessY(float x) {
    
      float w0 = weights[0];
      float w1 = weights[1];
      float w2 = weights[2];
      
      return - (w0/w1) * x - (w2/w1);
    
  }
  
  float guessM() {
     
    return -(weights[0]/weights[1]);
    
  }
  
  float guessB() {
    
   return -(weights[2]/weights[1]);
    
  }
  
  
}
