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
#   1 用于存放翻译等资源的链表
#   2 
#######################
# filename: LinkList.py
# author  : fanbaoju
# date    : 2018-12-22
# version : V1.0.0
# note    :
#
################################################################################

class Node(object):
    def __init__(self, eng, lang, trans, proj, filename):
        self.eng = eng #英语
        self.lang = lang #翻译为什么语言
        self.trans = trans #翻译
        self.proj = proj  #方案名称
        self.filename = filename  #文件名
        self.time = 0 #出现次数
        self.next = 0

class LinkList(object):
    def __init__(self):
        self.head = 0
        self.Length = 0

    def __getitem__(self, key):

        if self.is_empty():
            print 'linklist is empty.'
            return

        elif key <0  or key > self.getlength():
            print 'the given key is error'
            return

        else:
            return self.getitem(key)



    def __setitem__(self, key, value):

        if self.is_empty():
            print 'linklist is empty.'
            return

        elif key <0  or key > self.getlength():
            print 'the given key is error'
            return

        else:
            self.delete(key)
            return self.insert(key)

    def getlength(self):

        return self.Length

    def is_empty(self):

        if self.getlength() == 0:
            return True
        else:
            return False

    def clear(self):

        self.head = 0
        self.Length = 0


    def getitem(self,index): # Start at index 0

        if self.is_empty():
            print 'Linklist is empty.'
            return
        if index >= self.getlength():
            print 'getitem error, index is not correct.'
            return

        CurrentNode = self.head
        tindex = 0
        for tindex in range(index):
            CurrentNode = CurrentNode.next
        return CurrentNode

    def insert(self, eng, lang, trans, proj, filename, index=0): # Start at index 0

        if index<0:
            print 'insert error, index is not correct.'
            return

        if index == 0:
            CurrentNode = self.head
            if self.Length == 0:
                tNode = Node(eng, lang, trans, proj, filename);
                self.head = tNode
                tNode.next = 0
                self.Length += 1
            else:
                tindex = 0
                for tindex in range(self.getlength()):
                    CheckNode = self.getitem(tindex)
                    if CheckNode.eng == eng and CheckNode.lang == lang and CheckNode.trans == trans:
                        CheckNode.time+=1
                    else:
                        tNode = Node(eng, lang, trans, proj, filename)
                        self.head = tNode
                        tNode.next = CurrentNode
                        self.Length += 1
        else:
            assert 0, 'LinkList insert func is empty!'


    def delete(self,index):

        if self.is_empty() or index<0 or index >= self.getlength():
            print 'delete error, index is not correct.'
            return

        CurrentNode = self.head
        tindex = 1
        for tindex in range(index):
            CurrentNode = CurrentNode.next

        DeleteNode = CurrentNode.next
        NextNode = DeleteNode.next

        CurrentNode.next = NextNode


    def index(self, eng, lang, trans, proj, filename):

        if self.is_empty():
            print 'Linklist is empty.'
            return

        CurrentNode = self.head
        tindex = 0
        for tindex in range(self.getlength()):
            CurrentNode = CurrentNode.next
            if CurrentNode.eng == eng and CurrentNode.lang == lang and CurrentNode.trans == trans and CurrentNode.proj == proj and CurrentNode.filename == filename:
                return tindex


LL = LinkList()

LL.insert('DVB Select type', '#French', 'Sélection du type DVB', '3463', 'Mstar_DVB.xls')
LL.insert('DVB1 Select type', '#French', 'Sélection du type DVB', '3463', 'Mstar_DVB.xls')
LL.insert('DVB2 Select type', '#French', 'Sélection du type DVB', '3463', 'Mstar_DVB.xls')
LL.insert('DVB3 Select type', '#French', 'Sélection du type DVB', '3463', 'Mstar_DVB.xls')

print LL.getitem(0)
print LL.getitem(LL.getlength())
print LL.getitem(1)

LL.delete(2)
print LL.getitem(2)