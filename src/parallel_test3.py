import multiprocessing
from Raw_data_processing import *
from date_time_handling import *
import time

Directory             = '../OBU_Proxy'
filter_obu_data_type  = 'all'      # 'all' for all messages, [2,16,14,...] for the messages type you want
d0 = date(2020, 1, 1)
d1 = date(2020, 6, 1)
Nprocs   = 8
para = 1
periods = generate_periods(d0, d1, Nprocs)
if __name__ == '__main__':
    
    if(para == 1):
        start = time.perf_counter()
        jobs = []
        RMR_Messages = []
        for i in range(Nprocs):
            p = multiprocessing.Process(target=extract_and_decode_rawData_para2, args=(Directory,periods[i],filter_obu_data_type,i, Nprocs))
            p.start()
            jobs.append(p)
        for proc in jobs:
            proc.join()

        finish = time.perf_counter()
        print(finish - start)
        

        for iproc in range(0,Nprocs):
            f = open('FilePROC'+str(iproc)+'.txt', 'r')
            lines = f.readlines()
            for i in range(0,len(lines)):
                if((lines[i].find('<G1>') != -1)):
                    k = i
                    data_str = lines[i]
                    while((lines[k].find('</G1>') == -1)):
                        k = k + 1
                        data_str = data_str + lines[k]
                    index_G1     = data_str.find('<G1>')
                    index_G1_end = data_str.find('</G1>')+5
                    Index        = findIndexof(data_str, ';', 8)
                        
                    OBU_LEN       = str(int((data_str[(index_G1+4):(Index[0])]).encode().hex(),16))
                    OBU_VER       = data_str[(Index[0]+1):Index[1]]
                    OBU_ID        = data_str[(Index[1]+1):Index[2]]
                    OBU_ACK       = data_str[(Index[2]+1):Index[3]]
                    OBU_GPS       = data_str[(Index[3]+1):Index[4]]
                    OBU_DATA_TYPE = data_str[(Index[4]+1):Index[5]]
                    OBU_CUSTOM    = data_str[(Index[5]+1):Index[6]]
                    OBU_DATA_LEN  = data_str[(Index[6]+1):Index[7]]
                    OBU_DATA      = data_str[(Index[7]+1):index_G1_end-5]

                    RMR_Messages.append(RMR_Message(OBU_LEN,OBU_VER,OBU_ID,OBU_ACK,OBU_GPS,OBU_DATA_TYPE,OBU_CUSTOM,OBU_DATA_LEN,OBU_DATA))
                    
            print('End of File : FilePROC'+str(iproc)+'.txt')
            f.close()
        
        finish = time.perf_counter()
        print(finish - start)
        
        
    else:
        start = time.perf_counter()
        RMR_Messages = extract_and_decode_rawData(Directory, [period0[0],period7[1]], filter_obu_data_type)
        finish = time.perf_counter()
        print(finish - start)
        print('LENGTH MESSAGES : '+str(len(RMR_Messages)))
