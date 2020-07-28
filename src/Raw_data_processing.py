from functions import *
from Variables import *


############################ Classes ############################

class Message(object):

    def __init__(self, Raw_data):

        self.Raw_data = Raw_data        

    def getID(self):

        ID = ''
        Raw_data = self.Raw_data
        Index = findIndexof(Raw_data, ';', 8)
        ID = Raw_data[(Index[1]+1):Index[2]]
        return ID

    def getGPSfull(self):

        Raw_data = self.Raw_data
        size = 10
        index = findIndexof(Raw_data, ';', 8)
        gps_full = arrayAllocate('',size)
        gps_full = Raw_data[index[3]+1:index[4]]
        
        Index = findIndexof(gps_full,',', size-1)
        gps_field = arrayAllocate('',size)
        
        gps_field[GPS_VALIDITY] = gps_full[0:Index[0]]
        gps_field[GPS_TIME] = gps_full[Index[0]+1:Index[1]]
        gps_field[GPS_DATE] = gps_full[Index[1]+1:Index[2]]
        gps_field[GPS_LATITUDE] = gps_full[Index[2]+1:Index[3]]
        gps_field[GPS_LONGITUDE] = gps_full[Index[3]+1:Index[4]]
        gps_field[GPS_ALTITUDE] = gps_full[Index[4]+1:Index[5]]
        gps_field[GPS_HDOP_STATUS] = gps_full[Index[5]+1:Index[6]]
        gps_field[GPS_SPEED] = gps_full[Index[6]+1:Index[7]]
        gps_field[GPS_DIRECTION] = gps_full[Index[7]+1:Index[8]]
        gps_field[GPS_SATELLITE_NB] = gps_full[Index[8]+1:(len(gps_full)-1)]
        
        return gps_field 

    def getLongitude(self):
        
        GPS = self.getGPSfull()
        long = GPS[GPS_LONGITUDE]
        return long

    def getLatitude(self):
        
        GPS = self.getGPSfull()
        lat = GPS[GPS_LATITUDE]
        return lat

    def getOBUtime(self):
        
        GPS = self.getGPSfull()
        obu_time = GPS[GPS_TIME]
        return obu_time

    def getOBUdate(self):
        
        GPS = self.getGPSfull()
        obu_date = GPS[GPS_DATE]
        return obu_date

    def getRMRdate(self):

        Raw_data = self.Raw_data
        rmr_date = Raw_data[1:(Raw_data.find(' '))]
        return rmr_date

    def getRMRtime(self):

        Raw_data = self.Raw_data
        rmr_time = Raw_data[(Raw_data.find(' ')+1):(Raw_data.find('|'))]
        return rmr_time

    def getDiag(self):
    
        Raw_data = self.Raw_data
        index = index = findIndexof(Raw_data, ';', 8)
        Diag = Raw_data[(index[len(index)-1]+1):(len(Raw_data)-1)]
        return Diag

    def decode_RMR_message(self):

        Raw_data = self.Raw_data
        G1_index = Raw_data.find('<G1>')
        G1_end_index = Raw_data.find('</G1>')
        Index = findIndexof(Raw_data, ';', 8)
        
        OBU_LEN = Raw_data[(G1_index+4):(Index[0])]
        OBU_VER = Raw_data[(Index[0]+1):Index[1]]
        OBU_ID  = Raw_data[(Index[1]+1):Index[2]]
        OBU_ACK = Raw_data[(Index[2]+1):Index[3]]
        OBU_GPS = Raw_data[(Index[3]+1):Index[4]]
        OBU_DATA_TYPE = Raw_data[(Index[4]+1):Index[5]]
        OBU_CUSTUM = Raw_data[(Index[5]+1):Index[6]]
        OBU_DATA_LEN = Raw_data[(Index[6]+1):Index[7]]
        OBU_DATA = Raw_data[(Index[7]+1):G1_end_index]

        return [OBU_LEN,OBU_VER,OBU_ID,OBU_ACK,OBU_GPS,OBU_DATA_TYPE, \
                OBU_CUSTUM,OBU_DATA_LEN,OBU_DATA]

class Mess_treated(object):
    
    time_for_sort = 0
    date_for_sort = 0
    double_check  = 0

    def __init__(self, OBU_LEN,OBU_VER,OBU_ID,OBU_ACK,OBU_GPS,OBU_DATA_TYPE, \
                OBU_CUSTOM,OBU_DATA_LEN,OBU_DATA):

        self.OBU_LEN = int(OBU_LEN.encode().hex(),16)
        self.OBU_VER = OBU_VER
        self.OBU_ID = OBU_ID
        self.OBU_ACK = OBU_ACK
        self.OBU_GPS = OBU_GPS
        self.OBU_DATA_TYPE = OBU_DATA_TYPE
        self.OBU_CUSTOM = OBU_CUSTOM
        self.OBU_DATA_LEN = OBU_DATA_LEN
        self.OBU_DATA = OBU_DATA

    def decode_GPS(self):
        
        Index = findIndexof(self.OBU_GPS,',', 9)
        gps_field = arrayAllocate('',10)
        
        gps_field[GPS_VALIDITY] = self.OBU_GPS[0:Index[0]]
        gps_field[GPS_TIME] = self.OBU_GPS[Index[0]+1:Index[1]]
        gps_field[GPS_DATE] = self.OBU_GPS[Index[1]+1:Index[2]]
        gps_field[GPS_LATITUDE] = self.OBU_GPS[Index[2]+1:Index[3]]
        gps_field[GPS_LONGITUDE] = self.OBU_GPS[Index[3]+1:Index[4]]
        gps_field[GPS_ALTITUDE] = self.OBU_GPS[Index[4]+1:Index[5]]
        gps_field[GPS_HDOP_STATUS] = self.OBU_GPS[Index[5]+1:Index[6]]
        gps_field[GPS_SPEED] = self.OBU_GPS[Index[6]+1:Index[7]]
        gps_field[GPS_DIRECTION] = self.OBU_GPS[Index[7]+1:Index[8]]
        gps_field[GPS_SATELLITE_NB] = self.OBU_GPS[Index[8]+1:(len(self.OBU_GPS)-1)]
        
        return gps_field

    def print(self):

        print('=================================================')
        print('OBU Length : ',self.OBU_LEN)
        print('OBU Version : '+self.OBU_VER)
        print('OBU ID : '+self.OBU_ID)
        print('OBU Ack : '+self.OBU_ACK)
        print('OBU GPS : '+self.OBU_GPS)
        print('OBU Data type : '+self.OBU_DATA_TYPE)
        print('OBU Cust : '+self.OBU_CUSTOM)
        print('OBU data length : ',self.OBU_DATA_LEN)
        print('OBU data : ',self.OBU_DATA)

    def nameFromeId(self,Id_name_strings):
        
        i = 0
        Name = ''
        for line in Id_name_strings:
            Id = line[0:line.find('\t')]
            Name = line[line.find('\t')+1:len(line)-1]
            if(Id==self.OBU_ID):
                break
        return Name


############################ Functions ############################


def extract_rawData(OBU_Proxy_dir, period):
    temp1     = period[0]
    temp2     = period[1]
    period_rev = ['','']
    period_rev[0] = temp1[4]+temp1[5]+temp1[2]+temp1[3]+temp1[0]+temp1[1]
    period_rev[1] = temp2[4]+temp2[5]+temp2[2]+temp2[3]+temp2[0]+temp2[1]
    date1_int = int(period_rev[0])
    date2_int = int(period_rev[1])
    
    ListDir   = os.listdir('./'+OBU_Proxy_dir)  # List all directories present in OBU_proxy
    Raw_data_str = []
    Messages = []
    M_treated = []
    index_G1 = 0
    index_G1_end = 0
    dir_flag = 0
    for directory in ListDir:
        #print('Directory : '+directory)
        ListFiles = os.listdir('./'+OBU_Proxy_dir+'/'+directory)
        dir_flag = 1
        for filename in ListFiles:
            filename_date = filename[2:4]+filename[5:7]+filename[8:10]
            filename_date_int = int(filename_date)
            if(date1_int <= filename_date_int <= date2_int):
                if(dir_flag == 1):
                    print('Directory : '+directory)
                    dir_flag = 0
                print('File name : '+filename)
                f = open('./'+OBU_Proxy_dir+'/'+directory+'/'+filename,'r+')
                lines = f.readlines()
                for i in range(0,len(lines)):
                    if((lines[i].find('<G1>') != -1)):
                        k = i
                        data_str = lines[i]
                        while((lines[k].find('</G1>') == -1)):
                            k = k + 1
                            data_str = data_str + lines[k]
                        index_G1 = data_str.find('<G1>')
                        index_G1_end = data_str.find('</G1>')+5
                        Raw_data_str.append(data_str[index_G1:index_G1_end])
                        
                        #print(ascii(data_str[index_G1:index_G1_end]))
                        #Raw_data_str.append(data_str)
                f.close()
            
    len_raw_data = len(Raw_data_str)
    print('The number of messages to be treated : ',len_raw_data)
    return Raw_data_str


def decode_filtered_rawData_0(Raw_data, Filename_out, File_len_rawdata, filtering_tag):
    len_raw_data = len(Raw_data)
    w = open(Filename_out,'w+')
    Messages = []
    M_treated = []
    i = 0
    k = 0
    cond = 0
    for data in Raw_data:
        Index = findIndexof(data, ';', 8)
        OBU_DATA_TYPE = data[(Index[4]+1):Index[5]]
        data_hex = bytes(OBU_DATA_TYPE, "utf-8")
        TRU_NID_MESSAGE = data_hex[0:2]
        if(filtering_tag == 'report_md'):
            cond = ((OBU_DATA_TYPE == '2') and ((data.find(MOBILE_DEFECT_1) != -1) or (data.find(MOBILE_DEFECT_2) != -1))) or (OBU_DATA_TYPE == '14') or (OBU_DATA_TYPE == '2')
        elif(filtering_tag == 'comet_init'):
            cond = (OBU_DATA_TYPE == '14')
        elif(filtering_tag == 'evc_tru'):
            cond = (OBU_DATA_TYPE == '2')
        else:
            print('The filtering tag is incorrect, the process aborted !')
            exit(1)
        if(cond):
            w.write(data+'\n') ################################################################
            Messages.append(Message(data))
            [OBU_LEN,OBU_VER,OBU_ID,OBU_ACK,OBU_GPS,\
            OBU_DATA_TYPE,OBU_CUSTOM,OBU_DATA_LEN,OBU_DATA] = Messages[i].decode_RMR_message()
            M_treated.append(Mess_treated(OBU_LEN,OBU_VER,OBU_ID,OBU_ACK,OBU_GPS,OBU_DATA_TYPE, \
                    OBU_CUSTOM,OBU_DATA_LEN,OBU_DATA))
            gps_field = M_treated[i].decode_GPS()
            M_treated[i].date_for_sort = dateStringToIntConvert(gps_field[GPS_DATE])
            obu_time = gps_field[GPS_TIME]
            M_treated[i].time_for_sort = int(obu_time[0:6])
            i = i + 1
        if((k%100000)==0):
            load = (k/len_raw_data)*100
            print('Loading... ',load)
        k = k + 1
    len_raw_data_filtered = len(M_treated)

    w2 = open(File_len_rawdata,'w+')
    w2.write(str(len_raw_data_filtered))
    w2.close()
    
    print('\n')
    print('------------------- Data filtered ! -------------------')
    print('\n')
    print('Initial number of data : ',len_raw_data)
    print('Number of filtered data : ',len_raw_data_filtered)
    w.close()
    return M_treated

def decode_filtered_rawData_1(Filename_in,File_len_rawdata):
    Messages = []
    M_treated = []
    f = open(Filename_in,'r+')
    f2 = open(File_len_rawdata,'r+')
    len_raw_data = int(f2.readline())
    print(len_raw_data)
    f2.close()
    lines = f.readlines()
    j = 0
    for i in range(0,len(lines)):
        if((lines[i].find('<G1>') != -1)):
            k = i
            data_str = lines[i]
            while((lines[k].find('</G1>') == -1)):
                k = k + 1
                data_str = data_str + lines[k]
            index_G1 = data_str.find('<G1>')+4
            index_G1_end = data_str.find('</G1>')
            Messages.append(Message(data_str))
            [OBU_LEN,OBU_VER,OBU_ID,OBU_ACK,OBU_GPS,\
            OBU_DATA_TYPE,OBU_CUSTOM,OBU_DATA_LEN,OBU_DATA] = Messages[j].decode_RMR_message()
            M_treated.append(Mess_treated(OBU_LEN,OBU_VER,OBU_ID,OBU_ACK,OBU_GPS,OBU_DATA_TYPE, \
                    OBU_CUSTOM,OBU_DATA_LEN,OBU_DATA))
            gps_field = M_treated[j].decode_GPS()
            M_treated[j].date_for_sort = dateStringToIntConvert(gps_field[GPS_DATE])
            obu_time = gps_field[GPS_TIME]
            M_treated[j].time_for_sort = int(obu_time[0:6])
            if((j%100000)==0):
                load = (j/len_raw_data)*100
                print('Loading... ',load)
            j = j + 1
    f.close()
    return M_treated


def getIDs(Train_type, id_name_map):
    ids = []
    for line in id_name_map:
        if(line.find(Train_type) != -1):
            ids.append(line[0:6])
    return ids

def getNames(Train_type, id_name_map):
    names = []
    for line in id_name_map:
        if(line.find(Train_type) != -1):
            names.append(line[7:(len(line)-1)])
    return names


def list_separation(M_treated):
    M_treated_occ_1    = []
    M_treated_occ_2    = []
    M_treated_occTotal = []
    M_treated_tot      = []
    for mess in M_treated:
        if(mess.OBU_DATA_TYPE == '2'):
            data = mess.OBU_DATA
            data_hex = data.encode().hex()
            TRU_NID_MESSAGE = int(data_hex[0:2],16)
            if(TRU_NID_MESSAGE == 9):
                DRU_NID_PACKET   = int(data_hex[16:18],16)
                if(DRU_NID_PACKET == 5):
                    DRU_Q_TEXT = int(data_hex[34:36],16)
                    if(DRU_Q_TEXT == 57):
                        M_treated_occTotal.append(mess)
        if(mess.OBU_DATA_TYPE == '14'):
            M_treated_tot.append(mess)
        if((mess.OBU_DATA_TYPE == '2') and (mess.OBU_DATA.find(MOBILE_DEFECT_1) != -1)):
            M_treated_occ_1.append(mess)
        if((mess.OBU_DATA_TYPE == '2') and (mess.OBU_DATA.find(MOBILE_DEFECT_2) != -1)):
            M_treated_occ_2.append(mess)

    return [M_treated_tot,M_treated_occ_1,M_treated_occ_2,M_treated_occTotal]
