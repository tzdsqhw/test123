# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
class test():
    r = requests.get("https://blog.csdn.net/m0_37857151/article/details/81330699")
    demo = r.text
    soup = BeautifulSoup(demo, "html.parser")
    context = soup.find_all('div' , class_ = 'htmledit_views')
    print(context)

    context = soup.find_all('div' , class_ = 'htmledit_views')
    for hh in context: print(hh.get_text())
if __name__ == '__main__':
    test