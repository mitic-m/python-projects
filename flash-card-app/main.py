from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
current_word = {}
flip_timer = None

try:
    words = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    words = pandas.read_csv("data/english_words.csv")
words_to_learn = words.to_dict(orient="records")

def mark_as_known():
    if current_word in words_to_learn:
        words_to_learn.remove(current_word)
        data = pandas.DataFrame(words_to_learn)
        data.to_csv("data/words_to_learn.csv", index=False)
    next_word()


def next_word():
    global current_word, flip_timer
    if flip_timer is not None:
        window.after_cancel(flip_timer)
        flip_timer = None

    if not words_to_learn:
        canvas.itemconfig(card_background, image=card_front_img)
        canvas.itemconfig(title_text, text="Bravo!", fill="black")
        canvas.itemconfig(word_text, text="All learned!", fill="black")
        return

    current_word = choice(words_to_learn)
    canvas.itemconfig(card_background, image=card_front_img)
    canvas.itemconfig(title_text, text="English", fill="black")
    canvas.itemconfig(word_text, text=current_word["English"], fill="black")
    flip_timer = window.after(3000, flip_card)

def flip_card():
    global current_word
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(title_text, text="Serbian", fill="white")
    canvas.itemconfig(word_text, text=current_word["Serbian"], fill="white")


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
title_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

wrong_button_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=next_word)
wrong_button.grid(row=1, column=0)

right_button_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_button_img, highlightthickness=0, command=mark_as_known)
right_button.grid(row=1, column=1)


next_word()

window.mainloop()

