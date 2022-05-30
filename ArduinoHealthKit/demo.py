# Random Forest Classification

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('Project.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

#Encoding Independent Variables
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct= ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1])], remainder='passthrough')
X = np.array(ct.fit_transform(X))
print(X)

#Encoding Dependent Variables
from sklearn.preprocessing import LabelEncoder
l= LabelEncoder()
y= l.fit_transform(y)
print(y)


# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)
#print(X_train)
#print(y_train)
#print(X_test)
#print(y_test)

#Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train[:,2:3] = sc.fit_transform(X_train[:,2:3])
X_test[:,2:3] = sc.transform(X_test[:,2:3])
#print(X_train)
#print(X_test)

# Training the Random Forest Classification model on the Training set
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

#taking inputs
from tkinter import *

root = Tk()
root.title('Final Year Project')
root.geometry('550x450')
root['background'] = "#fff0b8"
   

       
label=Label(root, fg='red', font=("Helvetica", 25),pady=2)
label1=Label(root, fg='red', font=("Helvetica", 25),pady=2)
label2=Label(root, fg='red', font=("Helvetica", 25),pady=2)
label3=Label(root, fg='red', font=("Helvetica", 25),pady=2)
label4=Label(root, fg='red', font=("Helvetica", 25),pady=2)
label5=Label(root, fg='red', font=("Helvetica", 25),pady=2)
label6=Label(root, fg='red', font=("Helvetica", 25),pady=2)

Label(root,text="Enter your age:", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 15)).pack()
e1= Entry(root, width=20)
e1.configure(font=("Helvetica", 15))
e1.pack()
Label(root,text="Enter your gender:", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 15)).pack()
e2= Entry(root, width=20)
e2.configure(font=("Helvetica", 15))
e2.pack()

Label(root,text="Pulse Rate", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 15)).place(x=20,y=120)
Label(root,text="Oxygen Level", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 15)).place(x=310,y=120)
Label(root,text="Temperature", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 15)).place(x=160,y=120)
Label(root,text="Any Diseases you are having:", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 15)).place(x=120,y=240)

label.place(x=80,y=150)
label1.place(x=325,y=150)
label2.place(x=200,y=150)

#Manual values
pulse=104
oxy=94
temp=96.6

pulse_string=str(pulse)
oxy_string=str(oxy)
temp_string=str(temp)

label.configure(text=pulse_string,bg="#fff0b8")
label1.configure(text=oxy_string,bg="#fff0b8")
label2.configure(text=temp_string,bg="#fff0b8")
#e3= Entry(root, width=20)
#e3.place(x=20,y=150)
#e4= Entry(root, width=20)
#e4.place(x=160,y=150)
#e5= Entry(root, width=20)
#e5.place(x=310,y=150)



#creating a button and making it work on click
def myClick():
    if(e2.get()=="Male"):
        c=0.0;
        d=1.0
    elif(e2.get()=="Female"):
        c=1.0;
        d=0.0;
    
    # Predicting a new result
    a=classifier.predict([[c,d,sc.transform([[e1.get()]]),temp,oxy,pulse]])
    
    if a==0:
        Label(root,text="Arrhythmia", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 25)).place(x=120,y=270)
        #e6.insert(0,"Arrhythmia")
    elif a==1:
        Label(root,text="Arrhythmia and Hyperthermia", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 25)).place(x=120,y=270)
       #e6.insert(0,"Arrhythmia and Hyperthermia")
    elif a==2:
        Label(root,text="Arrhythmia, Hyperthermia and Hypoxemia", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 25)).place(x=120,y=270)
       #e6.insert(0,"Arrhythmia, Hyperthermia and Hypoxemia")
    elif a==3:
        Label(root,text="Arrhythmia and Hypoxemia", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 25)).place(x=120,y=270)
        #e6.insert(0,"Arrhythmia and Hypoxemia")
    elif a==4:
        Label(root,text="Hyperthermia", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 25)).place(x=120,y=270)
        #e6.insert(0,"Hyperthermia")
    elif a==5:
        Label(root,text="Hyperthermia and Hypoxemia", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 25)).place(x=120,y=270)
       #e6.insert(0,"Hyperthermia and Hypoxemia")
    elif a==6:
        Label(root,text="Hypoxemia", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 25)).place(x=120,y=270)
      # e6.insert(0,"Hypoxemia")
    elif a==7:
        Label(root,text="None", fg='#ff2d26',bg="#fff0b8", font=("Helvetica", 25)).place(x=120,y=270)
        #e6.insert(0,"None")
    
    
myButton = Button(root, text="OK",padx=40, pady=5, command = myClick)
myButton.place(x=200,y=200)

root.mainloop()
