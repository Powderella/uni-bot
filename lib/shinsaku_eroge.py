import datetime
import requests
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta


def shinsaku_eroges(months=0, idx=0):
    url = "http://panapanapana.web.fc2.com/"

    today = datetime.date.today()
    view_month = today + relativedelta(months=months)
    current_month = view_month.strftime("%Y%m")
    trans = str.maketrans({"\r": "", "\n": "", "\t": ""})

    with requests.get(url) as response:
        soup = BeautifulSoup(response.content, "html.parser")
        currentMonthEroges = soup.find_all("tr", attrs={"class": current_month})

    eroge = currentMonthEroges[idx]
    
    product = eroge.find("p", attrs={"class": "nameProduct"}).text.translate(trans)
    maker = eroge.find("p", attrs={"class": "nameMaker"}).text.translate(trans)
    homepage_url = eroge.img.get("alt")
    image = url+eroge.img.get("data-original")

    return product, maker, homepage_url, image

def num_shinsaku_eroges(months=0):
    url = "http://panapanapana.web.fc2.com/"

    today = datetime.date.today()
    view_month = today + relativedelta(months=months)
    current_month = view_month.strftime("%Y%m")

    with requests.get(url) as response:
        soup = BeautifulSoup(response.content, "html.parser")
        currentMonthEroges = soup.find_all("tr", attrs={"class": current_month})


    return len(currentMonthEroges)

if __name__ == "__main__":
    for eroge in shinsaku_eroges():
        print(eroge)