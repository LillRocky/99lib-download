from db import db
import sys, getopt
from selenium import webdriver
import time
# Keys 是用作关键词输入
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# 设置无头浏览器信息
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('log-level=3')
# chrome_options.add_argument("--proxy-server=http://127.0.0.1:1080")
chrome_position = 'F:\\chromedriver\\chromedriver.exe'

class Download():
    def __init__(self):
        result_list = self.get_results()
        check_list = self.check(result_list)
        self.get_content(check_list)
    
    # 配置脚本命令行参数
    def get_results(self):
        opts, args = getopt.getopt(sys.argv[1:], 'k:nac')
        key = ''
        name = True
        author = True
        category = True

        for op, value in opts:
            if op == '-k':
                key = value
            elif op == '-n':
                name = False
            elif op == '-a':
                author = False
            elif op == '-c':
                category = False
        result_list = db.query(key,name,author,category)
        return result_list

    # 获取想要下载的书籍
    def check(self,result_list):
        if len(result_list) == []:
            print('查询结果为空')
            return
        choose = input('请输入你要下载的书籍的编号（多选用单个空格分隔）：')
        if choose.strip() == '':
            return
        choose_list = choose.strip().split(' ')
        choose_list = list(map(lambda x: int(x) - 1, choose_list))
        # print(choose_list)
        check_list = []
        for i in choose_list:
            check_list.append(result_list[i])
        return check_list

    # 获取书籍内容内容
    def get_content(self,check_list):
        driver = webdriver.Chrome(executable_path=chrome_position,chrome_options=chrome_options)   
        for check in check_list:
            page = 0
            total = len(check['content_list'])
            print('书籍《' + check['name'] + '》开始下载')      
            for link in check['content_list']:
                page += 1
                driver.get(link)
                # 等待一段时间
                driver.implicitly_wait(1)
                for i in range(40):
                    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    time.sleep(0.02)
                # 找到name为"q"的元素
                elem = driver.find_element_by_id("content").text
                self.save_content(elem, check['name'])
                # print(elem.text)
                print('第' + str(page) + '章下载完毕/共' + str(total) + '章')
            print('书籍下载完成！')
        driver.quit()
    
    # 保存为文本文档
    def save_content(self, content, name):
        with open(name + '.txt', 'a', encoding="utf-8") as f:
            f.write(content + '\n')

if __name__ == '__main__':
    Download()