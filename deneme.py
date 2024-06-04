import requests
from bs4 import BeautifulSoup
import time
import smtplib

URLs = {
    "uzaki": "https://buyee.jp/mercari/search?keyword=%E5%AE%87%E5%B4%8E%E6%9C%88&category_id=81&status=all",
    "eris": "https://buyee.jp/mercari/search?keyword=%E3%83%9C%E3%83%AC%E3%82%A2%E3%82%B9%20%201%2F7&category_id=81&status=all",
    "alice": "https://buyee.jp/mercari/search?keyword=%E3%82%B7%E3%83%B3%E3%82%BB%E3%82%B7%E3%82%B9&category_id=81&status=all",
    "raphtalia": "https://buyee.jp/mercari/search?keyword=%E3%83%A9%E3%83%95%E3%82%BF%E3%83%AA%E3%82%A2&category_id=81&status=all",
    "raphtalia 2": "https://buyee.jp/mercari/search?keyword=%E7%9B%BE%E3%81%AE%E5%8B%87%E8%80%85%E3%81%AE%E6%88%90%E3%82%8A%E4%B8%8A%E3%81%8C%E3%82%8A&category_id=81&status=all",
    "ochaco" : "https://buyee.jp/mercari/search?keyword=%E3%81%8A%E8%8C%B6%E5%AD%90%201%2F8&category_id=81&status=all",
    "nisekoi" : "https://buyee.jp/mercari/search?keyword=%E3%83%8B%E3%82%BB%E3%82%B3%E3%82%A4&category_id=81&status=all",
    "rias" : "https://buyee.jp/mercari/search?keyword=%E3%83%AA%E3%82%A2%E3%82%B9%E3%83%BB%E3%82%B0%E3%83%AC%E3%83%A2%E3%83%AA%E3%83%BC&category_id=81&status=all",
    "akeno" : "https://buyee.jp/mercari/search?keyword=%E5%A7%AB%E5%B3%B6%20%E6%9C%B1%E4%B9%83&category_id=81&status=all",
    "rent a girlfriend" : "https://buyee.jp/mercari/search?keyword=%E5%BD%BC%E5%A5%B3%E3%80%81%E3%81%8A%E5%80%9F%E3%82%8A%E3%81%97%E3%81%BE%E3%81%99%201%2F7&category_id=81&status=all",
    "rimuru 1/7" : "https://buyee.jp/mercari/search?keyword=%E8%BB%A2%E3%82%B9%E3%83%A9%201%2F7&category_id=81&status=all",
    "himeragi" : "https://buyee.jp/mercari/search?keyword=%E5%A7%AB%E6%9F%8A&category_id=81&status=all",
    "satıcı 1" : "https://buyee.jp/mercari/search?seller_id=501367046",
    "yahari 1/8": "https://buyee.jp/mercari/search?keyword=%E3%82%84%E3%81%AF%E3%82%8A%E4%BF%BA%E3%81%AE%E9%9D%92%E6%98%A5%E3%83%A9%E3%83%96%E3%82%B3%E3%83%A1%E3%81%AF%E3%81%BE%E3%81%A1%E3%81%8C%E3%81%A3%E3%81%A6%E3%81%84%E3%82%8B%20%201%2F8&category_id=81&status=all",
    "milim " : "https://buyee.jp/mercari/search?keyword=%E3%83%9F%E3%83%AA%E3%83%A0%E3%83%BB%E3%83%8A%E3%83%BC%E3%83%B4%E3%82%A1%201%2F7&category_id=81&status=all",
    "ryza" :"https://buyee.jp/mercari/search?keyword=%E3%83%A9%E3%82%A4%E3%82%B6%E3%81%AE%E3%82%A2%E3%83%88%E3%83%AA%E3%82%A8&category_id=81&status=all"
    
    
}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
old_items = {}
first_run = {URL: True for URL in URLs.values()}
counter = 0

def check_for_new_items(URL, name):
    global counter
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    items = soup.find_all("li", class_="list")
    new_items = [item.get_text() for item in items if item.get_text() not in old_items.get(URL, [])]
    if new_items:
        send_email(new_items, name, URL)
        old_items[URL] = old_items.get(URL, []) + new_items
    counter += 1
    print(f"Checked {counter} times")

def send_email(new_items, name, URL):
    global first_run
    global counter
    if first_run[URL]:
        first_run[URL] = False
        return
    server = smtplib.SMTP("smtp-mail.outlook.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("figureshopp@hotmail.com", "********")
    subject = f"New item(s) listed on {name}!"
    body = f"URL: {URL}"
    msg = f"Subject: {subject}\n\n{body}".encode('utf-8')
    server.sendmail("figureshopp@hotmail.com", "20COMP1013@isik.edu.tr", msg)
    print("Email has been sent!")
    server.quit()



while True:
    for name, URL in URLs.items():
        check_for_new_items(URL, name)
    time.sleep(30)
