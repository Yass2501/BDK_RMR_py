import os
import xlsxwriter
from Raw_data_processing import *
from Statistics_processing import *
import numpy as np
from functions import *
from Variables import *
from bit_bytes_manipulation import *
from evc_tru import *




#----------------------------------------------------- Inputs ----------------------------------------------------
Name                  = 'DSB MQ 4116' # 
period                = ['170320','240520']
Directory             = '../OBU_Proxy'
filter_obu_data_type  = 'all'      # 'all' for all messages, [2,16,14,...] for the messages type you want
LLRU_IDs              = [101,102]
LLRU_STATEs           = [2,1]       # 0->OK ---- 1->Warning ---- 2->Defect ---- 3->Blocking Defect
f = open('id_train_mapping.txt','r+')
id_name_map = f.readlines()
ID = getIdFromName(Name, id_name_map)
f.close()
#----------------------------------------------------- Raw data loading ----------------------------------------------------


RMR_Messages_comet_init = extract_and_decode_rawData(Directory, period, filter_obu_data_type)
'''
RMR_Messages_MM         = Maintenance_Manager_Management(RMR_Messages, LLRU_IDs, LLRU_STATEs)



RMR_Messages_comet_init_sorted = sorted(RMR_Messages_comet_init, key = lambda x: (x.date_for_sort,x.time_for_sort))
km_odo      = kmODO_compute(period, ID, RMR_Messages_comet_init_sorted)
trainOpTime = trainOpTime_compute(period, ID, RMR_Messages_comet_init_sorted)
print(km_odo, trainOpTime)
'''

'''
RMR_Messages_MM_mobile_1 = []
RMR_Messages_MM_mobile_2 = []

for m in RMR_Messages_MM:
    data_hex   = (m.OBU_DATA).encode().hex()
    DRU_M_DIAG = data_hex[24:27]
    DRU_M_DIAG_INT = int(DRU_M_DIAG,16)
    if((DRU_M_DIAG_INT % 160) == LLRU_IDs[0]):
        print(DRU_M_DIAG_INT)
        RMR_Messages_MM_mobile_1.append(m)'''
    
















