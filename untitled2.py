#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 13:25:25 2018

@author: sachin
"""

from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import pymysql
mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
hostName        = "127.0.0.1"

userName        = "root"

userPassword    = "sachin123"

databaseName    = "BucketList"

databaseCharset = "utf8mb4"

cusrorType      = pymysql.cursors.DictCursor

 

databaseConnection   = pymysql.connect(host=hostName,

                                       user=userName,

                                       password=userPassword,

                                       db=databaseName,

                                       charset=databaseCharset,

                                       cursorclass=cusrorType)
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            cursorObject    = databaseConnection.cursor()                                    
            cursorObject.execute("call Top10Students('name')")
            _hashed_password = generate_password_hash(_password)
            data = cursorObject.fetchall()
 #           conn = mysql.connect()
 #           cursor = conn.cursor()
            
#            cursor.callproc('sp_createUser_new',(_name,_email,_hashed_password))
            

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursorObject.close() 
        conn.close()

if __name__ == "__main__":
    app.run(port=5007)