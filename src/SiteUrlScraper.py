import requests
from bs4 import BeautifulSoup


def main():
    # scrape links from categories page
    soup = get_page("https://www.msy.com.au/categories")
    # parse html content
    soup = BeautifulSoup(soup.content, "html.parser")

    # find all divs with class "ovhide productsIn productsz"
    divs = soup.find_all("div", {"class": "ovhide productsIn productsz"})

    # list to store links
    links: list[str] = []
    # for each div, get the link and append to list
    for div in divs:
        links.append(div.find("a")["href"] if div else None)  # type: ignore

    # write links to file for later use
    with open("data/links.txt", "w") as f:
        for link in links:
            f.write(f"https://www.msy.com.au/{link}\n")


def get_page(url: str) -> requests.models.Response:
    page = requests.get(url)
    return page


if __name__ == "__main__":
    main()
