import requests
from bs4 import BeautifulSoup


def get_coordinates(location: str) -> list:
    url = f'https://pl.wikipedia.org/wiki/{location}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    response_html = BeautifulSoup(response.text, 'html.parser')
    latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
    longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
    return [latitude, longitude]


# FIRMY TŁUMACZENIOWE

def add_company(companies: list,
                name: str,
                location: str,
                language: str) -> None:

    companies.append({
        'name': name,
        'location': location,
        'language': language,
        'marker': None
    })


def remove_company(companies: list, index: int) -> None:
    companies.pop(index)


def update_company(companies: list,
                   index: int,
                   name: str,
                   location: str,
                   language: str) -> None:

    companies[index]['name'] = name
    companies[index]['location'] = location
    companies[index]['language'] = language


def get_companies(companies: list) -> list:
    return companies


def get_companies_by_language(companies: list,
                              language: str) -> list:

    return [
        company
        for company in companies
        if company['language'].lower() == language.lower()
    ]


# KLIENCI

def add_client(clients: list,
               name: str,
               location: str,
               company: str,
               service: str) -> None:

    clients.append({
        'name': name,
        'location': location,
        'company': company,
        'service': service,
        'marker': None
    })


def remove_client(clients: list, index: int) -> None:
    clients.pop(index)


def update_client(clients: list,
                  index: int,
                  name: str,
                  location: str,
                  company: str,
                  service: str) -> None:

    clients[index]['name'] = name
    clients[index]['location'] = location
    clients[index]['company'] = company
    clients[index]['service'] = service


def get_clients(clients: list) -> list:
    return clients


def get_clients_by_company(clients: list,
                           company_name: str) -> list:

    return [
        client
        for client in clients
        if client['company'] == company_name
    ]


# PRACOWNICY

def add_employee(employees: list,
                 name: str,
                 location: str,
                 company: str,
                 role: str) -> None:

    employees.append({
        'name': name,
        'location': location,
        'company': company,
        'role': role,
        'marker': None
    })


def remove_employee(employees: list,
                    index: int) -> None:

    employees.pop(index)


def update_employee(employees: list,
                    index: int,
                    name: str,
                    location: str,
                    company: str,
                    role: str) -> None:

    employees[index]['name'] = name
    employees[index]['location'] = location
    employees[index]['company'] = company
    employees[index]['role'] = role


def get_employees(employees: list) -> list:
    return employees


def get_employees_by_company(employees: list,
                             company_name: str) -> list:

    return [
        employee
        for employee in employees
        if employee['company'] == company_name
    ]
