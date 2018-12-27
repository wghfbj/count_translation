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
# filename: count_translation.py
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
global file
global ConSql
global DBFileName
global SqlHand
global CommitCount
file = 0
ConSql = 0
SqlHand = 0
CommitCount = 0
DBFileName = "StringTrans.db"


def read_excel_to_flie(projectname, filename):

    global file
    global DBFileName
    global ConSql
    global SqlHand
    global CommitCount
    workbook = xlrd.open_workbook(filename, formatting_info=True)

    sheet = workbook.sheet_by_name(u'word')
    if sheet.nrows == 0:
        print '[ERROR]***The XLS file has nothing!***' + projectname + '_' + filename
        return
    if sheet.cell(0, 1).value != "#English":
        print '[ERROR]***The XLS Format is not Correct, Please keep English in the frist rank!***' + projectname + '_' + filename
        return
    # assert sheet.nrows > 0, '[ERROR]***The XLS file has nothing!***'
    # assert sheet.cell(0, 1).value == "#English", '[ERROR]***The XLS Format is not Correct, Please keep English in the frist rank!***'

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
                Result_Like = SqlHand.execute('''SELECT proj, filename, time FROM StringTrans WHERE  eng= ? AND lang = ? AND trans = ? ''', (eng, lang, trans))
                Result_Like_Count = Result_Like.fetchall()
                if len(Result_Like_Count) > 0:
                    Result_Same = SqlHand.execute('''SELECT eng FROM StringTrans WHERE  eng= ? AND lang = ? AND trans = ? AND proj = ? AND filename = ? ''', (eng, lang, trans, proj, filename))
                    Result_Same_count = Result_Same.fetchall()
                    if len(Result_Same_count) > 0: #Skip the same English string in one Sheet
                        row += 1
                        continue
                    else:
                        #Need to Update proj & filename & time
                        for tIndex in Result_Like_Count: #使用迭代器查询
                            AddProj = tIndex[0] + '_' + proj
                            AddFilen = tIndex[1] + '_' + filen
                            AddTime = tIndex[2] + 1
                            SqlHand.execute('''UPDATE StringTrans SET time = ? ,proj = ? ,filename = ? WHERE  eng = ? AND lang = ? AND trans = ? ''', (AddTime, AddProj, AddFilen, eng, lang, trans))
                            break
                else:
                    SqlHand.execute('''INSERT INTO StringTrans VALUES (?, ?, ?, ?, ?, 1)''', (eng, lang, trans, proj, filen))
                #SQL

                #Convert XLS to txt
                #Table 1
                # cell_value = sheet.cell(row, 1).value #English
                # if type(cell_value) == float:
                #     cell_value = int(cell_value)
                #     cell_value = str(cell_value)
                # file.write(cell_value)
                # file.write(',')
                # #Table 2
                # cell_value = sheet.cell(0, rank).value #Language
                # if type(cell_value) == float:
                #     cell_value = int(cell_value)
                #     cell_value = str(cell_value)
                # file.write(cell_value)
                # file.write(',')
                # #Table 3
                # cell_value = sheet.cell(row,rank).value #Translation
                # if type(cell_value) == float:
                #     cell_value = int(cell_value)
                #     cell_value = str(cell_value)
                # file.write(cell_value)
                # file.write(',')
                # #Table 4
                # file.write(projectname)
                # file.write(',')
                # #Table 5
                # file.write(filename)
                # file.write('\r\n')      #change row in file
                #Convert XLS to txt
                row += 1
        row = 1
        rank += 1

    CommitCount += 1
    if CommitCount > 100: #For Saving time to commit data to DB
        CommitCount = 0
        ConSql.commit()


#SQL
def sqllite3_create():

    global ConSql
    global DBFileName
    global SqlHand
    # if os.path.exists(DBFileName):   #For Debug
    #     os.remove(DBFileName)
    ConSql = sqlite3.connect(DBFileName)

    SqlHand = ConSql.cursor()

    SqlHand.execute('''CREATE TABLE IF NOT EXISTS 'StringTrans'
          (eng varchar(100) DEFAULT NULL,
           lang varchar(50) DEFAULT NULL,
           trans varchar(100) DEFAULT NULL,
           proj varchar(500) DEFAULT NULL,
           filename varchar(1000) DEFAULT NULL,
           time INTEGER DEFAULT 1)''')

    ConSql.commit()
    ConSql.close()

def sqllite3_openfile():
    global ConSql
    global SqlHand
    ConSql = sqlite3.connect(DBFileName)
    SqlHand = ConSql.cursor()
    SqlHand.execute('PRAGMA synchronous = OFF') #Speed up saving time

def sqllite3_closefile():
    global ConSql
    ConSql.commit()
    ConSql.close()
#SQL


if __name__ == '__main__':
    ProjectName = sys.argv[1]
    filename = sys.argv[2]
    print 'Testing Start Time:' + time.strftime('%Y.%m.%d.%H.%M.%S',time.localtime(time.time()))
    #for i in range(1, len(sys.argv)):
        #print "参数", i, sys.argv[i]
    sqllite3_create()
    sqllite3_openfile()
    for i in range(2, len(sys.argv)):
        #Convert XLS to txt
        # OutFileName = './StringTranslation_' + ProjectName + '_' + filename + '.txt'
        # file = open(OutFileName, 'w') #a->追加写 w->只写 r->只读 r+->读写
        # file.seek(0)
        #Convert XLS to txt
        filename = sys.argv[i]
        read_excel_to_flie(ProjectName, filename)
        # file.close
        print "进度: " + str(float(i) / len(sys.argv) * 100) + "%"
    sqllite3_closefile()
    print "进度: 100%"
    print 'Testing End Time:' + time.strftime('%Y.%m.%d.%H.%M.%S',time.localtime(time.time()))
    sys.exit(0)
