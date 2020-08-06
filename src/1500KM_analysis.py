import multiprocessing
from Raw_data_processing import *
from date_time_handling import *
from comet_init_functions import *
import time
import numpy as np


#----------------------------------------------------- Inputs ----------------------------------------------------
Directory = '../OBU_Proxy'
KM_TARGET = 4500
filter_obu_data_type = [14]
d0 = date(2020, 6, 10)
d1 = date(2020, 7, 8)
Nprocs   = 8
TrainName = ['DSB IC3 5058']
ODO_or_GPS = 'ODO'
print_successive = 1
#-----------------------------------------------------------------------------------------------------------------
if(Nprocs > 1):
    para = 1
else:
    para = 0
periods = generate_periods(d0, d1, Nprocs)
print(periods)
#----------------------------------------------------- Raw data loading ----------------------------------------------------

if __name__ == '__main__':
    
    if(para == 1):
        start = time.perf_counter()
        p = multiprocessing.Pool(processes=Nprocs)
        RMR_Messages = p.starmap(extract_and_decode_rawData_para, [(Directory, periods[i], filter_obu_data_type) for i in range(Nprocs)])
        p.close()
        p.join()
        RMR_Messages_reduce = []
        for i in range(0,Nprocs):
            for m in RMR_Messages[i]:
                RMR_Messages_reduce.append(m)
        RMR_Messages_sorted = sorted(RMR_Messages_reduce, key = lambda x: (x.date_for_sort,x.time_for_sort))
        del RMR_Messages_reduce
        del RMR_Messages
        finish = time.perf_counter()
        print('Time for loading RMR Messages : ', finish - start)
    else:
        start = time.perf_counter()
        RMR_Messages = extract_and_decode_rawData_para(Directory, periods[0], filter_obu_data_type)
        RMR_Messages_sorted = sorted(RMR_Messages, key = lambda x: (x.date_for_sort,x.time_for_sort))
        del RMR_Messages
        finish = time.perf_counter()
        print('Time for loading RMR Messages : ', finish - start)

    TrainID   = []
    f = open('id_train_mapping.txt','r+')
    id_name_map = f.readlines()
    f.close()
    for train_name in TrainName:
        TrainID.append(getIdFromName(train_name, id_name_map))

    for i in range(len(TrainName)):
        check_KM_ODO_or_KM_GPS(TrainID[i], TrainName[i], RMR_Messages_sorted, KM_TARGET, ODO_or_GPS, print_successive)





