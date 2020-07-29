from functions import *
from Variables import *
import Raw_data_processing


def mobileDefectOcc_compute(period, ID, M_treated_occ):
    occ = 0
    i = 1
    for mess in M_treated_occ:
        gps_field = mess.decode_GPS()
        obu_date  = dateStringToIntConvert(gps_field[GPS_DATE])
        obu_data  = mess.OBU_DATA
        obu_id    = mess.OBU_ID
        obu_time  = gps_field[GPS_TIME]
        obu_time  = int(obu_time[0:6])
        if((dateStringToIntConvert(period[0]) <= obu_date < dateStringToIntConvert(period[1])) and (obu_id == ID) and (mess.double_check == 0)):
            occ = occ + 1
    return occ

def mobileDefectTotalOcc_compute(period, ID, M_treated_occTotal):
    occ = 0
    i = 1
    for mess in M_treated_occTotal:
        gps_field = mess.decode_GPS()
        obu_date  = dateStringToIntConvert(gps_field[GPS_DATE])
        obu_data  = mess.OBU_DATA
        obu_id    = mess.OBU_ID
        obu_time  = gps_field[GPS_TIME]
        obu_time  = int(obu_time[0:6])
        if((dateStringToIntConvert(period[0]) <= obu_date < dateStringToIntConvert(period[1])) and (obu_id == ID) and (mess.double_check == 0)):
            occ = occ + 1
    return occ

        
def trainOpTime_compute(period, ID, RMR_Messages):
    tuples = []
    for mess in RMR_Messages:
        gps_field = mess.decode_GPS()
        obu_date  = dateStringToIntConvert(gps_field[GPS_DATE])
        obu_data  = mess.OBU_DATA
        obu_id    = mess.OBU_ID
        obu_time  = gps_field[GPS_TIME]
        obu_time  = int(obu_time[0:6])
        if((dateStringToIntConvert(period[0]) <= obu_date < dateStringToIntConvert(period[1])) and (obu_id == ID)):
            index = findIndexof(mess.OBU_DATA, ',', 17)
            TRAIN_OP_TIME = int(obu_data[(index[0]+1):(index[1])])
            tuples.append((TRAIN_OP_TIME,obu_date,obu_time))
    tuples_sorted = sorted(tuples, key = lambda x: (x[1],x[2]))
    i = 0
    TOT = []
    for t in tuples_sorted:
        print(t[0],t[1],t[2])
        TOT.append(t[0])
        i = i + 1
    offset = 0
    for i in range(0,len(TOT)-1):
        #print(TOT[i])
        if((TOT[i+1] < TOT[i]) and ((TOT[i]-TOT[i+1]) > 10)):
            #print('cc')
            offset = TOT[i]
            index = i
            print('Reset comet or anomaly (TOT): '+str(tuples_sorted[index]))
            break
    if(offset > 0):
        for i in range(index+1,len(TOT)):
            TOT[i] = TOT[i] + offset
            #print(TOT[i])
    '''for i in TOT:
        print(i)'''
    if(len(TOT) == 0):
        return 0
    else:
        return (max(TOT)-min(TOT))



def kmODO_compute(period, ID, RMR_Messages):
    tuples = []
    for mess in RMR_Messages:
        gps_field = mess.decode_GPS()
        obu_date  = dateStringToIntConvert(gps_field[GPS_DATE])
        obu_data  = mess.OBU_DATA
        obu_id    = mess.OBU_ID
        obu_time  = gps_field[GPS_TIME]
        obu_time  = int(obu_time[0:6])
        if((dateStringToIntConvert(period[0]) <= obu_date < dateStringToIntConvert(period[1])) and (obu_id == ID)):
            index = findIndexof(mess.OBU_DATA, ',', 17)
            km_odo = int(obu_data[(index[7]+1):(index[8])])
            km_gps = int(obu_data[(index[6]+1):(index[7])])
            tuples.append((km_odo,km_gps,obu_date,obu_time))
    tuples_sorted = sorted(tuples, key = lambda x: (x[2],x[3]))
    i = 0
    KM_ODO = []
    for t in tuples_sorted:
        print(i,t[0],t[1],t[2])
        KM_ODO.append(t[0])
        i = i + 1
    offset = 0
    for i in range(0,len(KM_ODO)-1):
        #print(KM_ODO[i])
        if((KM_ODO[i+1] < KM_ODO[i])):
            #print('cc')
            offset = KM_ODO[i]
            index = i
            print('======= '+str(index))
            print('Reset comet or anomaly (ODO): '+str(tuples_sorted[index]))
            break
    if(offset > 0):
        for i in range(index+1,len(KM_ODO)):
            KM_ODO[i] = KM_ODO[i] + offset
            #print(KM_ODO[i])
    '''for i in TOT:
        print(i)'''
    if(len(KM_ODO) == 0):
        return 0
    else:
        return (KM_ODO[len(KM_ODO)-1]-KM_ODO[0])




def kmODO_trainOpTime_compute(period, ID, M_treated_tot):
    tuples_odo = []
    tuples_tot = []
    km_final = 0
    tot_final = 0
    comet_init_odo = []
    comet_init_tot = []
    COMET_FLAG_ODO = 0
    COMET_FLAG_TOT = 0
    for mess in M_treated_tot:
        gps_field = mess.decode_GPS()
        obu_date  = dateStringToIntConvert(gps_field[GPS_DATE])
        obu_data  = mess.OBU_DATA
        obu_id    = mess.OBU_ID
        obu_time  = gps_field[GPS_TIME]
        obu_time  = int(obu_time[0:6])
        if((dateStringToIntConvert(period[0]) <= obu_date < dateStringToIntConvert(period[1])) and (obu_id == ID)):
            index = findIndexof(mess.OBU_DATA, ',', 17)
            tot = int(obu_data[(index[0]+1):(index[1])])
            km_odo = int(obu_data[(index[7]+1):(index[8])])
            tuples_tot.append((tot,obu_date,obu_time))
            tuples_odo.append((km_odo,obu_date,obu_time))
    tuples_odo_sorted = sorted(tuples_odo, key = lambda x: (x[1],x[2]))
    tuples_tot_sorted = sorted(tuples_tot, key = lambda x: (x[1],x[2]))
    i = 0
    TOT = []
    KM_ODO = []
    Date_odo = []
    Date_tot = []
    for k in range(0,len(tuples_odo_sorted)):
        t_odo = tuples_odo_sorted[k]
        t_tot = tuples_tot_sorted[k]
        KM_ODO.append(t_odo[0])
        TOT.append(t_tot[0])
        Date_odo.append(t_odo[1])
        Date_tot.append(t_tot[1])
    offset_odo = 0
    offset_tot = 0
    for i in range(0,len(KM_ODO)-1):
        #print(KM_ODO[i])
        if((KM_ODO[i+1] < KM_ODO[i]) and (((KM_ODO[i]-KM_ODO[i+1])/KM_ODO[i]) > 0.1)):
            COMET_FLAG_ODO = 1
            offset_odo = KM_ODO[i]
            index_odo = i
            comet_init_odo = [Date_odo[i],KM_ODO[i],Date_odo[i+1],KM_ODO[i+1]]
            print('Reset comet or anomaly (ODO)')
            break
    for i in range(0,len(TOT)-1):
        #print(KM_ODO[i])
        if((TOT[i+1] < TOT[i]) and (((TOT[i]-TOT[i+1])/TOT[i]) > 0.1)):
            COMET_FLAG_TOT = 1
            offset_tot = TOT[i]
            index_tot = i
            comet_init_tot = [Date_tot[i],TOT[i],Date_tot[i+1],TOT[i+1]]
            print('Reset comet or anomaly (TOT)')
            break
    if(offset_odo > 0):
        for i in range(index_odo+1,len(KM_ODO)):
            KM_ODO[i] = KM_ODO[i] + offset_odo
            #print(KM_ODO[i])
    if(offset_tot > 0):
        for i in range(index_tot+1,len(TOT)):
            TOT[i] = TOT[i] + offset_tot
            #print(TOT[i])
    if(len(KM_ODO) == 0):
        km_final = 0
    else:
        km_final = (KM_ODO[len(KM_ODO)-1]-KM_ODO[0])
    if(len(TOT) == 0):
        tot_final = 0
    else:
        tot_final = (TOT[len(KM_ODO)-1]-TOT[0])

    return [COMET_FLAG_ODO,COMET_FLAG_TOT,comet_init_odo,comet_init_tot,km_final,tot_final]
    
    

def double_check(RMR_Messages):
    for i in range(0,len(RMR_Messages)-1):
        gps_field_curr = RMR_Messages[i].decode_GPS()
        gps_field_next = RMR_Messages[i+1].decode_GPS()
        if((gps_field_curr[GPS_DATE] == gps_field_next[GPS_DATE]) and (gps_field_curr[GPS_TIME] == gps_field_next[GPS_TIME]) \
           and (RMR_Messages[i].OBU_ID == RMR_Messages[i+1].OBU_ID)):
            RMR_Messages[i+1].double_check = 1
