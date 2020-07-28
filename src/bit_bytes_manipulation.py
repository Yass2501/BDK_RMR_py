def hexToBin(x_hex):
    x_bin = ''
    if(x_hex == '0'):
        x_bin = '0000'
    elif(x_hex == '1'):
        x_bin = '0001'
    elif(x_hex == '2'):
        x_bin = '0010'
    elif(x_hex == '3'):
        x_bin = '0011'
    elif(x_hex == '4'):
        x_bin = '0100'
    elif(x_hex == '5'):
        x_bin = '0101'
    elif(x_hex == '6'):
        x_bin = '0110'
    elif(x_hex == '7'):
        x_bin = '0111'
    elif(x_hex == '8'):
        x_bin = '1000'
    elif(x_hex == '9'):
        x_bin = '1001'
    elif(x_hex == 'A' or x_hex == 'a'):
        x_bin = '1010'
    elif(x_hex == 'B' or x_hex == 'b'):
        x_bin = '1011'
    elif(x_hex == 'C' or x_hex == 'c'):
        x_bin = '1100'
    elif(x_hex == 'D' or x_hex == 'd'):
        x_bin = '1101'
    elif(x_hex == 'E' or x_hex == 'e'):
        x_bin = '1011'
    elif(x_hex == 'F' or x_hex == 'f'):
        x_bin = '1111'
    else:
        exit(1)
    return x_bin
