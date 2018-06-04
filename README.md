## 99lib-download 使用注意事项
本脚本仅支持python3

## 脚本所需要的库
```
pip3 install requests
pip3 install beautifulsoup4
pip3 install selenium
pip3 install pymongo
```

## 使用说明
脚本共包括三个文件：book.py,db.py,download.py
其中，book.py是从99藏书网获取网站全部书籍并存入本地数据库中
db.py 是本地数据库操作模块
download.py是执行书籍下载的模块，接受四个参数
+ -k 搜索书籍的关键字，默认会从书名，作者，分类信息中搜索包含关键字参数
+ -n 是否从书名中搜索，默认为True,添加此参数后，搜索时将不在书名中搜索
+ -a 是否从作者中搜索，默认为True,添加此参数后，搜索时将不在作者中搜索
+ -n 是否从分类中搜索，默认为True,添加此参数后，搜索时将不在书籍分类中搜索

该脚本使用了MongoDB数据库来存储该网站书籍信息，也可使用json文件来存储
使用json文件存储以及更加详细的文档说明请查看[我的博客](https://lillrocky.github.io/)

**注意**
该脚本仅供交流学习使用，禁止用于商业用途。