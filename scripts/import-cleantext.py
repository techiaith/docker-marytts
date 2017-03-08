#!/bin/python3
import sys
import mysql.connector

mysql_host = sys.argv[1]
mysql_user = sys.argv[2]
mysql_password = sys.argv[3]
mysql_db = sys.argv[4]
locale = sys.argv[5]
infile = sys.argv[6]

connection = mysql.connector.connect(user=mysql_user,
                                         password=mysql_password,
                                         host=mysql_host,
                                         database=mysql_db)

cursor = connection.cursor()
insertsql = "INSERT INTO " + locale + "_cleanText" + " (page_id, text_id, processed, cleanText) VALUES (%s, %s, %s, %s)"
text_id = int(1)
page_id = int(1)
text_per_page = int(1000)

with open(infile, 'r', encoding='utf-8') as in_file:
    for line in in_file.readlines():
        print (page_id, text_id, line.rstrip())
        cursor.execute(insertsql, (page_id, text_id, 0, line.rstrip()))
        connection.commit()
        if text_id % text_per_page == 0:
            page_id += 1

        text_id += 1
