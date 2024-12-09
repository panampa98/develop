import cv2
import tkinter as tk
from tkinter import OptionMenu, ttk
from customtkinter import CTkOptionMenu, StringVar

class CameraSelectorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Camera Selector")
        self.master.geometry("400x200")

        # Detectar cámaras disponibles
        self.cameras = self.detect_cameras()

        # Crear Dropdown para seleccionar cámaras
        self.camera_var = StringVar(value=self.cameras[0])  # Por defecto, la primera cámara
        self.dropdown = CTkOptionMenu(self.master, variable=self.camera_var, values=self.cameras, command=self.select_camera)
        self.dropdown.pack(pady=20)

        # Etiqueta para mostrar la cámara seleccionada
        self.label = tk.Label(self.master, text="Selecciona una cámara")
        self.label.pack(pady=10)

        # Inicializar captura de video
        self.video_cap = None
        self.select_camera(self.camera_var.get())

    def detect_cameras(self):
        """Detecta las cámaras disponibles."""
        cameras = []
        for i in range(2):  # Intenta detectar hasta 10 cámaras
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap.isOpened():
                cameras.append(f"Camera {i}")
                cap.release()
        return cameras if cameras else ["No cameras found"]

    def select_camera(self, selected_camera):
        """Selecciona la cámara para capturar video."""
        # Obtener el índice de la cámara seleccionada
        camera_index = int(selected_camera.split()[-1])  # Extraer el índice (e.g., 'Camera 1' -> 1)

        # Liberar cualquier captura previa
        if self.video_cap:
            self.video_cap.release()

        # Abrir la cámara seleccionada
        self.video_cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        self.video_cap.set(3, 1280)  # Ancho
        self.video_cap.set(4, 720)  # Alto

        self.label.config(text=f"Usando {selected_camera}")

    def close(self):
        """Cierra la aplicación y libera recursos."""
        if self.video_cap:
            self.video_cap.release()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraSelectorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)  # Asegura liberar recursos al cerrar
    root.mainloop()
