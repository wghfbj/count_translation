#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
# Copyright Statement: CVTE
# Copyright (C) 2018 Guangzhou Shiyuan Electronics Co.,Ltd. All rights reserved.
#      ____________        _______________  ___________
#     / / ________ \      / / _____   ____|| |  _______|
#    / / /      \ \ \    / / /   | | |     | | |
#   | | |        \ \ \  / / /    | | |     | | |_______
#   | | |         \ \ \/ / /     | | |     | |  _______|
#   | | |          \ \ \/ /      | | |     | | |
#    \ \ \______    \ \  /       | | |     | | |_______
#     \_\_______|    \_\/        |_|_|     |_|_________|
#
################################################################################
#   1 
#   2 
#######################
# filename: create_customer_file.py
# author  : fanbaoju
# date    : 2018-12-22
# version : V1.0.0
# note    :
#
################################################################################

import xlrd
import xlwt
import sys
import LinkList
reload(sys)
sys.setdefaultencoding( "utf-8" )
from datetime import date,datetime

#variable
file


def read_excel_to_flie(projectname, filename):

    global file
    workbook = xlrd.open_workbook(filename, formatting_info=True)

    sheet = workbook.sheet_by_name(u'word')
    assert sheet.nrows > 0, '***The XLS file has nothing!***'
    assert sheet.cell(0, 1).value == "#English", '***The XLS Format is not Correct, Please keep English in the frist rank!***'

    row = 1   # start at '0' 行
    rank = sheet.ncols - 1  # start at '0' 列

    #print "row = ", row
    #print "rank = ", rank

    rank = 2 # Enlish+!

    while rank <= sheet.ncols - 1:
        while row <= sheet.nrows - 1:
                #Table 1
                cell_value = sheet.cell(row, 1).value #English
                #print cell_value, '  +  rank = ', rank, '   +  row = ', row
                #print type(cell_value)
                if type(cell_value) == float:
                    cell_value = int(cell_value)
                    cell_value = str(cell_value)
                file.write(cell_value)
                file.write(',')
                #Table 2
                cell_value = sheet.cell(0, rank).value #English
                #print cell_value, '  +  rank = ', rank, '   +  row = ', row
                #print type(cell_value)
                if type(cell_value) == float:
                    cell_value = int(cell_value)
                    cell_value = str(cell_value)
                file.write(cell_value)
                file.write(',')
                #Table 3
                cell_value = sheet.cell(row,rank).value
                #print cell_value, '  +  rank = ', rank, '   +  row = ', row
                #print type(cell_value)
                if type(cell_value) == float:
                    cell_value = int(cell_value)
                    cell_value = str(cell_value)
                file.write(cell_value)
                file.write(',')
                #Table 4
                file.write(projectname)
                file.write(',')
                #Table 5
                file.write(filename)
                file.write('\r\n')      #change row in file
                row += 1
        #file.write('\r\n')      #change row in file
        row = 1
        rank += 1


if __name__ == '__main__':
    ProjectName = sys.argv[1]
    filename = sys.argv[2]
    #for i in range(1, len(sys.argv)):
        #print "参数", i, sys.argv[i]
    OutFileName = './StringTranslation_' + ProjectName + '_' + filename + '.txt'
    file = open(OutFileName, 'w') #a->追加写 w->只写 r->只读 r+->读写
    file.seek(0)
    read_excel_to_flie(ProjectName, filename)
    #print '已生成翻译文件'
    file.close
    sys.exit(0)

