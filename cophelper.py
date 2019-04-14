# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 21:44:49 2019

@author: wanda
"""

import sqlite3
import datetime

#create database
conn=sqlite3.connect('copdb.sqlite')
cur=conn.cursor()

cur.execute('''create table if not exists cases(case_no varchar(20) not null,
               case_name varchar(50),
               primary key(case_no)
               )''')

cur.execute('''create table if not exists suspects(sus_no varchar(20) not null,
                                     first_name varchar(50) not null,
                                     last_name varchar(50) not null,
                                     gender varchar(10),
                                     birth_date varchar(10) not null,
                                     street_name varchar(50) not null,
                                     street_no integer not null,
                                     case_no varchar(20) not null,
                                     primary key (sus_no),
                                     foreign key(case_no) references cases(case_no))''')

cur.execute('''create table if not exists experiences(exp_no varchar(20) not null,
                                        sus_no varchar(20) not null,
                                        start_date varchar(10) not null,
                                        end_date varchar(10) not null,
                                        location varchar(50) not null,
                                        primary key (exp_no),
                                        foreign key (sus_no) references suspects(sus_no))''')

def strToDate(s):
    [year,month,day]=[int(item) for item in s.split('-')]
    return datetime.date(year,month,day)

def getCaseInfo():
    case_no=input("Case number: ")
    case_name=input("Case Name: ")
    return case_no,case_name

def getSuspectInfo():
    sus_no=input("Suspect no: ")
    first_name=input("First name: ")
    last_name=input("Last name: ")
    gender=input("Gender: ")
    birth_date=input("Date of birth(YYYY-MM-DD): ")
    street_name=input("Street name: ")
    street_no=input("Street number: ")
    case_no=input("Case number: ")
    return sus_no,first_name,last_name,gender,birth_date,street_name,street_no,case_no

def getExperience():
    exp_no=input("file number: ")
    sus_no=input("Suspect number: ")
    start_date=input("Start date: ")
    end_date=input("End date: ")
    location=input("Location: ")
    return exp_no,sus_no,start_date,end_date,location

def print_menu():
    print(30* '*', "Menu",30*'*')
    print("Enter Case Information: 1")
    print("Enter Suspect Information: 2")
    print("Enter Suspect Experience: 3")
    print("Check if two suspects are connected: 4")
    print("Exit: 5")
    print(70*'*')
    
def main_menu():
    loop=True
    while loop:
        print_menu()
        choice=int(input("Enter your choice [1-5]: "))
        if choice==1:
            case_no,case_name=getCaseInfo()
            cur.execute('''insert into cases(case_no,case_name) values(?,?)''',(case_no,case_name))
        elif choice==2:
            cur.execute('''insert into suspects(sus_no,first_name,last_name,gender,birth_date,street_name,street_no,case_no) values(?,?,?,?,?,?,?,?)''',(getSuspectInfo()))
        elif choice==3:
            cur.execute('''insert into experiences(exp_no,sus_no,start_date,end_date,location) values(?,?,?,?,?)''',(getExperience()))
        elif choice==4:
            print("Do nothing")
        elif choice==5:
            loop=False
        conn.commit()
    

if __name__=='__main__':
    main_menu()
    conn.close()

