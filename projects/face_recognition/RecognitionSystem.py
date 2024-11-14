import cv2
import face_recognition as fr
import numpy as np
import mediapipe as mp
import os
from tkinter import *
from PIL import Image, ImageTk
import imutils
import math

users_path = 'projects/face_recognition/databases/users'
faces_path = 'projects/face_recognition/databases/faces'

info = []

screen = Tk()
screen.title('FACE RECOGNITION SYSTEM')
screen.geometry('1280x720')

screen.mainloop()