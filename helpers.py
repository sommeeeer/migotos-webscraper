import re
import time

from datetime import datetime

def simulate_scroll(driver):
    SCROLL_PAUSE_TIME = 0.5
    i = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        i += 1
        if i == 5:
            break
        

def convert_birth_into_datetime(birthstr):
    day, rest = birthstr.split(maxsplit=1)

    cleaned_day = re.sub(r"\D", "", day)  # Remove non-digit characters
    formatted_date = f"{cleaned_day.zfill(2)} {rest}"  # Ensure day is zero-padded

    return datetime.strptime(
        formatted_date.replace("Deember", "December").replace("Augusy", "August"),
        "%d of %B %Y",
    ).date().isoformat()


def parse_date(date):
    parts = date.lower().split()

    day = int(parts[1].rstrip("nd").rstrip("st").rstrip("rd").rstrip("th"))
    month = datetime.strptime(parts[3], "%B").month
    year = int(parts[4])

    new_date = datetime(year, month, day).date().isoformat()
    return new_date

def special_print(text):
    print(f"[*] - {text}")