from tests.functions import signup, signin
import tkinter as tk
from tkinter import PhotoImage

class FaceRecognition():

    def __init__(self, register_action, signin_action):
        self.ui = None
        self.create_ui(register_action, signin_action)

    def run(self):
        self.ui.mainloop()
    
    def create_ui(self, register_action, signin_action):
        # Create screen
        self.ui = tk.Tk()
        self.ui.title('FACE RECOGNITION SYSTEM')
        self.ui.geometry('1280x720')

        # Set background and read backgrounds
        bg_img = PhotoImage(file='projects/face_recognition_system/images/Main.png')
        background = tk.Label(self.ui, image=bg_img, text='Inicio')
        background.place(x=0, y=0, relheight=1, relwidth=1)

        # bg_profile_img = tk.PhotoImage(file='projects/face_recognition/setup/Back2.png')

        # Create text input fields
        user_field = tk.Entry(self.ui, width=23, font=("Arial", 18))
        user_field.place(x=181, y=184)

        pass_field = tk.Entry(self.ui, width=23, font=("Arial", 18), show='*')
        pass_field.place(x=181, y=307)

        # Create buttons
        reg_img = PhotoImage(file='projects/face_recognition_system/images/RegButton.png')
        reg_btn = tk.Button(self.ui, text='Register', image=reg_img, command=register_action)
        reg_btn.place(x=181, y=400)

        log_img = PhotoImage(file='projects/face_recognition_system/images/LogButton.png')
        log_btn = tk.Button(self.ui, text='Login', image=log_img, command=signin_action)
        log_btn.place(x=786, y=578)

        # Return the main window
        self.ui.mainloop()

if __name__ == "__main__":
    # Create the UI and pass the button functions
    app = FaceRecognition(signup, signin)

    # Start the main loop
    app.run()