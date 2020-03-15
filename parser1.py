import requests
import lxml
import json
import logging

from bs4 import BeautifulSoup



def to_json(data):
    """
    At the begging clean json file after putting data to json file.
    """
    with open('parser1.json', 'w') as f:
        json.dump(data, f)


def get_data(html):
    """
    Getting data from the snippet and putting to the list
    """
    spis = []

    soup = BeautifulSoup(html, 'lxml')
    phones = soup.find('span',class_="phone-num zphone").text
    cities = soup.find_all('div', class_ ="city-item")

    for city in cities:

        city_name = city.find('h4').text
        places = city.find_all('div', class_="shop-list-item")

        for place in places:

            local_address = "{}, {}".format(city_name,place.find('div', class_ = "shop-address").text)
            latlon = [place['data-shop-latitude'], place['data-shop-longitude']]
            name = place['data-shop-name']
            working_hours = "{} {}".format(place['data-shop-mode1'],place['data-shop-mode2'])

            data = {'address': local_address,
                    'latlon': latlon,
                    'name': name,
                    'phones': phones,
                    'working_hours':working_hours
                    }

            spis.append(data)


def get_html(url):
    """
    Getting request to the server
    """
    resp = requests.get(url)
    if resp.ok:
        return resp.text
    logging.warning("Connection problems")


def main():
    """
    Main function that starting all actions
    """

    logging.basicConfig(format='%(asctime)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S',
                        filename="parser1.log", level=logging.INFO,filemode='w')

    url = 'https://www.mebelshara.ru/contacts'

    logging.info("Starting")
    data = get_data(get_html(url))
    logging.info("Got data from the server.Put data to the list")
    to_json(data)
    logging.info("Put to json file. Done!")


if __name__ == "__main__":
    main()