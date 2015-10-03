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