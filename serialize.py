import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


categoria = "tutte"
tipologia = "tutte"
giorno_day = 26
giorno_month = 2
giorno_year = 2023
jaf_giorno_date_format = "dd/MM/yyyy"
evn_visualizza = "visualizza"


def extract_idaula(url):
    query_string = urlparse(url).query
    parameters = parse_qs(query_string)

    # get the value of the idaula parameter and return it
    idaula = parameters["idaula"][0]
    return idaula


acronyms = ["MIA", "MIB", "CRG", "LCF", "PCL", "MNI", "MIC", "MID", "COE"]

dict = {}

for acronym in acronyms:
    response = requests.get(
        'https://www7.ceda.polimi.it/spazi/spazi/controller/OccupazioniGiornoEsatto.do', params={"csic": acronym,
                                                                                                 "categoria": categoria,
                                                                                                 "tipologia": tipologia,
                                                                                                 "giorno_day": giorno_day,
                                                                                                 "giorno_month": giorno_month,
                                                                                                 "giorno_year": giorno_year,
                                                                                                 "jaf_giorno_date_format": jaf_giorno_date_format,
                                                                                                 "evn_visualizza": evn_visualizza})

    dict[acronym] = {}

    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all rooms
        for room in soup.find_all('td', class_='dove'):
            a_elements = room.find_all("a")
            for a in a_elements:
                text: str = room.text
                query_string = a["href"]
                dict[acronym][text.rstrip().lstrip()] = extract_idaula(
                    query_string)

    else:
        print('Error')

# Serialize dictionary to JSON
json_data = json.dumps(dict)

# Write JSON data to file
with open('data.json', 'w') as f:
    f.write(json_data)
