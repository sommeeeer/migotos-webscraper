import requests

from bs4 import BeautifulSoup
from constants import OUR_CATS, PREV_LITTERS


def get_cat_urls():
    response = requests.get(OUR_CATS)
    soup = BeautifulSoup(response.text, "html.parser")
    cats = soup.find_all(
        "a", class_="vc_single_image-wrapper vc_box_circle vc_box_border_grey"
    )
    return [f'https://www.migotos.com{cat["href"]}' for cat in cats]


def get_litter_urls():
    response = requests.get(PREV_LITTERS)
    soup = BeautifulSoup(response.text, "html.parser")

    litter_posts = []
    for d in soup.find_all("div", class_="item-inner layout-4"):
        url = (
            d.find("a", class_="post-link-overlay")["href"]
            .lower()
            .replace("http://", "https://")
        )
        post_image = (
            d.find("div", class_="post-image")["style"]
            .lstrip("background-image: url('")
            .rstrip("')")
        )
        if "placeholder.png" in post_image.lower():
            post_image = None
        litter_posts.append(
            {
                "url": url,
                "post_image": post_image.split("/")[-1] if post_image else None,
            }
        )

    menu_links = soup.find_all("li")

    for l in menu_links:
        if "portfolio" in l.a["href"]:
            url = {
                "url": l.a["href"].lower().replace("http://", "https://"),
                "post_image": None,
            }
            if url not in litter_posts:
                litter_posts.append(url)
    return litter_posts
