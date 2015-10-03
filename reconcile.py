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
        to_db = [(i["idnum"], i["givenName"], i["sn"], i["username"], i["mail"]) for i in dr] #create array to send to database

    #Insert the records to the temp table from the CSV
    cur.executemany("INSERT INTO temp (idnum, givenName, sn, username, mail) VALUES (?, ?, ?, ?, ?);", to_db)
    con.commit() #Clost transacation
