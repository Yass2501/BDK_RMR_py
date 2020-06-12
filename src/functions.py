import os
import math


def sumLine(A,i_index):
    n = len(A[0])
    sum = 0
    for j in range(0,n):
        sum = sum + A[i_index][j]
    return sum

def sumColumn(A,j_index):
    m = len(A)
    sum = 0
    for i in range(0,m):
        sum = sum + A[i][j_index]
    return sum

def printMatrix(A):
    m = len(A)
    n = len(A[0])
    for i in range(0,m):
        for j in range(0,n):
            print(A[i][j],end='\t')
        print('')

def index_G1_G1bar(line):
    index_G1 = 0
    index_G1_end = 0
    for i in range(0,len(line)):
        if(line[i:(i+4)] == '<G1>'):
            index_G1 = i
        if(line[i:(i+5)] == '</G1>'):
            index_G1_end = i+5
    return [index_G1,index_G1_end]
    
def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

def arrayAllocate(value,size):
    array = []
    for i in range(0,size):
        array.append(value)
    return array

def dateStringToIntConvert(string_date):
    # Input : ddmmyy (String)
    # Output : yymmdd (integer)
    date = ''
    index_date = [4,5,2,3,0,1]
    for x in range(0,len(index_date)):
        date = date + string_date[index_date[x]] 
    date = int(date)
    
    return date


def timeStringToIntConvert(string_time):
    # Input : hhmmss (String)
    # Output : hhmmss (integer)
    time = ''
    for x in range(0,6):
        time = time + string_time[x]
    time = int(time)
    return time


def matrixAllocate(value,sizeX, sizeY):
    matrix = []
    for i in range(sizeX):
        matrix.append([])
        for j in range(sizeY):
            matrix[i].append(value)
    return matrix

def findIndexof(line, char, size):
    
    index = arrayAllocate(1,size)
    j = 0
    for i in range(0,len(line)):
        if((line[i] == char) and (j < size)):
            index[j] = i
            j = j + 1
    return index

def findIndexof2(lines, char, size):
    cnt = 0
    for i in range(0,len(lines[0])):
        if(lines[0][i] == char):
            cnt = cnt + 1
    linesSize = len(lines)
    Index = arrayAllocate(0,linesSize)
    i = 0
    for line in lines:
        Index[i] = findIndexof(line, char, size)
        #print(Index[i],i)
        i = i + 1
    return Index


def minIndex(vector):
    min = math.inf
    index = 0
    size = len(vector)
    for i in range(0,size):
        if(vector[i] <= min):
            min = vector[i]
            index = i

    return [min,index]
    
        
def sortListe(vector):
    size = len(vector)
    sortlist = arrayAllocate(0,size)
    index = arrayAllocate(0,size)
    for i in range(0,size):
        [sortlist[i],index[i]] = minIndex(vector)
        vector[index[i]] = math.inf
    return [sortlist,index]

def getIdFromName(name, id_name_map):
    ID = ''
    for line in id_name_map:
        Id = line[0:line.find('\t')]
        Name = line[line.find('\t')+1:len(line)-1]
        if(Name == name):
            ID = Id
            break
    return ID


