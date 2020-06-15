import os
import xlsxwriter
import Raw_data_processing as Rdp
import Statistics_processing as Sp
from functions import *
from Variables import *


#----------------------------------------------------- Inputs ----------------------------------------------------
Name      = 'DSB MQ 4117' # 
period    = ['010120','010620']
Directory = '../OBU_Proxy'
KM_TARGET = 4500
filtring_tag = 'comet_init'
ODO       = 1  # if ODO = 1 --> KM_ODO else --> KM_GPS 
FLAG_LOAD = 0
#----------------------------------------------------- Raw data loading ----------------------------------------------------
if(FLAG_LOAD == 0):
    print('Big load has been selected !'+'\r\n')
    Raw_data  = Rdp.extract_rawData(Directory, period)
    M_treated = Rdp.decode_filtered_rawData_0(Raw_data, 'RawData_filtered.txt', 'RawData_length.txt', filtring_tag)
else:
    M_treated = Rdp.decode_filtered_rawData_1('RawData_filtered.txt', 'RawData_length.txt')


f = open('id_train_mapping.txt','r+')
id_name_map = f.readlines()
f.close()

M_treated_sorted = sorted(M_treated, key = lambda x: (x.date_for_sort,x.time_for_sort))

ID = getIdFromName(Name, id_name_map)
i  = 0
KM_ODO_prev   = 10000000
KM_GPS_prev   = 10000000
KM_prev       = 10000000
obu_date_prev = ''
obu_time_prev = ''
IsFound = False
if(ODO == 1):
    KM_str = 'KM_ODO'
else:
    KM_str = 'KM_GPS'
for mess in M_treated_sorted:
    #print(mess.OBU_ID+'  '+ID)
    if(mess.OBU_ID == ID):
        index = findIndexof(mess.OBU_DATA, ',', 17)
        gps_field      = mess.decode_GPS()
        obu_date       = gps_field[GPS_DATE]
        obu_time       = gps_field[GPS_TIME]
        obu_data       = mess.OBU_DATA
        KM_ODO         = int(obu_data[(index[7]+1):(index[8])])
        KM_GPS         = int(obu_data[(index[6]+1):(index[7])])
        if(ODO == 1):
            KM = KM_ODO
        else:
            KM = KM_GPS
        print('KM_ODO :', KM_ODO,'\t','KM_GPS :', KM_GPS,'\t','OBU Date :',obu_date)
        if(KM >= KM_TARGET and KM_prev <= KM_TARGET):
            IsFound = True
            break
        KM_GPS_prev   = KM_GPS
        KM_ODO_prev   = KM_ODO
        if(ODO == 1):
            KM_prev = KM_ODO_prev
        else:
            KM_prev = KM_GPS_prev
        obu_date_prev = obu_date
        obu_time_prev = obu_time
if(IsFound):
    hour = str(obu_time)
    hour = hour[0]+hour[1]+':'+hour[2]+hour[3]+':'+hour[4]+hour[5]
    hour_prev = str(obu_time_prev)
    hour_prev = hour_prev[0]+hour_prev[1]+':'+hour_prev[2]+hour_prev[3]+':'+hour_prev[4]+hour_prev[5]
    print('[20'+obu_date_prev[4]+obu_date_prev[5]+'-'+obu_date_prev[2]+obu_date_prev[3]+'-'+obu_date_prev[0]+obu_date_prev[1]+'  '+hour_prev+']',end=' ')
    print(KM_str+' of train '+Name+': '+' with value ['+str(KM_prev)+']')
    print('[20'+obu_date[4]+obu_date[5]+'-'+obu_date[2]+obu_date[3]+'-'+obu_date[0]+obu_date[1]+'  '+hour+']',end=' ')
    print(KM_str+' of train '+Name+': '+' with value ['+str(KM)+']')
else:
    print('The value of '+str(KM_TARGET)+' km has not been find in this period')










