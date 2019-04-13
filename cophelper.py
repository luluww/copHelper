# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 21:44:49 2019

@author: wanda
"""

import mysql.connector

mydb=mysql.connector.connect(
        host='localhost',
        user='lucy',
        password='123',
        database='test1')

mycursor=mydb.cursor()

mycursor.execute(
        "create table suspects(sus_no int(11) not null auto_increment,"
        "first_name varchar(14) not null,"
        "last_name varchar(16) not null,"
        "gender enum('M','F') not null,"
         "birth_date  date not null,"
         "street_no int(10) not null,"
         "street_name varchar(20) not null)"
        "primary key (sus_no)")

