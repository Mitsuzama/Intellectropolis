import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import pyautogui
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

face_cascade = cv2.CascadeClassifier()
# face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
frame_width = 200
frame_height = 200


class HeadTrackingThread(QThread):
    # change_pixmap_signal = pyqtSignal(cv2.cv2)
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        videoStream = cv2.VideoCapture(1)

        while self._run_flag:
            ret, cvImg = videoStream.read()

            if ret:
                cvImg = cv2.flip(cvImg, 1)
                gray = cv2.cvtColor(cvImg, cv2.COLOR_BGR2GRAY)
                faceRects = face_cascade.detectMultiScale(gray, 1.3, 5)

                if len(faceRects) > 0:
                    (x, y, w, h) = faceRects[0]
                    center_x = x + int(w / 2)
                    center_y = y + int(h / 2)

                    screen_width, screen_height = pyautogui.size()
                    mouse_x = int((center_x / frame_width) * screen_width)
                    mouse_y = int((center_y / frame_height) * screen_height)

                    pyautogui.moveTo(mouse_x, mouse_y)

            self.change_pixmap_signal.emit(cvImg)

    def stop(self):
        self._run_flag = False
        self.wait()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Creare și pornire fir de execuție pentru urmărirea capului
        self.head_tracking_thread = HeadTrackingThread()
        self.head_tracking_thread.change_pixmap_signal.connect(self.update_image)
        self.head_tracking_thread.start()

    def update_image(self, cvImg):
        # Actualizare imagine pe interfața grafică
        pass

    def closeEvent(self, event):
        # Oprire fir de execuție la închiderea ferestrei
        self.head_tracking_thread.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
