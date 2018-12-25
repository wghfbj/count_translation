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

class Node(object): #object表示继承object类
    def __init__(self, eng, lang, trans, proj, filename):
        self.eng = eng #英语
        self.lang = lang #翻译为什么语言
        self.trans = trans #翻译
        self.proj = proj  #方案名称
        self.filename = filename  #文件名
        self.time = 1 #出现次数
        self.next = 0

    def show(self):
        print self.eng + " + " + self.lang + " + " + self.trans + " + " + self.proj + " + " + self.filename + " + " + str(self.time)

class LinkList(object):
    def __init__(self):
        self.head = Node("", "", "", "", "")
        self.Length = 0

    def __getitem__(self, key):

        if self.Linklist_is_empty():
            print 'linklist is empty.'
            return

        elif key <0  or key > self.Linklist_getlength():
            print 'the given key is error'
            return

        else:
            return self.Linklist_getitem(key)



    def __setitem__(self, key, value):

        if self.Linklist_is_empty():
            print 'linklist is empty.'
            return

        elif key <0  or key > self.Linklist_getlength():
            print 'the given key is error'
            return

        else:
            self.Linklist_delete(key)
            return self.Linklist_insert(key)

    def Linklist_getlength(self):

        return self.Length

    def Linklist_is_empty(self):

        if self.Linklist_getlength() == 0:
            return True
        else:
            return False

    def Linklist_clear(self):

        self.head = 0
        self.Length = 0


    def Linklist_getitem(self,index): # Start at index 0

        if self.Linklist_is_empty():
            print 'Linklist is empty.'
            return
        if index >= self.Linklist_getlength():
            print 'getitem error, index is not correct.'
            return

        CurrentNode = self.head.next
        tindex = 0
        for tindex in range(index):
            CurrentNode = CurrentNode.next
        return CurrentNode

    def Linklist_insert(self, eng, lang, trans, proj, filename, index=0): # Start at index 0

        if index<0:
            print 'insert error, index is not correct.'
            return

        if index == 0:
            CurrentNode = self.head
            if self.Linklist_getlength() == 0:
                tNode = Node(eng, lang, trans, proj, filename);
                CurrentNode.next = tNode
                tNode.next = 0
                self.Length += 1
            else:
                tindex = 0
                for tindex in range(self.Linklist_getlength()):
                    CheckNode = self.Linklist_getitem(tindex)
                    if CheckNode.eng == eng and CheckNode.lang == lang and CheckNode.trans == trans:
                        CheckNode.time += 1
                        return
                tNode = Node(eng, lang, trans, proj, filename)
                NextNode = CurrentNode.next
                CurrentNode.next = tNode
                tNode.next = NextNode
                self.Length += 1
        else:
            assert 0, 'LinkList insert func is empty!'


    def Linklist_delete(self,index):

        if self.Linklist_is_empty() or index<0 or index >= self.Linklist_getlength():
            print 'delete error, index is not correct.'
            return

        CurrentNode = self.head
        tindex = 1
        for tindex in range(index):
            CurrentNode = CurrentNode.next

        DeleteNode = CurrentNode.next
        NextNode = DeleteNode.next

        CurrentNode.next = NextNode
        self.Length -= 1


    def Linklist_index(self, eng, lang, trans, proj, filename):

        if self.is_empty():
            print 'Linklist is empty.'
            return

        CurrentNode = self.head
        tindex = 0
        for tindex in range(self.Linklist_getlength()):
            CurrentNode = CurrentNode.next
            if CurrentNode.eng == eng and CurrentNode.lang == lang and CurrentNode.trans == trans and CurrentNode.proj == proj and CurrentNode.filename == filename:
                return tindex

    def Linklist_show(self):

        tindex = 0
        CurrentNode = self.head
        for tindex in range(self.Linklist_getlength()):
            CurrentNode = CurrentNode.next
            print CurrentNode.eng + " + " + CurrentNode.lang + " + " + CurrentNode.trans + " + " + CurrentNode.proj + " + " + CurrentNode.filename + " + " + str(CurrentNode.time)


# LL = LinkList()

# LL.Linklist_insert('DVB Select type', '#French', 'Sélection du type DVB', '3463', 'Mstar_DVB.xls')
# LL.Linklist_insert('DVB Select type', '#French', 'Sélection du type DVB', '3463', 'Mstar_DVB.xls')
# LL.Linklist_insert('DVB Select type', '#French', 'Sélection du type DVB', '3463', 'Mstar_DVB.xls')
# LL.Linklist_insert('DVB1 Select type', '#French', 'Sélection du type DVB', '3463', 'Mstar_DVB.xls')
# LL.Linklist_insert('DVB2 Select type', '#French', 'Sélection du type DVB', '3463', 'Mstar_DVB.xls')
# LL.Linklist_insert('DVB3 Select type', '#French', 'Sélection du type DVB', '3463', 'Mstar_DVB.xls')
# LL.Linklist_insert('DVB4 Select type', '#French', 'Sélection du type DVB', '3463', 'Mstar_DVB.xls')

# print LL.Linklist_getlength()
# LL.Linklist_show()

# LL.Linklist_delete(2)
# print LL.Linklist_getlength()
# LL.Linklist_show()