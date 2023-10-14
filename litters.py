import json
import requests
import time
import os

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from constants import LITTER_IMAGES_PATH
from helpers import get_base64, parse_date, simulate_scroll
from models import (
    Litter,
    LitterPictureWeek,
    KittenPictureImage,
    Kitten,
    Tag,
)

ACCEPTED_WIDTH = ("200", "186", "197")
ACCEPTED_HEIGHT = ("200", "186", "196")


def get_litter_pictures(url):
    if not "migotos.com" in url:
        url = f"https://migotos.com{url}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Kjører i bakgrunnen
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    simulate_scroll(driver)

    driver.implicitly_wait(10)

    cat_imgs = []

    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, "html.parser")

    cat_imgs = []

    imgs = soup.find_all("img")
    try:
        for i in imgs[2:]:
            cat_imgs.append(
                {
                    "title": i.find_previous("h4").text,
                    "src": i["src"],
                }
            )
    except:
        cat_imgs = [{"title": None, "src": cat_img["src"]} for cat_img in imgs]
    return cat_imgs


def get_litter_from_url(url, post_image):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    new_litter = Litter()

    new_litter.name = soup.find("h1").text.upper()
    new_litter.slug = url.split("/")[-2]
    new_litter.post_image = post_image
    new_litter.born = parse_date(
        soup.find("p", class_="text-muted text-uppercase").text
    )
    tags = soup.find("span", class_="post-tags").text.replace(" ", "").split("•")[1:]
    for t in tags:
        new_tag = Tag(value=t)
        new_litter.tags.append(new_tag)

    try:
        new_litter.pedigreeurl = soup.find(
            "p", class_="text-muted text-uppercase"
        ).find("a")["href"]
    except TypeError:
        new_litter.pedigreeurl = None

    mother_and_father_img = []
    imgs = soup.find_all("img", class_="vc_single_image-img")
    for img in imgs:
        img_width = img["width"]
        img_height = img["height"]

        if img_width in ACCEPTED_WIDTH and img_height in ACCEPTED_HEIGHT:
            mother_and_father_img.append(img)

    new_litter.mother_img = mother_and_father_img[0]["src"]
    new_litter.father_img = mother_and_father_img[1]["src"]

    h3s = soup.find_all("h3")

    new_litter.mother_name = h3s[0].text
    new_litter.mother_stamnavn = h3s[0].find_next_sibling("p").text.upper()

    new_litter.father_name = h3s[1].text
    new_litter.father_stamnavn = h3s[1].find_next_sibling("p").text.upper()

    new_litter.description = soup.find("div", class_="narrow-text").text.strip()

    weeks = []

    week_divs = soup.find_all(
        "div",
        attrs={
            "class": lambda e: e.startswith("vc_btn3-container vc_btn3-center")
            if e
            else False
        },
    )
    for div in week_divs:
        a = div.find("a")
        if a:
            a_link = a.get("href")
            a_text = a.text
        else:
            continue
        weeks.append((a_text, a_link))
    for w in weeks:
        new_week = LitterPictureWeek()
        new_week.name = w[0]
        new_week.link = w[1]

        week_images = get_litter_pictures(w[1])

        for d in week_images:
            new_image = KittenPictureImage()
            new_image.title = d["title"]
            new_image.src = d["src"]
            new_image.width = 0
            new_image.height = 0
            new_image.blururl = get_base64(d["src"])
            # try:
            #     new_image.width, new_image.height = Image.open(
            #         os.path.join(LITTER_IMAGES_PATH, d["src"].split("/")[-1])
            #     ).size
            # except FileNotFoundError:
            #     new_image.width, new_image.height = Image.open(
            #         os.path.join(
            #             "/home/lillemagga/Koding/git/migotos/newsite/public/static/images",
            #             d["src"].split("/")[-1],
            #         )
            #     ).size
            new_week.images.append(new_image)
        new_litter.litter_pictures.append(new_week)

    genders = soup.find_all(
        "div",
        attrs={
            "class": lambda e: e.startswith(
                "wpb_single_image wpb_content_element vc_align_center wpb_animate_when_almost_visible wpb_appear appear"
            )
            if e
            else False
        },
    )

    for g in genders:
        name = g.find_next_sibling("div").h3.text
        try:
            stamnavn = g.find_next_sibling("div").h5.text.split("\n")[0]
        except AttributeError:
            stamnavn = g.find_next_sibling("div").p.text
        gender = g.find("img")["title"]

        try:
            info = g.find_next("h5").em.text
        except:
            info = g.find_next("p").text
        new_litter.litter_kittens.append(
            Kitten(name=name, stamnavn=stamnavn, gender=gender, info=info)
        )
    return new_litter
