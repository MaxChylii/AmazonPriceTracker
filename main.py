import requests
from bs4 import BeautifulSoup
import lxml
import smtplib

# change to your wanted price
WANTED_PRICE = 100

# I use SMTP for GMAIL. If you are planing to use different email host, please, change the SMTP (line # 33)
MY_EMAIL = "YOUR@gmail.com"
MY_PASSWORD = "YOUR PASSWORD"

# link on product that you want to track
URL = "https://www.amazon.com/dp/B0BCBNGCHJ/ref=twister_bundle_kindle2022"

# better to add you own headers
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/84.0.4147.105 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
}

response = requests.get(url=URL, headers=headers)
amazon_web = response.text

soup = BeautifulSoup(amazon_web, "lxml")
price = float(soup.find(name="span", id="price_inside_buybox").getText().split("$")[1])
title = soup.find(name="span", id="productTitle").getText().strip()

message = f"{title} is now ${price}\n{URL}"

if price < WANTED_PRICE:
    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=MY_EMAIL, password=MY_PASSWORD)
    connection.sendmail(
        from_addr=MY_EMAIL,
        to_addrs=MY_EMAIL,
        msg=f"Subject:Amazon Price Alert!\n\n{message}"
    )
    connection.close()
