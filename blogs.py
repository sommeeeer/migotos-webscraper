from bs4 import BeautifulSoup
import requests

from models import BlogPost, BlogPostTag


def get_post_from_url(url):
    response = requests.get(
        "https://www.migotos.com/gic-nmigotos-kaia-n-03-22-bis-female-both-days-16-17-july-2023/"
    )
    soup = BeautifulSoup(response.text, "html.parser")

    new_post = BlogPost()

    post_hero_div = soup.find("div", class_="post-hero")
    new_post.hero_image_src = post_hero_div.img["src"] if post_hero_div.img else None
    new_post.title = soup.find("header", class_="post-heading").h1.text
    new_post.post_date = soup.find("span", class_="post-date").text
    tags = [i.text for i in soup.find("span", class_="post-tags").find_all("a")]
    for t in tags:
        new_tag = BlogPostTag(value=t)
        new_post.tags.append(new_tag)
    wpb_wrapper_div = soup.find("div", class_="wpb_wrapper")
    if wpb_wrapper_div:
        new_post.body = wpb_wrapper_div.text
    else:
        new_post.body = soup.find("div", class_="post-body").text
    return new_post