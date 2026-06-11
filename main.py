from tkinter import *
from tkinter import ttk
from controller import *

okno = Tk()

okno.title("System zarządzania firmami tłumaczeniowymi")
okno.geometry("1200x700")

notebook = ttk.Notebook(okno)
notebook.pack(fill="both", expand=True)

# Zakładki
tab_firmy = Frame(notebook)
tab_klienci = Frame(notebook)
tab_pracownicy = Frame(notebook)
tab_filtrowanie = Frame(notebook)

notebook.add(tab_firmy, text="Firmy")
notebook.add(tab_klienci, text="Klienci")
notebook.add(tab_pracownicy, text="Pracownicy")
notebook.add(tab_filtrowanie,text="Filtrowanie")

okno.mainloop()
