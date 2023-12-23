import json

from bs4 import BeautifulSoup
from SiteUrlScraper import get_page
from tqdm import tqdm


def main():
    all_products = []
    links = get_links("data/links.txt")

    for link in tqdm(links):
        all_products.append(get_products_from_page(link))

    # write products to file
    with open("data/products.json", "a") as f:
        json.dump([all_products], f, indent=4)


def get_products_from_page(link: str) -> list[dict]:
    coreURL = "https://www.msy.com.au"
    products = []
    soup = get_page(link)

    soup = BeautifulSoup(soup.content, "html.parser")

    divs = soup.find_all("li", {"class": "goods_info"})
    # for each product on page
    for div in divs:
        # store product info in dict
        product = {}
        try:
            product["name"] = div.find("span", {"itemprop": "name"}).text
            product["price"] = div.find("span", {"itemprop": "price"})["content"]
            # get link and add to coreURL to make absolute link
            product["link"] = coreURL + div.find("a")["href"]
            product["stock"] = div.find(
                "span", {"class": "goods_stock graphik-bold"}
            ).text
        except TypeError:
            continue

        products.append(product)

    return products


def get_links(file: str) -> list[str]:
    with open(file, "r") as f:
        return f.read().splitlines()


if __name__ == "__main__":
    main()
