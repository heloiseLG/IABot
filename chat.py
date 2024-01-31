from bs4 import BeautifulSoup as bs
import requests
from tabulate import tabulate

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

    titres_oeuvres = soup.find_all("div", class_="m-7col m-last part__content")
    info = [
        {
            'titre': titre.get_text(strip=True),
        }
        for titre in titres_oeuvres
    ]

    return info

def loop_page():
    base_url = "https://collections.louvre.fr/recherche?page="
    num_pages = 2

    for page_num in range(1, num_pages + 1):
        url = base_url + str(page_num)
        oeuvres_info = get_titles_and_hrefs_from_page(url)
        print(f"Page {page_num} - Œuvres :\n{tabulate(oeuvres_info, headers='keys', tablefmt='pretty')}")

def loop_lien(liens_oeuvres):
    href_url = "https://collections.louvre.fr"

    for oeuvre in liens_oeuvres:
        lien = href_url + oeuvre['href']
        info = get_infos_oeuvre(lien)

        if info:
            print(f"Œuvre : {tabulate(info, headers='keys', tablefmt='pretty')}")
        else:
            print("Aucune information trouvée pour cette œuvre.")

liens_oeuvres = get_titles_and_hrefs_from_page("https://collections.louvre.fr/recherche?page=1")

loop_lien(liens_oeuvres)
