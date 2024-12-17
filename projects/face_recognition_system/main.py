import os
import tkinter as tk
from tkinter import PhotoImage
import win32com.client
import cv2
from PIL import Image, ImageTk
import imutils
from customtkinter import CTkOptionMenu, StringVar
import math
import mediapipe as mp
import face_recognition as fr
import numpy as np


class FaceDetector():
    def __init__(self, th=0.5, off_x=0.3, off_y=0.4):
        # Draw tool
        self.mp_draw = mp.solutions.drawing_utils
        self.draw_config = self.mp_draw.DrawingSpec(thickness=1, circle_radius=1)

        # Face mesh
        self.face_mesh_object = mp.solutions.face_mesh
        self.face_mesh = self.face_mesh_object.FaceMesh(max_num_faces=1, refine_landmarks=True)

        # Face detector
        self.face_object = mp.solutions.face_detection
        self.face_detector = self.face_object.FaceDetection(min_detection_confidence=0.5, model_selection=1)

        # Threshold
        self.th = th

        # Offset for face frame
        self.off_x, self.off_y = off_x, off_y

        # Face box enabler
        self.flg_facebox = True

        # Step images
        self.check_img = cv2.cvtColor(cv2.imread('projects/face_recognition_system/images/check.png'), cv2.COLOR_BGR2RGB)
        self.nofaces_img = cv2.cvtColor(cv2.imread('projects/face_recognition_system/images/no_faces.png'), cv2.COLOR_BGR2RGB)
        self.face_det_img = cv2.cvtColor(cv2.imread('projects/face_recognition_system/images/step0.png'), cv2.COLOR_BGR2RGB)
        self.step1_img = cv2.cvtColor(cv2.imread('projects/face_recognition_system/images/step1.png'), cv2.COLOR_BGR2RGB)
        self.step2_img = cv2.cvtColor(cv2.imread('projects/face_recognition_system/images/step2.png'), cv2.COLOR_BGR2RGB)
        self.liv_ch_img = cv2.cvtColor(cv2.imread('projects/face_recognition_system/images/verified.png'), cv2.COLOR_BGR2RGB)

        # Step
        self.step = 0

        #Blink counts
        self.blink_count = 0
    
    def processs_frame(self, frame, frame_rgb, frame_tosave):
        # Inference face mesh
        face_landmarks = self.face_mesh.process(frame_rgb)

        # Result lists
        px = []
        py = []
        p_list = []

        if face_landmarks.multi_face_landmarks:
            # Extract face mesh
            for face_landmark_list in face_landmarks.multi_face_landmarks:
                # Draw
                self.mp_draw.draw_landmarks(image=frame,
                                            landmark_list=face_landmark_list,
                                            connections=self.face_mesh_object.FACEMESH_CONTOURS,
                                            landmark_drawing_spec=self.draw_config,
                                            connection_drawing_spec=self.draw_config)

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
                        faces = self.face_detector.process(frame_rgb)

                        blink_flg = False

                        if faces.detections is not None:
                            for face in faces.detections:
                                # Bbox: ID, BBOX, SCORE
                                scr = face.score[0]
                                bbox = face.location_data.relative_bounding_box

                                # Face detected image
                                h0, w0, c = self.face_det_img.shape
                                frame[195:195+h0, 0:0+w0] = self.face_det_img

                                cv2.putText(frame, f'{w} | {h}', (100, 280), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255), 1)

                                # Threshold
                                if scr > self.th:
                                    # Pixels
                                    xi, yi, wi, hi = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                    xi, yi, wi, hi = int(xi * w), int(yi * h), int(wi*w), int(hi*h)

                                    # Offset
                                    off_width = self.off_x * wi
                                    xi = int(xi - int(off_width/2))
                                    wi = int(wi + off_width)

                                    off_height = self.off_y * hi
                                    yi = int(yi - int(off_height/2))
                                    hi = int(hi + off_height)
                                    
                                    # Rectangular frame corners with offsets
                                    # cv2.circle(frame, (xi,yi), 4, (255,0,0), cv2.FILLED)
                                    # cv2.circle(frame, (xi+wi,yi+hi), 4, (0,0,255), cv2.FILLED)

                                    # Draw face box
                                    if self.flg_facebox:
                                        # Draw face tracker rectangle (Rose)
                                        cv2.rectangle(frame, (xi, yi, wi, hi), (255, 0, 255), 2)

                                    # Avoid error on borders
                                    if (xi < 0) or (yi < 0) or (xi+wi > w) or (yi+hi > h):
                                        cv2.putText(frame, f'{xi} | {yi} | {wi} | {hi} | {xi+wi} | {yi+hi}', (100, 375), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255), 1)
                                        wi = 0
                                        hi = 0

                                        self.step = 1
                                    # Centered face
                                    elif (xreb > xrp) & (xleb < xlp):
                                        self.step = 2
                                    
                                # Step 1 image
                                if self.step == 1:
                                    h1, w1, c = self.step1_img.shape
                                    frame[50:50+h1, 913:913+w1] = self.step1_img

                                # Step 2 image
                                if self.step >= 2:
                                    h1, w1, c = self.step2_img.shape
                                    frame[50:50+h1, 913:913+w1] = self.step2_img

                                    # Blink counter
                                    if (right_lenght <= 10) & (left_lenght <= 10) & (blink_flg == False):
                                        self.blink_count += 1
                                        blink_flg = True
                                    elif (right_lenght > 10) & (left_lenght > 10) & (blink_flg == True):
                                        blink_flg = False
                                    
                                    cv2.putText(frame, f'{self.blink_count}', (1055, 140), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 255, 255), 1)

                                    # Blink condition
                                    if self.blink_count >= 3:
                                        self.step = 3
                                else:
                                    self.blink_count = 0
                                    blink_flg = False

                                if self.step == 3:
                                    # Verified image
                                    h1, w1, c = self.liv_ch_img.shape
                                    frame[50:50+h1, 913:913+w1] = self.liv_ch_img
                                    
                                    # Take photo on open eyes (Set a threshold enough to have really open eyes)
                                    if (right_lenght > 15) & (left_lenght > 15):
                                        # Take photo
                                        user_face = frame_tosave[yi:yi+hi, xi:xi+wi]

                                        return frame, user_face

                                        # # Save photo
                                        # cv2.imwrite(f'{faces_path}/{new_user}.png', user_face)

                                        # # Step 1
                                        # liveness_flg = 1

                        else:
                            # No faces detected
                            h0, w0, c = self.nofaces_img.shape
                            frame[195:195+h0, 0:0+w0] = self.nofaces_img
                            self.step = 0


        return frame, None
    
    def find_faces(self, frame_rgb, users, user_faces):
        found_faces = fr.face_locations(frame_rgb)
        encod_faces = fr.face_encodings(frame_rgb, found_faces)

        for enc_face, found_face in zip(encod_faces, found_faces):
            # Match face
            match = fr.compare_faces(user_faces, enc_face)

            # Match error
            err = fr.face_distance(user_faces, enc_face)

            min_err = np.argmin(err)

            if match[min_err]:
                # Get username
                return users[min_err]   # .upper()
        
        return None


class Cameras():
    def __init__(self):
        self.n_cams = self.get_number_of_cams()
    
    def get_number_of_cams(self):
        wmi = win32com.client.GetObject("winmgmts:")
        n = 0
        for device in wmi.InstancesOf("Win32_PnPEntity"):
            if device.PNPClass == 'Camera':
                n += 1
        return n


class Users():
    def __init__(self, users_dir, faces_folder):
        self.users_dir = users_dir
        self.faces_folder = faces_folder
        self.users = None
        self.faces = None

        self.check_dirs_and_folders()

    def update_users(self):
        self.check_dirs_and_folders()

        with open(self.users_dir, 'r') as f:
                self.users = [line.strip().split(';') for line in f if line.strip()]
    
    def add_user(self, user_info, user_face, check=False):
        self.check_dirs_and_folders()

        if (check) or (not self.check_user(user_info[0])):
            with open(self.users_dir, 'a') as f:
                f.write(';'.join(map(str, user_info)) + '\n')
            
            # Save photo
            cv2.imwrite(f'{self.faces_folder}/{user_info[0]}.png', user_face)
            print(f'Welcome {user_info[0]}.')
    
    def check_user(self, user):
        self.update_users()

        for user_info in self.users:
            if (len(user_info) > 0) and (user_info[0] == user):
                return True
        return False
    
    def check_dirs_and_folders(self):
        dir = os.path.dirname(self.users_dir)
        
        # Check if directories exists
        if not os.path.exists(self.faces_folder):
            os.makedirs(self.faces_folder)
            print(f"Dir created: {self.faces_folder}")
        
        if not os.path.exists(dir):
            os.makedirs(dir)
            print(f"Dir created: {dir}")
        
        # Check if file exists
        if not os.path.exists(self.users_dir):
            with open(self.users_dir, 'w') as f:
                pass  # Create empty file
            print(f"File created: {self.users_dir}")
    
    def get_users_and_faces(self):
        faces = []
        users = []

        img_list = os.listdir(self.faces_folder)

        # Read face images
        for img_name in img_list:
            img = cv2.imread(f'{self.faces_folder}/{img_name}')

            # Save temporaly in a list
            faces.append(img)

            # Save user in a list
            users.append(os.path.splitext(img_name)[0])
        
        return users, faces

class FaceRecognition():

    def __init__(self):
        self.Users = Users('projects/face_recognition_system/databases/users.txt',
                           'projects/face_recognition_system/databases/faces')
        
        self.fd = FaceDetector()
        
        self.Cams = Cameras()

        self.main_screen = None
        self.facereg_screen = None
        
        self.bg_img = None
        self.reg_img = None
        self.log_img = None

        self.user_field = None
        self.pass_field = None

        self.video_cap = None
        self.facereg_video = None
        self.running = False        # Control the video cycle
        self.update_id = None       # Stores the after identifier

        self.height = 720
        self.width = 1280

        self.user_face = None

        self.sign_in = False
        self.users = None
        self.user_faces = None
        self.user_detected_flag = False

        self.create_main_screen(self.register_action, self.signin_action)

    def run(self):
        self.main_screen.mainloop()
    
    def create_main_screen(self, register_action, signin_action):
        # Create screen
        self.main_screen = tk.Tk()
        self.main_screen.title('FACE RECOGNITION SYSTEM')
        self.main_screen.geometry('1280x720')

        # Set background and read backgrounds
        self.bg_img = PhotoImage(file='projects/face_recognition_system/images/Main.png')
        background = tk.Label(self.main_screen, image=self.bg_img, text='Inicio')
        background.place(x=0, y=0, relheight=1, relwidth=1)

        # bg_profile_img = tk.PhotoImage(file='projects/face_recognition/setup/Back2.png')

        # Create text input fields
        self.user_field = tk.Entry(self.main_screen, width=23, font=("Arial", 18))
        self.user_field.place(x=181, y=184)

        self.pass_field = tk.Entry(self.main_screen, width=23, font=("Arial", 18), show='*')
        self.pass_field.place(x=181, y=307)

        # Create buttons
        self.reg_img = PhotoImage(file='projects/face_recognition_system/images/RegButton.png')
        reg_btn = tk.Button(self.main_screen, text='Register', image=self.reg_img, command=self.register_action)
        reg_btn.place(x=181, y=400)

        self.log_img = PhotoImage(file='projects/face_recognition_system/images/LogButton.png')
        log_btn = tk.Button(self.main_screen, text='Login', image=self.log_img, command=self.signin_action)
        log_btn.place(x=786, y=578)

    def create_face_detection_ui(self):
        # Face Recognition screen
        self.facereg_screen = tk.Toplevel(self.main_screen)
        self.facereg_screen.title('BIOMETRIC REGISTER')
        self.facereg_screen.geometry('1280x720')

        # Create close protocol after create the screen
        self.facereg_screen.protocol("WM_DELETE_WINDOW", self.close_window)

        self.label = tk.Label(self.facereg_screen, text="Select a camera")
        self.label.pack(pady=10)

        # Label video
        self.facereg_video = tk.Label(self.facereg_screen)
        self.facereg_video.place(x=0, y=0)

        cams = ['No cameras found -1']
        if self.Cams.n_cams > 0:
            cams = [f'Camera {i}' for i in range(self.Cams.n_cams)]

        # Create Dropdown to select cameras
        camera_var = StringVar(value=cams[0])  # Por defecto, la primera cámara
        dropdown = CTkOptionMenu(self.facereg_screen, variable=camera_var,
                                      values=cams, command=self.select_camera,
                                      bg_color='#1668CC', fg_color='#1668CC',
                                      dropdown_fg_color='#1E1E1E', dropdown_hover_color='#22CC5E',
                                      button_color='#1668CC', button_hover_color='#1668CC')
        dropdown.place(x=50, y=50)
    
    def close_window(self):
        if self.main_screen is not None:
            self.main_screen.destroy()
    
    def register_action(self):
        user = self.user_field.get()
        pwd = self.pass_field.get()

        if (len(user) != 0) and (len(pwd) != 0):
            if not self.Users.check_user(user):
                # self.Users.add_user([user, pwd], None, True)
                self.create_face_detection_ui()
            else:
                print(f'User exists. Choose another.')
    
    def signin_action(self):
        self.sign_in = True

        self.users, self.user_faces = self.Users.get_users_and_faces()
        self.user_faces = self.encode_faces(self.user_faces)

        self.create_face_detection_ui()
    
    def select_camera(self, selected_camera):
        """Select the camera to capture video."""

        # Detener la captura de la cámara anterior, si existe
        self.running = False

        if self.update_id:
            self.facereg_video.after_cancel(self.update_id)  # Cancel the current cycle

        # Release any previous capture
        if self.video_cap and self.video_cap.isOpened():
            self.video_cap.release()

        # Get the index of the selected camera
        camera_index = int(selected_camera.split()[-1])  # Extract the index (e.g., 'Camera 1' -> 1)

        # Open the selected camera
        if camera_index >= 0:
            self.video_cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
            self.video_cap.set(3, self.width)     # width
            self.video_cap.set(4, self.height)      # height
            
            # Start video update
            self.running = True
            self.update_video()
    
    def update_video(self):
        if self.running and self.video_cap  and self.video_cap.isOpened():
            ret, frame = self.video_cap.read()

            if ret:
                # Resize
                h, w, c = frame.shape
                frame = imutils.resize(frame, width=self.width)

                # Crop if necessary
                if h < self.height:
                    # Calculate coordinates for centered cropping
                    crop_y_start = int((h*self.width/self.height - self.height) // 2)
                    crop_y_end = crop_y_start + self.height

                    # Crop the image to (self.width ; self.height)
                    frame = frame[crop_y_start:crop_y_end, :]
                
                # Frame to save
                frame_tosave = frame.copy()
                
                # Change color profile
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                frame, self.user_face = self.fd.processs_frame(frame, frame_rgb, frame_tosave)

                # Register user with face
                if not self.sign_in:
                    if self.user_face is not None:
                        self.Users.add_user([self.user_field.get(), self.pass_field.get()], self.user_face)
                else:
                    user_detected = None
                    if not self.user_detected_flag:
                        user_detected = self.fd.find_faces(frame_rgb, self.users, self.user_faces)

                    if user_detected is not None:
                        self.user_detected_flag = True
                        print(f'Welcome {user_detected}')

                # Convert video
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)

                # Show video
                self.facereg_video.configure(image=img)
                self.facereg_video.image = img

            # Continue updating video after 10ms
            self.update_id = self.facereg_video.after(10, self.update_video)

        else:
            self.video_cap.release()
    
    def encode_faces(self, images):
        encoded_faces = []

        for img in images:
            # Color
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Encode
            cod = fr.face_encodings(img)[0]

            # Save to list
            encoded_faces.append(cod)
        
        return encoded_faces
    
if __name__ == "__main__":
    # Create the UI and pass the button functions
    app = FaceRecognition()

    # Start the main loop
    app.run()