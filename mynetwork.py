# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 20:46:44 2019

@author: wanda
"""
#This is my relation network
#node is suspect id
#relation means two nodes are connected, that is, they know each other


class myNetwork(object):
    def __init__(self,net_dict=None):
        if net_dict==None:
            net_dict={}
        self.__net_dict=net_dict
        
    def nodes(self):
        return list(self.__net_dict.keys())
    
    def relations(self):
        return self.__generate_relations()
    
    def add_node(self,node):
        if node not in self.__net_dict:
            self.__net_dict[node]=[]
            
    def add_relation(self, relation):
        #add a function to check if two peoples know each other
        relation=set(relation)
        node1=relation.pop()
        if relation:
            node2=relation.pop()
        else:
            node2=node1
        if node1 in self.__net_dict:
            self.__net_dict[node1].append(node2)
        else:
            self.__net_dict[node1]=[node2]
            
    def if_in_relation(self,relation):
        relation=set(relation)
        node1=relation.pop()
        node2=relation.pop()
        if node2 in self.__net_dict[node1]:
            return True
        return False
    
    def if_share_friend(self,two_sus):
        two_sus=set(two_sus)
        node1=two_sus.pop()
        node2=two_sus.pop()
        for friend in self.__net_dict[node1]:
            if friend in self.__net_dict[node2]:
                return True
        return False
            
    def generate_relations(self):
        relations=[]
        for node in self.__net_dict:
            for acquaintance  in self.__net_dict[node]:
                if {node, acquaintance} not in relations:
                    relations.append({node,acquaintance})
        return relations
    
#    #check if two suspects are connected
#    def find_path(self,sus1,sus2,path=[]):
#        net=self.__net_dict
#        path=path+[sus1]
#        if sus1==sus2:
#            return path
#        if sus1 not in graph:
#            return None
#        for sus in graph[sus1]:
#            if sus not in path:
#                extended_path=self.find_path(sus,sus2,path)
#                if extended_path:
#                    return extended_path
#        return None
    
    def return_Dict(self):
        return self.__net_dict
    
   
    
    
    
    