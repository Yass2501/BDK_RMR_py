

def Maintenance_Manager_Management(RMR_Messages, LLRU_IDs, LLRU_STATEs):
    RMR_Messages_MM = []
    for m in RMR_Messages:
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
                    #print(DRU_NID_PACKET)
                    DRU_NID_SOURCE  = data_hex[22:24]
                    DRU_M_DIAG      = data_hex[24:27]
                    DRU_M_DIAG_INT  = int(DRU_M_DIAG,16)
                    DRU_NID_CHANNEL = data_hex[27:28]
                    DRU_L_TEXT      = data_hex[28:30]
                    DRU_X_TEXT      = data_hex[30:]
                    #print_dru_x_text(DRU_X_TEXT)
                    #print(DRU_M_DIAG_INT)
                    filter_sum = 0
                    for i in range(0,len(LLRU_IDs)):
                        if((DRU_M_DIAG_INT % 160 == LLRU_IDs[i]) and (int(DRU_M_DIAG_INT / 160) == LLRU_STATEs[i])):
                            #print(i)
                            filter_sum = filter_sum + 1
                    if(filter_sum >= 1):
                        #print(DRU_M_DIAG_INT)
                        RMR_Messages_MM.append(m)
    return RMR_Messages_MM


def print_dru_x_text(DRU_X_TEXT):
    dru_x_text      = bytes.fromhex(DRU_X_TEXT)
    print(dru_x_text.decode("ascii"))
