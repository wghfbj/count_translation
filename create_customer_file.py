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
import sqlite3
import os
reload(sys)
sys.setdefaultencoding( "utf-8" )
from datetime import date,datetime
import time

#variable
file
DBFileName = "StringTrans.db"


def read_excel_to_flie(projectname, filename):

    global file
    workbook = xlrd.open_workbook(filename, formatting_info=True)

    sheet = workbook.sheet_by_name(u'word')
    assert sheet.nrows > 0, '***The XLS file has nothing!***'
    assert sheet.cell(0, 1).value == "#English", '***The XLS Format is not Correct, Please keep English in the frist rank!***'

    #SQL
    conn = sqlite3.connect(DBFileName)
    c = conn.cursor()
    #SQL

    row = 1   # start at '0' 行
    rank = sheet.ncols - 1  # start at '0' 列

    #print "row = ", row
    #print "rank = ", rank

    rank = 2 # Enlish+1

    while rank <= sheet.ncols - 1:
        while row <= sheet.nrows - 1:

                if sheet.cell(row, 1).value == "": #Skip Null string
                    row += 1
                    continue
                #SQL
                eng = sheet.cell(row, 1).value
                lang = sheet.cell(0, rank).value
                trans = cell_value = sheet.cell(row,rank).value
                proj = projectname
                filen = filename
                Result_Like = c.execute('''SELECT * FROM StringTrans WHERE  eng= ? AND lang = ? AND trans = ? ''', (eng, lang, trans))
                Result_Like_Count = Result_Like.fetchall()
                if len(Result_Like_Count) > 0:
                    Result_Same = c.execute('''SELECT * FROM StringTrans WHERE  eng= ? AND lang = ? AND trans = ? AND proj = ? AND filename = ? ''', (eng, lang, trans, proj, filename))
                    Result_Same_count = Result_Same.fetchall()
                    if len(Result_Same_count) > 0: #Skip the same English string in one Sheet
                        row += 1
                        continue
                    else:
                        #Need to Update
                        for tIndex in Result_Like_Count:
                            AddProj = tIndex[3] + '_' + proj
                            AddFilen = tIndex[4] + '_' + filen
                            AddTime = tIndex[5] + 1
                            c.execute('''UPDATE StringTrans SET time = ? ,proj = ? ,filename = ? WHERE  eng = ? AND lang = ? AND trans = ? ''', (AddTime, AddProj, AddFilen, eng, lang, trans))
                            break
                else:
                    c.execute('''INSERT INTO StringTrans VALUES (?, ?, ?, ?, ?, 1)''', (eng, lang, trans, proj, filen))
                #SQL

                #Convert XLS to txt
                #Table 1
                cell_value = sheet.cell(row, 1).value #English
                if type(cell_value) == float:
                    cell_value = int(cell_value)
                    cell_value = str(cell_value)
                file.write(cell_value)
                file.write(',')
                #Table 2
                cell_value = sheet.cell(0, rank).value #Language
                if type(cell_value) == float:
                    cell_value = int(cell_value)
                    cell_value = str(cell_value)
                file.write(cell_value)
                file.write(',')
                #Table 3
                cell_value = sheet.cell(row,rank).value #Translation
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
        row = 1
        rank += 1

    #SQL
    conn.commit()
    conn.close()
    #SQL

def sqllite3_create():

    if os.path.exists(DBFileName):
        os.remove(DBFileName)
    conn = sqlite3.connect(DBFileName)

    c = conn.cursor()

    c.execute('''CREATE TABLE StringTrans
          (eng varchar(100) DEFAULT NULL,
           lang varchar(50) DEFAULT NULL,
           trans varchar(100) DEFAULT NULL,
           proj varchar(50) DEFAULT NULL,
           filename varchar(100) DEFAULT NULL,
           time INTEGER DEFAULT 1)''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    ProjectName = sys.argv[1]
    filename = sys.argv[2]
    print 'Start:' + time.strftime('%Y.%m.%d.%H.%M.%S',time.localtime(time.time()))
    #for i in range(1, len(sys.argv)):
        #print "参数", i, sys.argv[i]
    sqllite3_create()
    OutFileName = './StringTranslation_' + ProjectName + '_' + filename + '.txt'
    file = open(OutFileName, 'w') #a->追加写 w->只写 r->只读 r+->读写
    file.seek(0)
    read_excel_to_flie(ProjectName, filename)
    file.close
    print 'End:' + time.strftime('%Y.%m.%d.%H.%M.%S',time.localtime(time.time()))
    sys.exit(0)
