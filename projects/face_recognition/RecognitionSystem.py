import cv2
import face_recognition as fr
import numpy as np
import mediapipe as mp
import os
from tkinter import *
from PIL import Image, ImageTk
import imutils
import math

global name_field, user_field, pass_field

def register_user():
    name, new_user, pwd = name_field.get(), user_field.get(), pass_field.get()

    if (len(name) == 0) | (len(new_user) == 0) | (len(pwd) == 0):
        print('Please complete form')
    else:
        users_listdir = os.listdir(users_path)
        users = []

        # Get users list
        for user in users_listdir:
            user = user.split('.')[0]
            users.append(user)

        # Check if user exists
        if new_user in users:
            print('User is not available. Please choose another user.')
        else:
            info.append(name)
            info.append(new_user)
            info.append(pwd)

            # Save new user
            f = open(f'{users_path}/{new_user}.txt', 'w')
            f.write(f'{name},{new_user},{pwd}')
            f.close()

            # Clear fields
            name_field.delete(0,END)
            user_field.delete(0,END)
            pass_field.delete(0,END)
    
            print('Successful register')

def login_user():
    print('Log')

users_path = 'projects/face_recognition/databases/users'
faces_path = 'projects/face_recognition/databases/faces'

info = []

# Create screen
screen = Tk()
screen.title('FACE RECOGNITION SYSTEM')
screen.geometry('1280x720')


# Set background
bg_img = PhotoImage(file='projects/face_recognition/setup/Inicio.png')
background = Label(image=bg_img, text='Inicio')
background.place(x=0, y=0, relheight=1, relwidth=1)


# Create text input fields
name_field = Entry(screen, width=50)
name_field.place(x=110, y=320)

user_field = Entry(screen, width=50)
user_field.place(x=110, y=430)

pass_field = Entry(screen, width=50)
pass_field.place(x=110, y=540)

# user_log_field = Entry(screen, width=50)
# user_log_field.place(x=750, y=380)

# pass_log_field = Entry(screen, width=50)
# pass_log_field.place(x=750, y=500)


# Create buttons
reg_img = PhotoImage(file='projects/face_recognition/setup/BtSign.png')
reg_btn = Button(screen, text='Register', image=reg_img, height=40, width=200, command=register_user)
reg_btn.place(x=300, y=580)

log_img = PhotoImage(file='projects/face_recognition/setup/BtLogin.png')
log_btn = Button(screen, text='Login', image=log_img, height=40, width=200, command=login_user)
log_btn.place(x=900, y=580)

screen.mainloop()