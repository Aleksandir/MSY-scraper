import requests
from bs4 import BeautifulSoup


def main():
    soup = get_page()
    soup = BeautifulSoup(soup.content, "html.parser")

    divs = soup.find_all("div", {"class": "ovhide productsIn productsz"})

    links: list[str] = []
    for div in divs:
        links.append(div.find("a")["href"] if div else None)  # type: ignore

    with open("links.txt", "w") as f:
        for link in links:
            f.write(f"{link}\n")


def get_page(
    url: str = "https://www.msy.com.au/categories",
) -> requests.models.Response:
    page = requests.get(url)
    return page


main()
