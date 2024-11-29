import cv2
import cv2.text
import face_recognition as fr
import numpy as np
import mediapipe as mp
import os
from tkinter import *
from PIL import Image, ImageTk
import imutils
import math

main_screen = None
facereg_screen = None
login_screen = None
profile_screen = None

def close_window():
    global liveness_flg, count, facereg_screen, main_screen, login_screen, profile_screen

    liveness_flg = 0
    count = 0

    # try:
    #     if facereg_screen is not None:
    #         facereg_screen.destroy()
    # except Exception as e:
    #     print(f"Error facereg_screen: {e}") 
    
    # try:
    #     if profile_screen is not None:
    #         profile_screen.destroy()
    # except Exception as e:
    #     print(f"Error profile_screen: {e}") 

    # try:
    #     if login_screen is not None:
    #         login_screen.destroy()
    # except Exception as e:
    #     print(f"Error login_screen: {e}") 
    
    try:
        if main_screen is not None:
            main_screen.destroy()
    except Exception as e:
        print(f"Error main_screen: {e}") 


def show_profile():
    global liveness_flg, count, profile_screen, username

    liveness_flg = 0
    count = 0

    # Face Recognition screen
    profile_screen = Toplevel(login_screen)
    profile_screen.title('PROFILE')
    profile_screen.geometry('1280x720')

    # Create close protocol after create the screen
    profile_screen.protocol("WM_DELETE_WINDOW", close_window)

    # Set background
    bg_img = PhotoImage(file='projects/face_recognition/setup/Back2.png')
    background = Label(image=bg_img, text='Profile')
    background.place(x=0, y=0, relheight=1, relwidth=1)

    # Get username's info
    user_file = open(f'{users_path}/{username}.txt', 'r')
    user_info = user_file.read().split(',')

    name, user, pwd = user_info

    txt1 = Label(profile_screen, text=f'WELCOME {name}')
    txt1.place(x=580, y=50)

    lbl_img = Label(profile_screen)
    lbl_img.place(x=490, y=80)

    user_img = cv2.imread(f'{faces_path}/{username}.png')
    user_img = cv2.cvtColor(user_img, cv2.COLOR_RGB2BGR)
    user_img = Image.fromarray(user_img)

    img = ImageTk.PhotoImage(image=user_img)

    lbl_img.configure(image=img)
    lbl_img.image = img
    


def encode_faces(images):
    
    encoded_faces = []

    for img in images:
        # Color
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Encode
        cod = fr.face_encodings(img)[0]

        # Save to list
        encoded_faces.append(cod)
    
    return encoded_faces


def biometric_log():
    global video_cap, lbl_video, login_screen, faces_path, encoded_faces, users, images, username, liveness_flg, blink, count

    if video_cap is not None:
        ret, frame = video_cap.read()

        # Frame to save
        frame_tosave = frame.copy()
        
        # Resize
        frame = imutils.resize(frame, width=1280)

        # Change color profile
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if ret==True:
            # Inference face mesh
            face_landmarks = face_mesh.process(frame_rgb)

            # Result lists
            px = []
            py = []
            p_list = []

            if face_landmarks.multi_face_landmarks:
                # Extract face mesh
                for face_landmark_list in face_landmarks.multi_face_landmarks:
                    # Draw
                    mp_draw.draw_landmarks(image=frame,
                                           landmark_list=face_landmark_list,
                                           connections=face_mesh_object.FACEMESH_CONTOURS,
                                           landmark_drawing_spec=draw_config,
                                           connection_drawing_spec=draw_config)
                    
                    for id, points in enumerate(face_landmark_list.landmark):
                        # Image shape
                        h, w, c = frame.shape
                        x, y = int(points.x * w), int(points.y * h)

                        px.append(x)
                        py.append(y)
                        p_list.append([id, x, y])

                        # 468 key points
                        if len(p_list) == 468:
                            # Right eye
                            xr1, yr1 = p_list[145][1:]
                            xr2, yr2 = p_list[159][1:]
                            right_lenght = math.hypot(xr2-xr1, yr2-yr1)

                            # Draw tracking points
                            cv2.circle(frame, (xr1,yr1), 2, (255,0,0), cv2.FILLED)
                            cv2.circle(frame, (xr2,yr2), 2, (255,0,0), cv2.FILLED)

                            # Left eye
                            xl1, yl1 = p_list[374][1:]
                            xl2, yl2 = p_list[386][1:]
                            left_lenght = math.hypot(xl2-xl1, yl2-yl1)

                            # Draw tracking points
                            cv2.circle(frame, (xl1,yl1), 2, (0,255,0), cv2.FILLED)
                            cv2.circle(frame, (xl2,yl2), 2, (0,255,0), cv2.FILLED)

                            # Right and left parietals
                            xrp, yrp = p_list[139][1:]
                            xlp, ylp = p_list[368][1:]

                            # Draw tracking points
                            cv2.circle(frame, (xrp,yrp), 2, (255,0,0), cv2.FILLED)
                            cv2.circle(frame, (xlp,ylp), 2, (0,255,0), cv2.FILLED)

                            # Right and left eyebrows
                            xreb, yreb = p_list[70][1:]
                            xleb, yleb = p_list[300][1:]

                            # Draw tracking points
                            cv2.circle(frame, (xreb,yreb), 2, (255,0,0), cv2.FILLED)
                            cv2.circle(frame, (xleb,yleb), 2, (0,255,0), cv2.FILLED)


                            # Face detection
                            faces = face_detector.process(frame_rgb)

                            if faces.detections is not None:
                                for face in faces.detections:
                                    # Bbox: ID, BBOX, SCORE
                                    scr = face.score[0]
                                    bbox = face.location_data.relative_bounding_box

                                    # Threshold
                                    if scr > th:
                                        # Pixels
                                        xi, yi, wi, hi = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                        xi, yi, wi, hi = int(xi * w), int(yi * h), int(wi*w), int(hi*h)

                                        # cv2.circle(frame, (xi,yi), 4, (255,0,0), cv2.FILLED)
                                        # cv2.circle(frame, (xi,100), 4, (255,0,0), cv2.FILLED)
                                        # cv2.circle(frame, (100,yi), 4, (255,255,0), cv2.FILLED)
                                        # cv2.circle(frame, (xi+wi,yi+hi), 4, (0,0,255), cv2.FILLED)

                                        # Offset
                                        off_width = off_x * wi
                                        xi = int(xi - int(off_width/2))
                                        wi = int(wi + off_width)

                                        off_height = off_y * hi
                                        yi = int(yi - int(off_height/2))
                                        hi = int(hi + off_height)

                                        # Error on borders
                                        xi = 0 if xi < 0 else xi
                                        yi = 0 if yi < 0 else yi
                                        wi = 0 if wi < 0 else wi
                                        hi = 0 if hi < 0 else hi

                                        cv2.circle(frame, (xi,yi), 4, (255,0,0), cv2.FILLED)
                                        cv2.circle(frame, (xi+wi,yi+hi), 4, (0,0,255), cv2.FILLED)


                                        # Verification steps
                                        if liveness_flg == 0:
                                            # Draw face tracker rectangle (Rose)
                                            cv2.rectangle(frame, (xi, yi, wi, hi), (255, 0, 255), 2)

                                            # Step 0 image
                                            h0, w0, c = step0_img.shape
                                            frame[50:50+h0, 50:50+w0] = step0_img

                                            # Step 1 image
                                            h1, w1, c = step1_img.shape
                                            frame[50:50+h1, 1030:1030+w1] = step1_img

                                            # Step 2 image
                                            h2, w2, c = step2_img.shape
                                            frame[270:270+h2, 1030:1030+w2] = step2_img

                                            # Centered face
                                            if (xreb > xrp) & (xleb < xlp):
                                                # Check image
                                                h_ch, w_ch, c = check_img.shape
                                                frame[165:165+h_ch, 1105:1105+w_ch] = check_img

                                                # Blink counter
                                                if (right_lenght <= 10) & (left_lenght <= 10) & (blink == False):
                                                    count += 1
                                                    blink = True
                                                elif (right_lenght > 10) & (left_lenght > 10) & (blink == True):
                                                    blink = False
                                                
                                                cv2.putText(frame, f'Blinks: {count}', (1070, 375), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                                                # Blinks condition
                                                if count >= 3:
                                                    # Check image
                                                    frame[385:385+h_ch, 1105:1105+w_ch] = check_img
                                                    
                                                    # Take photo on open eyes (Set a threshold enough to have really open eyes)
                                                    if (right_lenght > 15) & (left_lenght > 15):
                                                        # Take photo
                                                        photo = frame_tosave[yi:yi+hi, xi:xi+wi]

                                                        # # Save photo
                                                        # cv2.imwrite(f'{faces_path}/{new_user}.png', photo)

                                                        # Step 1
                                                        liveness_flg = 1
                                            else:
                                                count = 0
                                        
                                        if liveness_flg == 1:
                                            cv2.rectangle(frame, (xi, yi, wi, hi), (0, 255, 0), 2)

                                            # Liveness check image
                                            hl, wl, c = liv_ch_img.shape
                                            frame[50:50+hl, 50:50+wl] = liv_ch_img

                                            # Find faces
                                            found_faces = fr.face_locations(frame_rgb)
                                            encod_faces = fr.face_encodings(frame_rgb, found_faces)

                                            for enc_face, found_face in zip(encod_faces, found_faces):

                                                # Match face
                                                match = fr.compare_faces(encoded_faces, enc_face)

                                                # Match error
                                                err = fr.face_distance(encoded_faces, enc_face)

                                                min_err = np.argmin(err)

                                                if match[min_err]:
                                                    # Get username
                                                    username = users[min_err].upper()

                                                    show_profile()

        
        # Convert video
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=img)

        # Show video
        lbl_video.configure(image=img)
        lbl_video.image = img
        lbl_video.after(10, biometric_log)

    else:
        video_cap.release()


def biometric_register():
    global facereg_screen, count, blink, liveness_flg, video_cap, lbl_video

    if video_cap is not None:
        ret, frame = video_cap.read()

        # Frame to save
        frame_tosave = frame.copy()
        
        # Resize
        frame = imutils.resize(frame, width=1280)

        # Change color profile
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if ret==True:
            # Inference face mesh
            face_landmarks = face_mesh.process(frame_rgb)

            # Result lists
            px = []
            py = []
            p_list = []

            if face_landmarks.multi_face_landmarks:
                # Extract face mesh
                for face_landmark_list in face_landmarks.multi_face_landmarks:
                    # Draw
                    mp_draw.draw_landmarks(image=frame,
                                           landmark_list=face_landmark_list,
                                           connections=face_mesh_object.FACEMESH_CONTOURS,
                                           landmark_drawing_spec=draw_config,
                                           connection_drawing_spec=draw_config)
                    
                    for id, points in enumerate(face_landmark_list.landmark):
                        # Image shape
                        h, w, c = frame.shape
                        x, y = int(points.x * w), int(points.y * h)

                        px.append(x)
                        py.append(y)
                        p_list.append([id, x, y])

                        # 468 key points
                        if len(p_list) == 468:
                            # Right eye
                            xr1, yr1 = p_list[145][1:]
                            xr2, yr2 = p_list[159][1:]
                            right_lenght = math.hypot(xr2-xr1, yr2-yr1)

                            # Draw tracking points
                            cv2.circle(frame, (xr1,yr1), 2, (255,0,0), cv2.FILLED)
                            cv2.circle(frame, (xr2,yr2), 2, (255,0,0), cv2.FILLED)

                            # Left eye
                            xl1, yl1 = p_list[374][1:]
                            xl2, yl2 = p_list[386][1:]
                            left_lenght = math.hypot(xl2-xl1, yl2-yl1)

                            # Draw tracking points
                            cv2.circle(frame, (xl1,yl1), 2, (0,255,0), cv2.FILLED)
                            cv2.circle(frame, (xl2,yl2), 2, (0,255,0), cv2.FILLED)

                            # Right and left parietals
                            xrp, yrp = p_list[139][1:]
                            xlp, ylp = p_list[368][1:]

                            # Draw tracking points
                            cv2.circle(frame, (xrp,yrp), 2, (255,0,0), cv2.FILLED)
                            cv2.circle(frame, (xlp,ylp), 2, (0,255,0), cv2.FILLED)

                            # Right and left eyebrows
                            xreb, yreb = p_list[70][1:]
                            xleb, yleb = p_list[300][1:]

                            # Draw tracking points
                            cv2.circle(frame, (xreb,yreb), 2, (255,0,0), cv2.FILLED)
                            cv2.circle(frame, (xleb,yleb), 2, (0,255,0), cv2.FILLED)


                            # Face detection
                            faces = face_detector.process(frame_rgb)

                            if faces.detections is not None:
                                for face in faces.detections:
                                    # Bbox: ID, BBOX, SCORE
                                    scr = face.score[0]
                                    bbox = face.location_data.relative_bounding_box

                                    # Threshold
                                    if scr > th:
                                        # Pixels
                                        xi, yi, wi, hi = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                        xi, yi, wi, hi = int(xi * w), int(yi * h), int(wi*w), int(hi*h)

                                        # cv2.circle(frame, (xi,yi), 4, (255,0,0), cv2.FILLED)
                                        # cv2.circle(frame, (xi,100), 4, (255,0,0), cv2.FILLED)
                                        # cv2.circle(frame, (100,yi), 4, (255,255,0), cv2.FILLED)
                                        # cv2.circle(frame, (xi+wi,yi+hi), 4, (0,0,255), cv2.FILLED)

                                        # Offset
                                        off_width = off_x * wi
                                        xi = int(xi - int(off_width/2))
                                        wi = int(wi + off_width)

                                        off_height = off_y * hi
                                        yi = int(yi - int(off_height/2))
                                        hi = int(hi + off_height)

                                        # Error on borders
                                        xi = 0 if xi < 0 else xi
                                        yi = 0 if yi < 0 else yi
                                        wi = 0 if wi < 0 else wi
                                        hi = 0 if hi < 0 else hi

                                        cv2.circle(frame, (xi,yi), 4, (255,0,0), cv2.FILLED)
                                        cv2.circle(frame, (xi+wi,yi+hi), 4, (0,0,255), cv2.FILLED)


                                        # Verification steps
                                        if liveness_flg == 0:
                                            # Draw face tracker rectangle (Rose)
                                            cv2.rectangle(frame, (xi, yi, wi, hi), (255, 0, 255), 2)

                                            # Step 0 image
                                            h0, w0, c = step0_img.shape
                                            frame[50:50+h0, 50:50+w0] = step0_img

                                            # Step 1 image
                                            h1, w1, c = step1_img.shape
                                            frame[50:50+h1, 1030:1030+w1] = step1_img

                                            # Step 2 image
                                            h2, w2, c = step2_img.shape
                                            frame[270:270+h2, 1030:1030+w2] = step2_img

                                            # Centered face
                                            if (xreb > xrp) & (xleb < xlp):
                                                # Check image
                                                h_ch, w_ch, c = check_img.shape
                                                frame[165:165+h_ch, 1105:1105+w_ch] = check_img

                                                # Blink counter
                                                if (right_lenght <= 10) & (left_lenght <= 10) & (blink == False):
                                                    count += 1
                                                    blink = True
                                                elif (right_lenght > 10) & (left_lenght > 10) & (blink == True):
                                                    blink = False
                                                
                                                cv2.putText(frame, f'Blinks: {count}', (1070, 375), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                                                # Blinks condition
                                                if count >= 3:
                                                    # Check image
                                                    frame[385:385+h_ch, 1105:1105+w_ch] = check_img
                                                    
                                                    # Take photo on open eyes (Set a threshold enough to have really open eyes)
                                                    if (right_lenght > 15) & (left_lenght > 15):
                                                        # Take photo
                                                        photo = frame_tosave[yi:yi+hi, xi:xi+wi]

                                                        # Save photo
                                                        cv2.imwrite(f'{faces_path}/{new_user}.png', photo)

                                                        # Step 1
                                                        liveness_flg = 1
                                            else:
                                                count = 0
                                        
                                        if liveness_flg == 1:
                                            cv2.rectangle(frame, (xi, yi, wi, hi), (0, 255, 0), 2)

                                            # Liveness check image
                                            hl, wl, c = liv_ch_img.shape
                                            frame[50:50+hl, 50:50+wl] = liv_ch_img            
        
        # Convert video
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=img)

        # Show video
        lbl_video.configure(image=img)
        lbl_video.image = img
        lbl_video.after(10, biometric_register)

    else:
        video_cap.release()

def register_user():
    global name_field, user_field, pass_field, video_cap, lbl_video, facereg_screen, new_user
    
    new_name, new_user, new_pwd = name_field.get(), user_field.get(), pass_field.get()

    if (len(new_name) == 0) | (len(new_user) == 0) | (len(new_pwd) == 0):
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
            info.append(new_name)
            info.append(new_user)
            info.append(new_pwd)

            # Save new user
            f = open(f'{users_path}/{new_user}.txt', 'w')
            f.write(f'{new_name},{new_user},{new_pwd}')
            f.close()

            # Clear fields
            name_field.delete(0,END)
            user_field.delete(0,END)
            pass_field.delete(0,END)

            # Face Recognition screen
            facereg_screen = Toplevel(main_screen)
            facereg_screen.title('BIOMETRIC REGISTER')
            facereg_screen.geometry('1280x720')

            # Create close protocol after create the screen
            facereg_screen.protocol("WM_DELETE_WINDOW", close_window)

            # Label video
            lbl_video = Label(facereg_screen)
            lbl_video.place(x=0, y=0)

            # Video capture
            video_cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
            video_cap.set(3, 1280)
            video_cap.set(4, 720)

            biometric_register()
                
            print('Successful register')

def login_user():
    global video_cap, lbl_video, login_screen, faces_path, encoded_faces, users, images

    # Read face database
    images = []
    users = []

    img_list = os.listdir(faces_path)

    # Read face images
    for img_name in img_list:
        img = cv2.imread(f'{faces_path}/{img_name}')

        # Save temporaly in a list
        images.append(img)

        # Save user in a list
        users.append(os.path.splitext(img_name)[0])

    # Encode face image
    encoded_faces = encode_faces(images)

    login_screen = Toplevel(main_screen)
    login_screen.title('BIOMETRIC LOGIN')
    login_screen.geometry('1280x720')

    # Create close protocol after create the screen
    login_screen.protocol("WM_DELETE_WINDOW", close_window)

    # Label video
    lbl_video = Label(login_screen)
    lbl_video.place(x=0, y=0)

    # Video capture
    video_cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    video_cap.set(3, 1280)
    video_cap.set(4, 720)
    
    biometric_log()


# Users' data folders
users_path = 'projects/face_recognition/databases/users'
faces_path = 'projects/face_recognition/databases/faces'


# Step images
check_img = cv2.cvtColor(cv2.imread('projects/face_recognition/setup/check.png'), cv2.COLOR_BGR2RGB)
step0_img = cv2.cvtColor(cv2.imread('projects/face_recognition/setup/Step0.png'), cv2.COLOR_BGR2RGB)
step1_img = cv2.cvtColor(cv2.imread('projects/face_recognition/setup/Step1.png'), cv2.COLOR_BGR2RGB)
step2_img = cv2.cvtColor(cv2.imread('projects/face_recognition/setup/Step2.png'), cv2.COLOR_BGR2RGB)
liv_ch_img = cv2.cvtColor(cv2.imread('projects/face_recognition/setup/LivenessCheck.png'), cv2.COLOR_BGR2RGB)

# Register variables
blink = False
count = 0
sample = 0
liveness_flg = 0

# Offset params (Percentaje)
off_x = 0.3
off_y = 0.4

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


# Create buttons
reg_img = PhotoImage(file='projects/face_recognition/setup/BtSign.png')
reg_btn = Button(main_screen, text='Register', image=reg_img, height=40, width=200, command=register_user)
reg_btn.place(x=300, y=580)

log_img = PhotoImage(file='projects/face_recognition/setup/BtLogin.png')
log_btn = Button(main_screen, text='Login', image=log_img, height=40, width=200, command=login_user)
log_btn.place(x=900, y=580)

main_screen.mainloop()