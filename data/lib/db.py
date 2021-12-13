#!/usr/bin/env python3

import os, json

import sqlite3

db_path = str()
resources_folder = str()




######################################################
# Misc Handlers
######################################################

def _path_parent(path):
	return os.path.dirname(path)

def db_path():
	return os.path.join(_path_parent(os.getcwd()), "data.db")


def backup_folder():
	return os.path.join(_path_parent(os.getcwd()), "backups")

def resources_folder():
	return os.path.join(_path_parent(os.getcwd()), "resources")

######################################################
# DB Structure loading
######################################################

def get_db_structure():
	structure_file = os.path.join(resources_folder(), "schema.json")
	with open(structure_file, "r") as structure_in:
		structure = json.load(structure_in)

	return structure


######################################################
# DB Transacation handlers
######################################################

# 
# class for any transaction to the database
#
class DB_Transaction():
	def __init__(self, path):
		self.path = path
		self.con = None
		self.cur = None
		self.sql = None
		self.req_type = None


	def _connect(self):
		self.con = sqlite3.connect(self.path) 
		self.cur = self.con.cursor()

	def _disconnect(self):
		if self.con != None:
			self.con.close()
		self._reset()

	def _reset(self):
		self.con = None
		self.cur = None
		self.sql = None
		self.req_type = None

	def _commit(self):
		self.con.commit()

	def _primary_key(self, name):
		return name + "_id"

	def create_new(self):
		self._connect()
		self._disconnect()


	def exec(self, exec_type, params):
		self._connect()
		parsed_params = self._parse_exec(exec_type, params)
		print (parsed_params)
		self.con.execute(parsed_params)
		self._commit()
		self._disconnect()

	def query(self, query_type, params):
		self._connect()
		results = self.con.execute(self._parse_query(query_type, params))

		self._disconnect()
		return results


	# request types documented wihin the _parse_req_type handl;er
	def _parse_exec(self, exec_type, params):
		print ("Parsing request of type {}".format(exec_type))
		if exec_type == "create_table":
			return self._parse_create_table(params)



	# parse params to get create table SQL
	# params in form loaded from resources/schema.json
	#
	# params dict of form 
	# name
	# columns :	array
		# name : column name
		# type : type
	# primary key 

	def _parse_create_table(self, params):
		
		name = params["name"]
		columns = params["columns"]
		primary_key = self._primary_key(name)

		# build columns create statement
		columns_create = "{} INTEGER PRIMARY KEY AUTOINCREMENT".format(primary_key)

		for i in range(len(columns)):
			column_name = columns[i]["name"]
			column_type = columns[i]["type"]

			columns_create += ", {} {}".format(column_name, column_type)

		return "CREATE TABLE {} ({});".format(name, columns_create)
		
		


	def _parse_query(self, query_type, params):
		pass


def exec(exec_type, params):
	print (params)
	db = DB_Transaction(db_path())
	db.exec(exec_type, params)

def query(query_type, params):
	db = DB_Transaction(db_path())
	return db.query(query_type, params)

def create_new():
	db = DB_Transaction(db_path())
	db.create_new()

