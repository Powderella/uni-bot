import requests
import bs4
def getDMMCampaigns(idx):
    """
    エッチゲームのセールを取得
    """
    url = "https://dlsoft.dmm.co.jp/"
    with requests.get(url=url) as res:
        soup = bs4.BeautifulSoup(res.content, "html.parser")
        pricedown = [tag.text for tag in soup.find_all("p", attrs={"class": "tx-pricedown"})] 
        saleterm = [tag.text for tag in soup.find_all("p", attrs={"class": "tx-saleterm"})]
        campaign = [tag.text for tag in soup.find_all("p", attrs={"class": "ttl-campaign"})]
        urls = [tag.get("href") for tag in soup.find_all("a", attrs={"class": "content-url list-sale-box-link"})]


    return pricedown[idx], saleterm[idx], campaign[idx], urls[idx], _get_sale_top_eroge(urls[idx])

def get_num_DMM_sale():
    url = "https://dlsoft.dmm.co.jp/"
    with requests.get(url=url) as res:
        soup = bs4.BeautifulSoup(res.content, "html.parser")
        saleterm = [tag.text for tag in soup.find_all("p", attrs={"class": "tx-saleterm"})]
    return len(saleterm)

def _get_sale_top_eroge(url):
    # 人気順で一番上のエッチゲームを取得する
    with requests.get(url=url) as res:
        soup = bs4.BeautifulSoup(res.content, "html.parser")
        eroge_top = soup.find("div", attrs={"class": "tmb"})
        if eroge_top is None:
            return None, None, None
        eroge_img = eroge_top.find("img")
        src = eroge_img.get("src")
        alt = eroge_img.get("alt")
        href = eroge_top.a.get("href")
    return src, alt, href
