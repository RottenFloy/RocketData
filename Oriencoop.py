import requests
import re
from bs4 import BeautifulSoup


def get_data():
    """Getting links to store pages"""
    response = requests.get("https://oriencoop.cl/sucursales.htm")
    soup = BeautifulSoup(response.text, "lxml")
    link_data = soup.find("ul", class_="c-list c-accordion")
    link_list = []
    for a in link_data.find_all("a", href=True):
        link = a["href"]
        if "javascript" in link:
            continue
        link_list.append(link)
    return link_list


def get_items_oriencoop():
    """Gathering information from pages and saving"""

    link_list = get_data()
    address_list = []
    phone_list = []
    schedule_list = []
    coord_list = []

    for link in link_list:
        url = "https://oriencoop.cl" + link
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        data_address = (
            soup.find("div", class_="s-dato")
            .text.replace("\n", "")
            .split("Teléfono:")[0]
        )
        address_list.append(data_address.split("Dirección:")[1])

        data_phone = (
            soup.find("div", class_="s-dato").text.replace("\n", "").split("Agente:")[0]
        )
        phone_list.append(data_phone.split("Teléfono:")[1].replace("-", ""))

        data_schedule = (
            soup.find("div", class_="s-dato")
            .text.replace("\n", "")
            .split("Horarios:")[1]
            .replace("Tarde:", "/")
        )
        schedule_val = (
            data_schedule.replace("Mañana:", "")
            .replace("hrs.", "")
            .replace(" horas ", "")
            .replace("Hasta", "")
            .replace("a", "-")
            .split("/")
        )
        try:
            res_time = f"mon-thu{schedule_val[0]}{schedule_val[1].replace('(L - J) ', '').strip()}," \
                       f"fri{schedule_val[0]}{schedule_val[1].split('-')[0]}-{schedule_val[2].replace('(V)', '')}"\
                .replace("  ", " ")\
                .strip()\
                .split(",")
        except IndexError:
            res_time = "mon-thu 8.50 - 17.10, fri 8.50 - 16.10".split(",")

        schedule_list.append(res_time)

        data_link = soup.find("div", class_="s-mapa").find("iframe").get("src")

        pattern = re.compile(r"-\d{2}\.\d+")
        data_coord = pattern.findall(data_link)[::-1]
        data_coord = [float(x) for x in data_coord]
        coord_list.append(data_coord)
    shops = []

    for i in range(len(schedule_list)):
        shops.append(
            {
                "address": address_list[i],
                "latlon": coord_list[i],
                "name": "Oriencoop",
                "phones": [phone_list[i]],
                "working_hours": schedule_list[i],
            }
        )
    return shops
