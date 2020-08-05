import multiprocessing
from Raw_data_processing import *
from date_time_handling import *
import time
import numpy as np

def check_KM_ODO_or_KM_GPS(TrainID, TrainName, RMR_Messages, KM_TARGET, ODO_or_GPS):
        COMET_KM_ODO_prev   = np.inf
        COMET_KM_GPS_prev   = np.inf
        COMET_KM_prev = np.inf
        IsFound = False
        for m in RMR_Messages:
            if(m.OBU_ID == TrainID):
                index = findIndexof(m.OBU_DATA, ',', 17)
                gps_field      = m.decode_GPS()
                OBU_DATE       = gps_field[GPS_DATE]
                OBU_TIME       = gps_field[GPS_TIME]
                OBU_DATA       = m.OBU_DATA
                COMET_KM_ODO   = int(OBU_DATA[(index[7]+1):(index[8])])
                COMET_KM_GPS   = int(OBU_DATA[(index[6]+1):(index[7])])
                if(ODO_or_GPS == 'ODO'):
                    COMET_KM = COMET_KM_ODO
                if(ODO_or_GPS == 'GPS'):
                    COMET_KM = COMET_KM_GPS
                if(COMET_KM >= KM_TARGET and COMET_KM_prev <= KM_TARGET):
                    IsFound = True
                    break
                if(ODO_or_GPS == 'ODO'):
                    COMET_KM_prev = COMET_KM_ODO
                if(ODO_or_GPS == 'GPS'):
                    COMET_KM_prev = COMET_KM_GPS
                OBU_DATE_prev       = OBU_DATE
                OBU_TIME_prev       = OBU_TIME
        if(IsFound):
            hour = str(OBU_TIME)
            hour = hour[0]+hour[1]+':'+hour[2]+hour[3]+':'+hour[4]+hour[5]
            hour_prev = str(OBU_TIME_prev)
            hour_prev = hour_prev[0]+hour_prev[1]+':'+hour_prev[2]+hour_prev[3]+':'+hour_prev[4]+hour_prev[5]
            print('===============================================================================')
            print('[20'+OBU_DATE_prev[4]+OBU_DATE_prev[5]+'-'+OBU_DATE_prev[2]+OBU_DATE_prev[3]+'-'+OBU_DATE_prev[0]+OBU_DATE_prev[1]+'  '+hour_prev+']',end=' ')
            print('KM_'+ODO_or_GPS+' of train '+TrainName+': '+' with value ['+str(COMET_KM_prev)+']')
            print('[20'+OBU_DATE[4]+OBU_DATE[5]+'-'+OBU_DATE[2]+OBU_DATE[3]+'-'+OBU_DATE[0]+OBU_DATE[1]+'  '+hour+']',end=' ')
            print('KM_'+ODO_or_GPS+' of train '+TrainName+': '+' with value ['+str(COMET_KM)+']')
            print('===============================================================================')
        else:
            print('The value of '+str(KM_TARGET)+' km has not been find in this period')


#----------------------------------------------------- Inputs ----------------------------------------------------
Directory = '../OBU_Proxy'
KM_TARGET = 1500
filter_obu_data_type = [14]
d0 = date(2020, 5, 1)
d1 = date(2020, 6, 2)
Nprocs   = 8
if(Nprocs > 1):
    para = 1
else:
    para = 0
periods = generate_periods(d0, d1, Nprocs)
ODO       = 1  # if ODO = 1 --> KM_ODO else --> KM_GPS
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

    
    TrainName = ['DSB IC3 5042','DSB IC3 5058','DSB IC3 5059']
    ODO_or_GPS = 'ODO'
    TrainID   = []
    f = open('id_train_mapping.txt','r+')
    id_name_map = f.readlines()
    f.close()
    for train_name in TrainName:
        TrainID.append(getIdFromName(train_name, id_name_map))

    for i in range(len(TrainName)):
        check_KM_ODO_or_KM_GPS(TrainID[i], TrainName[i], RMR_Messages_sorted, KM_TARGET, ODO_or_GPS)





