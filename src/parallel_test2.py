import multiprocessing
from Raw_data_processing import *
import time

period0               = ['070320','140320']
period1               = ['140320','210320']
period2               = ['210320','280320']
period3               = ['280320','040420']
period4               = ['040420','110420']
period5               = ['110420','180420']
period6               = ['180420','250420']
period7               = ['250420','020520']
period                = [period0,period1,period2,period3,period4,period5,period6, period7]
#period = [period0, period1]
Directory             = '../OBU_Proxy'
filter_obu_data_type  = 'all'      # 'all' for all messages, [2,16,14,...] for the messages type you want
Nprocs   = len(period)
para = 1

if __name__ == '__main__':

    if(para == 1):
        start = time.perf_counter()
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        jobs = []
        for i in range(Nprocs):
            p = multiprocessing.Process(target=extract_and_decode_rawData_para, args=(Directory,period[i],filter_obu_data_type,i,return_dict))
            p.start()
            jobs.append(p)
        for proc in jobs:
            proc.join()
        finish = time.perf_counter()
        print(finish - start)

        start = time.perf_counter()
        list_RMR = return_dict.values()
        finish = time.perf_counter()
        print(finish - start)
        
        sum = 0
        for l in list_RMR:
            sum = sum + len(l)
        print('LENGTH MESSAGES : '+str(sum))
        
    else:
        start = time.perf_counter()
        RMR_Messages = extract_and_decode_rawData(Directory, [period0[0],period7[1]], filter_obu_data_type)
        finish = time.perf_counter()
        print(finish - start)
        print('LENGTH MESSAGES : '+str(len(RMR_Messages)))
