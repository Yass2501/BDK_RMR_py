import multiprocessing as mp
import time 
   
  
def square(x): 
    return x * x 
   
if __name__ == '__main__':  
    pool = mp.Pool(mp.cpu_count())
    print(mp.cpu_count())
    inputs = [0,1,2,3,4] 
    outputs = pool.map(square, inputs) 
    print("Input: {}".format(inputs)) 
    print("Output: {}".format(outputs))
    
