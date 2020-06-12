import os
import xlsxwriter
from functions import *
import Raw_data_processing as Rdp
import Statistics_processing as Sp

workbook = xlsxwriter.Workbook('mobile_defect.xlsx')

merge_format = workbook.add_format({
    'bold':     True,
    'border':   1,
    'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#FFFFFF',
    'text_wrap':'true',
})
NA_format = workbook.add_format({
    'bold':     True,
    'border':   0,
    'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#808080',
})
report_format = workbook.add_format({
    'bold':     True,
    'border':   1,
    #'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#FFFFFF',
    'text_wrap':'true',
})
report_white_format = workbook.add_format({
    'bold':     True,
    'border':   1,
    #'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#FFFFFF',
})

def write_periods_trainNames(worksheet, period, names, start):
    j = 0
    for p in period:
        worksheet.write(start[0]-2,start[1]+j,p[0][0]+p[0][1]+'-'+p[0][2]+p[0][3]+'-'+p[0][4]+p[0][5])
        worksheet.write(start[0]-1,start[1]+j,p[1][0]+p[1][1]+'-'+p[1][2]+p[1][3]+'-'+p[1][4]+p[1][5])
        j = j + 1
    i = 0
    for name in names:
        worksheet.write(start[0]+i,start[1]-1,name)
        i = i + 1

def write_report(worksheet, workbook, Train_type, period, start, id_name_map, Occ, Occ1, Occ2, ToT, range_color):

    names = Rdp.getNames(Train_type, id_name_map)
    IDs   = Rdp.getIDs(Train_type, id_name_map)
    write_periods_trainNames(worksheet, period, names, start)
    worksheet.set_column(start[1]-1,start[1]-1,20)
    worksheet.merge_range(start[0]-2,start[1]-1,start[0]-1,start[1]-1,\
                          'Report Analysis'+'\r\n'+Train_type, merge_format)
    #vertical
    worksheet.write(start[0]+len(names),start[1]-1,'Mobile defect 1 / period',report_format)
    worksheet.write(start[0]+len(names)+1,start[1]-1,'Mobile defect 2 / period',report_format)
    worksheet.write(start[0]+len(names)+2,start[1]-1,'Total defect / period',report_format)
    worksheet.write(start[0]+len(names)+3,start[1]-1,'Total number of hour'+'\r\n'+'/ period',report_format)
    worksheet.write(start[0]+len(names)+4,start[1]-1,'Failure rate'+'\r\n'+'/ 24h / period',report_format)
    
    #horizontal
    worksheet.merge_range(start[0]-2,start[1]+len(period),start[0]-1,start[1]+len(period),'Total defect / train',report_format)
    worksheet.set_column(start[1]+len(period),start[1]+len(period),15)
    worksheet.merge_range(start[0]-2,start[1]+len(period)+1,start[0]-1,start[1]+len(period)+1,'Total number of hour'+'\r\n'+'/ train',report_format)
    worksheet.set_column(start[1]+len(period)+1,start[1]+len(period)+1,15)
    worksheet.merge_range(start[0]-2,start[1]+len(period)+2,start[0]-1,start[1]+len(period)+2,'Failure rate'+'\r\n'+'/ 24h / train',report_format)
    worksheet.set_column(start[1]+len(period)+2,start[1]+len(period)+2,15)

    for i in range(0,len(Occ)):
        for j in range(0,len(Occ[0])):
            if(ToT[i][j] == 0):
                worksheet.write(start[0]+i,start[1]+j,'',NA_format)
            else:
                worksheet.write(start[0]+i,start[1]+j,(Occ[i][j]/ToT[i][j])*24)
            if(i == 0):
                sumOcc = sumColumn(Occ,j)
                sumToT = sumColumn(ToT,j)
                worksheet.write(start[0]+len(Occ),start[1]+j,sumColumn(Occ1,j))
                worksheet.write(start[0]+len(Occ)+1,start[1]+j,sumColumn(Occ2,j))
                worksheet.write(start[0]+len(Occ)+2,start[1]+j,sumOcc) 
                worksheet.write(start[0]+len(Occ)+3,start[1]+j,sumToT)
                if(sumToT == 0):
                    worksheet.write(start[0]+len(Occ)+4,start[1]+j,'',NA_format)
                else:
                    worksheet.write(start[0]+len(Occ)+4,start[1]+j,(sumOcc/sumToT)*24)
        sumOcc = sumLine(Occ,i)
        sumToT = sumLine(ToT,i)
        worksheet.write(start[0]+i,start[1]+len(Occ[0]),sumOcc)
        worksheet.write(start[0]+i,start[1]+len(Occ[0])+1,sumToT)
        if(sumToT == 0):
            worksheet.write(start[0]+i,start[1]+len(Occ[0])+2,'',NA_format)
        else:
            worksheet.write(start[0]+i,start[1]+len(Occ[0])+2,(sumOcc/sumToT)*24)
            
    worksheet.conditional_format(start[0],start[1],start[0]+len(Occ)-1,start[1]+len(Occ[0])-1,\
                                 {'type': '3_color_scale','min_color': '#63BE7B',\
                                  'mid_color': '#FFEB84','max_color': '#F8696B','min_value': range_color[0],\
                                  'mid_value': range_color[1],'max_value': range_color[2],'min_type': 'num','mid_type': 'num',\
                                  'max_type': 'num'})
    worksheet.conditional_format(start[0]+len(Occ)+4,start[1],start[0]+len(Occ)+4,start[1]+len(Occ[0])-1,\
                                 {'type': '3_color_scale','min_color': '#63BE7B',\
                                  'mid_color': '#FFEB84','max_color': '#F8696B','min_value': range_color[0],\
                                  'mid_value': range_color[1],'max_value': range_color[2],'min_type': 'num','mid_type': 'num',\
                                  'max_type': 'num'})
    worksheet.conditional_format(start[0],start[1]+len(Occ[0])+2,start[0]+len(Occ),start[1]+len(Occ[0])+2,\
                                 {'type': '3_color_scale','min_color': '#63BE7B',\
                                  'mid_color': '#FFEB84','max_color': '#F8696B','min_value': range_color[0],\
                                  'mid_value': range_color[1],'max_value': range_color[2],'min_type': 'num','mid_type': 'num',\
                                  'max_type': 'num'})

def write_tableStats(worksheet, workbook, Title, IDs, names, period, start, data, range_color):
    
    write_periods_trainNames(worksheet, period, names, start)
    worksheet.set_column(start[1]-1,start[1]-1,20)
    worksheet.merge_range(start[0]-2,start[1]-1,start[0]-1,start[1]-1,\
                              Title, merge_format)
    i = 0
    for id in IDs:
        j = 0
        for p in period:
            if(data[i][j] == ''):
                worksheet.write(start[0]+i,start[1]+j,'',NA_format)
            else:
                worksheet.write(start[0]+i,start[1]+j,data[i][j])
            j = j + 1
        i = i + 1
    worksheet.conditional_format(start[0],start[1],i+start[0],j+start[1],\
                                     {'type': '3_color_scale','min_color': '#63BE7B',\
                                      'mid_color': '#FFEB84','max_color': '#F8696B','min_value': range_color[0],\
                                      'mid_value': range_color[1],'max_value': range_color[2],'min_type': 'num','mid_type': 'num',\
                                      'max_type': 'num'})
