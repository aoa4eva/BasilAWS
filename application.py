import os
import psycopg2
from flask import Flask
from flask import render_template
from flask import request 
from flask import session 
from flask import url_for, redirect, escape
application = Flask(__name__)
application.secret_key = 'super secret key'
application.config['SESSION_TYPE'] = 'filesystem'

@application.route("/")
def hello():
    return "Hello World!"

@application.route("/basil")
def showIndex():
	return render_template('index.html')

@application.route("/connect")
def showadded():
	return render_template('connect.html')

@application.route("/addstuff", methods=['POST'])
def addStuff():

	session['databasename'] = request.form['dbname']
	session['host'] = request.form['hostname']
	session['user'] = request.form['username']
	session['password'] = request.form['password']
	session['port'] = request.form['port']
	connektBasilR()
	return render_template("showtables.html")

@application.route("/test")
def testHTML():
    return render_template('test.html')

@application.route("/showtables")
def showTables():
	connektBasilR()
	return render_template('showtables.html')

@application.route("/showdata", methods=['POST'])
def showData():
	session['chosentable']=request.form['chosentable']
	connektBasil(request.form['chosentable'])
	return render_template("basetemplatecopy.html")

def connektBasilR():
	mydatabase = session['databasename']
	myuser = session['user'] 
	mypassword = session['password'] 
	myhost = session['host']
	myport = session['port']

	theList = []

	try:
	    conn = psycopg2.connect(database=mydatabase, user=myuser, password=mypassword, host=myhost, port=myport)
	except:
	    return "Unable to connect to the database" 

	cursor = conn.cursor()
	cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
	alltables = cursor.fetchall()

	for table in alltables:
	    stripped = "%s" % table
	    theList.applicationend(stripped)
 
	cursor.close()	    	    
	session['alltables']=theList



def connektBasil(tablename):
	mydatabase = session['databasename']
	myuser = session['user'] 
	mypassword = session['password'] 
	myhost = session['host']
	myport = session['port']

	theList = []

	try:
	    conn = psycopg2.connect(database=mydatabase, user=myuser, password=mypassword, host=myhost, port=myport)
	except:
	    return "Unable to connect to the database" 
	cursor = conn.cursor()
	cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
	alltables = cursor.fetchall()
	table = tablename

	for oneTable in alltables:
  		theList.applicationend(oneTable)
  	
  	showsql="select * from "+table
	cursor.execute(showsql)
	colnames = [desc[0] for desc in cursor.description]
	values = cursor.fetchall()

	cursor.close()	    	    
	session['alltables']=theList
	session['colnames']=colnames
	session['values']=values

