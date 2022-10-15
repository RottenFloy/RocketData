import requests
import re
from bs4 import BeautifulSoup

cookies = {
    "_ym_uid": "1661846002585218879",
    "_ym_d": "1661846002",
    "BX_USER_ID": "4973c2904c4036c79aac897f0a457b59",
    "PHPSESSID": "MdBJF0DjrEx2PElUefJcpFeWhMyONZFj",
    "BITRIX_SM_GUEST_ID": "7830719",
    "BITRIX_SM_SALE_UID": "63527839",
    "BITRIX_CONVERSION_CONTEXT_s1":
        "%7B%22ID%22%3A2%2C%22EXPIRE%22%3A1665773940%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D",
    "_ym_isad": "2",
    "BITRIX_SM_DETECTED": "N",
    "BITRIX_SM_CITY_ID": "3215",
    "BITRIX_SM_LAST_VISIT": "14.10.2022%2017%3A39%3A13",
}

headers = {
    "authority": "som1.ru",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image"
    "/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
    "cache-control": "max-age=0",
    "origin": "https://som1.ru",
    "referer": "https://som1.ru/shops/",
    "sec-ch-ua": '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"
    "/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42",
}


def get_data():
    """Retrieving data from the site"""

    response = requests.post("https://som1.ru/shops/", cookies=cookies, headers=headers)

    soup = BeautifulSoup(response.text, "lxml")

    area_list = soup.find("div", class_="col-xs-12 col-sm-6 citys-box")

    city_list = area_list.findAll("div", class_="col-sm-12")

    data_id = []

    for city_id in city_list:
        city_id = city_id.find("input").get("id")
        data_id.append(city_id)

    return data_id


def get_inf():
    """Get coordinates, page links, store names"""
    data_id = get_data()
    city_links = []
    coords = []
    shop_name = []

    for i in data_id:
        data = {
            "CITY_ID": i,
        }

        response = requests.post(
            "https://som1.ru/shops/", cookies=cookies, headers=headers, data=data
        )
        soup = BeautifulSoup(response.text, "lxml")
        shops_dat = soup.find("div", class_="shops-list")
        shops_data = shops_dat.findAll("a", class_="btn btn-blue")
        coord_data = shops_dat.findAll("div", class_="shops-col shops-icon")

        shops_name_data = soup.find_all("div", class_="shops-col shops-name")

        for s_names in shops_name_data:
            s_names = s_names.text
            shop_name.append(
                s_names.split("г.")[0].replace("\n", "").replace("', ' ", "").strip()
            )

        for links in shops_data:
            links = links.get("href")
            city_links.append(links)

        for coord in coord_data:
            coord = coord.find("a").get("onclick")
            data_coord = [
                float(x)
                for x in coord.replace("setCenterMap(", "")
                .replace(")", "")
                .replace("[", "")
                .replace("]", "")
                .split(",")
            ]
            coords.append(data_coord)

    return city_links, coords, shop_name


def get_items_som1():
    """Gathering information from pages and saving"""

    city_links, coords, shop_name = get_inf()

    cookies_get = {
        "_ym_uid": "1661846002585218879",
        "_ym_d": "1661846002",
        "BX_USER_ID": "4973c2904c4036c79aac897f0a457b59",
        "PHPSESSID": "MdBJF0DjrEx2PElUefJcpFeWhMyONZFj",
        "BITRIX_SM_GUEST_ID": "7830719",
        "BITRIX_SM_SALE_UID": "63527839",
        "BITRIX_CONVERSION_CONTEXT_s1":
            "%7B%22ID%22%3A2%2C%22EXPIRE%22%3A1665773940%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D",
        "_ym_isad": "2",
        "BITRIX_SM_DETECTED": "N",
        "POLICY": "Y",
        "BITRIX_SM_CITY_ID": "3215",
        "BITRIX_SM_LAST_VISIT": "14.10.2022%2020%3A00%3A51",
    }

    headers_get = {
        "authority": "som1.ru",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image"
        "/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
        "cache-control": "max-age=0",
        "referer": "https://som1.ru/shops/552624",
        "sec-ch-ua": '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"
        "/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42",
    }
    address_list = []
    phone_list = []
    schedule_list = []

    for i in city_links:
        url = "https://som1.ru" + i

        response = requests.get(url, cookies=cookies_get, headers=headers_get)
        soup = BeautifulSoup(response.text, "lxml")

        address_list.append(
            soup.find("table", class_="shop-info-table")
            .find("tr")
            .text.split("Телефоны")[0]
            .replace("\n", " ")
            .replace("Адрес", "")
            .strip()
        )

        phone_val = (
            soup.find("table", class_="shop-info-table")
            .text.split("Телефон")[1]
            .split("Время")[0]
            .replace("\n", "")
            .replace(" ", "")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
        )
        phone_list.append(re.sub(r"доб.\s?\d{3}", ",", phone_val))

        schedule_val = (
            soup.find("table", class_="shop-info-table")
            .text.split("работы")[1]
            .replace("\n", "")
            .replace(" с ", " ")
            .replace("до", "-")
            .replace("Ежедневно", "пн – вс")
            .replace(": ", " ")
            .replace("Вск", "вс")
            .replace("пн-сб", "пн - сб")
            .lower()
        )
        schedule_list.append(schedule_val)

    shops = []

    for i in range(len(address_list)):
        shops.append(
            {
                "address": address_list[i],
                "latlon": coords[i],
                "name": shop_name[i],
                "phones": phone_list[i].split(",,"),
                "working_hours": [schedule_list[i]],
            }
        )

    return shops
