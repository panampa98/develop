import os
import tkinter as tk
from tkinter import PhotoImage

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

        if (check) | (not self.check_user(user_info[0])):
            with open(self.users_dir, 'a') as f:
                f.write(';'.join(map(str, user_info)) + '\n')
            print(f'Welcome {user_info[0]}.')
    
    def check_user(self, user):
        self.update_users()

        for user_info in self.users:
            if (len(user_info) > 0) & (user_info[0] == user):
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
        
        self.main_screen = None
        self.facereg_screen = None
        
        self.bg_img = None
        self.reg_img = None
        self.log_img = None

        self.user_field = None
        self.pass_field = None

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

        # Label video
        lbl_video = tk.Label(self.facereg_screen)
        lbl_video.place(x=0, y=0)
    
    def close_window(self):
        if self.main_screen is not None:
            self.main_screen.destroy()
    
    def register_action(self):
        user = self.user_field.get()
        pwd = self.pass_field.get()

        if (len(user) != 0) & (len(pwd) != 0):
            if not self.Users.check_user(user):
                self.Users.add_user([user, pwd], None, True)
                self.create_facereg_ui()
    
    def signin_action(self):
        self.create_facereg_ui()
    
if __name__ == "__main__":
    # Create the UI and pass the button functions
    app = FaceRecognition()

    # Start the main loop
    app.run()