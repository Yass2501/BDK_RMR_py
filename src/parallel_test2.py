import multiprocessing
from Raw_data_processing import *
from date_time_handling import *
import time

Directory             = '../OBU_Proxy'
filter_obu_data_type  = [2,14]      # 'all' for all messages, [2,16,14,...] for the messages type you want
d0 = date(2018, 12, 10)
d1 = date(2020, 6, 1)
Nprocs   = 8
para = 1
periods = generate_periods(d0, d1, Nprocs)
print(periods)

if __name__ == '__main__':

    if(para == 1):
        start = time.perf_counter()
        p = multiprocessing.Pool(processes=Nprocs)
        RMR_Messages = p.starmap(extract_and_decode_rawData_para, [(Directory, periods[i], filter_obu_data_type) for i in range(Nprocs)])
        p.close()
        p.join()
        finish = time.perf_counter()
        print(finish - start)
        size = 0
        for i in range(Nprocs):
            size = size + len(RMR_Messages[i])
            
        print('LENGTH MESSAGES : ', size)
    else:
        start = time.perf_counter()
        RMR_Messages = extract_and_decode_rawData_para(Directory, periods[0], filter_obu_data_type)
        finish = time.perf_counter()
        print(finish - start)
        size = len(RMR_Messages)
        print('LENGTH MESSAGES : ', size)
