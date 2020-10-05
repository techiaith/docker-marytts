#!/bin/python3
# -*- coding:utf-8 -*-
import sys
import csv
import mysql.connector

mysql_host = sys.argv[1]
mysql_user = sys.argv[2]
mysql_password = sys.argv[3]
mysql_db = sys.argv[4]
locale = sys.argv[5]
selectedsentencestable = sys.argv[6]

connection = mysql.connector.connect(user=mysql_user,
                                     password=mysql_password,
                                     host=mysql_host,
                                     database=mysql_db)

fullsourcetablename = locale + "_" + selectedsentencestable + "_selectedSentences"
cursor = connection.cursor()

try:
    print ("Dropping " + fullsourcetablename)
    cursor.execute("DROP TABLE " + fullsourcetablename)
except:
    print (fullsourcetablename + " does not exist")

try:
    print ("Reseting selected flag in " + locale + "_dbselection")
    cursor.execute("UPDATE " + locale + "_dbselection set selected=0")
except:
    print (locale + "_dbselection does not exist")
