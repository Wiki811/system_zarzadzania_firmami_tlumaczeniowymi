from model import firmy
import requests
import folium
from bs4 import BeautifulSoup

# FIRMY TŁUMACZENIOWE

def add_firma():
    nazwa = input("Podaj nazwę firmy: ")
    miasto = input("Podaj miasto: ").title()
    jezyk = input("Podaj język tłumaczeń: ")

    coordinates = get_coordinates(miasto)

    firmy.append({
        "nazwa": nazwa,
        "miasto": miasto,
        "jezyk": jezyk,
        "lat": coordinates[0],
        "lon": coordinates[1]
    })

    print("Firma została dodana")


def read_firmy():
    if len(firmy) == 0:
        print("Brak firm")
        return

    for i, firma in enumerate(firmy):
        print(
            f"{i + 1}. {firma['nazwa']} - {firma['miasto']} - {firma['jezyk']}"
        )


def update_firma():
    if len(firmy) == 0:
        print("Brak firm")
        return

    read_firmy()

    numer = int(input("Podaj numer firmy do edycji: "))

    if 1 <= numer <= len(firmy):

        nowa_nazwa = input("Nowa nazwa firmy: ")
        nowe_miasto = input("Nowe miasto: ").title()
        nowy_jezyk = input("Nowy język tłumaczeń: ")

        firmy[numer - 1]["nazwa"] = nowa_nazwa
        firmy[numer - 1]["miasto"] = nowe_miasto
        firmy[numer - 1]["jezyk"] = nowy_jezyk

        nowe_wspolrzedne = get_coordinates(nowe_miasto)

        firmy[numer - 1]["lat"] = nowe_wspolrzedne[0]
        firmy[numer - 1]["lon"] = nowe_wspolrzedne[1]

        print("Firma została zaktualizowana")

    else:
        print("Nieprawidłowy numer")


def delete_firma():
    if len(firmy) == 0:
        print("Brak firm")
        return

    read_firmy()

    numer = int(input("Podaj numer firmy do usunięcia: "))

    if 1 <= numer <= len(firmy):

        firmy.pop(numer - 1)

        print("Firma została usunięta")

    else:
        print("Nieprawidłowy numer")


def get_coordinates(miasto):
    url = f'https://pl.wikipedia.org/wiki/{miasto}'

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(url, headers=headers)

    response_html = BeautifulSoup(response.text, 'html.parser')

    latitude = float(
        response_html.select('.latitude')[1].text.replace(',', '.')
    )

    longitude = float(
        response_html.select('.longitude')[1].text.replace(',', '.')
    )

    return [latitude, longitude]


def get_mapa_firm():
    m = folium.Map([52, 21], zoom_start=6)

    for firma in firmy:
        folium.Marker(
            location=[
                firma['lat'],
                firma['lon']
            ],
            popup=firma['nazwa']
        ).add_to(m)

    m.save("mapa_firm.html")

    print("Mapa firm została zapisana")

