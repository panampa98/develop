from tests.functions import signup, signin
import tkinter as tk
from tkinter import PhotoImage

class FaceRecognition():

    def __init__(self):
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
        if (len(self.user_field.get()) != 0) & (len(self.pass_field.get()) != 0):
            self.create_facereg_ui()
    
    def signin_action(self):
        self.create_facereg_ui()
    
if __name__ == "__main__":
    # Create the UI and pass the button functions
    app = FaceRecognition()

    # Start the main loop
    app.run()