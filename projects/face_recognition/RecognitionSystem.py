import cv2
import face_recognition as fr
import numpy as np
import mediapipe as mp
import os
from tkinter import *
from PIL import Image, ImageTk
import imutils
import math

def biometric_log():
    global facereg_screen, count, blink, img_info, step, video_cap, lbl_video

    if video_cap is not None:
        ret, frame = video_cap.read()

        # Resize
        frame = imutils.resize(frame, width=1280)

        # Change color profile
        frame_temp = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if ret==True:
            # Inference face mesh
            res = face_mesh.process(frame_temp)

            # Result lists
            pos_x = []
            pos_y = []
            temp_list = []

            if res.multi_face_landmarks:
                # Extract face mesh
                for face in res.multi_face_landmarks:
                    # Draw
                    mp_draw.draw_landmarks(frame, face, face_mesh_object.FACEMESH_CONTOURS, draw_config, draw_config)
        
        # Convert video
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=img)

        # Show video
        lbl_video.configure(image=img)
        lbl_video.image = img
        lbl_video.after(10, biometric_log)

    else:
        video_cap.release()

def register_user():
    global name_field, user_field, pass_field, video_cap, lbl_video, facereg_screen
    
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

            # Face Recognition screen
            facereg_screen = Toplevel(main_screen)
            facereg_screen.title('BIOMETRIC REGISTER')
            facereg_screen.geometry('1280x720')

            # Label video
            lbl_video = Label(facereg_screen)
            lbl_video.place(x=0, y=0)

            # Video capture
            video_cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
            video_cap.set(3, 1280)
            video_cap.set(4, 720)

            biometric_log()
                
            print('Successful register')

def login_user():
    print('Log')

users_path = 'projects/face_recognition/databases/users'
faces_path = 'projects/face_recognition/databases/faces'

# Register variables
blink = False
count = 0
sample = 0
step = 0

# Offset params
off_x = 30
off_y = 20

# Threshold
th = 0.5

# Draw tool
mp_draw = mp.solutions.drawing_utils
draw_config = mp_draw.DrawingSpec(thickness=1, circle_radius=1)

# Face mesh
face_mesh_object = mp.solutions.face_mesh
face_mesh = face_mesh_object.FaceMesh(max_num_faces=1, refine_landmarks=True)

# Face detector
face_object = mp.solutions.face_detection
face_detector = face_object.FaceDetection(min_detection_confidence=th, model_selection=1)

info = []

# Create screen
main_screen = Tk()
main_screen.title('FACE RECOGNITION SYSTEM')
main_screen.geometry('1280x720')


# Set background
bg_img = PhotoImage(file='projects/face_recognition/setup/Inicio.png')
background = Label(image=bg_img, text='Inicio')
background.place(x=0, y=0, relheight=1, relwidth=1)


# Create text input fields
name_field = Entry(main_screen, width=50)
name_field.place(x=110, y=320)

user_field = Entry(main_screen, width=50)
user_field.place(x=110, y=430)

pass_field = Entry(main_screen, width=50)
pass_field.place(x=110, y=540)

# user_log_field = Entry(main_screen, width=50)
# user_log_field.place(x=750, y=380)

# pass_log_field = Entry(main_screen, width=50)
# pass_log_field.place(x=750, y=500)


# Create buttons
reg_img = PhotoImage(file='projects/face_recognition/setup/BtSign.png')
reg_btn = Button(main_screen, text='Register', image=reg_img, height=40, width=200, command=register_user)
reg_btn.place(x=300, y=580)

log_img = PhotoImage(file='projects/face_recognition/setup/BtLogin.png')
log_btn = Button(main_screen, text='Login', image=log_img, height=40, width=200, command=login_user)
log_btn.place(x=900, y=580)

main_screen.mainloop()