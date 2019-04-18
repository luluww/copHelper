# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 21:44:49 2019

@author: wanda
"""

import sqlite3
import datetime
from mynetwork import myNetwork5
import csv

#read csv file to get network dictionary
network=myNetwork()

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

nets={}

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
    
#get suspect experience from database in the type of list
def get_experience_from_db(sus_no):
    sus_exp=[]
    cur.execute('''select * from experiences where sus_no==?''',(sus_no))
    all_records=cur.fetchall()
    for record in all_records:
        #get start date, end date, and location
        sus_exp.append([record[2],record[3],record[4]])
    return sus_exp

def add_suspect_into_network():
    #get suspect information from cop
    sus_no,first_name,last_name,gender,birth_date,street_name,street_no,case_no=getSuspectInfo()
    #enter basic information into database
    cur.execute('''insert into suspects(sus_no,first_name,last_name,gender,birth_date,street_name,street_no,case_no) values(?,?,?,?,?,?,?,?)''',(sus_no,first_name,last_name,gender,birth_date,street_name,street_no,case_no))
    #ask cop to enter suspect experience
    choice=input("Enter suspect experience: y/n")
    if choice=='y':
       cur.execute('''insert into experiences(exp_no,sus_no,start_date,end_date,location) values(?,?,?,?,?)''',(getExperience())) 
    network.add_node(sus_no)
    #compare suspect experience with all suspects in the database, if two are connected, add relation into our network
    sus1_exp=get_experience_from_db(sus_no)
    for sus in network().nodes():
        if sus!=sus_no:
            sus2_exp=get_experience_from_db(sus)
            if are_acquaintances(sus1_exp,sus2_exp):
                network().add_relation({sus,sus_no})
                
def are_acquaintances(exp1,exp2):
    for e1 in exp1:
        for e2 in exp2:
            if e1[2]==e2[2]:
                if time_overlap(strToDate(e1[0]),strToDate(e1[1]),strToDate(e2[0]),strToDate(e2[1])):
                    return True
    return False
                
def time_overlap(start_date1,end_date1,start_date2,end_date2):
    if start_date1>start_date2 and start_date1<end_date2:
        return True
    if start_date2>start_date1 and start_date2<end_date1:
        return True
    return False
                
def main_menu():
    loop=True
    while loop:
        print_menu()
        choice=int(input("Enter your choice [1-5]: "))
        if choice==1:
            cur.execute('''insert into cases(case_no,case_name) values(?,?)''',(getCaseInfo()))
        elif choice==2:
            add_suspect_into_network()
        elif choice==3:
            print("Do nothing")
        elif choice==4:
            loop=False
        conn.commit()
    

if __name__=='__main__':
    main_menu()
    #save network dictionary into csv file
    conn.close()

