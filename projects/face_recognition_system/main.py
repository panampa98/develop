import os
import tkinter as tk
from tkinter import PhotoImage
import win32com.client
import cv2
from PIL import Image, ImageTk
import imutils
from customtkinter import CTkOptionMenu, StringVar

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
            print(f'Welcome {user_info[0]}.')
    
    def check_user(self, user):
        self.update_users()

        for user_info in self.users:
            if (len(user_info) > 0) and (user_info[0] == user):
                print(f'User exists. Choose another.')
                return True
        return False
    
    def check_dirs_and_folders(self):
        dir = os.path.dirname(self.users_dir)
        
        # Check if dir exists
        if not os.path.exists(dir):
            os.makedirs(dir)
            print(f"Dir created: {dir}")
        
        # Check if file exists
        if not os.path.exists(self.users_dir):
            with open(self.users_dir, 'w') as f:
                pass  # Create empty file
            print(f"File created: {self.users_dir}")


class FaceRecognition():

    def __init__(self):
        self.Users = Users('projects/face_recognition_system/databases/users.txt',
                           'projects/face_recognition_system/databases/faces')
        
        # Step images
        self.check_img = cv2.cvtColor(cv2.imread('projects/face_recognition/setup/check.png'), cv2.COLOR_BGR2RGB)
        self.step0_img = cv2.cvtColor(cv2.imread('projects/face_recognition/setup/Step0.png'), cv2.COLOR_BGR2RGB)
        self.step1_img = cv2.cvtColor(cv2.imread('projects/face_recognition/setup/Step1.png'), cv2.COLOR_BGR2RGB)
        self.step2_img = cv2.cvtColor(cv2.imread('projects/face_recognition/setup/Step2.png'), cv2.COLOR_BGR2RGB)
        self.liv_ch_img = cv2.cvtColor(cv2.imread('projects/face_recognition/setup/LivenessCheck.png'), cv2.COLOR_BGR2RGB)
        
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

        self.create_ui()

    def run(self):
        self.main_screen.mainloop()
    
    def create_ui(self):
        self.create_main_screen(self.register_action, self.signin_action)
    
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

    def create_facereg_ui(self):
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
                self.Users.add_user([user, pwd], None, True)
                self.create_facereg_ui()
    
    def signin_action(self):
        self.create_facereg_ui()
    
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
            self.video_cap.set(3, 1280)  # width
            self.video_cap.set(4, 720)  # height
            
            # Start video update
            self.running = True
            self.update_video()
    
    def update_video(self):
        if self.running and self.video_cap  and self.video_cap.isOpened():
            ret, frame = self.video_cap.read()

            if ret:
                # Frame to save
                frame_tosave = frame.copy()

                # Resize
                frame = imutils.resize(frame, width=1280)
                
                # Convert video
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)

                # Show video
                self.facereg_video.configure(image=img)
                self.facereg_video.image = img

            # Continue updating video after 10ms
            self.update_id = self.facereg_video.after(10, self.update_video)

        else:
            self.video_cap.release()
    
if __name__ == "__main__":
    # Create the UI and pass the button functions
    app = FaceRecognition()

    # Start the main loop
    app.run()