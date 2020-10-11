#!/bin/python3
# -*- coding:utf-8 -*-
import os
import sys
import csv

import mysql.connector

from pathlib import  Path

mysql_host = sys.argv[1]
mysql_user = sys.argv[2]
mysql_password = sys.argv[3]
mysql_db = sys.argv[4]
locale = sys.argv[5]
selectedsentencestable = sys.argv[6]
outfile = sys.argv[7]


def new_cursor():
    connection = mysql.connector.connect(user=mysql_user,
                                         password=mysql_password,
                                         host=mysql_host,
                                         database=mysql_db)
    return connection, connection.cursor()


#
connection, cursor = new_cursor()
id_connection, id_cursor = new_cursor()
del_connection, del_cursor = new_cursor()

fullsourcetablename = locale + "_" + selectedsentencestable + "_selectedSentences"
cursor.execute("SELECT * FROM " + fullsourcetablename)

#
with open(outfile, 'w', encoding='utf-8') as out_file:
    for row in cursor:
        text = row[1].decode('utf-8')        
        out_file.write(text + '\n')

        # delete from cleanText
        id_cursor.execute("SELECT cleanText_Id FROM " + locale + "_dbselection WHERE Id=" + str(row[3]))
        cleanText_Id = id_cursor.fetchone()
        del_cursor.execute("DELETE FROM " + locale + "_cleanText WHERE id=" + str(cleanText_Id[0]))
        del_connection.commit()
        
#
cursor.close()
connection.close()

id_cursor.close()
id_connection.close()

del_cursor.close()
del_connection.close()

#
drop_connection, drop_cursor = new_cursor()

drop_cursor.execute("DROP TABLE " + locale + "_dbselection")
drop_cursor.commit()

drop_cursor.execute("DROP TABLE " + fullsourcetablename)
drop_cursor.commit()

drop_cursor.execute("UPDATE " + locale + "_cleanText SET processed=0")
drop_cursor.commit()

drop_cursor.close()
drop_connection.close()
    