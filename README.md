# Operations Test

## Background

The file input.csv contains example employee records from an ERP system, which
is the authoritative source of employee data.  The file students.db is a SQLite
database that contains a set of employee records.  The database needs to be
reconciled with the input from the ERP.


## Requirements

Write a program that efficiently updates employees.db, such that the data in the
database accurately reflects the data changes in input.csv.  Any records present
in input.csv that are missing from the database should be inserted, and any
extra records not in the database should be removed. All records should be keyed
on ID number. It is not necessary to update any records with changed attributes.
All attributes are required, and any record with missing or empty fields should
be considered malformed. Malformed records should generate an exception, but
should not halt the task. All updates should be logged to an easily parsed log
file.


## Language choice

Any language may be chosen that can be easily executed from source without
manual compilation. These languages are sometimes called "interpreted"
languages, though the term is imprecise. Python, Ruby, Bash, Powershell, and
Haskell would all be good examples of interpreted languages by this definition.
There are many others. Java, C#, and C are languages where programs are
typically compiled by the programmer prior to execution, and therefore should be
avoided. Inlining code from a compiled language is allowed only if it is done
for a specific reason. If the program is submitted as a binary or needs to be
compiled prior to running, then it will be disqualified.


## Deliverables

Fork this repository on Github and create a new branch containing your solution.
Solutions must be submitted by creating a pull request back into this repository.
