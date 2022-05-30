import time
from tkinter import *
import random
import urllib.request
import requests
import threading
import serial
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#Random Forest Algorithm
# Importing the dataset
dataset = pd.read_csv('Project.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

#Encoding Independent Variables
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct= ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

#Encoding Dependent Variables
from sklearn.preprocessing import LabelEncoder
l= LabelEncoder()
y= l.fit_transform(y)


# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)


#Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train[:,2:3] = sc.fit_transform(X_train[:,2:3])
X_test[:,2:3] = sc.transform(X_test[:,2:3])

# Training the Random Forest Classification model on the Training set
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

# creating the desktop application
class gui:
    def __init__(self, master,pulse,tempp,spo2):
        self.master=master
        self.label=Label(master, fg='red', font=("Helvetica", 25),pady=2)
        self.label1=Label(master, fg='red', font=("Helvetica", 25),pady=2)
        self.label2=Label(master, fg='red', font=("Helvetica", 25),pady=2)
       
        Label(master,text="Enter your age:", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 15)).pack()
        e1= Entry(master,width=20)
        e1.configure(font=("Helvetica", 15))
        e1.pack()
        Label(master,text="Enter your gender:", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 15)).pack()
        e2= Entry(master,width=20)
        e2.configure(font=("Helvetica", 15))
        e2.pack()
       
        Label(master,text="PulseRate", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 15)).place(x=20,y=120)
        Label(master,text="Oxygen Level", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 15)).place(x=310,y=120)
        Label(master,text="Temperature", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 15)).place(x=160,y=120)
        Label(master,text="Any problems you are having:", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 15)).place(x=120,y=240)

        self.label.place(x=80,y=150)
        self.label1.place(x=325,y=150)
        self.label2.place(x=200,y=150)
        self.pulse=pulse
        self.eeg=eeg
        self.tempp=tempp
        self.spo2=spo2
        self.label.configure(text='nothing',bg="#fff0b8")
        self.label1.configure(text='nothing',bg="#fff0b8")
        self.label2.configure(text='nothing',bg="#fff0b8")
        self.update_label()
       
        myButton = Button(master, text="OK",padx=40, pady=5, command = update_label)
        myButton.place(x=200,y=200)


    def update_label(self):

        if(self.pulse<10):
             self.label.configure(text = "....")
        else:
            self.label.configure(text = '{}'.format(self.pulse))
        if(self.spo2<10):
            self.label1.configure(text ="....")
        else:
            self.label1.configure(text = '{}'.format(self.eeg))
        if(self.tempp<10):
            self.label2.configure(text ="....")
        else:
            self.label2.configure(text = '{}'.format(self.tempp))
        print("Pulse:",self.pulse)
        print("Oxygen Level:",self.spo2)
        print("Temperature",self.tempp)
        random_forest_pred()
       
       
    def random_forest_pred(self):
        if(e2.get()=="Male"):
            c=0.0;
            d=1.0
        elif(e2.get()=="Female"):
            c=1.0;
            d=0.0;
   
        # Predicting a new result
        a=classifier.predict([[c,d,sc.transform([[e1.get()]]),self.tempp,self.spo2,self.pulse]])
   
        if a==0:
            Label(root,text="Arrhythmia", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 25)).place(x=170,y=270)
 
        elif a==1:
            Label(root,text="Arrhythmia and Hyperthermia", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 25)).place(x=170,y=270)
       
        elif a==2:
            Label(root,text="Arrhythmia, Hyperthermia and Hypoxemia", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 25)).place(x=170,y=270)
   
        elif a==3:
            Label(root,text="Arrhythmia and Hypoxemia", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 25)).place(x=170,y=270)
       
        elif a==4:
            Label(root,text="Hyperthermia", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 25)).place(x=170,y=270)
     
        elif a==5:
            Label(root,text="Hyperthermia and Hypoxemia", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 25)).place(x=170,y=270)
       
        elif a==6:
            Label(root,text="Hypoxemia", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 25)).place(x=170,y=270)

        elif a==7:
            Label(root,text="None", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 25)).place(x=170,y=270)
       
       

#Uploading data to thing speak
def thingspeak_post(pulse,spo2,tempp):
    URL='https://api.thingspeak.com/update?api_key='

    #Here should be your thingspeak API Key
    KEY='#YOURAPIHERE'
    HEADER='&field1={}&field2={}&field3={}'.format(pulse,spo2,tempp)
    NEW_URL=URL+KEY+HEADER
    print(NEW_URL)
   
    data=urllib.request.urlopen(NEW_URL)
    print(data)

def start_function():
    threading.Timer(2,start_function).start()


    b=ser.readline()
    val=b.decode()
    pulse,eeg,tempp=list(map(int,val.split()))
    pulse_rate_oxy=pulse
    oxygen_level=spo2
    temperature_coming=tempp
 
    gui(root,pulse_rate_oxy,oxygen_level,temperature_coming)
    thingspeak_post(pulse_rate_oxy,oxygen_level,temperature_coming)
   
   

if __name__=="__main__":

    ser=serial.Serial('COM5',baudrate=9600,timeout=2)
    root = Tk()
    root.title('Mini Project')
    root.geometry('550x450')
    root['background'] = "#fff0b8"
    start_function()
    root.mainloop()
