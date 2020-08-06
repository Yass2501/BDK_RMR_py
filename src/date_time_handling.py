#from datetime import datetime, date, timedelta
import math
import datetime


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
        date_iter = date_iter + datetime.timedelta(days=days_per_period[i])
        periods.append([date_fisrt, date_iter])
    return periods

def print_date(date, format):
    print(date.strftime(format))
	
def generate_periods2(date0, days_per_period, Nperiods):
    periods = []
    date_iter = date0
    for i in range(Nperiods):
        date_fisrt = date_iter
        date_iter = date_iter + datetime.timedelta(days=days_per_period)
        periods.append([date_fisrt, date_iter])
    return periods

if __name__ == '__main__':
    t = datetime.date(2020,8,6)
    #print(t.strftime('%Y%m%d'))
    
    date0 = datetime.date(2020,8,6)
    date1 = datetime.date(2020,10,6)
    interval = 8
    periods = generate_periods2(date0, 7, 5)
    format = '%Y%m%d'
    for p in periods:
        print(p[0].strftime(format),p[1].strftime(format))


    




    
    

