import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import os
URL = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"

my_email = os.getenv("MY_EMAIL")
gmail_password = os.getenv("MY_GMAIL_PASSWORD ")
gmail_password_code = os.getenv("MY_GMAIL_PASSWORD_CODE")


MAX_PRICE = 100

headers = {
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
   "Accept-Language": "en-US,en;q=0.9,nl;q=0.8,zu;q=0.7,bg;q=0.6,fr;q=0.5"
}
response = requests.get(URL, headers=headers)
web_page = response.text
soup = BeautifulSoup(web_page, "lxml")

product = soup.find("span", class_="a-size-large product-title-word-break", id="productTitle")
product_name = product.text.strip(" ")
print(product_name)


dollar_price = soup.find("span", class_="a-price-whole").getText().strip(".")
cent_price = soup.find("span", class_="a-price-fraction").getText()
full_price = int(dollar_price) + (int(cent_price) / 100)


if full_price < MAX_PRICE:
    message = f"The {product_name} is now only ${full_price}"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=gmail_password_code)
        connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=("Subject: Amazon Price Alert!\n\n"
                                                                        f"{message}").encode('utf-8'))

