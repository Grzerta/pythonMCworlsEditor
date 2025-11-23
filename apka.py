import tkinter as tk
from tkinter import PhotoImage, messagebox
import ttkbootstrap as ttk
import ttkbootstrap.constants as tb




# Utwórz główne okno z tkbootstrap
root = ttk.Window(themename="superhero")
root.title("Aplikacja z grafiką i ikonkami (tkbootstrap)")
root.geometry("400x800")

# Załaduj grafikę do wyświetlenia
main_image = PhotoImage(file="icon3.png")  # Podmień na własny plik

# Wyświetl grafikę (ttk.Label z tkbootstrap)
label_img = ttk.Label(root, image=main_image)
label_img.pack(pady=10)

# Załaduj ikony do przycisków
icon1 = PhotoImage(file="icon1.png")  # Podmień na własny plik
icon2 = PhotoImage(file="icon2.png")  # Podmień na własny plik

# Funkcje obsługi przycisków
def akcja1():
    messagebox.showinfo("Akcja", "Kliknięto przycisk 1!")

def akcja2():
    messagebox.showinfo("Akcja", "Kliknięto przycisk 2!")

# Przycisk 1 z ikonką (ttk.Button)
btn1 = ttk.Button(root, image=icon1, compound="left", command=akcja1, bootstyle=(tb.SUCCESS,tb.OUTLINE))
btn1.pack(pady=5)

# Przycisk 2 z ikonką (ttk.Button)
btn2 = ttk.Button(root, text="Przycisk 2", image=icon2, compound="left", command=akcja2)
btn2.pack(pady=5)

root.mainloop()
