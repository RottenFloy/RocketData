import requests
from yandex_geocoder import Client

cookies = {
    "BITRIX_SM_GUEST_ID": "12055470",
    "BITRIX_SM_LAST_VISIT": "22.09.2022+16%3A44%3A07",
    "BITRIX_SM_LAST_ADV": "5_Y",
    "BITRIX_CONVERSION_CONTEXT_s1":
        "%7B%22ID%22%3A68%2C%22EXPIRE%22%3A1663883940%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D",
    "BX_USER_ID": "886bdaf1164a33f9eb7a5c75cfd0cbc0",
    "_ga": "GA1.2.151865935.1660163330",
    "_ym_uid": "166016333033455123",
    "_ym_d": "1660163330",
    "PHPSESSID": "updnh7t3ep3sl603f18cnk0ub2",
    "_gid": "GA1.2.24688905.1663857786",
    "_ym_isad": "2",
    "_ym_visorc": "w",
    "_gat": "1",
}

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://naturasiberica.ru",
    "Connection": "keep-alive",
    "Referer": "https://naturasiberica.ru/our-shops/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

data = {
    "type": "all",
}

client = Client("051c5d21-9583-41a5-b83b-744a542069fb")


def get_json_data():
    """Getting data from json"""
    response = requests.post(
        "https://naturasiberica.ru/local/php_interface/ajax/getShopsData.php",
        cookies=cookies,
        headers=headers,
        data=data,
    )
    json_list = response.json()
    return json_list


def get_items_natura():
    """Get data from json and write it into the list of dictionaries"""
    json_list = get_json_data()
    shops = []

    for j_l in json_list["original"]:
        if not isinstance(j_l["schedule"], str) or not isinstance(j_l["phone"], str):
            continue

        address = (
            f"{j_l['city']}, "
            f"{j_l['address']}".replace("г. Москва,", "")
            .replace("МО,", "")
            .replace(", МЕГА Уфа", "")
            .split(", ТЦ")[0]
            .split(",  ТРК")[0]
            .split(", ТРЦ")[0]
            .split(", ТРК")[0]
            .split(" ТРК")[0]
            .split(",  ТЦ")[0]
            .split(",ТРЦ")[0]
            .split(", ТВК")[0]
        )
        coordinates = (
            str(client.coordinates(address))
            .replace("Decimal", "")
            .replace("(", "")
            .replace(")", "")
            .replace("'", "")
            .strip()
            .split(",")[::-1]
        )
        coordinates = [float(x) for x in coordinates]

        shops.append(
            {
                "address": address,
                "latlon": coordinates,
                "name": "Natura Siberica",
                "phones": [
                    j_l["phone"]
                    .replace("(", "")
                    .replace(")", "")
                    .replace("-", "")
                    .replace(" ", "")
                ],
                "working_hours": j_l["schedule"]
                .lower()
                .replace("\r\n", " ")
                .lower()
                .split("в магазине")[0]
                .replace("ежедневно ", "")
                .replace("с ", "пн-вс ")
                .replace("с :", "пн-вс")
                .replace(
                    "from 09 a.m 21 p.m., from monday to saturday",
                    "mon-sat 09:00-21:00",
                )
                .replace(
                    "from 10 a.m. till 10 p.m., 7 days a week", "mon-sun 10:00-22:00"
                )
                .replace("пн-вс:", "пн-вс")
                .replace("пн.- пт., пн-вс", "пн-пт")
                .replace("пт, сб:", "пт-сб")
                .replace("10 до 22", "10:00-22:00")
                .replace(
                    "пн-вс 10:00 до 23:00 часов пн-вс воскресенья по четверг",
                    "вс-чт 10:00-23:00",
                )
                .replace(
                    "пн-вс 10:00 до 00:00 в пятницу, субботу и в праздничные дни.",
                    "пт-сб 10:00-00:00",
                )
                .replace("10-22", "10:00-22:00")
                .replace("сб:", "сб")
                .replace(".", ":")
                .replace("вс:", "вс")
                .replace("пн-пт:", "пн-пт")
                .replace("пн: - вск::", "пн-вс ")
                .replace(" до ", "-")
                .replace(" - ", "-")
                .replace("пон:-субб:: 09:00-21: 00", "пн-сб 09:00-21:00,")
                .replace("воскр::", "вс")
                .replace("- ", "-")
                .strip(),
            }
        )
    return shops
