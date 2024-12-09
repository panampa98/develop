import tkinter as tk
from PIL import Image, ImageTk
from tkinter import PhotoImage
import customtkinter as ctk
from functions import signup, signin

class MyApp():
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
    root.columnconfigure(2, weight=1)
    root.columnconfigure(3, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)
    root.rowconfigure(3, weight=1)
    root.rowconfigure(4, weight=1)

    ctk.CTkLabel(root, text='Register', font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=20)

    # User label and entry
    ctk.CTkLabel(root, text='User').grid(row=1, column=0, sticky='e', padx=5, pady=20)
    ctk.CTkEntry(root).grid(row=1, column=1, sticky='ew', padx=5, pady=20)

    # Name label and entry
    ctk.CTkLabel(root, text='Name').grid(row=2, column=0, sticky='e', padx=5, pady=20)
    ctk.CTkEntry(root).grid(row=2, column=1, sticky='ew', padx=5, pady=20)

    # Password label and entry
    ctk.CTkLabel(root, text='Password').grid(row=3, column=0, sticky='e', padx=5, pady=20)
    ctk.CTkEntry(root, show='*').grid(row=3, column=1, sticky='ew', padx=5, pady=20)

    # Sign Up button
    btn_signup = ctk.CTkButton(root, text='Sign Up', width=150, height=30, command=signup)
    btn_signup.grid(row=4, column=0, columnspan=2, padx=5, pady=20)

    btn_img = 'projects/face_recognition_system/images/LogButton.png'
    button_image = PhotoImage(file=btn_img) 
    # Sign In button
    btn_signin = tk.Button(root, text='', command=signin, image=button_image, height=40, width=300)
    btn_signin.grid(row=3, column=3)

app = MyApp()
app.root.mainloop()