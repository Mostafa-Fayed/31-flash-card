import tkinter as tk
import pandas as pd
from random import choice


BACKGROUND_COLOR = "#B1DDC6"
WHITE_COLOR = "#FFFFFF"
BLACK_COLOR = "#000000"
FONT_NAME = "Ariel"
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv("data/french_words.csv")
cards = data.to_dict(orient="records")
current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(cards)
    canvas.itemconfig(language, text="French", fill=BLACK_COLOR)
    canvas.itemconfig(word, text=current_card["French"], fill=BLACK_COLOR)
    canvas.itemconfig(card_face, image=card_front_photo)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(word, text=current_card["English"], fill=WHITE_COLOR)
    canvas.itemconfig(language, text="English", fill=WHITE_COLOR)
    canvas.itemconfig(card_face, image=card_back_photo)


def known_word():
    global cards
    cards.remove(current_card)
    df = pd.DataFrame(cards)
    df.to_csv("data/words_to_learn.csv", index=False)
    next_card()

    
# ---------------------- Creating GUI ----------------------
window = tk.Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

card_front_photo = tk.PhotoImage(file="images/card_front.png")
card_back_photo = tk.PhotoImage(file="images/card_back.png")
right_photo = tk.PhotoImage(file="images/right.png")
wrong_photo = tk.PhotoImage(file="images/wrong.png")
canvas = tk.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)
card_face = canvas.create_image(400, 263, image=card_front_photo)
language = canvas.create_text(400, 150, text="", font=(FONT_NAME, 40, "italic"))
word = canvas.create_text(400, 283, text="", font=(FONT_NAME, 60, "bold"))
wrong_button = tk.Button(image=wrong_photo, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)
right_button = tk.Button(image=right_photo, highlightthickness=0, command=known_word)
right_button.grid(column=1, row=1)

next_card()

window.mainloop()
