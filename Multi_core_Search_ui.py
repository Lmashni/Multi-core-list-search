#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 20:21:14 2021

@author: lyth
"""

import csv
import multiprocessing
import random
import string
from tkinter import *

#random.seed(1)
availabe_cores = multiprocessing.cpu_count() # this find out how many processors the system has

def generate(list_length=1000,string_length=5):
    """this funtion generates a list of random strings by appending
        to global parameter called word_list. The strings generated
        are made up from lower key english letters. 

    Parameters:
    list_length (int): Number of words in the list
    string_length (int): maximum length genrated strings

    Returns: none
    

   """
   
    global word_list  
    word_list =[]
    
    for j in range(int(list_length)):
        strn = ''
        
        for i in range(random.randint(1,int(string_length))):
            strn += random.choice(string.ascii_lowercase)
            
        word_list.append(strn)

def list_to_string(word_list):
    """ Converts a list to a string with like breaks
        for display purposes

    Parameters:
    word_list (python list(string)): list to convert

    Returns:
    strn (string): single string of words in input list with line breaks added

   """
    strn = ''
    
    for i in word_list:
        strn = strn + i+ '\n'
        
    return strn

def search(queue,tofind,word_list):
    """commpares given string to the initial characte wrs of
       of a given list and returns all words with matching 
       initial letters. It puts found words in an 
       multiprocessing.queues.Queue to send to cores.

    Parameters:
    queue (Queue): empty Queue from mp_search. Check Docs of multiprocessing.queues.Queue
    tofind(string): string to look for
    word_list(list(string)): list to look in
    
    Returns:
    none

   """
   
    found = {}
    
    for i in range(len(word_list)):
        
        if word_list[i][:len(tofind)] == tofind:
            found[i] = word_list[i]
            
    queue.put(found)

def mp_search(list_of_word,tofind, processes):
    
    """Takes care of spliting the search over processors. The list is
        is split up eveny over the number processors given to the function.
        each core applies the function search separetly. the matching words
        are returned as a single sting to be saved or printed.
        

    Parameters:
    list_of_words (list(string)): list to look in
    tofind (string): String to look for
    processes(int): number of processes to use

    Returns:
    string: single sting containg words found seperated by line breaks

   """
    
    queue = multiprocessing.Queue()
    chunks = int(len(list_of_word) / processes)
    
    procs = []
    for i in range(processes):
        proc = multiprocessing.Process(target=search, args=(queue,tofind ,list_of_word[chunks*i:chunks*(i+1)]))
        procs.append(proc)
        proc.start()
        
    results = []
    for i in range(processes):
        got = queue.get()
        results += list(got.values())
        
    for i in procs:
        i.join()
        
    return list_to_string(results)

def load_list(list_file):
    """converts csv to a python list to be used and packs them in gloabal variable
       word_list

    Parameters:
    list_file (.txt): csv file. can be of any number of (colsXrows)

    Returns:
    none

   """
    global word_list
    word_list = []
    
    with open(list_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = 0
        
        for row in csv_reader:
            
            if True:
                word_list = word_list + row
            row_count += 1
    
def search_button():
    global found_list
    T.delete(1.0,END)
    found_list = mp_search( word_list , E_look_up_word.get() , int(E_n_pocs.get())  )
    T.insert(END,found_list)
    
def save_list():
    global found_list
    text_file = open("found_list.txt", "wt")
    n = text_file.write(found_list)
    text_file.close()



root = Tk()

root.geometry('1200x700')

T = Text(root, font='helvetica')
T.grid(row=1,column=0)

###########  search frame #############
F = Frame(root)
F.grid(row=0,column=0)

L = Label(F, text = 'word to look up',font='times').grid(row=0,column=0)
E_look_up_word = Entry(F)
E_look_up_word.grid(row=0,column=1)

L2 = Label(F, text = f'Number of processor (max = {availabe_cores})',font='times').grid(row=1,column=0)
E_n_pocs = Entry(F)
E_n_pocs.grid(row=1,column=1)

B_search =  Button(F , text='search' ,command= search_button)
B_search.grid(row = 2, column = 0)

######### Load file #########
F2 = Frame(root)
F2.grid(row=0,column=1)

E_load = Entry(F2)
E_load.grid(row=3,column=1)
E_load.insert(0,'file path')

B_load =  Button(F2 , text='load list' ,command= lambda: load_list(E_load.get()))
B_load.grid(row = 3, column = 0)

B_save = Button(F2, text = 'save',command = save_list)
B_save.grid(row = 4 , column = 0)
###########  generation frame #############



L_word_number = Label(F2, text = 'how many word',font='times').grid(row=0,column=0)
E_word_number  = Entry(F2)
E_word_number.insert(0,'1000')
E_word_number .grid(row=0,column=1)

list_length = E_word_number.get()

L_word_length = Label(F2, text = 'max. length',font='times').grid(row=1,column=0)
E_word_length = Entry(F2)
E_word_length.insert(0,'5')
E_word_length.grid(row=1,column=1)

string_length = E_word_length.get()

B_generate =  Button(F2 , text='generate list' ,command= lambda: generate(list_length =E_word_number.get(), string_length = E_word_length.get()))
B_generate.grid(row = 2, column = 0)

############ found words #########
L = Label(F, text = 'word to look up',font='times').grid(row=0,column=0)


root.mainloop()











