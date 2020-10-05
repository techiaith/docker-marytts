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

import cld3

outfile = sys.argv[7]

connection = mysql.connector.connect(user=mysql_user,
                                     password=mysql_password,
                                     host=mysql_host,
                                     database=mysql_db)

fullsourcetablename = locale + "_" + selectedsentencestable + "_selectedSentences"
cursor = connection.cursor()
cursor.execute("SELECT * FROM " + fullsourcetablename)

ext = Path(outfile).suffix

outfile_cy = open(outfile.replace(ext, ".cy" + ext), 'w', encoding='utf-8')
outfile_en = open(outfile.replace(ext, ".en" + ext), 'w', encoding='utf-8')

with open(outfile, 'w', encoding='utf-8') as out_file:
    for row in cursor:
        text = row[1].decode('utf-8')
        out_file.write(text + '\n')
        lang_detect = cld3.get_language(text)
        if (lang_detect.language == "cy"):
            outfile_cy.write(text + '\n')
        elif (lang_detect.language == "en"):
            outfile_en.write(text +'\n')

outfile_cy.close()
outfile_en.close()
