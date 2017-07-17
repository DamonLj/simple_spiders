import requests

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status() # 如果状态不是200，引发异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产品异常"