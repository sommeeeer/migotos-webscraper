import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from blogs import get_blogpost_from_url
from helpers import special_print
from litters import get_litter_from_url
from scrape_urls import get_blog_urls, get_cat_urls, get_litter_urls
from cats import get_cat_from_url
from models import Base, CatImage
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


special_print(f"Connecting to database at {DATABASE_URL}")
engine = create_engine(DATABASE_URL, echo=False)
special_print(f"Creating tables in database...")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

cat_urls = get_cat_urls()
litter_urls = get_litter_urls()
blog_urls = get_blog_urls()


for cat_url in cat_urls:
    new_cat = get_cat_from_url(cat_url)
    session.add(new_cat)
    num_images = session.query(CatImage).filter_by(cat=new_cat).count()
    special_print(f"Adding '{new_cat.name}' to database with {num_images} images")

special_print(f"Committing cats to database...")
session.commit()

for litter_url in litter_urls:
    special_print(f'Doing {litter_url["url"]}')
    new_litter = get_litter_from_url(litter_url["url"], litter_url["post_image"])
    session.add(new_litter)
    special_print(f"Adding '{new_litter.name}' to database")
special_print(f"Commiting all litters to database...")
session.commit()

for blog_url in blog_urls:
    special_print(f"Doing {blog_url['url']}")
    new_blog = get_blogpost_from_url(blog_url["url"])
    session.add(new_blog)
    special_print(f"Adding '{new_blog.title}' to database")

special_print(f"Closing the database session")
session.close()
