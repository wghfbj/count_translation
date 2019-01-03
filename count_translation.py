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
import gc

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
    withEnligh = False
    EnlishRank = 0

    workbook = xlrd.open_workbook(filename, formatting_info=True)

    sheet = workbook.sheet_by_index(0) #Frist sheet
    if sheet.nrows == 0:
        print '[ERROR]***The XLS file has nothing!***' + projectname + '_' + filename
        return
    for tindex in range(1, sheet.ncols):
        if sheet.cell(0, tindex).value == '#English':
            withEnligh = True
            EnlishRank = tindex
            break
    if withEnligh != True:
        print '[ERROR]***The XLS Format is not Correct, Please keep English in the XLS!***Erro file ==>> ' + projectname + '_' + filename
        return
    # assert sheet.nrows > 0, '[ERROR]***The XLS file has nothing!***'
    # assert sheet.cell(0, 1).value == "#English", '[ERROR]***The XLS Format is not Correct, Please keep English in the frist rank!***'
    print 'Analysis proj:' + projectname + ' file:' + filename

    row = 1   # start at '0' 行
    rank = sheet.ncols - 1  # start at '0' 列

    #print "row = ", row
    #print "rank = ", rank

    if EnlishRank == 1:
        rank = 2 #Skip english rank
    else:
        rank = 1 #Skip english rank

    while rank <= sheet.ncols - 1:
        while row <= sheet.nrows - 1:

                if sheet.cell(row, 1).value == "": #Skip Null string
                    row += 1
                    continue
                #SQL
                eng = sheet.cell(row, EnlishRank).value
                lang = sheet.cell(0, rank).value
                lang = lang.capitalize() #统一大小写
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
                            AddProj = tIndex[0]
                            if AddProj.find(proj) == -1:
                                AddProj = tIndex[0] + '_' + proj
                            AddFilen = tIndex[1]
                            if AddFilen.find(filen) == -1:
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
        if rank == EnlishRank: #Skip english rank
            rank += 1

    CommitCount += 1
    if CommitCount > 100: #For Saving time to commit data to DB
        CommitCount = 0
        ConSql.commit()

def set_style(name,height,bold=False,back_color=255,is_border=False):

    style = xlwt.XFStyle() # 初始化样式

    font = xlwt.Font() # 为样式创建字体
    font.name = name # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    style.font = font

    if is_border == True:
        borders = xlwt.Borders()
        borders.left = 5
        borders.right = 5
        borders.top = 5
        borders.bottom = 5
        style.borders = borders

    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    #pattern.pattern_fore_colour = back_color #设置单元格背景颜色 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta

    style.pattern = pattern

    return style

def write_excel_to_flie(OutFilename, DBFilename):
    global ConSql
    global SqlHand
    pre_eng = 0

    if os.path.exists(OutFilename):
        os.remove(OutFilename)

    SheetOut = xlwt.Workbook(encoding = 'utf-8')

    SheetStyle = set_style('Times New Roman', 220, False)
    Title = [u'#英文', u'#语言', u'#翻译', u'#方案', u'#文件名', u'#次数']

    #Write DB to Xls file
    ConSql = sqlite3.connect(DBFilename)
    SqlHand = ConSql.cursor()
    SqlHand.execute('''SELECT * FROM StringTrans''')
    Result_All_Count = SqlHand.fetchone() #Error will return None
    if len(Result_All_Count) > 0:
        row = 1
        SheetCount = 1
        pre_lang = 0 #Use for adding new translation sheet
        
        for tIndexx in SqlHand.execute('''SELECT * FROM StringTrans order by lang, eng, time DESC'''): #使用迭代器查询
            now_eng = tIndexx[0]
            # lang = tIndexx[1]
            now_lang = tIndexx[1]
            if pre_lang == 0:
                pre_lang = now_lang
                Sheet1 = SheetOut.add_sheet(str(now_lang), cell_overwrite_ok=True)
                for tIndex in range(0,len(Title)):
                    Sheet1.write(0, tIndex, Title[tIndex], SheetStyle)
                row = 1
            elif pre_lang != now_lang:
                pre_lang = now_lang
                Sheet1 = SheetOut.add_sheet(str(now_lang), cell_overwrite_ok=True)
                for tIndex in range(0,len(Title)):
                    Sheet1.write(0, tIndex, Title[tIndex], SheetStyle)
                row = 1
                SheetCount = 1
            # trans = tIndexx[2]
            # proj = tIndexx[3]
            # filen = tIndexx[4]
            # time = tIndexx[5]
            for tIndexy in range(0, 6):
                if tIndexy == 4:
                    continue
                if pre_eng == now_eng and tIndexy == 0:
                    continue
                pre_eng = now_eng
                Sheet1.write(row, tIndexy, tIndexx[tIndexy], SheetStyle)
            if row == 65535: #Max row of one sheet in XLS
                row = 1
                Sheet1 = SheetOut.add_sheet(str(now_lang) + str(SheetCount), cell_overwrite_ok=True)
                for tIndex in range(0,len(Title)):
                    Sheet1.write(0, tIndex, Title[tIndex], SheetStyle)
                SheetCount += 1
                SheetOut.save(OutFilename);
            row += 1

    ConSql.close()
    #Write DB to Xls file

    SheetOut.save(OutFilename);
    print "Create release file " + OutFilename + " finish!"

#SQL
def sqllite3_create():

    global ConSql
    global DBFileName
    global SqlHand

    # if os.path.exists(DBFileName):   #For Debug #For Debug #For Debug #For Debug
    #     os.remove(DBFileName)

    ConSql = sqlite3.connect(DBFileName)
    SqlHand = ConSql.cursor()

    SqlHand.execute('''CREATE TABLE IF NOT EXISTS 'StringTrans'
          (eng varchar(100) DEFAULT NULL,
           lang varchar(50) COLLATE NOCASE DEFAULT NULL,
           trans varchar(100) DEFAULT NULL,
           proj varchar(500) DEFAULT NULL,
           filename varchar(1000) DEFAULT NULL,
           time INTEGER DEFAULT 1)''')

    SqlHand.execute('''CREATE INDEX IF NOT EXISTS 'CountTrans' ON 'StringTrans' (eng, lang, trans)''')

    ConSql.commit()
    ConSql.close()

def sqllite3_openfile():
    global ConSql
    global SqlHand
    ConSql = sqlite3.connect(DBFileName)
    SqlHand = ConSql.cursor()
    SqlHand.execute('PRAGMA synchronous = OFF') #Speed up insert time

def sqllite3_closefile():
    global ConSql
    ConSql.commit()
    ConSql.close()

def sqllite3_clearfile():
    global DBFileName
    if os.path.exists(DBFileName):   #For Debug
        os.remove(DBFileName)
        print "Clear file finish"
#SQL


if __name__ == '__main__':
    print 'Start Time:' + time.strftime('%Y.%m.%d.%H.%M.%S',time.localtime(time.time()))
    if sys.argv[1] == "clear":
        sqllite3_clearfile()
        print 'End Time:' + time.strftime('%Y.%m.%d.%H.%M.%S',time.localtime(time.time()))
        sys.exit(0)
    if sys.argv[1] == "release":
        if len(sys.argv) < 4:
            print "[ERROR]Please type output & db filename!"
        else:
            write_excel_to_flie(sys.argv[2], sys.argv[3])
        print 'End Time:' + time.strftime('%Y.%m.%d.%H.%M.%S',time.localtime(time.time()))
        sys.exit(0)
    ProjectName = sys.argv[1]
    filename = sys.argv[2]
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
        print "进度: " + str(round((float(i) / len(sys.argv) * 100), 1)) + "%"
    sqllite3_closefile()
    print "进度: 100%"
    print 'End Time:' + time.strftime('%Y.%m.%d.%H.%M.%S',time.localtime(time.time()))
    sys.exit(0)
