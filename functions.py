"""
Nume proiect: PokEevee
Autor: Chelarașu Elena-Denisa
Versiune: 1.0.0
Descriere: Acest proiect este un joc în care trebuie să ajuți Eevee să evite Pokeball-urile și să rămână un Pokemon sălbatic.
"""

import json
import random
import time
import pygame
import pyttsx3
import sys

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QPixmap, QColor, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QDesktopWidget
from PyQt5.uic.properties import QtCore
from pyttsx3 import engine
from PyQt5.QtCore import QThread
from audio_input import VoiceCommandThread


# Funcție pentru redarea sunetelor de fundal
def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


# Funcție pentru citirea culorilor dintr-un fișier JSON
def read_colors_from_file(file_path):
    with open(file_path, 'r') as file:
        colors_data = json.load(file)
    return colors_data


# Salvarea culorilor intr-o variabila globala
jsonList = read_colors_from_file("./colors.json")


class GameOverSignal(QWidget):
    game_over_signal = pyqtSignal(int)


class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PokEevee")
        self.setGeometry(300, 300, 500, 500)
        # self.center_on_screen()
        self.setStyleSheet(f'''
             background: {jsonList['backgroundColor']};
        ''')

        label = QLabel("PokEevee", self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(f'''
            font-size: 40px;
            color: {jsonList['titleColor']};
            font-weight: bold;
            font-family: "Crete Round";
            text-align: center;
            padding: 5px;
            margin-top: 50px;
            font-weight: bold;
        ''')

        label2 = QLabel("Ajut-o pe Eevee să rămână\n un Pokemon sălbatic\n și evită Pokeball-urile care vin spre ea!",
                        self)
        label2.setAlignment(Qt.AlignCenter)
        label2.setStyleSheet(f'''
            font-size: 30px;
            color: {jsonList["messageColor"]};
            font-weight: bold;
            font-family: "Crete Round";
            text-align: center;
            padding: 75px;
            margin-top: 20px;
        ''')

        play_button = QPushButton("Începe jocul", self)
        play_button.setStyleSheet(f'''
                    QPushButton {{
                        border: 4px solid {jsonList['buttonColor']};
                        border-radius: 45px;
                        font-size: 35px;
                        padding: 25px 0;
                        margin: 50px 50px;
                        color: {jsonList["black"]};
                    }}
                    QPushButton:hover {{
                        background: {jsonList['buttonColor']};
                    }}
                ''')
        play_button.clicked.connect(self.open_game_window)

        exit_button = QPushButton("Ieșire", self)
        exit_button.setStyleSheet(f'''
                    QPushButton {{
                        border: 4px solid {jsonList['buttonColor']};
                        border-radius: 45px;
                        font-size: 35px;
                        padding: 25px 0;
                        margin: 50px 50px;
                        color: {jsonList["black"]};
                    }}
                    QPushButton:hover {{
                        background: {jsonList['buttonColor']};
                    }}
                ''')
        exit_button.clicked.connect(self.close_func)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(label2)
        layout.addWidget(play_button)
        layout.addWidget(exit_button)

        self.setLayout(layout)

    """
    close_func() este apelata atunci cand utilizatorul apasa butonul "Iesire".
    Aceasta reda un sunet de notificare, asteapta 1 secunda si inchide fereastra curenta.
    """

    def close_func(self):
        play_sound("notification_ambient.mp3")
        time.sleep(1)
        self.close()

    """
    open_game_window() este apelata atunci cand utilizatorul apasa butonul "Incepe jocul".
    Aceasta ascunde fereastra curenta, reda un sunet de fundal si deschide fereastra jocului.
    De asemenea, se conecteaza semnalul game_over_signal al ferestrei jocului la metoda show_game_over_window().
    """

    def open_game_window(self):
        self.hide()
        play_sound("abstract-sounds-02.mp3")
        self.game_window = GameWindow()
        self.game_window.game_over_signal.connect(self.show_game_over_window)
        self.game_window.show()

    """
    show_game_over_window(score) este apelata atunci cand jocul se incheie si se afiseaza fereastra de final.
    Aceasta ascunde fereastra curenta, creeaza si afiseaza fereastra de final (GameOverWindow).
    De asemenea, se conecteaza semnalul game_over_signal al ferestrei de final la metoda show_menu_window().
    """

    def show_game_over_window(self, score):
        self.hide()
        game_over_window = GameOverWindow(score)
        game_over_window.game_over_signal.connect(self.show_menu_window)
        game_over_window.show()

    """
    center_on_screen() centreaza fereastra curenta pe ecranul dispozitivului.
    Aceasta calculeaza coordonatele x si y pentru a plasa fereastra in centrul ecranului.
    """

    def center_on_screen(self):
        screen_geometry = QApplication.desktop().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)


class GameWindow(GameOverSignal, QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('PokEevee')
        self.setStyleSheet(f"""
                    background-color: {jsonList["backgroundColor"]};  /* Schimbă culoarea de fundal */
                """)
        self.center_on_screen()

        self.character_x = 250
        self.character_width = 100
        self.character_height = 100
        self.object_size = 40

        self.character_image = QPixmap('eevee.png').scaled(self.character_width, self.character_height)
        self.object_image = QPixmap('pokeball.svg.png').scaled(self.object_size, self.object_size)

        self.objects = []
        self.score = 0
        self.lives = 5

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(10)

        self.show()

    """
    paintEvent(event) deseneaza elementele grafice ale jocului pe fereastra.
    deseneaza personajul principal (Eevee), obiectele (pokeball-uri), scorul si numarul de vieti.
    """

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.character_x, self.height() - self.character_height, self.character_image)

        for obj in self.objects:
            painter.drawPixmap(obj['x'], obj['y'], self.object_image)

        painter.setPen(QColor(jsonList["messageColor"]))  # Set label color to #81C4E3
        font = QFont('Arial', 12)
        font.setBold(True)  # Set the font to bold
        painter.setFont(font)
        painter.drawText(10, 20, f"Scor: {self.score}")
        painter.drawText(10, 40, f"Vieți rămase: {self.lives}")

    """
    keyPressEvent(event) gestioneaza evenimentul apasarii unei taste.
    Daca tasta apasata este Sagetă-Stanga, personajul se deplaseaza spre stanga.
    Daca tasta apasata este Sagetă-Dreapta, personajul se deplaseaza spre dreapta.
    """

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.character_x -= 10
            self.character_x = max(self.character_x, 0)
        elif event.key() == Qt.Key_Right:
            self.character_x += 10
            self.character_x = min(self.character_x, self.width() - self.character_width)

    """
    update_game() actualizeaza starea jocului la fiecare interval de timp.
    Aceasta actualizeaza pozitia obiectelor, verifica coliziunile, si redeseneaza fereastra.
    """

    def update_game(self):
        self.update_objects()
        self.check_collision()
        self.repaint()

    """
    update_objects() actualizeaza pozitia obiectelor pe ecran.
    Obiectele se misca in jos si sunt eliminate daca ies din fereastra.
    Daca numarul de obiecte este mai mic de 5, se genereaza un nou obiect.
    """

    def update_objects(self):
        for obj in self.objects:
            obj['y'] += 1
            if obj['y'] > self.height():
                self.objects.remove(obj)
                self.score += 1
                play_sound("alert-03.mp3")

        if len(self.objects) < 5:
            self.spawn_object()

    """
    spawn_object() generează un obiect nou și îl adaugă în lista de obiecte.
    Poziția obiectului este aleatorie pe axa x, iar pe axa y este setată la 0.
    """

    def spawn_object(self):
        obj_x = random.randint(0, self.width() - self.object_size)
        obj_y = 0
        self.objects.append({'x': obj_x, 'y': obj_y})

    """
    check_collision() verifică coliziunile dintre personaj și obiecte.
    Dacă există o coliziune, obiectul este eliminat, numărul de vieți este decrementat,
    și se verifică dacă jocul s-a încheiat.
    """

    def check_collision(self):
        character_rect = self.character_image.rect().translated(self.character_x, self.height() - self.character_height)
        for obj in self.objects:
            obj_rect = self.object_image.rect().translated(obj['x'], obj['y'])
            if character_rect.intersects(obj_rect):
                self.objects.remove(obj)
                self.lives -= 1

                play_sound("positive-selection.mp3")
                if self.lives == 0:
                    self.game_over()

    """
    game_over() afișează fereastra de game over și oprește cronometrul.
    De asemenea, afișează scorul final al jocului.
    """

    def game_over(self):
        self.hide()
        self.timer.stop()
        print(f"Game Over! Your score: {self.score}")
        self.game_over_window = GameOverWindow(self.score)
        self.game_over_window.show()

    """
    center_on_screen() centreaza fereastra curenta pe ecranul dispozitivului.
    Aceasta calculeaza coordonatele x si y pentru a plasa fereastra in centrul ecranului.
    """

    def center_on_screen(self):
        screen_geometry = QApplication.desktop().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)


class GameOverWindow(QWidget):
    def __init__(self, score):
        super().__init__()

        self.setWindowTitle("Sfarsitul jocului")
        self.setGeometry(0, 0, 500, 300)
        self.center_on_screen()

        label1 = QLabel("Sfârșitul jocului", self)
        label1.setAlignment(Qt.AlignCenter)
        label1.setStyleSheet(f'''
                    font-size: 40px;
                    color: {jsonList['titleColor']};
                    font-weight: bold;
                    font-family: "Crete Round";
                    text-align: center;
                    padding: 5px;
                    margin-top: 50px;
                    font-weight: bold;
                ''')

        label2 = QLabel(f"Scorul tău este: {score}", self)
        label2.setAlignment(Qt.AlignCenter)
        label2.setStyleSheet(f'''
                            font-size: 30px;
                            color: {jsonList['titleColor']};
                            font-weight: bold;
                            font-family: "Crete Round";
                            text-align: center;
                            padding: 5px;
                            margin-top: 50px;
                            font-weight: bold;
                        ''')

        back_button = QPushButton("Înapoi la meniu", self)
        back_button.setStyleSheet(f'''
                    QPushButton {{
                        border: 4px solid {jsonList['buttonColor']};
                        border-radius: 45px;
                        font-size: 35px;
                        padding: 25px 0;
                        margin: 50px 50px;
                        color: {jsonList["black"]};
                    }}
                    QPushButton:hover {{
                        background: {jsonList['buttonColor']};
                    }}
                ''')
        back_button.clicked.connect(self.back_to_menu)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(back_button)

        self.setLayout(layout)

    """
    back_to_menu() ascunde fereastra curentă și deschide fereastra meniului principal.
    """

    def back_to_menu(self):
        self.hide()
        play_sound("abstract-sounds-02.mp3")
        self.menu_window = MenuWindow()
        self.menu_window.show()

    """
    center_on_screen() centreaza fereastra curenta pe ecranul dispozitivului.
    Aceasta calculeaza coordonatele x si y pentru a plasa fereastra in centrul ecranului.
    """

    def center_on_screen(self):
        screen_geometry = QApplication.desktop().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu_window = MenuWindow()
    play_sound("background.mp3")
    menu_window.show()
    audiot = VoiceCommandThread()
    audiot.start()

    sys.exit(app.exec_())
