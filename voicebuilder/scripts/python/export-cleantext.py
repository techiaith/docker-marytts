#!/bin/python3
# -*- coding:utf-8 -*-
import os
import sys
import csv
import mysql.connector

mysql_host = sys.argv[1]
mysql_user = sys.argv[2]
mysql_password = sys.argv[3]
mysql_db = sys.argv[4]
locale = sys.argv[5]
selectedsentencestable = sys.argv[6]

outfile = sys.argv[7]

connection = mysql.connector.connect(user=mysql_user,
                                     password=mysql_password,
                                     host=mysql_host,
                                     database=mysql_db)

fullsourcetablename = locale + "_" + selectedsentencestable + "_selectedSentences"
cursor = connection.cursor()
cursor.execute("SELECT * FROM " + fullsourcetablename)

with open(outfile, 'w', encoding='utf-8') as out_file:

    if outfile.endswith('.csv'):
        csv_writer = csv.writer(out_file, delimiter='|')
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
    elif outfile.endswith('.txt'):
        for row in cursor:
            out_file.write(row[1].decode('utf-8') + '\n')
    elif outfile.endswith('.py'):
        out_file.write("""
#!/usr/bin/env python 
# #encoding: UTF-8 
# PROMPTS = [    
""")
        sample_id = 1
        for row in cursor:
            text = row[1].decode('utf-8')
            if not any(i.isdigit() for i in text):
                if len(text) < 90:
                    # tidy up
                    text = text.upper()
                    text = text.replace('?', '')
                    text = text.replace(',', '')
                    text = text.replace('.', '')
                    text = text.replace(':', '')
                    out_file.write("    {\"identifier\": \"sample" + str(sample_id) + "\"" \
                                   ", \"text\": u\"" + text + "\"},\n")
                    sample_id += 1

        out_file.write("]")

out_file.close()
