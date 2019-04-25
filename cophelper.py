# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 21:44:49 2019

@author: wanda
"""

import sqlite3
import datetime
from mynetwork import myNetwork

#read csv file to get network dictionary
myFile='network.txt'
myDict={}

try:
    with open(myFile,'r') as f:
        for line in f:
            dict_key,*dict_value=line.split()
            myDict[dict_key]=dict_value
except:
    print('Create a new file')    
finally:
    network=myNetwork(myDict)
    

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
                                     primary key (sus_no),
                                     foreign key(case_no) references cases(case_no))''')

cur.execute('''create table if not exists experiences(exp_no integer auto_increment,
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
    return sus_no,first_name,last_name,gender,birth_date,street_name,street_no

def getExperience():
    sus_no=input("Suspect number: ")
    start_date=input("Start date(YYYY-MM-DD): ")
    end_date=input("End date(YYYY-MM-DD): ")
    location=input("Location: ")
    return sus_no,start_date,end_date,location

def getExperienceWithSusNo():
    start_date=input("Start date(YYYY-MM-DD): ")
    end_date=input("End date(YYYY-MM-DD): ")
    location=input("Location: ")
    return start_date,end_date,location

def print_menu():
    print(30* '*', "Menu",30*'*')
    print("Enter Case Information: 1")
    print("Enter Suspect Information: 2")
    print("Enter Suspect Experience: 3")
    print("Check if two suspects are connected: 4")
    print("Print connection network: 5")
    print("Exit: 6")
    print(70*'*')
    
#get suspect experience from database in the type of list
def get_experience_from_db(sus_no):
    sus_exp=[]
    cur.execute('''select * from experiences where sus_no=?''',(sus_no,))
    all_records=cur.fetchall()
    for record in all_records:
        #get start date, end date, and location
        sus_exp.append([record[2],record[3],record[4]])
    return sus_exp

def add_suspect():
    #get suspect information from cop
    sus_no,first_name,last_name,gender,birth_date,street_name,street_no,case_no=getSuspectInfo()
    #enter basic information into database
    cur.execute('''insert into suspects(sus_no,first_name,last_name,gender,birth_date,street_name,street_no) values(?,?,?,?,?,?,?)''',(sus_no,first_name,last_name,gender,birth_date,street_name,street_no,case_no))
    conn.commit()
    #ask cop to enter suspect experience
    choice=input("Enter suspect experience: y/n ")
    if choice=='y':
        loop=1
        while loop:
            cur.execute('''insert into experiences(sus_no,start_date,end_date,location) values(?,?,?,?)''',(sus_no,getExperienceWithSusNo())) 
            conn.commit()
            loop=input("Continue entering experience? Yes-1, No-0 :")
    
#    network.add_node(sus_no)
#   
#    #compare suspect experience with all suspects in the database, if two are connected, add relation into our network
#    sus1_exp=get_experience_from_db(sus_no)
#    for sus in network.nodes():
#        if sus!=sus_no:
#            sus2_exp=get_experience_from_db(sus)
#            if work_together(sus1_exp,sus2_exp):
#                network.add_relation({sus,sus_no})
#                print(network.return_Dict())
                
def work_together(sus_no1,sus_no2):
    exp1=get_experience_from_db(sus_no1)
    exp2=get_experience_from_db(sus_no2)
    for e1 in exp1:
        for e2 in exp2:
            if e1[2]==e2[2]:
                if time_overlap(strToDate(e1[0]),strToDate(e1[1]),strToDate(e2[0]),strToDate(e2[1])):
                    return True
    return False

def get_suspect_address(sus_no):
    cur.execute('''select street_name,street_no from suspects where sus_no=?''',(sus_no,))
    street_name,street_no=cur.fetchone()
    return street_name,street_no

def are_neighbours(sus_no1,sus_no2):
    street_name1,street_no1=get_suspect_address(sus_no1)
    street_name2,street_no2=get_suspect_address(sus_no2)
    if street_name1==street_name2:
        if abs(street_no1-street_no2)<=5:
            return True
    return False
    
def are_acquaintances(sus_no1,sus_no2):
    #if two suspects work together
    if work_together(sus_no1,sus_no2):
        return True
    #if two suspects are neighbours(same street, difference of street numbers is less than 5)
    if are_neighbours(sus_no1,sus_no2):
        return True
    #if two suspects have common friend
                
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
            try:
                cur.execute('''insert into cases(case_no,case_name) values(?,?)''',(getCaseInfo()))
                conn.commit()
            except:
                print("Wrong info, try again")
        elif choice==2:
            try:
                add_suspect()
            except:
                print("Wrong info, try again")   
        elif choice==3:
            try:
                cur.execute('''insert into experiences(sus_no,start_date,end_date,location) values(?,?,?,?)''',(getExperience()))
                conn.commit()
            except:
                print("Wrong info, try again")
        elif choice==4:
            print('xxx')
        elif choice==5:
            print("x")
        elif choice==6:
            loop=False
        
    

if __name__=='__main__':
    main_menu()
    #save network dictionary into csv file
    myDict=network.return_Dict()
    print(myDict)
    with open(myFile,'w') as f:
        line=''
        for k in myDict:
            line+=k+' '
            for element in myDict[k]:
                line+=element+' '
            line+='\n'
            f.write(line)
            line=''
    conn.close()

