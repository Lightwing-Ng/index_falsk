# -*- coding: utf-8 -*-

# @File    : model.py
# @Date    : 2018-05-15

from peewee import *

db = SqliteDatabase("webdata.db")

class BaseModel(Model):
    class Meta:
        database = db

# 分类表
class ClassifyModel(BaseModel):
    name = CharField(null=True)  # 分类名称

    # 备用字段
    flag = IntegerField(default=0)
    info = CharField(default="")

# 网站名称表
class WebsiteModel(BaseModel):
    title = CharField(null=True)  # 网站名称
    ico = CharField(null=False)  # 网站图标
    description = CharField(default="")  # 网站描述
    url = CharField(null=True)  # 网站链接
    # 网站分类
    classify = ForeignKeyField(model=ClassifyModel, backref="websites",default=1)
    # 网站权重，排列顺序
    weight = IntegerField(default=0)

    # 备用字段
    flag = IntegerField(default=0)
    info = CharField(default="")


tables = [ClassifyModel, WebsiteModel]
db.connect()
db.create_tables(tables, safe=True)
db.close()

if __name__ == "__main__":
    ClassifyModel.create(name="未分类")
    WebsiteModel.create(
        title="百度",
        ico="https://www.baidu.com/favicon.ico",
        description="百度一下，你就知道",
        url="https://www.baidu.com",
        classify="1",
        weight="0",
    )
    print("数据库初始化完成")