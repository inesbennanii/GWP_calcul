import tkinter as tk
from tkinter import *
from tkinter import messagebox, Label, Button, Entry
from tkinter import ttk 
import xlwings as xw
from PIL import Image, ImageTk
import streamlit as st


def sendd():
    fenetre = tk.Toplevel()
    fenetre.title("Jeu de Nim")
    fenetre.geometry("1500x900")
    image2 = ImageTk.PhotoImage(Image.open("sustain.png").resize((1500, 900)))
    fenetre.image2 = image2
    canvas = tk.Canvas(fenetre, width=1500, height=900, highlightthickness=0)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=image2)
    
    section1 = section11.get()
    distance1 = distance11.get()
    section2 = section22.get()
    distance2 = distance22.get()
    
    wb = xw.Book("Calcul_GWP.xlsx") 
    ws = wb.sheets[0]
    
    ws.range("A33").value = section1
    ws.range("A35").value = distance1
    ws.range("G33").value = section2
    ws.range("G35").value = distance2
    
    materiau = ws.range("E47").value
    GWP1 = ws.range("D43").value
    GWP1= str(round(GWP1, 2))
    GWP2 = ws.range("J43").value
    GWP2= str(round(GWP2, 2))
    
    s1 = tk.Label(fenetre, text=f"Le matériau à utiliser est {materiau}",fg="#144614", font=("Georgia", 50), bg="white")
    canvas.create_window(730, 200, window=s1)
    
    s2 = tk.Label(fenetre, text=f"{GWP1} kg CO₂",fg="#144614", font=("Georgia", 35), bg="white")
    canvas.create_window(510, 600, window=s2)
    
    s4 = tk.Label(fenetre, text=f"Total GWP de l'aluminium",fg="#144614", font=("Georgia", 20), bg="white")
    canvas.create_window(500, 650, window=s4)
    
    s3 = tk.Label(fenetre, text=f"{GWP2} kg CO₂",fg="#144614", font=("Georgia", 35), bg="white")
    canvas.create_window(1000, 600, window=s3)
    
    s5 = tk.Label(fenetre, text=f"Total GWP du cuivre",fg="#144614", font=("Georgia", 20), bg="white")
    canvas.create_window(990, 650, window=s5)


root = tk.Tk()
root.title("Bienvenue")
root.attributes('-fullscreen',True)
image1 = ImageTk.PhotoImage(Image.open("sss.jpg").resize((1500, 900)))
root.image1 = image1
canvas = tk.Canvas(root, width=1500, height=900, highlightthickness=0)
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=image1)


label1 = tk.Label(root, text="Choisissez la section pour l'aluminium :",fg="#144614", font=("Georgia", 25), bg="white")
canvas.create_window(730, 200, window=label1)
sections = [50, 120, 150, 185]
section11 = ttk.Combobox(root, values=sections, state="readonly", font=('Georgia', 20), width=3)
section11.current(0)
canvas.create_window(730, 270, window=section11)

label2 = tk.Label(root, text="Distance pour l'aluminium :",fg="#144614",font=("Georgia", 25), bg="white")
canvas.create_window(730, 330, window=label2)

distance11 = tk.Entry(root, justify="center", font=("Georgia", 20))
canvas.create_window(730, 380, window=distance11)

label3 = tk.Label(root, text="Choisissez la section pour le cuivre :",fg="#144614",font=("Georgia", 25), bg="white")
canvas.create_window(730, 460, window=label3)

section22 = ttk.Combobox(root, values=sections, state="readonly", font=('Georgia', 20), width=3)
section22.current(0)
canvas.create_window(730, 510, window=section22)

label4 = tk.Label(root, text="Distance pour le cuivre :",fg="#144614",font=("Georgia", 25), bg="white")
canvas.create_window(730, 590, window=label4)

distance22 = tk.Entry(root, justify="center", font=("Georgia", 20))
canvas.create_window(730, 650, window=distance22)

btn_valider = tk.Button(root, text="Valider", font=("Georgia", 25),
                        bg="white", command=sendd)
canvas.create_window(730, 690, window=btn_valider)

root.mainloop()