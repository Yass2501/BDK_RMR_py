import os
import xlsxwriter
import Raw_data_processing as Rdp
import Statistics_processing as Sp
import numpy as np
from functions import *
from Variables import *
from bit_bytes_manipulation import *


#----------------------------------------------------- Inputs ----------------------------------------------------
Name   = 'DSB MQ 4112' # 
period = ['120219','130219']
Directory = '../OBU_Proxy'
rmr_filtering_tag = 'evc_tru'
ODO    = 1  # if ODO = 1 --> KM_ODO else --> KM_GPS 
FLAG_LOAD = 0
#----------------------------------------------------- Raw data loading ----------------------------------------------------


Raw_data  = Rdp.extract_rawData(Directory, period)
M_treated = Rdp.decode_filtered_rawData_0(Raw_data, 'RawData_filtered.txt', 'RawData_length.txt', rmr_filtering_tag)


def evc_dru_search(M_treated_in, type_of_search, data):
    M_treated_out = []
    LLRU_ID1   = 101 # Mobile 1
    LLRU_ID2   = 102 # Mobile 2
    LLRU_STATE = 2   # Defect
    DRU_NID_SOURCE = '00'
    DRU_NID_PACKET = '00'
    for m in M_treated_in:
        if(m.OBU_DATA_TYPE == '2'):           
            data_hex = (m.OBU_DATA).encode().hex()
            TRU_NID_MESSAGE = data_hex[0:2]
            if(TRU_NID_MESSAGE == '09'):               # DRU Messages
                L_MESSAGE        = data_hex[2:6]
                DATE             = data_hex[6:10]
                TIME_PADDING     = data_hex[10:16]
                DRU_NID_PACKET   = data_hex[16:18]
                DRU_L_PACKET     = data_hex[18:22]
                VARIABLES_PACKET = data_hex[22:]
                if(DRU_NID_PACKET == '01'):
                    DRU_NID_SOURCE  = data_hex[22:24]
                    DRU_M_DIAG      = data_hex[24:27]
                    DRU_M_DIAG_INT  = int(DRU_M_DIAG,16)
                    #print(DRU_M_DIAG_INT)
                    #if((DRU_M_DIAG_INT % 160 == LLRU_ID1) and (int(DRU_M_DIAG_INT / 160) == LLRU_STATE)):
                        #print(DRU_M_DIAG_INT)
                    DRU_NID_CHANNEL = data_hex[27:28]
                    DRU_L_TEXT      = data_hex[28:30]
                    DRU_X_TEXT      = data_hex[30:]
                    '''
                    dru_bytes = bytes.fromhex(DRU_X_TEXT)
                    dru_ascii = dru_bytes.decode("ascii")
                    print(dru_ascii)
                    print('============================================================================================')'''
                elif(DRU_NID_PACKET == '05'):
                    DRU_NID_SOURCE    = data_hex[22:24]
                    DRU_N_ITER        = data_hex[24:26]
                    # Allocation
                    DRU_NID_DATA      = ['0' for i in range(int(DRU_N_ITER,16))]
                    DRU_L_PACKET      = ['0' for i in range(int(DRU_N_ITER,16))]
                    DRU_Q_TEXTCLASS   = ['0' for i in range(int(DRU_N_ITER,16))]
                    DRU_Q_TEXTCONFIRM = ['0' for i in range(int(DRU_N_ITER,16))]
                    DRU_Q_TEXT        = ['0' for i in range(int(DRU_N_ITER,16))]
                    DRU_L_TEXT        = ['0' for i in range(int(DRU_N_ITER,16))]
                    DRU_X_TEXT        = ['0' for i in range(int(DRU_N_ITER,16))]
                    L_reste = int(len(data_hex[26:]) / int(DRU_N_ITER,16))
                    for i in range(0,int(DRU_N_ITER,16)):  # Loop on N_ITER
                        index = 26 + L_reste*i
                        DRU_NID_DATA[i]      = data_hex[index:index+2]
                        DRU_L_PACKET[i]      = data_hex[index+2:index+4]
                        DRU_Q_TEXTCLASS[i]   = data_hex[index+4:index+6]
                        DRU_Q_TEXTCONFIRM[i] = data_hex[index+6:index+8]
                        DRU_Q_TEXT[i]        = data_hex[index+8:index+10]
                        DRU_L_TEXT[i]        = data_hex[index+10:index+12]
                        DRU_X_TEXT[i]        = data_hex[index+12:((index+12)+int(DRU_L_TEXT[i],16)*2)]
                        dru_bytes = bytes.fromhex(DRU_X_TEXT[i])
                        dru_ascii = dru_bytes.decode("ascii")
                        print(dru_ascii, end=' ')
                    print('\n============================================================================================')
                    #print(DRU_N_ITER,DRU_L_TEXT,DRU_Q_TEXT,DRU_X_TEXT)
            if(type_of_search == 'DRU_EVC'):
                if((DRU_NID_PACKET == '01') and (DRU_NID_SOURCE == '01')):
                    M_treated_out.append(m)
                    date = ''
                    time = ''
                    for i in range(0,len(DATE)):
                        #print(DATE[i],len(DATE))
                        date = date + hexToBin(DATE[i])
                    for i in range(0,len(TIME_PADDING)):
                        time = time + hexToBin(TIME_PADDING[i])
                    year   = int(bytes(date[0:7],'utf-8'),2)
                    mounth = int(bytes(date[7:11],'utf-8'),2)
                    day    = int(bytes(date[11:],'utf-8'),2)
                    hour    = int(bytes(time[0:5],'utf-8'),2)
                    minutes = int(bytes(time[5:11],'utf-8'),2)
                    seconds = int(bytes(time[11:17],'utf-8'),2)
                    TTS     = int(bytes(time[17:22],'utf-8'),2)
                    Seconds = (float(seconds) + float(TTS/100)) % 60
                    Minutes = (minutes + int((float(seconds) + float(TTS/100))/60)) % 60
                    Hour    = hour + int(minutes/60)
                    gps_field = m.decode_GPS()
                    UTC_DATE = gps_field[GPS_DATE]
                    UTC_TIME = gps_field[GPS_TIME]
                    EVC_DATE = [day,mounth,year]
                    EVC_TIME = [Hour,Minutes,Seconds]
                    print('UTC date : '+UTC_DATE,'\t','UTC time : '+UTC_TIME)
                    print('EVC date : ',EVC_DATE,'\t','UTC time : ',EVC_TIME)
                    print('=============================================================')
            elif(type_of_search == 'DRU_EVC_CORE'):
                if((DRU_NID_PACKET == '01') and (DRU_NID_SOURCE == '02')):
                    print(int(DRU_M_DIAG,16))
            elif(type_of_search == 'DRU_EVC_TIU'):
                if((DRU_NID_PACKET == '01') and (DRU_NID_SOURCE == '03')):
                    print(int(DRU_M_DIAG,16))
            elif(type_of_search == 'DRU_DMI'):
                if((DRU_NID_PACKET == '01') and (DRU_NID_SOURCE == '04')):
                    print(int(DRU_M_DIAG,16))
            elif(type_of_search == 'DRU_EIRENE'):
                if((DRU_NID_PACKET == '01') and (DRU_NID_SOURCE == '05')):
                    print(int(DRU_M_DIAG,16))
            elif(type_of_search == 'DRU_TRU'):
                if((DRU_NID_PACKET == '01') and (DRU_NID_SOURCE == '06')):
                    print(DRU_X_TEXT, int(DRU_L_TEXT,16))
            elif(type_of_search == 'EVC_TEXT_MESSAGES'):
                if((DRU_NID_PACKET == '05') and (DRU_NID_SOURCE == '01')):
                    #print(int(DRU_N_ITER,16), DRU_Q_TEXT, DRU_X_TEXT)
                    continue

    return M_treated_out
                        
# MM
obu_data_type   = '2'
tru_nid_message = b'09'
dru_nid_packet  = b'01'
dru_nid_source  = b'07'


LLRU_ID1   = 101 # Mobile 1
LLRU_ID2   = 102 # Mobile 2
LLRU_STATE = 0   # Defect

data = 0
type_of_search = 'EVC_TEXT_MESSAGES'

M_treated_out = evc_dru_search(M_treated, type_of_search, data)


                
            

    















