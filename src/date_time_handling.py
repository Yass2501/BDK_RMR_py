from datetime import datetime, date, timedelta
import math


def nearest_multiple(input_number, multiple):
    nearest_multiple = 0
    for i in range(0,2*multiple):
        if((input_number+i) % multiple == 0):
            nearest_multiple = input_number+i
            return [nearest_multiple, i]
        if((input_number-i) % multiple == 0):
            nearest_multiple = input_number-i
            return [nearest_multiple, -i]

def array_of_equivalent_days(total_of_days, multiple):
    days_array  = [0 for i in range(multiple)]
    nearest_mult, delta = nearest_multiple(total_of_days, multiple)
    for i in range(multiple):
        if((multiple - (i+1)) < abs(delta)):
            days_array[i] = int(nearest_mult / multiple) - int((delta)/abs(delta))
        else:
            days_array[i] = int (nearest_mult / multiple)
    
    return days_array

def generate_periods(date0, date1, interval):
    delta = date1 - date0
    total_of_days = delta.days
    days_per_period  = array_of_equivalent_days(total_of_days, interval)
    periods = []
    date_iter = date0
    periods = []
    for i in range(interval):
        date_fisrt = date_iter
        date_iter = date_iter + timedelta(days=days_per_period[i])
        periods.append([date_fisrt,date_iter])
    #print(days_per_period, sum(days_per_period))
    #print('Total of days : '+str(total_of_days))
    PERIODS = []
    for p in periods:
        tmp0 = str(p[0])
        tmp1 = str(p[1])
        PERIODS.append([tmp0[8]+tmp0[9]+tmp0[5]+tmp0[6]+tmp0[2]+tmp0[3],tmp1[8]+tmp1[9]+tmp1[5]+tmp1[6]+tmp1[2]+tmp1[3]])
    return PERIODS




    
    

