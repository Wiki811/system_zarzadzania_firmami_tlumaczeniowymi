from tkinter import *
from tkinter import ttk
import tkintermapview

from model import factories, clients, employees, users
from controller import *

root = Tk()
root.title("System zarządzania firmami tłumaczeniowymi")
root.geometry("1200x800")

notebook = ttk.Notebook(root)

tab_firmy = Frame(notebook)
tab_klienci = Frame(notebook)
tab_pracownicy = Frame(notebook)
tab_wyszukiwarka = Frame(notebook)

notebook.add(tab_firmy, text="Firmy")
notebook.add(tab_klienci, text="Klienci")
notebook.add(tab_pracownicy, text="Pracownicy")
notebook.add(tab_wyszukiwarka, text="Wyszukiwarka")

notebook.pack(fill=BOTH, expand=True)

# FIRMY TŁUMACZENIOWE

frame_company_list = Frame(tab_firmy)
frame_company_form = Frame(tab_firmy)
frame_company_details = Frame(tab_firmy)
frame_company_map = Frame(tab_firmy)

frame_company_list.grid(row=0, column=0, padx=10, pady=10, sticky=N)
frame_company_form.grid(row=0, column=1, padx=10, pady=10, sticky=N)
frame_company_details.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
frame_company_map.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

