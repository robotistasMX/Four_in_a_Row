import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import os
import time

def sf():
	dificultad.set(1)
	time.sleep(1)
	ventana.destroy()
	print(dificultad.get())

def f():
	dificultad.set(2)
	time.sleep(1)
	ventana.destroy()
	print(dificultad.get())

def im():
	dificultad.set(3)
	time.sleep(1)
	ventana.destroy()
	print(dificultad.get())

def df():
	dificultad.set(4)
	time.sleep(1)
	ventana.destroy()
	print(dificultad.get())

def mdf():
	dificultad.set(5)
	time.sleep(1)
	ventana.destroy()
	print(dificultad.get())

ventana = tk.Tk()
ventana.geometry('1300x500')
ventana.title("HolaMundo")

ventana.configure(background = 'black')
dificultad = tk.IntVar()

titulo = tk.Label(ventana, text = "Conecta4 IA", bg = "black", fg = "white")
titulo.pack(fill = tk.X)

img_sf = ImageTk.PhotoImage(Image.open("sf.png"))
sfacil = tk.Button(ventana, image= img_sf, text = "Muy Facil", bg = "black", bd=0, activebackground="black" ,command = sf)
sfacil.pack(side = LEFT, expand = True, fill = BOTH)

img_f = ImageTk.PhotoImage(Image.open("f.png"))
facil = tk.Button(ventana, text = "Facil", image= img_f, bg = "black", bd=0, activebackground="black", command = f)
facil.pack(side = LEFT, expand = True, fill = BOTH)

img_im = ImageTk.PhotoImage(Image.open("im.png"))
intermedio = tk.Button(ventana, text = "Intermedio", image= img_im, bg = "black", bd=0, activebackground="black", command = im)
intermedio.pack(side = LEFT, expand = True, fill = BOTH)

img_df = ImageTk.PhotoImage(Image.open("df.png"))
dificil = tk.Button(ventana, text = "Dificil", image= img_df, bg = "black", bd=0, activebackground="black", command = df)
dificil.pack(side = LEFT, expand = True, fill = BOTH)

img_mdf = ImageTk.PhotoImage(Image.open("mdf.png"))
mdificil = tk.Button(ventana, text = "Muy Dificil", image= img_mdf, bg = "black", bd=0, activebackground="black", command = mdf)
mdificil.pack(side = LEFT, expand = True, fill = BOTH)

ventana.mainloop()
