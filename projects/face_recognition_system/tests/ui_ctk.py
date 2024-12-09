import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from functions import signup, signin

def create_ui(signup_action, signin_action):
    # Create the main window
    root = ctk.CTk()
    root.title('Sign Up and Sign In Form')

    # Set the initial size of the window to 720x1080
    root.geometry('1280x720')

    # Load and set the background image
    # bg_img = 'projects/face_recognition/setup/Inicio.png'
    bg_img = 'projects/face_recognition_system/images/Main.png'
    background_image = ctk.CTkImage(light_image=Image.open(bg_img), size=(1280, 720))                                         # Replace with your image file
    background_label = ctk.CTkLabel(root, image=background_image, text='')          # Label to hold the image
    background_label.place(relwidth=1, relheight=1)                                 # Stretch to fill the entire window

    # Configure the main columns
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)

    # Configure the left frame (Sign Up)
    frame_left = ctk.CTkFrame(root, corner_radius=200)
    frame_left.grid(row=0, column=0, padx=20, pady=20)
    frame_left.columnconfigure(0, weight=1)
    frame_left.columnconfigure(1, weight=1)
    frame_left.rowconfigure(0, weight=1)
    frame_left.rowconfigure(1, weight=1)
    frame_left.rowconfigure(2, weight=1)
    frame_left.rowconfigure(3, weight=1)
    frame_left.rowconfigure(4, weight=1)

    bg_left_frm = ctk.CTkLabel(frame_left, text='')          # Label to hold the image
    bg_left_frm.place(relwidth=1, relheight=1)  

    # Configure the right frame (Sign In)
    frame_right = ctk.CTkFrame(root)
    frame_right.grid(row=0, column=1, padx=20, pady=20, sticky='ns')
    frame_right.columnconfigure(0, weight=1)
    frame_right.rowconfigure(0, weight=1)
    frame_right.rowconfigure(1, weight=1)
    frame_right.rowconfigure(2, weight=1)
    frame_right.rowconfigure(3, weight=1)
    frame_right.rowconfigure(4, weight=1)

    ctk.CTkLabel(frame_left, text='Register', font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=20)

    # User label and entry
    ctk.CTkLabel(frame_left, text='User').grid(row=1, column=0, sticky='e', padx=5, pady=20)
    ctk.CTkEntry(frame_left).grid(row=1, column=1, sticky='ew', padx=5, pady=20)

    # Name label and entry
    ctk.CTkLabel(frame_left, text='Name').grid(row=2, column=0, sticky='e', padx=5, pady=20)
    ctk.CTkEntry(frame_left).grid(row=2, column=1, sticky='ew', padx=5, pady=20)

    # Password label and entry
    ctk.CTkLabel(frame_left, text='Password').grid(row=3, column=0, sticky='e', padx=5, pady=20)
    ctk.CTkEntry(frame_left, show='*').grid(row=3, column=1, sticky='ew', padx=5, pady=20)

    # Sign Up button
    btn_signup = ctk.CTkButton(frame_left, text='Sign Up', width=150, height=30, command=signup_action)
    btn_signup.grid(row=4, column=0, columnspan=2, padx=5, pady=20)

    # Sign In button
    btn_signin = ctk.CTkButton(frame_right, text='Sign In', width=150, height=30, command=signin_action)
    btn_signin.grid(row=3, column=0, padx=5, pady=20)

    # Return the main window
    return root

if __name__ == "__main__":
    # Create the UI and pass the button functions
    app = create_ui(signup, signin)

    # Start the main loop
    app.mainloop()