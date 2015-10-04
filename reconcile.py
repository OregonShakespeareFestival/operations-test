#!/usr/bin/python

# -*- coding: utf-8 -*-

import sqlite3
import csv


#Create database connection.
dbConnect = sqlite3.connect('employees.db')

#Create file handle for logging and open.
logFile = open("logs.txt", 'w')

#Use database connection to iterate.
with dbConnect:
    cursor = dbConnect.cursor()

    #Drops temp table if exists.
    cursor.execute("DROP TABLE IF EXISTS temp;")

    #Needs to correlate index numbers.  Revisit as needed.
    cursor.execute("CREATE TABLE temp (idnum INTEGER, givenName, sn, username, mail);") #Create table for sorting.
    cursor.execute("CREATE INDEX s_index on temp (idnum);") #Create index based on id_number.
    cursor.execute("CREATE INDEX IF NOT EXISTS e_index on employees (idnum);") #Create an index (dictionary) for fast sort in employee table.

    with open('input.csv','rb') as employeeFile:
        dictReader = csv.DictReader(employeeFile, fieldnames=("idnum", "givenName", "sn", "username", "mail")) #Comma is default delimiter.
        tempEmployeeCollection = [(i["idnum"], i["givenName"], i["sn"], i["username"], i["mail"]) for i in dictReader] #Create array to send to database.

    #Insert the records to the temp table from the CSV.
    cursor.executemany("INSERT INTO temp (idnum, givenName, sn, username, mail) VALUES (?, ?, ?, ?, ?);", tempEmployeeCollection)
    dbConnect.commit() #Close transacation.

    #Return all employee records from SQLite3 to cursor object.
    cursor.execute("SELECT * FROM employees")

    #Create rows object to iterate over.
    rows = cursor.fetchall() # Return all records from the employee table.

    for row in rows:
        cursor.execute("SELECT * FROM temp WHERE idnum = " + str(row[0]) + ";") #Comparing idnum to string. Return mathing row.
        try:
            cursor.fetchall()[0] #Try to return primary key.
        except:
            cursor.execute("DELETE from employees WHERE idnum = " + str(row[0]) + ";") #If no match, generate exception, drop record.
            logFile.write("DELETED row with idnum = " + str(row[0]) + " from employees\n") #Log deletion.
            logFile.flush() #Save and Close file.

    dbConnect.commit() #Commits transactions to database.

    #Return all records from temp database.
    cursor.execute("SELECT * FROM temp")
    rows = cursor.fetchall()

    #Inserting new records.
    count = 0
    for row in rows:
        count += 1
        error = False
        for i in range(5):
            if not row[i] and row[i] != 0: #Checks to see if range is not empty.
                logFile.write("Malformed row at line " + str(count) + " in input.csv\n")
                print "Malformed row at line " + str(count) + " in input.csv"
                error = True
                break
        if not error: #If not malformed continue.
            cursor.execute("SELECT * FROM employees WHERE idnum = " + str(row[0]) + ";") #Attempt match on exisitng employee.
            try:
                cursor.fetchall()[0]
            except:
                cursor.execute("INSERT INTO employees VALUES (?, ?, ?, ?, ?);", row) #Consider entry of new insert record.
                logFile.write("INSERTED row with idnum = " + str(row[0]) + " to employees\n")
                logFile.flush()

    cursor.execute("DROP TABLE IF EXISTS temp;") #Drop temporary table.
    dbConnect.commit() #Commit any transactions to database.

