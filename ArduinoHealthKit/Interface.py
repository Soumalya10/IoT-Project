import time
from tkinter import *
import random
import urllib.request
import requests
import threading
import serial

class gui:
    def __init__(self, master,pulse,eeg,tempp):
        self.master=master
        self.label=Label(master, fg='red', font=("Helvetica", 25),pady=2)
        self.label1=Label(master, fg='red', font=("Helvetica", 25),pady=2)
        self.label2=Label(master, fg='red', font=("Helvetica", 25),pady=2)
        
        Label(master,text="PulseRate", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 15)).place(x=20,y=80)
        Label(master,text="Eeg Heart Pattern", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 15)).place(x=310,y=80)
        Label(master,text="Temperature", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 15)).place(x=140,y=80)

        self.label.place(x=120,y=120)
        self.label1.place(x=325,y=120)
        self.label2.place(x=200,y=120)
        self.pulse=pulse
        self.eeg=eeg
        self.tempp=tempp
        self.label.configure(text='nothing',bg="#fff0b8")
        self.label1.configure(text='nothing',bg="#fff0b8")
        self.label2.configure(text='nothing',bg="#fff0b8")
        self.update_label()

    def update_label(self):

        if(self.pulse<10):
             self.label.configure(text = "....")
        else:
            self.label.configure(text = '{}'.format(self.pulse))
        if(self.eeg<10):
            self.label1.configure(text ="....")
        else:
            self.label1.configure(text = '{}'.format(self.eeg))
        if(self.tempp<10):
            self.label2.configure(text ="....")
        else:
            self.label2.configure(text = '{}'.format(self.tempp))
        print("Pulse:",self.pulse)
        print("Eeg:",self.eeg)
        print("Temperature",self.tempp)


def thingspeak_post(pulse,eeg,tempp):
    URL='https://api.thingspeak.com/update?api_key='

    #Here should be your thingspeak API Key
    KEY='#YOURAPIHERE'
    HEADER='&field1={}&field2={}&field3={}'.format(pulse,eeg,tempp)
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
    eeg_heart_pattern=eeg
    temperature_coming=tempp
  
    gui(root,pulse_rate_oxy,eeg_heart_pattern,temperature_coming)
    thingspeak_post(pulse_rate_oxy,eeg_heart_pattern,temperature_coming)
    
    

if __name__=="__main__":

    ser=serial.Serial('COM5',baudrate=9600,timeout=2)
    root = Tk()
    root.title('Mini Project')
    root.geometry('550x450')
    root['background'] = "#fff0b8"
    start_function()
    root.mainloop()
