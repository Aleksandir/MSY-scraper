import requests
from bs4 import BeautifulSoup


def main():
    soup = get_page()
    soup = BeautifulSoup(soup.content, "html.parser")

    div = soup.find_all("div", {"class": "ovhide productsIn productsz"})

    links = []
    for div in div:
        links.append(div.find("a")["href"] if div else None)

    with open("links.txt", "w") as f:
        for link in links:
            f.write(f"{link}\n")


def get_page(url: str = "https://www.msy.com.au/categories"):
    page = requests.get(url)
    return page


main()
