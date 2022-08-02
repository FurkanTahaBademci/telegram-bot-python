import os
import pyautogui

def screenshot():
    ekran_goruntusu = pyautogui.screenshot()
    dosya_adi = "output/screen.jpg"
    dosya_yolu = os.path.join(dosya_adi)
    ekran_goruntusu.save(dosya_yolu)

