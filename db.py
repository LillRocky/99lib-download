import pymongo
import json

class db_handle():
    # 配置默认数据库信息
    def __init__(self,host='localhost',port=27017):
        client = pymongo.MongoClient(host=host, port=port)
        db = client.table
        self.collection = db.t_name
        # self.t = t

    # 查询结果是否已存在
    def is_exist(self,id):
        result = self.collection.find({'_id': id}).count()
        if result == 0:
            return True
        else:
            return False

    # 插入书籍信息
    def save(self,i_dic):
        self.collection.insert_one(i_dic)
    
    # 根据给定关键字进行查询
    def query(self,q_str,name=True,author=True,category=True):
        query_string = {'$or':[]}
        {'$or': [{'name': {'$regex': q_str}},{'author': {'$regex': q_str}},{'category': {'$regex': q_str}}]}
        if name:
            query_string['$or'].append({'name': {'$regex': q_str}})
        if author:
            query_string['$or'].append({'author': {'$regex': q_str}})
        if category:
            query_string['$or'].append({'category': {'$regex': q_str}})
        if not (name or author or category):
            print('查询条件为空')
            return []
        # print(query_string)
        results = self.collection.find(query_string)
        count = 0
        re_list = []
        for result in results:
            count += 1
            re_list.append(result)
            print('{0:<10}\t{1:{4}<20}\t{2:{4}<10}\t{3:{4}<10}'.format(count,result['name'],result['author'],result['category'],chr(12288)))
        return re_list

# db_handle().query('小')
db = db_handle()