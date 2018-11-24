# from flask import Flask, jsonify, request, Response
# import json

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://PKASHYAP02PC/Credentials'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#LOCAL_DATABASE_URI = 'mssql+pyodbc://ffdam_services:6HQwAN9Zobxvn97s@ffdamsql-prod.prod.factset.com/ffdam?driver=ODBC+Driver+11+for+SQL+Server&MultiSubnetFailover=Yes'
LOCAL_DATABASE_URI = r'mssql+pyodbc://PKASHYAP02PC\\SQLEXPRESS/Credentials?trusted_connection=yes&driver=ODBC+Driver+11+for+SQL+Server'