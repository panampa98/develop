import os
import tkinter as tk
from tkinter import PhotoImage
from customtkinter import CTkOptionMenu, StringVar
from PIL import Image, ImageTk
import imutils
import win32com.client
import cv2
import math
import mediapipe as mp
import face_recognition as fr
import numpy as np

class Users():
    def __init__(self, users_dir, faces_folder):
        self.users_dir = users_dir
        self.faces_folder = faces_folder

        self.users = None
        self.faces = None

        self.check_dirs_and_folders()

    def check_dirs_and_folders(self):
        dir = os.path.dirname(self.users_dir)

        if not os.path.exists(dir):
            os.makedirs(dir)
        
        if not os.path.exists(self.users_dir):
            with open(self.users_dir, 'w'):
                pass
        
        if not os.path.exists(self.faces_folder):
            os.makedirs(self.faces_folder)
    
    def check_user(self, user):
        self.update_users()

        for user_info in self.users:
            if (len(user) > 0) and (user_info[0] == user):
                return True
        return False

    def update_users(self):
        with open(self.users_dir, 'r') as f:
            self.users = [line.strip().split(';') for line in f if line.strip()]
    
    def add_user(self, user_info, user_face):
        if (not self.check_user(user_info[0])):
            with open(self.users_dir, 'a') as f:
                f.write(';'.join(map(str, user_info)) + '\n')
            
            cv2.imwrite(f'{self.faces_folder}/{user_info[0]}.png', user_face)
            print(f'Welcome {user_info[0]}')
    
    def get_users_and_faces(self):
        faces = []
        users = []

        img_list = os.listdir(self.faces_folder)

        for img_name in img_list:
            img = cv2.imread(f'{self.faces_folder}/{img_name}')

            faces.append(img)

            users.append(os.path.splitext(img_name)[0])
        
        return users, faces


class Cameras():
    def __init__(self):
        self.n_cams = self.get_number_of_cams()

    def get_number_of_cams(self):
        wmi = win32com.client.GetObject('winmgmts:')

        n = 0

        for device in wmi.InstancesOf('Win32_PnPEntity'):
            if device.PNPClass == 'Camera':
                n+=1
        
        return n


class FaceDetector():
    def __init__(self, th=0.5, off_x=0.3, off_y=0.4):
        # Draw tool
        self.mp_draw = mp.solutions.drawing_utils
        self.draw_config = self.mp_draw.DrawingSpec(thickness=1, circle_radius=1)

        # Face mesh
        self.face_mesh_object = mp.solutions.face_mesh
        self.face_mesh = self.face_mesh_object.FaceMesh(max_num_faces=1, refine_landmarks=True)

        # Face detector
        self.face_detector_object = mp.solutions.face_detection
        self.face_detector = self.face_detector_object.FaceDetection(min_detection_confidence=0.5, model_selection=1)

        # Threshold
        self.th = th

        # Offsets
        self.off_x, self.off_y = off_x, off_y

        # Step images
        self.nofaces_img = cv2.cvtColor(cv2.imread('projects/fr_system/images/no_faces.png'), cv2.COLOR_BGR2RGB)
        self.face_det_img = cv2.cvtColor(cv2.imread('projects/fr_system/images/step0.png'), cv2.COLOR_BGR2RGB)
        self.step1_img = cv2.cvtColor(cv2.imread('projects/fr_system/images/step1.png'), cv2.COLOR_BGR2RGB)
        self.step2_img = cv2.cvtColor(cv2.imread('projects/fr_system/images/step2.png'), cv2.COLOR_BGR2RGB)
        self.liv_ch_img = cv2.cvtColor(cv2.imread('projects/fr_system/images/verified.png'), cv2.COLOR_BGR2RGB)

        self.step = 0

        self.blink_count = 0
        self.blink_flag = False

        self.flg_facebox = True

        self.color_faceframe = (255, 0, 255) # Magenta
        self.width_faceframe = 2

    def process_frame(self, frame, frame_rgb, frame_tosave):

        face_landmarks = self.face_mesh.process(frame_rgb)

        px = []
        py = []
        p_list = []

        if face_landmarks.multi_face_landmarks:
            for face_landmark_list in face_landmarks.multi_face_landmarks:
                self.mp_draw.draw_landmarks(image=frame,
                                            landmark_list=face_landmark_list,
                                            connections=self.face_mesh_object.FACEMESH_CONTOURS,
                                            landmark_drawing_spec=self.draw_config,
                                            connection_drawing_spec=self.draw_config)
                
                for id, points in enumerate(face_landmark_list.landmark):
                    h, w, c = frame.shape
                    x, y = int(points.x*w), int(points.y*h)

                    px.append(x)
                    py.append(y)
                    p_list.append([id, x, y])

                    if len(p_list) == 468:
                        # Right eye
                        xr1, yr1 = p_list[145][1:]
                        xr2, yr2 = p_list[159][1:]
                        right_lenght = math.hypot(xr2-xr1, yr2-yr1)

                        cv2.circle(frame, (xr1, yr1), 2, (255,0,0), cv2.FILLED)
                        cv2.circle(frame, (xr2, yr2), 2, (255,0,0), cv2.FILLED)

                        # Left eye
                        xl1, yl1 = p_list[374][1:]
                        xl2, yl2 = p_list[386][1:]
                        left_lenght = math.hypot(xl2-xl1, yl2-yl1)

                        cv2.circle(frame, (xl1, yl1), 2, (255,0,0), cv2.FILLED)
                        cv2.circle(frame, (xl2, yl2), 2, (255,0,0), cv2.FILLED)

                        # Parietals
                        xrp, yrp = p_list[139][1:]
                        xlp, ylp = p_list[368][1:]
                        cv2.circle(frame, (xrp, yrp), 2, (255,0,0), cv2.FILLED)
                        cv2.circle(frame, (xlp, ylp), 2, (255,0,0), cv2.FILLED)

                        # Eyebrows
                        xreb, yreb = p_list[70][1:]
                        xleb, yleb = p_list[300][1:]
                        cv2.circle(frame, (xreb, yreb), 2, (255,0,0), cv2.FILLED)
                        cv2.circle(frame, (xleb, yleb), 2, (255,0,0), cv2.FILLED)

                        faces = self.face_detector.process(frame_rgb)

                        if faces.detections is not None:
                            for face in faces.detections:
                                scr = face.score[0]
                                bbox = face.location_data.relative_bounding_box

                                h0, w0, c = self.face_det_img.shape
                                frame[195:195+h0,0:0+w0] = self.face_det_img

                                right_rat = -1
                                left_rat = -1

                                if scr > self.th:
                                    xi, yi, wi, hi = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                    xi, yi, wi, hi = int(xi*w), int(yi*h), int(wi*w), int(hi*h)

                                    off_width = self.off_x*wi
                                    xi = int(xi-off_width/2)
                                    wi = int(wi + off_width)

                                    off_height = self.off_y*hi
                                    yi = int(yi-off_height/2)
                                    hi = int(hi + off_height)

                                    if self.flg_facebox:
                                        cv2.rectangle(frame, (xi,yi,wi,hi), self.color_faceframe, self.width_faceframe)

                                    if (xi < 0) or (yi < 0) or (xi+wi > w) or (yi+hi > h):
                                        wi = 0
                                        hi = 0

                                        self.step = 1
                                    elif (xreb > xrp) and (xleb < xlp):
                                        self.step = 2

                                        right_rat = round(100.0*right_lenght/hi, 1)
                                        left_rat = round(100.0*left_lenght/hi, 1)
                                else:
                                    self.step = 1
                                
                                if self.step == 1:
                                    h1, w1, c = self.step1_img.shape
                                    frame[50:50+h1, 913:913+w1] = self.step1_img
                                
                                if self.step >= 2:
                                    h1, w1, c = self.step2_img.shape
                                    frame[50:50+h1, 913:913+w1] = self.step2_img

                                    # Blink counter
                                    if (right_rat > 0) and (right_rat <= 1.5) and (left_rat > 0) and (left_rat <= 1.5) and (self.blink_flag == False):
                                        self.blink_count += 1
                                        self.blink_flag = True

                                    elif (right_rat > 3.4) and (left_rat > 3.4) and (self.blink_flag == True):
                                        self.blink_flag = False
                                    
                                    cv2.putText(frame, f'{self.blink_count}', (1055,140), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 255, 255), 1)

                                    if self.blink_count >= 3:
                                        self.step = 3
                                else:
                                    self.blink_count = 0
                                    self.blink_flag = False
                                
                                if self.step == 3:
                                    h1, w1, c = self.liv_ch_img.shape
                                    frame[50:50+h1, 913:913+w1] = self.liv_ch_img

                                    if (right_rat > 3.4) and (left_rat > 3.4):
                                        # Take photo
                                        user_face = frame_tosave[yi:yi+hi, xi:xi+wi]

                                        return frame, user_face
                        else:
                            h1, w1, c = self.nofaces_img.shape
                            frame[195:195+h1, 0:0+w1] = self.nofaces_img

                            self.step = 0
                            self.blink_count = 0
                            self.blink_flag = 0
        
        return frame, None
    
    def find_faces(self, frame_rgb, users, user_faces):
        found_faces = fr.face_locations(frame_rgb)
        encod_faces = fr.face_encodings(frame_rgb, found_faces)

        for enc_face, found_face in zip(encod_faces, found_faces):
            match = fr.compare_faces(user_faces, enc_face)

            err = fr.face_distance(user_faces, enc_face)
            min_error = np.argmin(err)

            if match[min_error]:
                return users[min_error]
        
        return None
    
    def get_step(self):
        return self.step
    
    def set_faceframe_params(self, color, width):
        self.color_faceframe = color
        self.width_faceframe = width
    
    def reset_params(self):
        self.step = 0
        self.blink_count = 0

class FaceRecognition():
    def __init__(self):
        self.Users = Users('projects/fr_system/databases/users.txt',
                           'projects/fr_system/databases/faces')
        self.Cams = Cameras()
        self.fd = FaceDetector()

        self.main_screen = None
        self.facedet_ui = None
        self.bg_img = None

        self.name_field = None
        self.id_field  = None

        self.video_cap = None
        self.running = False
        self.update_id = None

        self.width = 1280
        self.height = 720

        self.sign_in = False

        self.user_face = None
        self.valid_face_flag = False
        self.users, self.user_faces = None, None

        self.create_main_screen()

    def run(self):
        self.main_screen.mainloop()

    def create_main_screen(self):
        self.main_screen = tk.Tk()
        self.main_screen.title('FACE RECOGNITION SYSTEM')
        self.main_screen.geometry('1280x720')

        self.bg_img = PhotoImage(file='projects/fr_system/images/Main.png')
        background = tk.Label(self.main_screen, image=self.bg_img, text='')
        background.place(x=0, y=0, relheight=1, relwidth=1)

        self.name_field = tk.Entry(self.main_screen, width=23, font=('Arial', 18))
        self.name_field.place(x=181, y=184)

        self.id_field = tk.Entry(self.main_screen, width=23, font=('Arial', 18))
        self.id_field.place(x=181, y=307)

        self.reg_img = PhotoImage(file='projects/fr_system/images/RegButton.png')
        reg_btn = tk.Button(self.main_screen, text='', image=self.reg_img, command=self.register_action)
        reg_btn.place(x=181, y=400)

        self.log_img = PhotoImage(file='projects/fr_system/images/LogButton.png')
        log_btn = tk.Button(self.main_screen, text='', image=self.log_img, command=self.signin_action)
        log_btn.place(x=786, y=535)
    
    def register_action(self):
        self.sign_in = False
        user_name = self.name_field.get()
        user_id = self.id_field.get()

        if (len(user_name) > 0) and (len(user_id) > 0):
            if not self.Users.check_user(user_name):
                # self.Users.add_user([user_name, user_id])
                self.create_face_detection_ui()
    
    def signin_action(self):
        self.sign_in = True
        
        self.users, self.user_faces = self.Users.get_users_and_faces()
        self.user_faces =  self.encode_faces(self.user_faces)

        self.create_face_detection_ui()

    
    def create_face_detection_ui(self):
        self.facedet_ui = tk.Toplevel(self.main_screen)
        self.facedet_ui.title('FACE DETECTOR')
        self.facedet_ui.geometry('1280x720')

        self.facedet_ui.protocol('WM_DELETE_WINDOW', self.close_window)

        label = tk.Label(self.facedet_ui, text='Select a camera')
        label.place(x=300, y=50)

        self.face_video = tk.Label(self.facedet_ui)
        self.face_video.place(x=0, y=0)

        cams = ['No cameras found -1']
        if self.Cams.n_cams > 0:
            cams = [f'Camera {i}' for i in range(self.Cams.n_cams)]

        camera_var = StringVar(value=cams[0])
        dropdown = CTkOptionMenu(self.facedet_ui, variable=camera_var,
                                 values=cams, command=self.select_camera,
                                 bg_color='#1668CC', fg_color='#1668CC',
                                 button_color='#1668CC', button_hover_color='#1668CC',
                                 dropdown_fg_color='#1E1E1E', dropdown_hover_color='#22CC5E')
        dropdown.place(x=50, y=50)
    
    def select_camera(self, selected_camera):

        self.fd.reset_params()

        self.running = False

        camera_index = int(selected_camera.split()[-1])

        if self.update_id:
            self.face_video.after_cancel(self.update_id)

        if camera_index >= 0:
            self.video_cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
            self.video_cap.set(3, self.width)
            self.video_cap.set(4, self.height)

            self.update_video()

    def update_video(self):
        if self.video_cap and self.video_cap.isOpened():
            ret, frame = self.video_cap.read()

            if ret:
                h, w, c = frame.shape

                frame = imutils.resize(frame, width=self.width)
            
                if h < self.height:
                    crop_y_start = int((h*self.width/self.height - self.height) // 2)
                    crop_y_end = crop_y_start + self.height

                    frame = frame[crop_y_start:crop_y_end, :]
                
                frame_tosave = frame.copy()

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                frame, self.user_face = self.fd.process_frame(frame, frame_rgb, frame_tosave)
                step = self.fd.get_step()

                user_detected = None

                if (step != 3):
                    self.fd.set_faceframe_params((255, 0, 255), 2)
                    self.valid_face_flag = False

                if not self.sign_in:
                    if self.user_face is not None:
                        self.Users.add_user([self.name_field.get(), self.id_field.get()], self.user_face)
                elif self.user_face is not None:
                    if not self.valid_face_flag:
                        user_detected = self.fd.find_faces(frame_rgb, self.users, self.user_faces)
                    
                    # Valid face
                    if (user_detected is not None) and (step == 3):
                        self.valid_face_flag = True
                        self.fd.set_faceframe_params((0, 255, 0), 6)
                    
                    # Invalid face
                    if (not self.valid_face_flag) and (step == 3):
                        self.fd.set_faceframe_params((255, 0, 0), 6)


                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)

                self.face_video.configure(image=img)
                self.face_video.image = img

            self.update_id = self.face_video.after(10, self.update_video)
        
        else:
            self.video_cap.release()

    def encode_faces(self, imgs):
        encoded_faces = []

        for img in imgs:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            cod = fr.face_encodings(img)[0]

            encoded_faces.append(cod)
        
        return encoded_faces
    
    def close_window(self):
        if self.main_screen is not None:
            self.main_screen.destroy()


if __name__ == '__main__':
    app = FaceRecognition()

    app.run()