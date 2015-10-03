#!/usr/bin/python

# -*- coding: utf-8 -*-

import sqlite3 as lite
import csv


#Create database connection
con = lite.connect('employees.db')

#Create file handle for logging and open.
f = open("logs.txt", 'w')

#Use database connection to iterate.
with con:
    cur = con.cursor()

    #Drops temp table if exists.
    cur.execute("DROP TABLE IF EXISTS temp;")

    #Needs to correlate index numbers.  Revisit as needed.
    cur.execute("CREATE TABLE temp (idnum INTEGER, givenName, sn, username, mail);") #Create table for sorting
    cur.execute("CREATE INDEX s_index on temp (idnum);") #Create index based on id_number
    cur.execute("CREATE INDEX IF NOT EXISTS e_index on employees (idnum);") #Create an index (dictionary) for fast sort in employee table

    with open('input.csv','rb') as fin:
        dr = csv.DictReader(fin, fieldnames=("idnum", "givenName", "sn", "username", "mail")) # comma is default delimiter
        to_db = [(i["idnum"], i["givenName"], i["sn"], i["username"], i["mail"]) for i in dr] #create assoc-array to send to database

    #Insert the records to the temp table from the CSV
    cur.executemany("INSERT INTO temp (idnum, givenName, sn, username, mail) VALUES (?, ?, ?, ?, ?);", to_db)
    con.commit() #Close transacation

    #Return all employee records from SQLite to cur obj.
    cur.execute("SELECT * FROM employees")

    #Create rows object to iterate over.
    rows = cur.fetchall() #Return all records from the employee table

    for row in rows:
        cur.execute("SELECT * FROM temp WHERE idnum = " + str(row[0]) + ";") #Comparing idnum to string, returning mathing row
        try:
            cur.fetchall()[0] # Try to return pk
        except:
            cur.execute("DELETE from employees WHERE idnum = " + str(row[0]) + ";") #If no match, generate exception drop record
            f.write("DELETED row with idnum = " + str(row[0]) + " from employees\n") #Log deletion
            f.flush() #Save and Close file

    con.commit() #Commits transactions to database

    #Return all records from temp database
    cur.execute("SELECT * FROM temp")
    rows = cur.fetchall()

    #Inserting new records
    count = 0
    for row in rows:
        count += 1
        error = False
        for i in range(5):
            if not row[i] and row[i] != 0: #Checks to see if range is not empty
                f.write("Malformed row at line " + str(count) + " in input.csv\n")
                print "Malformed row at line " + str(count) + " in input.csv"
                error = True
                break
        if not error: #If not malformed contine
            cur.execute("SELECT * FROM employees WHERE idnum = " + str(row[0]) + ";") #attempt match on exisitng employee
            try:
                cur.fetchall()[0]
            except:
                cur.execute("INSERT INTO employees VALUES (?, ?, ?, ?, ?);", row) #Consider entry new insert record
                f.write("INSERTED row with idnum = " + str(row[0]) + " to employees\n")
                f.flush()

    cur.execute("DROP TABLE IF EXISTS temp;") #Drop temp table
    con.commit() #Commit any transactions to database

