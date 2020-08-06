from Raw_data_processing import *
import numpy as np


def check_reset_COMET(TrainID, TrainName, RMR_Messages, ODO_or_GPS, print_successive):
        COMET_TRAIN_OP_TIME_prev = 0
        COMET_KM_ODO_prev   = np.inf
        COMET_KM_GPS_prev   = np.inf
        COMET_TRAIN_OP_TIME_prev = 0
        COMET_KM_prev = np.inf
        IsReset = False
        for m in RMR_Messages:
            if(m.OBU_ID == TrainID):
                index = findIndexof(m.OBU_DATA, ',', 17)
                gps_field      = m.decode_GPS()
                OBU_DATE       = gps_field[GPS_DATE]
                OBU_TIME       = gps_field[GPS_TIME]
                OBU_DATA       = m.OBU_DATA
                COMET_KM_ODO   = int(OBU_DATA[(index[7]+1):(index[8])])
                COMET_KM_GPS   = int(OBU_DATA[(index[6]+1):(index[7])])
                COMET_TRAIN_OP_TIME = int(OBU_DATA[(index[0]+1):(index[1])])
                if(print_successive):
                    print(COMET_TRAIN_OP_TIME)
                if(ODO_or_GPS == 'ODO'):
                    COMET_KM = COMET_KM_ODO
                if(ODO_or_GPS == 'GPS'):
                    COMET_KM = COMET_KM_GPS
                if(COMET_TRAIN_OP_TIME < COMET_TRAIN_OP_TIME_prev):
                    IsReset = True
                    break
                if(ODO_or_GPS == 'ODO'):
                    COMET_KM_prev = COMET_KM_ODO
                if(ODO_or_GPS == 'GPS'):
                    COMET_KM_prev = COMET_KM_GPS
                OBU_DATE_prev       = OBU_DATE
                OBU_TIME_prev       = OBU_TIME
                COMET_TRAIN_OP_TIME_prev = COMET_TRAIN_OP_TIME
                COMET_KM_ODO_prev = COMET_KM_ODO
                COMET_KM_GPS_prev = COMET_KM_GPS
        if(IsReset):
            hour = str(OBU_TIME)
            hour = hour[0]+hour[1]+':'+hour[2]+hour[3]+':'+hour[4]+hour[5]
            hour_prev = str(OBU_TIME_prev)
            hour_prev = hour_prev[0]+hour_prev[1]+':'+hour_prev[2]+hour_prev[3]+':'+hour_prev[4]+hour_prev[5]
            print('===============================================================================================================================')
            print('[20'+OBU_DATE_prev[4]+OBU_DATE_prev[5]+'-'+OBU_DATE_prev[2]+OBU_DATE_prev[3]+'-'+OBU_DATE_prev[0]+OBU_DATE_prev[1]+'  '+hour+']',end=' ')
            print('TRAIN_OP_TIME of train '+TrainName+': '+' with value ['+str(COMET_TRAIN_OP_TIME_prev)+']; ',end=' ')
            print('KM_GPS is : '+str(COMET_KM_GPS_prev)+'; ', end=' ')
            print('KM_ODO is : '+str(COMET_KM_ODO_prev))
            print('[20'+OBU_DATE[4]+OBU_DATE[5]+'-'+OBU_DATE[2]+OBU_DATE[3]+'-'+OBU_DATE[0]+OBU_DATE[1]+'  '+hour+']',end=' ')
            print('TRAIN_OP_TIME of train '+TrainName+': '+' with value ['+str(COMET_TRAIN_OP_TIME)+']; ',end=' ')
            print('KM_GPS is : '+str(COMET_KM_GPS)+'; ', end=' ')
            print('KM_ODO is : '+str(COMET_KM_ODO))
            print('===============================================================================================================================')
        else:
            print('No reset comet has been detected in this period')

#############################################################

def check_KM_ODO_or_KM_GPS(TrainID, TrainName, RMR_Messages, KM_TARGET, ODO_or_GPS, print_successive):
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
                if(print_successive):
                    print(COMET_KM)
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
