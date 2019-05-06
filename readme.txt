Cop Helper

I like watch detective stories and films very much. One day, I was watching a detective show, suddenly an idea came into my head: to create an app to check if two peoples know each other.

Use a database to store Personal information, like he or she works at xxx company from xxxx to xxxx.
Use python to check if any overlap blablabla

2019-4-12
- create readme.txt
- create cophelper.py
	- try to create database by python
		- install mysql-connector-python
		- install flake

problem: can't not build localhost

2019-4-13
- decide to use sqlite to do database part
- create sqlite database files
- create database and tables in py file
- create interactive menu to enter data
so far so good

2019-4-15
to-do-list:
- relation graph
- check if two nodes connect

2019-4-17
- add myNetwork file to create mynetwork class for relationship network
- modified cophelper file to add network
- to be done: 
	- read/write network dictionary into csv file
	- add more data to check functions

2019-4-23
- add read/write file
- insert data to test
- more details to finish
	- id already exists ?
	- check if two suspects know each other?
	- repeat inserting suspect experiences ?
	- if two suspects live in same street, they might know each other

2019-4-24
- change an attribute to auto_increment
- add exceptions
- add repeating entering experiences option
- add function to check two suspects are acquaintances 
- To do list:
	- finish the function to check if two suspects have common friend
	- add function to input all relationships into dict for network
	- import networkx to draw relationship graph

2019-4-27
- finish all codes but not test yet

2019-4-28
- remove one unnecessary table
- fix type error 
- fix graph
- mostly done

2019-5-5
to-do-list:
- setup.py
- __init__.py
- requirements.txt
- peewee to replace sqlite
- add an attribute to describe two peoples' friendship, by example, if friendship=100, two peoples are best friends, if friendship=-100, they are enemies
- change object to dict