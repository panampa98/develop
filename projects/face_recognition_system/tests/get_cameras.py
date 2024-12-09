import cv2
import win32com.client

def get_camera_names_windows():
    """Obtiene los nombres descriptivos de las cámaras en Windows."""
    cameras = {}
    wmi = win32com.client.GetObject("winmgmts:")
    count = 0
    for device in wmi.InstancesOf("Win32_PnPEntity"):
        # if (device.Name is not None) and (device.Service is not None):
        #     print(f'{(device.Name):<60}| {(device.Service):<20}| {device.PNPClass:<20}| {device.DeviceID:<20}')
        if device.PNPClass == 'Camera':
            print(f'{(device.Name):<60}| {(device.Service):<20}| {device.PNPClass:<20}| {device.DeviceID:<20}')
            cameras[count] = device.Name
            count += 1
    return cameras

# Mostrar nombres de cámaras con índices
if __name__ == "__main__":
    cameras = get_camera_names_windows()

    print(cameras)
