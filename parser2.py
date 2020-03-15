import requests
import lxml
import json
import time 
import logging

from bs4 import BeautifulSoup


def main():
    """
    Main function that starting all actions
    """

    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', 
                        filename="parser2.log", level=logging.INFO, filemode='w')

    url = 'https://www.tui.ru/api/office/cities/'
    basic_url = 'https://www.tui.ru/api/office/list/?cityId='

    logging.info("Starting")
    data = get_json(get_html(url))
    logging.info("Got request to the server")
    list_cities = get_cities(data)
    logging.info("Got list of cities")

    global json_list
    json_list = []

    logging.info("Starting cicle for each city")
    for item in list_cities:

        url_item = basic_url + str(item)
        data = get_json(get_html(url_item))
        get_data(data)
        logging.info(f'Request to the: {url_item} url done successfully. Put data to the list. ')
        time.sleep(0.2)

    logging.info("End cicle. Got data from the server. Put data to the list")
    to_json(json_list)
    logging.info("Put to json file. Done!")


def get_cities(data):
    """
    Getting all cities and returnig list
    """
    spis_cit = []
    for item in data:
        spis_cit.append(item['cityId'])
    return spis_cit


def get_working_hours(data):
    """
    Function for formating working hours
    """
    if not data.get('workdays').get('isDayOff'):
        workdays = "пн-пт {} до {}".format(data.get('workdays').get('startStr'),data.get('workdays').get('endStr'))
    else:
        workdays = "пн-пт выходной"
        
    if not data.get('saturday').get('isDayOff'):
        saturday = "сб {} до {}".format(data.get('saturday').get('startStr'),data.get('saturday').get('endStr'))
    else:
        saturday = "сб выходной"

    if not data.get('sunday').get('isDayOff'):
        sunday = "вс {} до {}".format(data.get('sunday').get('startStr'),data.get('sunday').get('endStr'))
    else:
        sunday = "вс выходной"

    return [workdays, saturday, sunday]


def get_data(data):
    """
    Getting data from the snippet and putting to the list
    """
    for item in data:

        address = item.get('address')

        latlon = [item.get('latitude'), item.get('longitude')]

        name = item.get('name')

        phones = [item['phone'] for item in item.get('phones', '')]

        hours_dict = item.get('hoursOfOperation')
        working_hours = get_working_hours(hours_dict)


        result_data = {'address': address,
                       'latlon': latlon,
                       'name': name,
                       'phones': phones,
                       'working_hours':working_hours
                      }
        json_list.append(result_data)


def get_json(json_data):
    """
    Loads data from json
    """
    load_data = json.loads(json_data)
    return load_data


def get_html(url):
    """
    Getting request to the server
    """
    resp = requests.get(url)
    if resp.ok:
        return resp.text
    logging.warning("Connection problems")


def to_json(data):
    """
    At the begging clean json file after putting data to json file.
    """
    with open('parser2.json', 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()