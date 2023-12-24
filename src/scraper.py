import concurrent.futures
import json

from bs4 import BeautifulSoup
from SiteUrlScraper import get_page
from tqdm import tqdm


def main():
    # as products are gathered, they are added to this list to be written to file at the end
    all_products = []
    # load links from file previously generated by SiteUrlScraper.py
    links = get_links("data/links.txt")

    # for each link, get products from page using multithreading
    # max workers is set to 5 to avoid overloading the server
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_link = {
            executor.submit(get_products_from_page, link): link for link in links
        }
        for future in tqdm(
            concurrent.futures.as_completed(future_to_link), total=len(future_to_link)
        ):
            link = future_to_link[future]
            try:
                all_products.extend(future.result())
            except Exception as exc:
                print("%r generated an exception: %s" % (link, exc))

    # write products to file
    with open("data/products.json", "w") as f:
        json.dump([all_products], f, indent=4)
        print("Products written to file")


def get_products_from_page(link: str) -> list[dict]:
    """
    Retrieves a list of products from a given page.

    Args:
        link (str): The URL of the page to scrape.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a product.
                    Each product dictionary contains the following keys:
                    - "name": The name of the product.
                    - "price": The price of the product.
                    - "link": The absolute URL of the product.
                    - "stock": The stock availability of the product.
    """

    # coreURL is used to make absolute links
    coreURL = "https://www.msy.com.au"
    # list to store products on page
    products = []
    # get beautifulsoup object from page
    soup = get_page(link)

    # parse html content
    soup = BeautifulSoup(soup.content, "html.parser")

    product_elements = soup.find_all("li", {"class": "goods_info"})
    # for each product on page
    for product_element in product_elements:
        # store product info in dict
        product = {}

        # try to get product info, if TypeError, skip product
        try:
            product["name"] = product_element.find("span", {"itemprop": "name"}).text
            product["price"] = product_element.find("span", {"itemprop": "price"})[
                "content"
            ]
            # get link and add to coreURL to make absolute link
            product["link"] = coreURL + product_element.find("a")["href"]
            product["stock"] = product_element.find(
                "span", {"class": "goods_stock graphik-bold"}
            ).text
        except TypeError:
            continue

        # add product to list of products after each product element is parsed
        products.append(product)

    return products


def get_links(file: str) -> list[str]:
    """
    Read the contents of a file and return a list of links.

    Args:
        file (str): The path to the file.

    Returns:
        list[str]: A list of links extracted from the file.
    """
    with open(file, "r") as f:
        return f.read().splitlines()


if __name__ == "__main__":
    main()
