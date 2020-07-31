import os
import multiprocessing
import time

def do_something():
    print('Sleeping 1 second...')
    time.sleep(1)
    print('Done Sleeping...')

def print_something(Name, ret):
    print(Name)
    ret = Name+' '+'sisi'

parallel = 1
Nprocs   = 8   

if __name__ == '__main__':

    if(parallel):

        start = time.perf_counter()
        
        jobs = []

        for _ in range(Nprocs):
            #manager = multiprocessing.Manager()
            p = multiprocessing.Process(target=print_something, args=('bob',))
            p.start()
            jobs.append(p)
        for j in jobs:
            j.join()
            
        finish = time.perf_counter()
        
        print(finish - start, 'Ncpu = '+str(Nprocs))

    else:
        start = time.perf_counter()

        for _ in range(Nprocs):
            #do_something()
            print_something('bob')
        finish = time.perf_counter()
        
        print(finish - start, 'Ncpu = '+str(Nprocs))

