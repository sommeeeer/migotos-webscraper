import os
import requests

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from constants import CAT_IMAGES_PATH, OUR_CATS
from helpers import convert_birth_into_datetime, simulate_scroll
from models import Cat, CatImage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image


def get_catimages_from_url(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Kjører i bakgrunnen
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    simulate_scroll(driver)

    cat_images = driver.find_elements(By.TAG_NAME, "img")

    imgs = []
    for img in cat_images[2:]:
        img_src = img.get_attribute("src")
        width, height = Image.open(
            os.path.join(CAT_IMAGES_PATH, img_src.split("/")[-1])
        ).size
        imgs.append(CatImage(src=img_src, width=width, height=height))

    driver.quit()
    return imgs


def get_cat_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    new_cat = Cat()

    p_text_muted = soup.find_all("p", attrs={"class": "text-muted"})

    new_cat.name = soup.find("h1").text.strip()
    new_cat.stamnavn = p_text_muted[0].text.splitlines()[0].strip().upper()
    new_cat.slug = url.split("/")[-2]

    new_cat.description = (
        p_text_muted[1].text.strip() if len(p_text_muted) > 1 else None
    )

    try:
        pedigree_url = p_text_muted[0].find("a")["href"]
    except TypeError:
        pedigree_url = None
    new_cat.pedigreeurl = pedigree_url

    info_chunk = soup.find(
        lambda tag: tag.name == "p" and "Birth" in tag.text
    ).text.splitlines()

    new_cat.birth = convert_birth_into_datetime(info_chunk[0].split(":")[1].strip())
    new_cat.gender = info_chunk[1].split(":")[1].strip()
    fertile = info_chunk[2].split(":")[1].strip()
    new_cat.fertile = True if fertile.lower() == "yes" else False
    new_cat.father = info_chunk[3].split(":")[1].strip()
    new_cat.mother = info_chunk[4].split(":")[1].strip()
    new_cat.breeder = info_chunk[5].split(":")[1].strip()
    new_cat.owner = info_chunk[6].split(":")[1].strip()

    imgs = get_catimages_from_url(url)
    for img in imgs:
        new_cat.images.append(img)

    return new_cat
