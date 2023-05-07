import json
import sys
import cmd
import os
import pandas as pd
from urllib.request import urlopen

from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtCore
import random
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout

from utils import read_colors_from_file, buttonClicked

json_file_path = 'colors.json'
parameters = {
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "correct": [],
    "score": [0],
    "index": []
}

widgets = {
        "logo": [],
        "button": [],
        "score": [],
        "question": [],
        "answer1": [],
        "answer2": [],
        "answer3": [],
        "answer4": [],
        "message": [],
        "message2": [],
        "scoreboard": [],
        "return_button": [],
        "score_labels": []
    }
with urlopen("https://opentdb.com/api.php?amount=50&category=18&difficulty=medium&type=multiple") as webpage:
    # read JSON file & extract data
    data = json.loads(webpage.read().decode())
    df = pd.DataFrame(data["results"])


# load 1 instance of questions & answers at a time from the database
def preload_data(idx):
    # idx parm: selected randomly time and again at function call
    question = df["question"][0]
    correct = df["correct_answer"][0]
    wrong = df["incorrect_answers"][0]

    # fixing charecters with bad formatting
    formatting = [
        ("#039;", "'"),
        ("&'", "'"),
        ("&quot;", '"'),
        ("&lt;", "<"),
        ("&gt;", ">")
    ]

    # # replace bad charecters in strings
    for tup in formatting:
        question = question.replace(tup[0], tup[1])
        correct = correct.replace(tup[0], tup[1])
    # # replace bad charecters in lists
    for tup in formatting:
        wrong = [char.replace(tup[0], tup[1]) for char in wrong]

    # store local values globally
    parameters["question"].append(question)
    parameters["correct"].append(correct)

    # combination of correct and incorrect answers
    all_answers = wrong + [correct]
    random.shuffle(all_answers)

    parameters["answer1"].append(all_answers[0])
    parameters["answer2"].append(all_answers[1])
    parameters["answer3"].append(all_answers[2])
    parameters["answer4"].append(all_answers[3])

    # print correct answer to the terminal (for testing)
    print(parameters["correct"][-1])


""" ascunde widget-urile si le sterge din dictionar """
def clear_widgets():
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()


''' creaza un buton identic cu margini personaizate la stanga si la dreapta'''
def create_buttons(answ, l_margin, r_margin):
    button = QPushButton(answ)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(400)
    button.setStyleSheet(f'''
                        *{{
                            margin-left: {str(l_margin)}px;
                            margin-right: {str(r_margin)}px;
                            border: 4px solid {jsonList['buttonColor']};
                            border-radius: 45px;
                            font-size: 35px;
                            padding: 25px 0;
                            margin-top: 20px;
                            color: white;
                        }}
                        *:hover {{
                            background: {jsonList['buttonColor']};
                        }}
                    ''')
    button.clicked.connect(lambda x: is_correct(answ))
    return button

def is_correct(answ):
    if answ == parameters["correct"][-1]:
        print(answ + " is correct")
        temp_score = parameters["score"][-1]
        parameters["score"].pop()
        parameters["score"].append(temp_score + 10)

        widgets["score"][-1].setText(str(parameters["score"][-1]))
        print("scor curent: ", str(parameters["score"][-1]))
    else:
        clear_widgets()
        show_frame4()

''' afisez frame-ul 1'''


def show_frame1():
    clear_widgets()
    frame1()


def show_frame2():
    clear_widgets()
    frame2()

def show_frame3():
    clear_widgets()
    frame3()

def show_frame4():
    clear_widgets()
    frame4()

def show_frame5():
    clear_widgets()
    # frame5()

# def frame5():
#     # Read data from file
#     scores = []
#     try:
#         with open('scores.txt', 'r') as file:
#             scores = file.readlines()
#     except FileNotFoundError:
#         print("File not found.")
#
#     # Create the scoreboard label
#     scoreboard = QLabel("Scoreboard:")
#     scoreboard.setAlignment(QtCore.Qt.AlignCenter)
#     scoreboard.setStyleSheet(f'''
#         font-size: 40px;
#         color: {jsonList["messageColor"]};
#         font-weight: 400;
#         font-family: "Crete Round";
#         text-align: center;
#         padding: 5px;
#         margin-top: 100px;
#         font-weight: bold;
#     ''')
#     widgets["scoreboard"].append(scoreboard)
#
#     # Create a label for each score
#     score_labels = []
#     for score in scores:
#         name, score_value = score.strip().split(',')
#         score_label = QLabel(f"{name}\t\t{score_value}")
#         score_label.setAlignment(QtCore.Qt.AlignCenter)
#         score_label.setStyleSheet(f'''
#             font-size: 30px;
#             color: {jsonList["messageColor"]};
#             font-weight: 400;
#             font-family: "Crete Round";
#             text-align: center;
#             padding: 5px;
#             margin-top: 20px;
#         ''')
#         score_labels.append(score_label)
#         widgets["score_labels"].append(score_label)
#
#     # Create the return button
#     return_button = QPushButton("Return to Main Menu")
#     return_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
#     return_button.setStyleSheet(f'''
#         *{{
#             border: 4px solid {jsonList["buttonColor"]};
#             border-radius: 45px;
#             font-size: 35px;
#             padding: 25px 0;
#             color: white;
#         }}
#         *:hover {{
#             background: {jsonList["buttonColor"]};
#         }}
#     ''')
#     return_button.clicked.connect(show_frame1)
#     widgets["return_button"].append(return_button)
#
#     # Place widgets on the grid
#     grid.addWidget(widgets["scoreboard"][-1], 0, 0, 1, 2)
#     for i, score_label in enumerate(score_labels, start=1):
#         grid.addWidget(score_label, i, 0, 1, 2)
#     grid.addWidget(widgets["return_button"][-1], len(score_labels) + 1, 0, 1, 2)


# *********************************************
#                  FRAME 1
# *********************************************
def frame1():
    for widget in widgets:
        if widgets[widget]:
            widgets[widget][-1].hide()
        widgets[widget] = []
    widgets["scoreboard"] = []
    widgets["score_labels"] = []
    widgets["return_button"] = []
    # display logo
    text = "Intellectropolis"
    titleColor = jsonList["titleColor"]

    logo = QLabel(window)
    logo.setText(text)
    logo.setStyleSheet(f'''
            font-size: 63px;
            color: {titleColor};
            font-weight: 400;
            font-family: "Crete Round";
            text-align: center;
            padding: 5px;
            margin-top: 100px;
            font-weight: bold;
        ''')
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.adjustSize()
    widgets["logo"].append(logo)

    # button widget
    buttonStart = QPushButton("Start")
    buttonStart.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    buttonStart.setStyleSheet(f'''
                    *{{
                        border: 4px solid {jsonList["buttonColor"]};
                        border-radius: 45px;
                        font-size: 35px;
                        padding: 25px 0;
                        margin: 50px 100px;
                        color: white;
                    }}
                    *:hover {{
                        background: {jsonList["buttonColor"]};
                    }}
                ''')

    buttonStop = QPushButton("Stop")
    buttonStop.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    buttonStop.setStyleSheet(f'''
                        *{{
                            border: 4px solid {jsonList["buttonColor"]};
                            border-radius: 45px;
                            font-size: 35px;
                            padding: 25px 0;
                            margin: 50px 100px;
                            color: white;
                        }}
                        *:hover {{
                            background: {jsonList["buttonColor"]};
                        }}
                    ''')

    # buttonScoreboard = QPushButton("Scoreboard")
    # buttonScoreboard.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    # buttonScoreboard.setStyleSheet(f'''
    #                         *{{
    #                             border: 4px solid {jsonList["buttonColor"]};
    #                             border-radius: 45px;
    #                             font-size: 35px;
    #                             padding: 25px 0;
    #                             margin: 50px 100px;
    #                             color: white;
    #                         }}
    #                         *:hover {{
    #                             background: {jsonList["buttonColor"]};
    #                         }}
    #                     ''')

    buttonStart.clicked.connect(show_frame2)
    buttonStop.clicked.connect(buttonClicked)
    # buttonScoreboard.clicked.connect(show_frame5)

    widgets["button"].append(buttonStart)
    widgets["button"].append(buttonStop)
    # widgets["button"].append(buttonScoreboard)

    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 1)
    grid.addWidget(widgets["button"][0], 1, 0, 1, 1)
    grid.addWidget(widgets["button"][1], 2, 0, 1, 1)
    # grid.addWidget(widgets["button"][2], 3, 0, 1, 1)


# *********************************************
#                  FRAME 2
# *********************************************
def frame2():
    # score = QLabel(str(parameters["score"][-1]))
    score = QLabel(str(int(parameters["score"][-1])))
    print(str(int(parameters["score"][-1])))
    score.setAlignment(QtCore.Qt.AlignCenter)
    score.setStyleSheet(
        f'''
        font-size: 35px;
        color: 'white';
        padding: 15px 15px;
        background: '{jsonList["scoreBackgroundColor"]}';
        border: 1px solid '{jsonList["scoreBackgroundColor"]}';
        border-radius: 35px;
        '''
    )
    score.setFixedSize(100, 100)
    score.setGeometry(window.width() - 30, window.height() - 30, 100, 100)
    widgets["score"].append(score)

    question = QLabel(str(parameters["question"][-1]))
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet(f'''
            font-size: 40px;
            color: {jsonList["messageColor"]};
            font-weight: 400;
            font-family: "Crete Round";
            text-align: center;
            padding: 75px;
            margin-top: 100px;
        ''')
    widgets["question"].append(question)

    button1 = create_buttons(parameters["answer1"][-1], 85, 5)
    button2 = create_buttons(parameters["answer2"][-1], 5, 85)
    button3 = create_buttons(parameters["answer3"][-1], 85, 5)
    button4 = create_buttons(parameters["answer4"][-1], 5, 85)

    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)
    widgets["answer3"].append(button3)
    widgets["answer4"].append(button4)

    grid.addWidget(widgets["score"][-1], 0, 3)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 4)
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["answer2"][-1], 2, 3)
    grid.addWidget(widgets["answer3"][-1], 3, 0)
    grid.addWidget(widgets["answer4"][-1], 3, 3)


# *********************************************
#             FRAME 3 - WIN GAME
# *********************************************
def frame3():
    # congradulations widget
    message = QLabel("Bravo, ai câștigat!")
    messageColor = jsonList["messageColor"]
    message.setAlignment(QtCore.Qt.AlignCenter)
    message.setStyleSheet(f'''
            font-size: 40px;
            color: {messageColor};
            font-weight: 400;
            font-family: "Crete Round";
            text-align: center;
            padding: 5px;
            margin-top: 100px;
            font-weight: bold;
        ''')
    widgets["message"].append(message)

    # go back to work widget
    message2 = QLabel("Scorul tău: ")
    message2.setAlignment(QtCore.Qt.AlignCenter)
    message2.setStyleSheet(f'''
            font-size: 30px;
            color: {messageColor};
            font-weight: 400;
            font-family: "Crete Round";
            text-align: center;
            padding: 5px;
            margin-top: 100px;
            font-weight: bold;
        ''')
    widgets["message2"].append(message2)

    # score widget
    scoreColor = jsonList["scoreColor"]
    score = QLabel("100")
    score.setAlignment(QtCore.Qt.AlignCenter)
    score.setStyleSheet(f'''
            color: {scoreColor};
            font-size: 100px;
            margin: 0 75px 0px 75px;
        ''')
    widgets["score"].append(score)

    # button widget
    buttonColor = jsonList["buttonColor"]
    button = QPushButton('Refă testul')
    button.setStyleSheet(f'''
                    *{{
                        border: 4px solid {buttonColor};
                        border-radius: 45px;
                        font-size: 35px;
                        padding: 25px 0;
                        margin: 50px 100px;
                        color: white;
                    }}
                    *:hover {{
                        background: {buttonColor};
                    }}
                ''')
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    widgets["button"].append(button)

    # place widgets on the grid
    grid.addWidget(widgets["message"][-1], 2, 0, 1, 2)
    grid.addWidget(widgets["message2"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["score"][-1], 4, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 5, 0, 1, 2)


# *********************************************
#                  FRAME 4 - FAIL
# *********************************************
def frame4():
    # sorry widget
    message = QLabel("Răspuns greșit!\nScorul tău:")
    message.setAlignment(QtCore.Qt.AlignCenter)
    message.setStyleSheet(f'''
                font-size: 40px;
                color: {jsonList["messageColor"]};
                font-weight: 400;
                font-family: "Crete Round";
                text-align: center;
                padding: 5px;
                margin-top: 100px;
                font-weight: bold;
            ''')
    widgets["message"].append(message)

    # score widget
    score = QLabel("100")
    score.setAlignment(QtCore.Qt.AlignCenter)
    score.setStyleSheet(f'''
                color: {jsonList["scoreColor"]};
                font-size: 100px;
                margin: 0 75px 0px 75px;
            ''')
    widgets["score"].append(score)

    # button widget
    button = QPushButton('Încearcă din nou')
    button.setStyleSheet(f'''
                    *{{
                        border: 4px solid {jsonList["buttonColor"]};
                        border-radius: 45px;
                        font-size: 35px;
                        padding: 25px 0;
                        margin: 50px 100px;
                        color: white;
                    }}
                    *:hover {{
                        background: {jsonList["buttonColor"]};
                    }}
                ''')
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    widgets["button"].append(button)

    # place widgets on the grid
    grid.addWidget(widgets["message"][-1], 1, 1, 1, 2)
    grid.addWidget(widgets["score"][-1], 2, 1, 1, 2)
    grid.addWidget(widgets["button"][-1], 3, 1, 1, 2)


if __name__ == '__main__':


    app = QApplication(sys.argv)
    jsonList = read_colors_from_file(json_file_path)



    preload_data(0)

    window = QWidget()
    window.setWindowTitle("Intellectropolis")
    window.setFixedWidth(1000)
    window.setFixedHeight(800)
    # window.move(2700, 200)
    backgroundColor = jsonList["backgroundColor"]
    window.setStyleSheet(f'''
        background: {backgroundColor};
    ''')

    # initiallize grid layout
    grid = QGridLayout()

    frame1()


    # frame2()
    window.setLayout(grid)

    window.show()
    sys.exit(app.exec())
