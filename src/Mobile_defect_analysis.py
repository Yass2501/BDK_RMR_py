import os
from Variables import *
from functions import *
from Excel_mobile_defects import *
from evc_tru import *
import xlsxwriter
import Raw_data_processing as Rdp
import Statistics_processing as Sp
import time as time

#----------------------------------------------------- Inputs ----------------------------------------------------
# Choose the periods and the families of train studied

f = open('period.csv','r+')
p = f.readlines()
for ip in p:
    print(ip)
print(p)
print(len(p))
period = []
period_tmp1 = []
period_tmp2 = []
p_cut = []
index = 0
for i in range(0,len(p)):
    if(p[i] == '\n'):
        index = i
        break
    else:
        p_cut.append(p[i])
for i in range(0,len(p_cut)-1):
    period_tmp1 = p_cut[i][0]+p_cut[i][1]+p_cut[i][3]+p_cut[i][4]+p_cut[i][6]+p_cut[i][7]
    period_tmp2 = p_cut[i+1][0]+p_cut[i+1][1]+p_cut[i+1][3]+p_cut[i+1][4]+p_cut[i+1][6]+p_cut[i+1][7]
    period.append([period_tmp1,period_tmp2])
    print(i,period[i])
    index = i
p0 = p_cut[0][0]+p_cut[0][1]+p_cut[0][3]+p_cut[0][4]+p_cut[0][6]+p_cut[0][7]
p1 = p_cut[len(p_cut)-1][0]+p_cut[len(p_cut)-1][1]+p_cut[len(p_cut)-1][3]+p_cut[len(p_cut)-1][4]+p_cut[len(p_cut)-1][6]+p_cut[len(p_cut)-1][7]
f.close()

Trains = ['DSB MQ','NJ Desiro','LINT41 AR','NJ LINT41','DSB IC3','DSB ABs','LT LINT41']
filtering_tag = 'report_md'
Directory = '../OBU_Proxy'

RMR_Messages  = Rdp.extract_and_decode_rawData(Directory, ['190520', '260520'], [2,14])


'''
FLAG_LOAD = 0

#----------------------------------------------------- Time initialization ----------------------------------------------------
# In order to estimate the time needed to run the code
t = time.time()

#----------------------------------------------------- Raw data loading ----------------------------------------------------
if(FLAG_LOAD == 0):
    print('Big load has been selected !'+'\r\n')
    print(p0,p1)
    Raw_data  = Rdp.extract_rawData(Directory,[p0,p1])
    M_treated = Rdp.decode_filtered_rawData_0(Raw_data, 'RawData_filtered.txt', 'RawData_length.txt',filtering_tag)
else:
    M_treated = Rdp.decode_filtered_rawData_1('RawData_filtered.txt', 'RawData_length.txt')




f = open('id_train_mapping.txt','r+')
id_name_map = f.readlines()
f.close()

#----------------------------------------------------- List separation ----------------------------------------------------
[M_treated_tot,M_treated_occ_1,M_treated_occ_2,M_treated_occTotal] = Rdp.list_separation(M_treated)


#----------------------------------------------------- List sorting ----------------------------------------------------
M_treated_occ_1    = sorted(M_treated_occ_1, key = lambda x: (x.date_for_sort,x.time_for_sort))
M_treated_occ_2    = sorted(M_treated_occ_2, key = lambda x: (x.date_for_sort,x.time_for_sort))
M_treated_occTotal = sorted(M_treated_occTotal, key = lambda x: (x.date_for_sort,x.time_for_sort))

#----------------------------------------------------- Double check ----------------------------------------------------
# Check if there are multiple same messages 
Sp.double_check(M_treated_occ_1)
Sp.double_check(M_treated_occ_2)
Sp.double_check(M_treated_occTotal)

#----------------------------------------------------- List concatenation ----------------------------------------------------
M_treated_occ   = M_treated_occ_1 + M_treated_occ_2
M_treated_occ   = sorted(M_treated_occ, key = lambda x: (x.date_for_sort,x.time_for_sort))


#----------------------------------------------------- Stats compute ----------------------------------------------------
IDs = []
names = []
indexTrains = []
cnt = 0
cnt_prev = 0
i = 0
for Train in Trains:
    ID    = Rdp.getIDs(Train, id_name_map)
    name  = Rdp.getNames(Train, id_name_map)
    cnt = cnt + len(name)
    indexTrains.append([[cnt_prev,cnt-1],Train])
    cnt_prev = cnt
    names = names + name
    IDs   = IDs + ID
    i     = i + 1
len_period = len(period)


Occ1     = []; Occ2     = []; Occ     = []; Occ24   = []; ToT     = []; Km_odo    = []; OccTotal     = []; OccTotal_24     = [];
tmp_occ1 = []; tmp_occ2 = []; tmp_occ = []; tmp_tot = []; tmp_odo = []; tmp_occ24 = []; tmp_occTotal = []; tmp_occTotal_24 = [];


w = open('../Logs/ANOMALY_LOG.txt','w+')
anomaly_str = ''
for i in range(0,len(IDs)):
    print('Computing stats ... : '+names[i]+' ('+str(i+1)+'/'+str(len(IDs))+')')
    tmp_occ1 = []
    tmp_occ2 = []
    tmp_occ  = []
    tmp_tot  = []
    tmp_odo  = []
    tmp_occ24 = []
    tmp_occTotal = []
    tmp_occTotal_24 = []
    for j in range(0,len(period)):
        occ_1 = Sp.mobileDefectOcc_compute(period[j], IDs[i], M_treated_occ_1)
        occ_2 = Sp.mobileDefectOcc_compute(period[j], IDs[i], M_treated_occ_2)
        occ_total = Sp.mobileDefectTotalOcc_compute(period[j], IDs[i], M_treated_occTotal)
        [COMET_FLAG_ODO,COMET_FLAG_TOT,comet_init_odo,comet_init_tot,odo,tot] = Sp.kmODO_trainOpTime_compute(period[j], \
                                                                                                             IDs[i], M_treated_tot)
        if(COMET_FLAG_ODO == 1):
            anomaly_str = names[i]+' -- ODO -- '+'Dates: '+str(comet_init_odo[0])+'-->'+str(comet_init_odo[2])+'\t'+'KM_ODO: '\
                          +str(comet_init_odo[1])+'-->'+str(comet_init_odo[3])
            w.write(anomaly_str+'\n')
        if(COMET_FLAG_TOT == 1):
            anomaly_str = names[i]+' -- TOT -- '+'Dates: '+str(comet_init_tot[0])+'-->'+str(comet_init_tot[2])+'\t'+'TRAIN_OP_TIME: '\
                          +str(comet_init_tot[1])+'-->'+str(comet_init_tot[3])
            w.write(anomaly_str+'\n')
        tmp_occ1.append(occ_1)
        tmp_occ2.append(occ_2)
        tmp_occTotal.append(occ_total)
        tmp_occ.append(occ_1+occ_2)
        tmp_tot.append(tot)
        tmp_odo.append(odo)
        if(tot == 0):
            tmp_occ24.append('')
            tmp_occTotal_24.append('')
        else:
            tmp_occ24.append((occ_1+occ_2)*24/tot)
            tmp_occTotal_24.append(occ_total*24/tot)
    Occ1.append(tmp_occ1)
    Occ2.append(tmp_occ2)
    OccTotal.append(tmp_occTotal)
    Occ.append(tmp_occ)
    ToT.append(tmp_tot)
    Km_odo.append(tmp_odo)
    Occ24.append(tmp_occ24)
    OccTotal_24.append(tmp_occTotal_24)
w.close()


#----------------------------------------------------- Excel work sheets ----------------------------------------------------
worksheet_dt_mb     = workbook.add_worksheet('Data treated mobile defect')
worksheet_dt_rd     = workbook.add_worksheet('Data treated radio failure')
worksheet_mb        = workbook.add_worksheet('Mobile defect')
worksheet_rd        = workbook.add_worksheet('Radio failure')
worksheet_kmodo     = workbook.add_worksheet('KmODO')
worksheet_tot       = workbook.add_worksheet('TrainOpTime')
worksheet_mb24      = workbook.add_worksheet('Mobile defect rate per 24H')
worksheet_rd24      = workbook.add_worksheet('Radio failure rate per 24H')
worksheet_report_mb    = workbook.add_worksheet('Report mobile failure')


# Data treated sheet filling
Inputs_fieds  = ['Train name','OBU date','OBU time','Latitude','Longitude','Full coordinates','Mobile defect','Full date']
true_format   = workbook.add_format({'bold': False, 'fg_color': 'red','align': 'center'})
false_format  = workbook.add_format({'bold': False, 'fg_color': 'yellow','align': 'center'})
titles_format = workbook.add_format({'bold': True,'align': 'center'})
coord_format  = workbook.add_format({'bold': False,'align': 'left'})
mobile_defect_format = workbook.add_format({'bold': False,'align': 'center'})
for j in range(0,len(Inputs_fieds)):
    worksheet_dt_mb.set_column(0,j,25)
    worksheet_dt_mb.write(0,j,Inputs_fieds[j],titles_format)
i = 1
for mess in M_treated_occ:
    if(mess.double_check == 0):
        if(mess.OBU_DATA.find(MOBILE_DEFECT_1) != -1):
            mobile = 1
        else:
            mobile = 2
        name  = mess.nameFromeId(id_name_map)
        gps   = mess.decode_GPS()
        date  = gps[GPS_DATE]
        date2 = date[0]+date[1]+'-'+date[2]+date[3]+'-'+date[4]+date[5]
        Time  = gps[GPS_TIME]
        Time  = Time[0]+Time[1]+':'+Time[2]+Time[3]+':'+Time[4]+Time[5]
        lat   = gps[GPS_LATITUDE]
        long  = gps[GPS_LONGITUDE]
        if(len(lat)>0):
            lat_maps  = float(lat[0]+lat[1])+float(lat[2:len(lat)-1])/60
            lat = lat[0:2]+u'\N{DEGREE SIGN}'+lat[2:len(lat)-1]+' '+lat[len(lat)-1]
        else:
            lat_maps  = ''
            lat = u'\N{DEGREE SIGN}'+' N'
        if(len(long)>0):
            long_maps = float(long[0]+long[1]+long[2])+float(long[3:len(long)-1])/60
            long = long[0:3]+u'\N{DEGREE SIGN}'+long[3:len(long)-1]+' '+long[len(long)-1]
        else:
            long_maps = ''
            long = u'\N{DEGREE SIGN}'+' E'
        worksheet_dt_mb.write(i,0,name)
        worksheet_dt_mb.write(i,1,date2)
        worksheet_dt_mb.write(i,2,Time)
        worksheet_dt_mb.write(i,3,lat_maps,coord_format)
        worksheet_dt_mb.write(i,4,long_maps,coord_format)
        worksheet_dt_mb.write(i,5,lat+' '+long)
        worksheet_dt_mb.write(i,6,mobile,mobile_defect_format)
        worksheet_dt_mb.write(i,7,'20'+date[4]+date[5]+'-'+date[2]+date[3]+'-'+date[0]+date[1]+'  '+Time)
        i = i + 1


# Data treated sheet filling
Inputs_fieds  = ['Train name','OBU date','OBU time','Latitude','Longitude','Full coordinates','Full date']
true_format   = workbook.add_format({'bold': False, 'fg_color': 'red','align': 'center'})
false_format  = workbook.add_format({'bold': False, 'fg_color': 'yellow','align': 'center'})
titles_format = workbook.add_format({'bold': True,'align': 'center'})
coord_format  = workbook.add_format({'bold': False,'align': 'left'})
mobile_defect_format = workbook.add_format({'bold': False,'align': 'center'})
for j in range(0,len(Inputs_fieds)):
    worksheet_dt_rd.set_column(0,j,25)
    worksheet_dt_rd.write(0,j,Inputs_fieds[j],titles_format)
i = 1
for mess in M_treated_occTotal:
    if(mess.double_check == 0):
        name  = mess.nameFromeId(id_name_map)
        gps   = mess.decode_GPS()
        date  = gps[GPS_DATE]
        date2 = date[0]+date[1]+'-'+date[2]+date[3]+'-'+date[4]+date[5]
        Time  = gps[GPS_TIME]
        Time  = Time[0]+Time[1]+':'+Time[2]+Time[3]+':'+Time[4]+Time[5]
        lat   = gps[GPS_LATITUDE]
        long  = gps[GPS_LONGITUDE]
        if(len(lat)>0):
            lat_maps  = float(lat[0]+lat[1])+float(lat[2:len(lat)-1])/60
            lat = lat[0:2]+u'\N{DEGREE SIGN}'+lat[2:len(lat)-1]+' '+lat[len(lat)-1]
        else:
            lat_maps  = ''
            lat = u'\N{DEGREE SIGN}'+' N'
        if(len(long)>0):
            long_maps = float(long[0]+long[1]+long[2])+float(long[3:len(long)-1])/60
            long = long[0:3]+u'\N{DEGREE SIGN}'+long[3:len(long)-1]+' '+long[len(long)-1]
        else:
            long_maps = ''
            long = u'\N{DEGREE SIGN}'+' E'
        worksheet_dt_rd.write(i,0,name)
        worksheet_dt_rd.write(i,1,date2)
        worksheet_dt_rd.write(i,2,Time)
        worksheet_dt_rd.write(i,3,lat_maps,coord_format)
        worksheet_dt_rd.write(i,4,long_maps,coord_format)
        worksheet_dt_rd.write(i,5,lat+' '+long)
        worksheet_dt_rd.write(i,6,'20'+date[4]+date[5]+'-'+date[2]+date[3]+'-'+date[0]+date[1]+'  '+Time)
        i = i + 1


# Occurences, Km odo, TrainOpTime and Occurences24h sheets filling

x_offset = 2+len(period)
i0 = 2; j0 = 1
start_occ  = [i0,j0]
start_occ1 = [i0,j0+x_offset]
start_occ2 = [i0,j0+2*x_offset]

write_tableStats(worksheet_mb, workbook, 'Mobile defect', IDs, names, period, start_occ, Occ, [0,5,10])
write_tableStats(worksheet_mb, workbook, 'Mobile 1', IDs, names, period, start_occ1, Occ1, [0,5,10])
write_tableStats(worksheet_mb, workbook, 'Mobile 2', IDs, names, period, start_occ2, Occ2, [0,5,10])
write_tableStats(worksheet_rd, workbook, 'Radio failure', IDs, names, period, start_occ, OccTotal, [0,2.5,5])
write_tableStats(worksheet_kmodo, workbook, 'Km Odo', IDs, names, period, start_occ, Km_odo, [0,3750,7500])
write_tableStats(worksheet_tot, workbook, 'Train op Time', IDs, names, period, start_occ, ToT, [0,90,180])
write_tableStats(worksheet_mb24, workbook, 'Mobile defect rate per 24h', IDs, names, period, start_occ, Occ24, [0,1,2])
write_tableStats(worksheet_rd24, workbook, 'Radio failure rate per 24h', IDs, names, period, start_occ, OccTotal_24, [0,1,2])


# Report sheet filling

start = [2,1]
for it in indexTrains:
    index = it[0]
    Train_type = it[1]
    Occ_trunc  = Occ[index[0]:index[1]+1][:]
    Occ1_trunc = Occ1[index[0]:index[1]+1][:]
    Occ2_trunc = Occ2[index[0]:index[1]+1][:]
    OccTotal_trunc = OccTotal[index[0]:index[1]+1][:]
    ToT_trunc  = ToT[index[0]:index[1]+1][:]
    write_report(worksheet_report_mb, workbook, Train_type, period, start, id_name_map, Occ_trunc, Occ1_trunc, Occ2_trunc, ToT_trunc, [0,1,2])
    offset = len(Rdp.getNames(Train_type, id_name_map)) + 9
    start[0] = start[0] + offset 



workbook.close()

# Final time 
elapsed = time.time() - t
print(' ============================ Time analysis ============================ ')
print('Elapsed time : '+str(elapsed)+' sec')

'''

