import requests
from services.const import MAIN_PAGE, MAIN_URL
from bs4 import BeautifulSoup, ResultSet, Tag


class Track:

    def __init__(self, page_element: Tag):

        attrs: object = page_element.attrs

        self.title = attrs.get('data-title', '')
        self.img = MAIN_URL + str(attrs.get('data-img', ''))
        self.url = MAIN_URL + str(attrs.get('data-track', ''))
        self.time = page_element.find('div', {'class': ['track-time']}).text
        self.style = None

    def to_dict(self) -> dict:
        return self.__dict__


class Style:

    def __init__(self, page_element: Tag):

        contents: list = page_element.contents

        if len(contents) != 0:
            content: Tag = contents[0]
            self.title = content.text
            self.img = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4dGnqZIxupgC-NMHaod686kq0UKtNT3jg8N" \
                       "-ngV4P-PFwZQdA2lno_Lg19-OnTV5Q2Oc&usqp=CAU "
            self.url = content.attrs.get('href', "")
        else:
            self.title = ""
            self.img = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4dGnqZIxupgC-NMHaod686kq0UKtNT3jg8N" \
                       "-ngV4P-PFwZQdA2lno_Lg19-OnTV5Q2Oc&usqp=CAU "
            self.url = ""

    def to_dict(self) -> dict:
        return self.__dict__


def get_styles() -> list:
    styles: list = get_styles_from_page(save_url(MAIN_PAGE+""))
    return styles


def get_all_track(url: str) -> list:
    tracks: list = get_urls_from_page(save_url(MAIN_PAGE+url))
    return tracks


def save_url(url: str) -> bytes:

    print("parsing: ", url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Content-Type': 'text/html; charset = utf-8'
    }
    r: requests.Response = requests.get(url, headers)

    return r.text.encode("utf-8")


def get_urls_from_page(page_text: bytes) -> list:

    results: list = []
    soup: BeautifulSoup = BeautifulSoup(page_text, features="html.parser")
    track_list: ResultSet = soup.find_all('div', {'class': ['track-item']})

    for i in track_list:
        results.append(Track(i).to_dict())

    return results


def get_styles_from_page(page_text: bytes) -> list:

    results: list = []
    soup: BeautifulSoup = BeautifulSoup(page_text, features="html.parser")
    styles_list: ResultSet = soup.find('li', {'class': ['submenu']}).find_all('li')

    for i in styles_list:
        results.append(Style(i).to_dict())

    return results
