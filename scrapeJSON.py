from bs4 import BeautifulSoup as bs
import requests
from tabulate import tabulate
import json
from itertools import zip_longest

def get_titles_and_hrefs_from_page(url):
    response = requests.get(url)
    html = response.content
    soup = bs(html, "html.parser")

    titres_oeuvres = soup.find_all("h3", class_="card__title ellipsis")
    liens_oeuvres = soup.find_all("a", class_="h_4")

    oeuvres_info = [
        {
            'titre': titre.get_text(strip=True),
            'href': lien.get('href')
        }
        for titre, lien in zip(titres_oeuvres, liens_oeuvres)
    ]

    return oeuvres_info

def get_infos_oeuvre(lien):
    response = requests.get(lien)
    html = response.content
    soup = bs(html, "html.parser")

    titre_oeuvre = soup.find_all("h1", class_="notice__title h_1")

    # Find all divs with class notice__fullcartel__group
    entries = soup.find_all("div", class_="notice__fullcartel__group")

    info_oeuvre = {'Titre': titre_oeuvre[0].get_text(strip=True)}

    for entry in entries:
        # Attempt to extract label and content
        label_element = entry.find("div", class_="part__label")
        content_element = entry.find("div", class_="part__content")

        # Check if the elements are found
        if label_element and content_element:
            label = label_element.get_text(strip=True)
            content = content_element.get_text(strip=True)

            # Add label and content to info_oeuvre dictionary
            info_oeuvre[label] = content

    return [info_oeuvre]

def loop_page():
    base_url = "https://collections.louvre.fr/recherche?page="
    num_pages = 2

    for page_num in range(1, num_pages + 1):
        url = base_url + str(page_num)
        oeuvres_info = get_titles_and_hrefs_from_page(url)
        print(f"Page {page_num} - Œuvres :\n{tabulate(oeuvres_info, headers='keys', tablefmt='pretty')}")

def loop_lien(liens_oeuvres):
    href_url = "https://collections.louvre.fr"
    all_data = []

    for oeuvre in liens_oeuvres:
        lien = href_url + oeuvre['href']
        info = get_infos_oeuvre(lien)
        all_data.extend(info)

    print(all_data)
    with open('molo.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_data, json_file, ensure_ascii=False, indent=4)

liens_oeuvres = get_titles_and_hrefs_from_page("https://collections.louvre.fr/recherche?page=3320")

loop_lien(liens_oeuvres)