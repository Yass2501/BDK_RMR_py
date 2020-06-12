from multiprocessing import Pool
import time as time

def square(x):
    # calculate the square of the value of x
    return x*x

if __name__ == '__main__':

    # Define the dataset
    dataset = []
    N = 32*800000
    for i in range(1,N+1):
        dataset.append(i)

    # Output the dataset
    #print ('Dataset: ' + str(dataset))

    # Run this with a pool of 5 agents having a chunksize of 3 until finished
    agents = 4
    chunksize = int(N/agents)
    t0= time.time()
    with Pool(processes=agents) as pool:
        result = pool.map(square, dataset, chunksize)
    elapsed_time = time.time() - t0
    print("Time elapsed:", elapsed_time) # CPU seconds elapsed (floating point)
