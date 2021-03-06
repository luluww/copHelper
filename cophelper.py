# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 21:44:49 2019

@author: wanda
"""

import sqlite3
import datetime
from mynetwork import myNetwork
from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt


#read csv file to get network dictionary
myFile='network.txt'
network=myNetwork()
    
#create database
conn=sqlite3.connect('copdb.sqlite')
cur=conn.cursor()

#cur.execute('''create table if not exists cases(case_no varchar(20) not null,
#               case_name varchar(50),
#               primary key(case_no)
#               )''')

cur.execute('''create table if not exists suspects(sus_no varchar(20) not null,
                                     first_name varchar(50) not null,
                                     last_name varchar(50) not null,
                                     gender varchar(10),
                                     birth_date varchar(10) not null,
                                     street_name varchar(50) not null,
                                     street_no integer not null,
                                     primary key (sus_no))''')

cur.execute('''create table if not exists experiences(exp_no integer not null,
                                        sus_no varchar(20) not null,
                                        start_date varchar(10) not null,
                                        end_date varchar(10) not null,
                                        location varchar(50) not null,
                                        primary key (exp_no),
                                        foreign key (sus_no) references suspects(sus_no))''')

def read_network_file():
    myDict={}
    try:
        with open(myFile,'r') as f:
            for line in f:
                dict_key,*dict_value=line.split()
                myDict[dict_key]=dict_value
    except:
        print('Create a new file')    
    return myDict


def str_to_date(s):
    [year,month,day]=[int(item) for item in s.split('-')]
    return datetime.date(year,month,day)

#def getCaseInfo():
#    case_no=input("Case number: ")
#    case_name=input("Case Name: ")
#    return case_no,case_name

def get_suspect_info():
    sus_no=input("Suspect no: ")
    first_name=input("First name: ")
    last_name=input("Last name: ")
    gender=input("Gender: ")
    birth_date=input("Date of birth(YYYY-MM-DD): ")
    street_name=input("Street name: ")
    street_no=input("Street number: ")
    return sus_no,first_name,last_name,gender,birth_date,street_name,street_no

def get_experience():
    exp_no=input("Experience No.: ")
    sus_no=input("Suspect number: ")
    start_date=input("Start date(YYYY-MM-DD): ")
    end_date=input("End date(YYYY-MM-DD): ")
    location=input("Location: ")
    return exp_no,sus_no,start_date,end_date,location

def get_experience_with_susno():
    exp_no=input("Experience No.: ")
    start_date=input("Start date(YYYY-MM-DD): ")
    end_date=input("End date(YYYY-MM-DD): ")
    location=input("Location: ")
    return exp_no,start_date,end_date,location

def print_menu():
    print(30* '*', "Menu",30*'*')
    print("Enter Suspect Information: 1")
    print("Enter Suspect Experience: 2")
    print("Check if two suspects are connected: 3")
    print("Print connection network: 4")
    print("Exit: 5")
    print(70*'*')
    
#get suspect experience from database in the type of list
def get_experience_from_db(sus_no):
    sus_exp=[]
    cur.execute('''select start_date,end_date,location from experiences where sus_no=?''',(sus_no,))
    all_records=cur.fetchall()
    for record in all_records:
        #get start date, end date, and location
        sus_exp.append([record[0],record[1],record[2]])
    return sus_exp

def add_suspect():
    #get suspect information from cop
    sus_no,first_name,last_name,gender,birth_date,street_name,street_no=get_suspect_info()
    #enter basic information into database
    cur.execute('''insert into suspects(sus_no,first_name,last_name,gender,birth_date,street_name,street_no) values(?,?,?,?,?,?,?)''',(sus_no,first_name,last_name,gender,birth_date,street_name,street_no))
    conn.commit()
    #ask cop to enter suspect experience
    choice=input("Enter suspect experience: y/n ")
    if choice=='y':
        add_experience(sus_no)
    
def add_experience(sus_no):
    loop=1
    while loop:
        exp_no,start_date,end_date,location=get_experience_with_susno()
        cur.execute('''insert into experiences(exp_no,sus_no,start_date,end_date,location) values(?,?,?,?,?)''',(exp_no,sus_no,start_date,end_date,location))
        conn.commit()
        loop=int(input("Continue entering experience? Yes-1, No-0 :"))
         
def add_experience_complete():
    loop=1
    while loop:
       cur.execute('''insert into experiences(exp_no,sus_no,start_date,end_date,location) values(?,?,?,?,?)''',(get_experience()))
       conn.commit()
       loop=int(input("Continue entering experience? Yes-1, No-0 :"))
       
#def work_together(sus_no1,sus_no2):
#    exp1=get_experience_from_db(sus_no1)
#    exp2=get_experience_from_db(sus_no2)
#    for e1 in exp1:
#        for e2 in exp2:
#            if e1[2]==e2[2]:
#                if time_overlap(strToDate(e1[0]),strToDate(e1[1]),strToDate(e2[0]),strToDate(e2[1])):
#                    return True
#    return False

def get_suspect_address(sus_no):
    cur.execute('''select street_name,street_no from suspects where sus_no=?''',(sus_no,))
    street_name,street_no=cur.fetchone()
    return street_name,street_no

def are_neighbours(twosus):
    sus1=list(twosus)[0]
    sus2=list(twosus)[1]
    street_name1,street_no1=get_suspect_address(sus1)
    street_name2,street_no2=get_suspect_address(sus2)
    if street_name1==street_name2:
        if abs(street_no1-street_no2)<=5:
            return True
    return False
    
def add_into_network():
    network.clear_all()
    #get info from database to create network
    #firstly get all suspects and add into network as nodes
    cur.execute('''select sus_no from suspects''')
    all_sus=cur.fetchall()
    #change tuple of tuple to list of list
    lst_sus=[]
    for sus in all_sus:
        lst_sus.append(list(sus)[0])
        
    for sus in lst_sus:
        network.add_node(sus)
    
    #secondly add relations (edges)
    #two ways to define if two nodes are connected
    #1: if they work together
    for sus in lst_sus:
        sus_exp=get_experience_from_db(sus)
        for exp in sus_exp:
            exp_location=exp[2]
            exp_start_date=exp[0]
            exp_end_date=exp[1]
            #check if there is a sus who has same location 
            cur.execute('''select sus_no,start_date,end_date from experiences where location=?''',(exp_location,))
            possible_sus=cur.fetchall()
            for possible in possible_sus:
                lst=list(possible)
                if lst[0]!=sus:
                    if time_overlap(exp_start_date,exp_end_date,lst[1],lst[2]):
                        if not network.if_in_relation({sus,lst[0]}):
                            network.add_relation({sus,lst[0]})
                            
                            
    #2: if two are neighbours
    for c in combinations(lst_sus,2):
        if not network.if_in_relation(c):
            if are_neighbours(c):
                network.add_relation(c)
                
    #write network info into txt file
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
    

def are_acquaintances(sus_no1,sus_no2):
    two_sus=set({sus_no1,sus_no2})
    #if they know directly
    if network.if_in_relation(two_sus):
        return True
    if network.if_share_friend(two_sus):
        return True
    return False

def check_two_suspects_acquaintances():
    add_into_network()
    sus_first_name1=input("Enter first suspect's first name:" )
    sus_last_name1=input("Enter first suspect's last name:" )
    sus_first_name2=input("Enter second suspect's first name:" )
    sus_last_name2=input("Enter second suspect's last name:" )
    try:
        cur.execute('''select sus_no from suspects where first_name=? and last_name=?''',(sus_first_name1,sus_last_name1))
        sus_no1=cur.fetchone()[0]
        cur.execute('''select sus_no from suspects where first_name=? and last_name=?''',(sus_first_name2,sus_last_name2))
        sus_no2=cur.fetchone()[0]
        if are_acquaintances(sus_no1,sus_no2):
            print("\n","#"*5,"They might know each other!","#"*5)
        else:
            print("\n","#"*5,"They might not know each other!","#"*5)
    except:
        print("Wrong info, try again")
                
def time_overlap(start_date1,end_date1,start_date2,end_date2):
    if start_date1>start_date2 and start_date1<end_date2:
        return True
    if start_date2>start_date1 and start_date2<end_date1:
        return True
    return False

def print_network():
    g=nx.Graph()
        
    add_into_network()
    net_dict=network.return_Dict()
        
    for k in net_dict:
        g.add_node(k)
    relations=network.generate_relations()
    for relation in relations:
        node1=relation.pop()
        node2=relation.pop()
        g.add_edge(node1,node2)
    nx.draw(g)
    plt.savefig('network.png')
    plt.show()
    
                
def main_menu():
    loop=True
    while loop:
        print_menu()
        choice=int(input("Enter your choice [1-5]: "))
        if choice==1:
            try:
                add_suspect()
            except:
                print("Wrong info, try again")   
        elif choice==2:
            try:
                add_experience_complete()
            except:
                print("Wrong info, try again")
        elif choice==3:
            check_two_suspects_acquaintances()
        elif choice==4:
            print_network()
        else:
            loop=False
        
    

if __name__=='__main__':
    main_menu()
    
    conn.close()

