import requests
import json
import re
from bs4 import BeautifulSoup
from db import db_handle

# 网站基础前缀
base_url = 'http://www.99lib.net'
# 起始页
page = 1

# 代理
proxie = {
    'http': 'http://127.0.0.1:1080',
}

# 获取章节列表
def get_chapter_list(book_link):
    res = requests.get(book_link,proxies=proxie)
    # res = requests.get(book_link)
    html = BeautifulSoup(res.text, 'html.parser')
    a_list = html.select('#dir')[0].find_all('a')
    link_list = list(map(lambda x: base_url + x['href'],a_list))
    return link_list

# 获取书籍信息
def get_book_info(page):
    page = page
    while True:
        url = base_url + '/book/index.php?page=%d' % page
        print('fecth:' + url) 
        # 发起请求
        res = requests.get(url,proxies=proxie)
        # res = requests.get(url)
        # 解析获取信息
        html = BeautifulSoup(res.text, 'html.parser')
        page_span = html.select('.total')[0].text
        total_page = int(re.match(r'^(\d+)/(\d+)$', page_span).group(2))
        name_list = html.select('#list_box h2 a')
        categories = html.select('.author')
        lenth = len(name_list)
        for j in range(0,lenth):
            link = name_list[j]['href']
            name = name_list[j].string
            book_id = re.search(r'\d+',link).group()
            # 查询书籍是否已存在
            tt = db_handle().is_exist(book_id)
            if tt:
                print('获取<' + name + '>的章节列表中...')
                link_list = get_chapter_list(base_url+link)
                t = {
                    '_id': book_id,
                    'name': name,
                    'link': base_url + link,
                    'author': categories[j].a.string if categories[j].a != None else 'none',
                    'category': categories[j].next_sibling.a.string,
                    'content_list': link_list
                }
                db_handle().save(t)
            else:
                return
        page += 1
        if page > total_page:
            print('获取书籍信息完成')
            return

if __name__ == '__main__':
    get_book_info(page)
