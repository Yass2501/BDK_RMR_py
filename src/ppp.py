import os
import xlsxwriter
import Raw_data_processing as Rdp
import Statistics_processing as Sp
from functions import *
from Variables import *


#----------------------------------------------------- Inputs ----------------------------------------------------
Name   = 'DSB IC3 5039' # 
period = ['010120','030120']
Directory = '../OBU_Proxy'
filtering_tag = 'evc_tru'
ODO    = 1  # if ODO = 1 --> KM_ODO else --> KM_GPS 
FLAG_LOAD = 0
#----------------------------------------------------- Raw data loading ----------------------------------------------------

Raw_data  = Rdp.extract_rawData(Directory, period)
M_treated = Rdp.decode_filtered_rawData_0(Raw_data, 'RawData_filtered.txt', 'RawData_length.txt', filtering_tag)

for m in M_treated:
    if(m.OBU_DATA_TYPE == '2'):
        data_hex_str = (m.OBU_DATA).encode().hex()
        data_hex = bytes(data_hex_str, "utf-8")
        TRU_NID_MESSAGE = data_hex[0:2]
        if(TRU_NID_MESSAGE == b'09'):
            L_MESSAGE = data_hex[2:6]
            DATE      = data_hex[6:10]
            TIME_PADDING = data_hex[10:16]
            DRU_NID_PACKET = data_hex[16:18]
            DRU_L_PACKET = data_hex[18:22]
            if(DRU_NID_PACKET == b'01'):
                DRU_NID_SOURCE = data_hex[22:24]
                #if(DRU_NID_SOURCE == b'01'):
                DRU_M_DIAG = data_hex[24:27]
                DRU_NID_CHANNEL = data_hex[27:28]
                print(int(DRU_M_DIAG,16))
                
            

    















