#!/usr/bin/env python3

# script to create database

import os, json, time, subprocess

import db


def create_db():

	# create a back up of the existing database
	db_path = db.db_path()
	if os.path.isfile(db_path):
		backup_file_name = "db" + str(int(time.time())) +  ".db"
		backup_file_path = os.path.join(db.backup_folder(), backup_file_name)
		move_command = "mv {} {}".format(db_path, backup_file_path)
		subprocess.run(move_command, shell=True, check=True)
		print ("Backed up datbase at {}".format(backup_file_path))

	# create new database
	db.create_new()
	
	# import the structure
	tables = db.get_db_structure()["tables"]

	for table_info in tables:

		db.exec("create_table", table_info)

# 		CREATE TABLE contacts (
# 	contact_id INTEGER PRIMARY KEY,
# 	first_name TEXT NOT NULL,
# 	last_name TEXT NOT NULL,
# 	email TEXT NOT NULL UNIQUE,
# 	phone TEXT NOT NULL UNIQUE
# );




create_db()



