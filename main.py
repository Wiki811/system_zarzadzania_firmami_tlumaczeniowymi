from tkinter import *
from tkinter import ttk
import tkintermapview
from model import companies, clients, employees, users
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

# lista
Label(frame_company_list, text="Lista firm tłumaczeniowych:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)
entry_company_filter = Entry(frame_company_list)
entry_company_filter.grid(row=1, column=0)
Button(frame_company_list, text="Szukaj", command=lambda: filter_companies()).grid(row=1, column=1)
listbox_companies = Listbox(frame_company_list, width=30, height=10)
listbox_companies.grid(row=2, column=0, columnspan=2)
Button(frame_company_list, text="Szczegóły", command=lambda: show_company_details()).grid(row=3, column=0)
Button(frame_company_list, text="Edytuj", command=lambda: edit_company_gui()).grid(row=3, column=1)
Button(frame_company_list, text="Usuń", command=lambda: delete_company_gui()).grid(row=4, column=0, columnspan=2)

# formularz
Label(frame_company_form, text="Formularz:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)
Label(frame_company_form, text="Nazwa firmy:").grid(row=1, column=0, sticky=W)
Label(frame_company_form, text="Miasto:").grid(row=2, column=0, sticky=W)
Label(frame_company_form, text="Język tłumaczeń:").grid(row=3, column=0, sticky=W)
entry_company_name = Entry(frame_company_form)
entry_company_location = Entry(frame_company_form)
entry_company_language = Entry(frame_company_form)
entry_company_name.grid(row=1, column=1)
entry_company_location.grid(row=2, column=1)
entry_company_language.grid(row=3, column=1)
button_add_company = Button(frame_company_form,text="Dodaj firmę", command=lambda: add_company_gui())
button_add_company.grid(row=4, column=0, columnspan=2, pady=5)

# szczegóły
Label(frame_company_details, text="Szczegóły:", font=("Arial", 10, "bold")).grid(row=0, column=0)
Label(frame_company_details, text="Nazwa firmy:").grid(row=1, column=0)
label_company_name_val = Label(frame_company_details, text="...")
label_company_name_val.grid(row=1, column=1)
Label(frame_company_details, text="Miasto:").grid(row=1, column=2)
label_company_location_val = Label(frame_company_details, text="...")
label_company_location_val.grid(row=1, column=3)
Label(frame_company_details, text="Język tłumaczeń:").grid(row=1, column=4)
label_company_language_val = Label(frame_company_details, text="...")
label_company_language_val.grid(row=1, column=5)

# mapa
map_companies = tkintermapview.TkinterMapView(frame_company_map, width=500, height=400)
map_companies.set_position(52.2, 21.0)
map_companies.set_zoom(6)
map_companies.grid(row=0,column=0)

def refresh_companies():
    listbox_companies.delete(0, END)
    for company in get_companies(companies):
        listbox_companies.insert(END, company['name'])

def show_company_details():
    i = listbox_companies.curselection()

    if not i:
        return

    i = i[0]
    company = companies[i]

    label_company_name_val.config(text=company['name'])
    label_company_location_val.config(text=company['location'])
    label_company_language_val.config(text=company['language'])

    coords = get_coordinates(company['location'])

    map_companies.set_position(coords[0], coords[1])
    map_companies.set_zoom(12)


def add_company_gui():
    name = entry_company_name.get()
    location = entry_company_location.get()
    language = entry_company_language.get()

    if not name or not location or not language:
        return

    add_company(companies, name, location, language)

    try:
        coords = get_coordinates(location)
        marker = map_companies.set_marker(coords[0], coords[1], text=name)
        companies[-1]['marker'] = marker
    except:
        pass

    entry_company_name.delete(0, END)
    entry_company_location.delete(0, END)
    entry_company_language.delete(0, END)

    refresh_companies()

def edit_company_gui():
    i = listbox_companies.curselection()

    if not i:
        return

    i = i[0]

    entry_company_name.delete(0, END)
    entry_company_location.delete(0, END)
    entry_company_language.delete(0, END)

    entry_company_name.insert(0, companies[i]['name'])
    entry_company_location.insert(0, companies[i]['location'])
    entry_company_language.insert(0, companies[i]['language'])

    button_add_company.config(
        text="Zapisz zmiany",
        command=lambda: save_company(i)
    )

def save_company(i):
    update_company(
        companies,
        i,
        entry_company_name.get(),
        entry_company_location.get(),
        entry_company_language.get()
    )

    if companies[i]['marker']:
        companies[i]['marker'].delete()
        companies[i]['marker'] = None

    try:
        coords = get_coordinates(companies[i]['location'])

        companies[i]['marker'] = map_companies.set_marker(
            coords[0],
            coords[1],
            text=companies[i]['name']
        )
    except:
        pass

    entry_company_name.delete(0, END)
    entry_company_location.delete(0, END)
    entry_company_language.delete(0, END)

    button_add_company.config(
        text="Dodaj firmę",
        command=lambda: add_company_gui()
    )

    refresh_companies()


def delete_company_gui():
    i = listbox_companies.curselection()

    if not i:
        return

    i = i[0]

    if companies[i]['marker']:
        companies[i]['marker'].delete()

    remove_company(companies, i)

    refresh_companies()

def filter_companies():
    search = entry_company_filter.get().lower()

    listbox_companies.delete(0, END)

    for company in companies:
        if search in company['name'].lower() or search in company['location'].lower():
            listbox_companies.insert(END, company['name'])

refresh_companies()

def load_company_markers():
    for company in companies:
        try:
            coords = get_coordinates(company['location'])

            company['marker'] = map_companies.set_marker(
                coords[0],
                coords[1],
                text=company['name']
            )
        except:
            pass


# klienci

frame_client_list = Frame(tab_klienci)
frame_client_form = Frame(tab_klienci)
frame_client_details = Frame(tab_klienci)
frame_client_map = Frame(tab_klienci)

frame_client_list.grid(row=0, column=0, padx=10, pady=10, sticky=N)
frame_client_form.grid(row=0, column=1, padx=10, pady=10, sticky=N)
frame_client_details.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
frame_client_map.grid(row=0, column=2, rowspan=2, padx=10, pady=10)


# lista


Label(frame_client_list, text="Lista klientów:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)

entry_client_filter = Entry(frame_client_list)
entry_client_filter.grid(row=1, column=0)

Button(frame_client_list, text="Szukaj", command=lambda: filter_clients()).grid(row=1, column=1)

listbox_clients = Listbox(frame_client_list, width=30, height=10)
listbox_clients.grid(row=2, column=0, columnspan=2)

Button(frame_client_list, text="Szczegóły", command=lambda: show_client_details()).grid(row=3, column=0)

Button(frame_client_list, text="Edytuj", command=lambda: edit_client_gui()).grid(row=3, column=1)

Button(frame_client_list, text="Usuń", command=lambda: delete_client_gui()).grid(row=4, column=0, columnspan=2)


# formularz

Label(frame_client_form, text="Formularz:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)

Label(frame_client_form, text="Imię i nazwisko:").grid(row=1, column=0, sticky=W)
Label(frame_client_form, text="Miasto:").grid(row=2, column=0, sticky=W)
Label(frame_client_form, text="Firma tłumaczeniowa:").grid(row=3, column=0, sticky=W)
Label(frame_client_form, text="Usługa:").grid(row=4, column=0, sticky=W)

entry_client_name = Entry(frame_client_form)
entry_client_location = Entry(frame_client_form)
entry_client_company = Entry(frame_client_form)
entry_client_service = Entry(frame_client_form)

entry_client_name.grid(row=1, column=1)
entry_client_location.grid(row=2, column=1)
entry_client_company.grid(row=3, column=1)
entry_client_service.grid(row=4, column=1)

button_add_client = Button(
    frame_client_form,
    text="Dodaj klienta",
    command=lambda: add_client_gui()
)

button_add_client.grid(row=5, column=0, columnspan=2, pady=5)

# szczegóły

Label(frame_client_details, text="Szczegóły:", font=("Arial", 10, "bold")).grid(row=0, column=0)

Label(frame_client_details, text="Klient:").grid(row=1, column=0)
label_client_name_val = Label(frame_client_details, text="...")
label_client_name_val.grid(row=1, column=1)

Label(frame_client_details, text="Miasto:").grid(row=1, column=2)
label_client_location_val = Label(frame_client_details, text="...")
label_client_location_val.grid(row=1, column=3)

Label(frame_client_details, text="Firma tłumaczeniowa:").grid(row=1, column=4)
label_client_company_val = Label(frame_client_details, text="...")
label_client_company_val.grid(row=1, column=5)

Label(frame_client_details, text="Usługa:").grid(row=1, column=6)
label_client_service_val = Label(frame_client_details, text="...")
label_client_service_val.grid(row=1, column=7)


# mapa

map_clients = tkintermapview.TkinterMapView(
    frame_client_map,
    width=500,
    height=400
)

map_clients.set_position(52.2, 21.0)
map_clients.set_zoom(6)

map_clients.grid(row=0, column=0)

def refresh_clients():
    listbox_clients.delete(0, END)

    for c in get_clients(clients):
        listbox_clients.insert(END, c['name'])

def show_client_details():
    i = listbox_clients.curselection()

    if not i:
        return

    i = i[0]
    c = clients[i]

    label_client_name_val.config(text=c['name'])
    label_client_location_val.config(text=c['location'])
    label_client_company_val.config(text=c['company'])
    label_client_service_val.config(text=c['service'])

    coords = get_coordinates(c['location'])

    map_clients.set_position(coords[0], coords[1])
    map_clients.set_zoom(12)


def add_client_gui():
    name = entry_client_name.get()
    location = entry_client_location.get()
    company = entry_client_company.get()
    service = entry_client_service.get()

    if not name or not location or not company:
        return

    add_client(clients, name, location, company, service)

    try:
        coords = get_coordinates(location)
        marker = map_clients.set_marker(coords[0], coords[1], text=name)
        clients[-1]['marker'] = marker
    except:
        pass

    entry_client_name.delete(0, END)
    entry_client_location.delete(0, END)
    entry_client_company.delete(0, END)
    entry_client_service.delete(0, END)

    refresh_clients()


def edit_client_gui():
    i = listbox_clients.curselection()

    if not i:
        return

    i = i[0]
    c = clients[i]

    entry_client_name.delete(0, END)
    entry_client_location.delete(0, END)
    entry_client_company.delete(0, END)
    entry_client_service.delete(0, END)

    entry_client_name.insert(0, c['name'])
    entry_client_location.insert(0, c['location'])
    entry_client_company.insert(0, c['company'])
    entry_client_service.insert(0, c['service'])

    button_add_client.config(
        text="Zapisz zmiany",
        command=lambda: save_client(i)
    )


def save_client(i):
    if clients[i]['marker']:
        clients[i]['marker'].delete()

    update_client(
        clients,
        i,
        entry_client_name.get(),
        entry_client_location.get(),
        entry_client_company.get(),
        entry_client_service.get()
    )

    try:
        coords = get_coordinates(clients[i]['location'])
        clients[i]['marker'] = map_clients.set_marker(
            coords[0],
            coords[1],
            text=clients[i]['name']
        )
    except:
        pass

    entry_client_name.delete(0, END)
    entry_client_location.delete(0, END)
    entry_client_company.delete(0, END)
    entry_client_service.delete(0, END)

    button_add_client.config(
        text="Dodaj klienta",
        command=lambda: add_client_gui()
    )

    refresh_clients()


def delete_client_gui():
    i = listbox_clients.curselection()

    if not i:
        return

    i = i[0]

    if clients[i]['marker']:
        clients[i]['marker'].delete()

    remove_client(clients, i)

    refresh_clients()


def filter_clients():
    search = entry_client_filter.get().lower()

    listbox_clients.delete(0, END)

    for c in clients:
        if search in c['name'].lower() or search in c['company'].lower():
            listbox_clients.insert(END, c['name'])


def load_client_markers():
    for c in clients:
        try:
            coords = get_coordinates(c['location'])
            c['marker'] = map_clients.set_marker(
                coords[0],
                coords[1],
                text=c['name']
            )
        except:
            pass


refresh_clients()

# pracownicy

frame_employee_list = Frame(tab_pracownicy)
frame_employee_form = Frame(tab_pracownicy)
frame_employee_details = Frame(tab_pracownicy)
frame_employee_map = Frame(tab_pracownicy)

frame_employee_list.grid(row=0, column=0, padx=10, pady=10, sticky=N)
frame_employee_form.grid(row=0, column=1, padx=10, pady=10, sticky=N)
frame_employee_details.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
frame_employee_map.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

# lista

Label(frame_employee_list, text="Lista pracowników:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)

entry_employee_filter = Entry(frame_employee_list)
entry_employee_filter.grid(row=1, column=0)

Button(frame_employee_list, text="Szukaj", command=lambda: filter_employees()).grid(row=1, column=1)

listbox_employees = Listbox(frame_employee_list, width=30, height=10)
listbox_employees.grid(row=2, column=0, columnspan=2)

Button(frame_employee_list, text="Szczegóły", command=lambda: show_employee_details()).grid(row=3, column=0)
Button(frame_employee_list, text="Edytuj", command=lambda: edit_employee_gui()).grid(row=3, column=1)
Button(frame_employee_list, text="Usuń", command=lambda: delete_employee_gui()).grid(row=4, column=0, columnspan=2)


# formularz

Label(frame_employee_form, text="Formularz:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)

Label(frame_employee_form, text="Imię i nazwisko:").grid(row=1, column=0, sticky=W)
Label(frame_employee_form, text="Miasto:").grid(row=2, column=0, sticky=W)
Label(frame_employee_form, text="Firma tłumaczeniowa:").grid(row=3, column=0, sticky=W)
Label(frame_employee_form, text="Stanowisko:").grid(row=4, column=0, sticky=W)

entry_employee_name = Entry(frame_employee_form)
entry_employee_location = Entry(frame_employee_form)
entry_employee_company = Entry(frame_employee_form)
entry_employee_role = Entry(frame_employee_form)

entry_employee_name.grid(row=1, column=1)
entry_employee_location.grid(row=2, column=1)
entry_employee_company.grid(row=3, column=1)
entry_employee_role.grid(row=4, column=1)

button_add_employee = Button(
    frame_employee_form,
    text="Dodaj pracownika",
    command=lambda: add_employee_gui()
)

button_add_employee.grid(row=5, column=0, columnspan=2, pady=5)


# szczegóły

Label(frame_employee_details, text="Szczegóły:", font=("Arial", 10, "bold")).grid(row=0, column=0)

Label(frame_employee_details, text="Pracownik:").grid(row=1, column=0)
label_employee_name_val = Label(frame_employee_details, text="...")
label_employee_name_val.grid(row=1, column=1)

Label(frame_employee_details, text="Miasto:").grid(row=1, column=2)
label_employee_location_val = Label(frame_employee_details, text="...")
label_employee_location_val.grid(row=1, column=3)

Label(frame_employee_details, text="Firma tłumaczeniowa:").grid(row=1, column=4)
label_employee_company_val = Label(frame_employee_details, text="...")
label_employee_company_val.grid(row=1, column=5)

Label(frame_employee_details, text="Stanowisko:").grid(row=1, column=6)
label_employee_role_val = Label(frame_employee_details, text="...")
label_employee_role_val.grid(row=1, column=7)


# mapa

map_employees = tkintermapview.TkinterMapView(frame_employee_map, width=500, height=400)
map_employees.set_position(52.2, 21.0)
map_employees.set_zoom(6)
map_employees.grid(row=0, column=0)

def refresh_employees():
    listbox_employees.delete(0, END)

    for e in get_employees(employees):
        listbox_employees.insert(END, e['name'])


def show_employee_details():
    i = listbox_employees.curselection()

    if not i:
        return

    i = i[0]
    e = employees[i]

    label_employee_name_val.config(text=e['name'])
    label_employee_location_val.config(text=e['location'])
    label_employee_company_val.config(text=e['company'])
    label_employee_role_val.config(text=e['role'])

    coords = get_coordinates(e['location'])

    map_employees.set_position(coords[0], coords[1])
    map_employees.set_zoom(12)


def add_employee_gui():
    name = entry_employee_name.get()
    location = entry_employee_location.get()
    company = entry_employee_company.get()
    role = entry_employee_role.get()

    if not name or not location or not company or not role:
        return

    add_employee(employees, name, location, company, role)

    try:
        coords = get_coordinates(location)
        marker = map_employees.set_marker(coords[0], coords[1], text=name)
        employees[-1]['marker'] = marker
    except:
        pass

    entry_employee_name.delete(0, END)
    entry_employee_location.delete(0, END)
    entry_employee_company.delete(0, END)
    entry_employee_role.delete(0, END)

    refresh_employees()


def edit_employee_gui():
    i = listbox_employees.curselection()

    if not i:
        return

    i = i[0]
    e = employees[i]

    entry_employee_name.delete(0, END)
    entry_employee_location.delete(0, END)
    entry_employee_company.delete(0, END)
    entry_employee_role.delete(0, END)

    entry_employee_name.insert(0, e['name'])
    entry_employee_location.insert(0, e['location'])
    entry_employee_company.insert(0, e['company'])
    entry_employee_role.insert(0, e['role'])

    button_add_employee.config(
        text="Zapisz zmiany",
        command=lambda: save_employee(i)
    )


def save_employee(i):
    if employees[i]['marker']:
        employees[i]['marker'].delete()

    update_employee(
        employees,
        i,
        entry_employee_name.get(),
        entry_employee_location.get(),
        entry_employee_company.get(),
        entry_employee_role.get()
    )

    try:
        coords = get_coordinates(employees[i]['location'])

        employees[i]['marker'] = map_employees.set_marker(
            coords[0],
            coords[1],
            text=employees[i]['name']
        )
    except:
        pass

    entry_employee_name.delete(0, END)
    entry_employee_location.delete(0, END)
    entry_employee_company.delete(0, END)
    entry_employee_role.delete(0, END)

    button_add_employee.config(
        text="Dodaj pracownika",
        command=lambda: add_employee_gui()
    )

    refresh_employees()


def delete_employee_gui():
    i = listbox_employees.curselection()

    if not i:
        return

    i = i[0]

    if employees[i]['marker']:
        employees[i]['marker'].delete()

    remove_employee(employees, i)

    refresh_employees()


def filter_employees():
    search = entry_employee_filter.get().lower()

    listbox_employees.delete(0, END)

    for e in employees:
        if search in e['name'].lower() or search in e['company'].lower():
            listbox_employees.insert(END, e['name'])


def load_employee_markers():
    for e in employees:
        try:
            coords = get_coordinates(e['location'])

            e['marker'] = map_employees.set_marker(
                coords[0],
                coords[1],
                text=e['name']
            )
        except:
            pass


refresh_employees()


# ========== WYSZUKIWARKA ==========

frame_views_filters = Frame(tab_wyszukiwarka)
frame_views_results = Frame(tab_wyszukiwarka)
frame_views_map = Frame(tab_wyszukiwarka)

frame_views_filters.grid(row=0, column=0, padx=10, pady=10, sticky=N)
frame_views_results.grid(row=0, column=1, padx=10, pady=10, sticky=N)
frame_views_map.grid(row=0, column=2, padx=10, pady=10, sticky=N)

Label(frame_views_filters, text="Filtry:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)

Label(frame_views_filters, text="Nazwa firmy tłumaczeniowej:").grid(row=1, column=0, sticky=W)

entry_filter_company = Entry(frame_views_filters)
entry_filter_company.grid(row=1, column=1)

Button(
    frame_views_filters,
    text="Klienci tej firmy",
    command=lambda: show_clients_by_company()
).grid(row=2, column=0, columnspan=2, pady=3)

Button(
    frame_views_filters,
    text="Pracownicy tej firmy",
    command=lambda: show_employees_by_company()
).grid(row=3, column=0, columnspan=2, pady=3)

Label(
    frame_views_filters,
    text="Język tłumaczeń:"
).grid(row=4, column=0, sticky=W, pady=(15, 0))

entry_filter_language = Entry(frame_views_filters)
entry_filter_language.grid(row=4, column=1, pady=(15, 0))

Button(
    frame_views_filters,
    text="Firmy obsługujące język",
    command=lambda: show_companies_by_language()
).grid(row=5, column=0, columnspan=2, pady=3)

Label(frame_views_results, text="Wyszukiwarka:", font=("Arial", 10, "bold")).grid(row=0, column=0)

listbox_views = Listbox(frame_views_results, width=50, height=20)
listbox_views.grid(row=1, column=0)

map_views = tkintermapview.TkinterMapView(frame_views_map, width=500, height=400)
map_views.set_position(52.2, 21.0)
map_views.set_zoom(6)
map_views.grid(row=0, column=0)



def show_clients_by_company():
    company_name = entry_filter_company.get()

    listbox_views.delete(0, END)
    map_views.delete_all_marker()

    result = get_clients_by_company(clients, company_name)

    if not result:
        listbox_views.insert(END, "Brak klientów dla tej firmy")
        return

    for c in result:
        listbox_views.insert(END, f"{c['name']} - {c['location']}")

        try:
            coords = get_coordinates(c['location'])
            map_views.set_marker(coords[0], coords[1], text=c['name'])
        except:
            pass


def show_employees_by_company():
    company_name = entry_filter_company.get()

    listbox_views.delete(0, END)
    map_views.delete_all_marker()

    result = get_employees_by_company(employees, company_name)

    if not result:
        listbox_views.insert(END, "Brak pracowników dla tej firmy")
        return

    for e in result:
        listbox_views.insert(END, f"{e['name']} - {e['role']}")

        try:
            coords = get_coordinates(e['location'])
            map_views.set_marker(coords[0], coords[1], text=e['name'])
        except:
            pass


def show_companies_by_language():
    language = entry_filter_language.get()

    listbox_views.delete(0, END)
    map_views.delete_all_marker()

    result = get_companies_by_language(companies, language)

    if not result:
        listbox_views.insert(END, "Brak firm dla tego języka")
        return

    for company in result:
        listbox_views.insert(
            END,
            f"{company['name']} - {company['location']}"
        )

        try:
            coords = get_coordinates(company['location'])

            map_views.set_marker(
                coords[0],
                coords[1],
                text=company['name']
            )
        except:
            pass


refresh_companies()
refresh_clients()
refresh_employees()

load_company_markers()
load_client_markers()
load_employee_markers()

root.mainloop()














