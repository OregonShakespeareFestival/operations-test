# OSF Quiz v2
# Created and tested in IDLE 3.5

import csv
import sqlite3
import time
import sys

#Variables
csvfile = 'input.csv'
dbase = 'employees.db'
err = "error"

#Open the CSV
f = open(csvfile)
csv_f = csv.reader(f)

#Connect to the database
con = sqlite3.connect(dbase)
cur = con.cursor()

# Start the log file
log = open("logfile.txt", "a")
log.write("Database update starting: " + time.strftime("%c") + "\n")

# Find the last record in the database
cur.execute("SELECT max(idnum) FROM employees") 
last = cur.fetchone()[0]
print("This could take a while...")
# Loop to the new records in the CSV, check for t3h Malform, then insert them into the database 
for row in csv_f:
        current = row[0]
        if (last < int(current)) and (len(row) == 5):
                cur.execute("INSERT INTO employees VALUES (?,?,?,?,?)",row)
                con.commit()
                log.write("Inserted: " + row[0] + " " + row[1] + "\n")
        elif (last < int(current)):
                cur.execute("INSERT INTO employees VALUES (?,?,?,?,?)",(row[0],err,err,err,err))
                con.commit()
                log.write("ERROR: " + row[0] + "\n")
                                
# Bonus Round
# Parse the database for missing records                

log.write("Checking database for errors.. \n")

cur.execute("SELECT * FROM employees")

while True:
        error = ""
        row = cur.fetchone()
        if (row == None):
                break
        if (row[1]==""):
                error ="No givenName, "
        if (row[2]==""):
                error +="No sn, "
        if (row[3]==""):
                error +="No username, "
        if (row[4]==""):
                error +="No mail "
        if (error != ""):
                log.write(row[0] + ", " + error + "\n")
                
log.write("Check Complete " + time.strftime("%c") + "\n")                               
log.close()
con.close()
input('Results are in the logfile. Press ENTER to exit.')
